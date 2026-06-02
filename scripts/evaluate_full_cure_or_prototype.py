#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cure_or_pp.eval_manifest import load_eval_rows  # noqa: E402

PROTOCOL = "full_cure_or_leave_clean_condition_out_prototype"


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate Full-CURE-OR with clean-condition-held-out prototypes.")
    parser.add_argument("--config", default="configs/hgnetv2_b0_full_cure_or_prototype_v04.json")
    parser.add_argument("--limit", type=int, default=None, help="Optional eval row limit for smoke tests.")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda", "mps"])
    args = parser.parse_args()

    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from tqdm import tqdm

    config = json.loads(resolve_project_path(args.config).read_text(encoding="utf-8"))
    clean_manifest_path = resolve_project_path(config["clean_manifest_path"])
    distorted_manifest_paths = [resolve_project_path(path) for path in config["distorted_manifest_paths"]]
    predictions_path = resolve_project_path(config["predictions_path"])
    summary_path = resolve_project_path(config["summary_path"])
    batch_size = int(config.get("batch_size", 32))

    rows = load_full_eval_rows(clean_manifest_path, distorted_manifest_paths)
    for row in rows:
        attach_source_metadata(row)

    clean_rows = [row for row in rows if row["family"] == "clean"]
    eval_rows = rows[: args.limit] if args.limit is not None else rows
    labels = sorted({row["label"] for row in clean_rows})
    if not labels:
        raise ValueError("No clean rows found; cannot build prototypes.")

    device = choose_device(args.device, torch)
    print(f"Loading {config['model_name']} ({config['backend']}) on {device}")
    model, transform = load_feature_model(config, nn)
    model = model.to(device)
    model.eval()

    print(f"Clean prototype rows: {len(clean_rows)}")
    print(f"Eval rows: {len(eval_rows)}")
    clean_features = extract_features(clean_rows, model, transform, device, torch, F, tqdm, batch_size)
    centroids_by_condition = build_centroids_by_condition(clean_rows, clean_features, labels, torch, F)

    predictions = []
    for batch_rows in tqdm(list(chunks(eval_rows, batch_size)), desc="Evaluating"):
        images = []
        valid_rows = []
        for row in batch_rows:
            try:
                with Image.open(resolve_project_path(row["image_path"])) as opened:
                    images.append(transform(opened.convert("RGB")))
                valid_rows.append(row)
            except (FileNotFoundError, UnidentifiedImageError, OSError) as exc:
                print(f"Skipping unreadable image {row['image_path']}: {exc}")

        if not valid_rows:
            continue

        batch = torch.stack(images).to(device)
        with torch.no_grad():
            features = F.normalize(model(batch), dim=-1)

        for row, feature in zip(valid_rows, features):
            condition = condition_key(row)
            centroids = centroids_by_condition[condition].to(device)
            logits = feature.unsqueeze(0) @ centroids.T
            probs = logits.softmax(dim=-1).squeeze(0)
            pred_idx = int(probs.argmax().item())
            predicted_label = labels[pred_idx]
            predictions.append(
                {
                    "image_path": row["image_path"],
                    "source_path": row["source_path"],
                    "source_condition": condition_to_string(condition),
                    "label": row["label"],
                    "predicted_label": predicted_label,
                    "correct": int(predicted_label == row["label"]),
                    "confidence": float(probs[pred_idx].item()),
                    "family": row["family"],
                    "recipe": row["recipe"],
                    "severity": row["severity"],
                    "model_id": config["model_id"],
                    "protocol": PROTOCOL,
                }
            )

    predictions_path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(predictions_path, predictions)
    summary = summarize(predictions)
    write_csv(summary_path, summary)
    print(f"Predictions: {predictions_path}")
    print(f"Summary: {summary_path}")
    print_key_results(summary)
    return 0


def load_full_eval_rows(clean_manifest_path: Path, distorted_manifest_paths: list[Path]) -> list[dict]:
    rows = []
    for index, distorted_manifest_path in enumerate(distorted_manifest_paths):
        loaded = load_eval_rows(clean_manifest_path, distorted_manifest_path)
        if index == 0:
            rows.extend(loaded)
        else:
            rows.extend(row for row in loaded if row["family"] != "clean")
    return rows


def load_feature_model(config: dict, nn):
    backend = config["backend"]
    if backend == "timm":
        import timm
        from timm.data import create_transform, resolve_model_data_config

        model = timm.create_model(config["model_id"], pretrained=bool(config.get("pretrained", True)), num_classes=0)
        transform = create_transform(**resolve_model_data_config(model))
        return model, transform

    if backend == "torchvision_mobilenet_v3_small":
        from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

        weights = getattr(MobileNet_V3_Small_Weights, config.get("weights", "IMAGENET1K_V1"))
        base = mobilenet_v3_small(weights=weights)
        model = nn.Sequential(base.features, base.avgpool, nn.Flatten(start_dim=1))
        return model, weights.transforms()

    raise ValueError(f"Unsupported backend: {backend}")


def extract_features(rows, model, transform, device, torch, F, tqdm, batch_size: int):
    features = []
    for batch_rows in tqdm(list(chunks(rows, batch_size)), desc="Extracting clean features"):
        images = []
        for row in batch_rows:
            with Image.open(resolve_project_path(row["image_path"])) as opened:
                images.append(transform(opened.convert("RGB")))
        batch = torch.stack(images).to(device)
        with torch.no_grad():
            features.append(F.normalize(model(batch), dim=-1).cpu())
    return torch.cat(features, dim=0)


def build_centroids_by_condition(clean_rows, clean_features, labels, torch, F):
    conditions = sorted({condition_key(row) for row in clean_rows})
    label_to_indices: dict[str, list[int]] = {label: [] for label in labels}
    for idx, row in enumerate(clean_rows):
        label_to_indices[row["label"]].append(idx)

    output = {}
    for condition in conditions:
        centroids = []
        for label in labels:
            indices = [idx for idx in label_to_indices[label] if condition_key(clean_rows[idx]) != condition]
            if not indices:
                indices = label_to_indices[label]
            centroid = clean_features[indices].mean(dim=0, keepdim=True)
            centroids.append(F.normalize(centroid, dim=-1))
        output[condition] = torch.cat(centroids, dim=0)
    return output


def attach_source_metadata(row: dict) -> None:
    metadata = parse_source_metadata(row.get("source_metadata_json", ""))
    for key in ("background", "device", "orientation", "object_id", "challenge_type", "challenge_level"):
        if key in metadata:
            row[key] = metadata[key]


def parse_source_metadata(raw: str) -> dict:
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def condition_key(row: dict) -> tuple[str, str, str]:
    return (row.get("background", ""), row.get("device", ""), row.get("orientation", ""))


def condition_to_string(condition: tuple[str, str, str]) -> str:
    return "/".join(condition)


def summarize(predictions: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str, str], list[dict]] = {}
    for row in predictions:
        groups.setdefault((row["family"], row["recipe"], row["severity"]), []).append(row)

    clean_acc = None
    summary = []
    for family, recipe, severity in sorted(groups):
        rows = groups[(family, recipe, severity)]
        accuracy = sum(int(row["correct"]) for row in rows) / len(rows)
        mean_confidence = sum(float(row["confidence"]) for row in rows) / len(rows)
        if family == "clean" and recipe == "clean":
            clean_acc = accuracy
        summary.append(
            {
                "family": family,
                "recipe": recipe,
                "severity": severity,
                "n": len(rows),
                "accuracy": accuracy,
                "mean_confidence": mean_confidence,
                "relative_accuracy_drop": "",
                "protocol": PROTOCOL,
            }
        )

    if clean_acc is not None:
        for row in summary:
            row["relative_accuracy_drop"] = clean_acc - float(row["accuracy"])
    return summary


def print_key_results(summary: list[dict]) -> None:
    clean = [row for row in summary if row["family"] == "clean"]
    if clean:
        print(f"Clean held-out accuracy: {float(clean[0]['accuracy']):.4f}")

    control = [row for row in summary if row["family"] == "control_cure_or"]
    if control:
        print(f"Grayscale control accuracy: {float(control[0]['accuracy']):.4f}")

    level5 = [
        row for row in summary
        if row["family"] == "native_cure_or" and row["severity"] == "level_5"
    ]
    if level5:
        mean_level5 = sum(float(row["accuracy"]) * int(row["n"]) for row in level5) / sum(int(row["n"]) for row in level5)
        print(f"Mean native level-5 accuracy: {mean_level5:.4f}")


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def chunks(rows: list[dict], batch_size: int):
    for start in range(0, len(rows), batch_size):
        yield rows[start : start + batch_size]


def choose_device(requested: str, torch) -> str:
    if requested != "auto":
        return requested
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
