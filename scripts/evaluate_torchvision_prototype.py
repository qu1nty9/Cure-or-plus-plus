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


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a torchvision backbone with a clean-train prototype classifier.")
    parser.add_argument("--config", default="configs/mobilenet_v3_small_prototype_v01.json")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda", "mps"])
    args = parser.parse_args()

    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small
    from tqdm import tqdm

    config = json.loads(resolve_project_path(args.config).read_text(encoding="utf-8"))
    clean_manifest_path = resolve_project_path(config["clean_manifest_path"])
    distorted_manifest_path = resolve_project_path(config["distorted_manifest_path"])
    predictions_path = resolve_project_path(config["predictions_path"])
    summary_path = resolve_project_path(config["summary_path"])

    rows = load_eval_rows(clean_manifest_path, distorted_manifest_path)
    for row in rows:
        attach_safe_source_metadata(row)

    train_rows = [
        row for row in rows
        if row["family"] == "clean" and row.get("split") == config.get("train_split", "train")
    ]
    eval_rows = [
        row for row in rows
        if row.get("split") == config.get("eval_split", "test")
    ]
    if args.limit is not None:
        eval_rows = eval_rows[: args.limit]

    labels = sorted({row["label"] for row in train_rows})

    device = choose_device(args.device, torch)
    print(f"Loading {config['model_id']} on {device}")
    model, transform = load_feature_model(config, mobilenet_v3_small, MobileNet_V3_Small_Weights, nn)
    model = model.to(device)
    model.eval()

    print(f"Train rows: {len(train_rows)}")
    print(f"Eval rows: {len(eval_rows)}")
    train_features, train_labels = extract_features(train_rows, model, transform, device, torch, F, tqdm, int(config["batch_size"]))
    centroids = build_centroids(train_features, train_labels, labels, torch, F).to(device)

    predictions = []
    for batch_rows in tqdm(list(chunks(eval_rows, int(config["batch_size"]))), desc="Evaluating"):
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
            logits = features @ centroids.T
            probs = logits.softmax(dim=-1)
            predicted_indices = probs.argmax(dim=-1).tolist()
            confidences = probs.max(dim=-1).values.tolist()

        for row, pred_idx, confidence in zip(valid_rows, predicted_indices, confidences):
            predicted_label = labels[pred_idx]
            predictions.append(
                {
                    "image_path": row["image_path"],
                    "source_path": row["source_path"],
                    "source_split": row.get("split", ""),
                    "label": row["label"],
                    "predicted_label": predicted_label,
                    "correct": int(predicted_label == row["label"]),
                    "confidence": float(confidence),
                    "family": row["family"],
                    "recipe": row["recipe"],
                    "severity": row["severity"],
                    "model_id": config["model_id"],
                    "protocol": "clean_train_prototype_test_split",
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


def load_feature_model(config, mobilenet_v3_small, MobileNet_V3_Small_Weights, nn):
    if config["model_id"] != "mobilenet_v3_small":
        raise ValueError("Only mobilenet_v3_small is currently supported.")

    weights = getattr(MobileNet_V3_Small_Weights, config.get("weights", "IMAGENET1K_V1"))
    base = mobilenet_v3_small(weights=weights)
    feature_model = nn.Sequential(
        base.features,
        base.avgpool,
        nn.Flatten(start_dim=1),
    )
    return feature_model, weights.transforms()


def extract_features(rows, model, transform, device, torch, F, tqdm, batch_size: int):
    features = []
    labels = []
    for batch_rows in tqdm(list(chunks(rows, batch_size)), desc="Extracting train features"):
        images = []
        batch_labels = []
        for row in batch_rows:
            with Image.open(resolve_project_path(row["image_path"])) as opened:
                images.append(transform(opened.convert("RGB")))
            batch_labels.append(row["label"])
        batch = torch.stack(images).to(device)
        with torch.no_grad():
            batch_features = F.normalize(model(batch), dim=-1).cpu()
        features.append(batch_features)
        labels.extend(batch_labels)
    return torch.cat(features, dim=0), labels


def build_centroids(features, train_labels, labels, torch, F):
    centroids = []
    for label in labels:
        indices = [idx for idx, train_label in enumerate(train_labels) if train_label == label]
        centroid = features[indices].mean(dim=0, keepdim=True)
        centroids.append(F.normalize(centroid, dim=-1))
    return torch.cat(centroids, dim=0)


def parse_source_metadata(raw: str) -> dict:
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def attach_safe_source_metadata(row: dict) -> None:
    metadata = parse_source_metadata(row.get("source_metadata_json", ""))
    for key in ("split", "image_id", "object_id", "challenge_type", "challenge_level", "background", "perspective"):
        if key in metadata:
            row[key] = metadata[key]


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
                "protocol": "clean_train_prototype_test_split",
            }
        )

    if clean_acc is not None:
        for row in summary:
            row["relative_accuracy_drop"] = clean_acc - float(row["accuracy"])
    return summary


def print_key_results(summary: list[dict]) -> None:
    clean = [row for row in summary if row["family"] == "clean"]
    if clean:
        print(f"Clean test accuracy: {float(clean[0]['accuracy']):.4f}")
    modern_high = [
        row for row in summary
        if row["family"] == "modern_transfer" and row["severity"] == "high"
    ]
    for row in sorted(modern_high, key=lambda item: float(item["accuracy"]))[:3]:
        print(
            f"  {row['recipe']}: acc={float(row['accuracy']):.4f}, "
            f"drop={float(row['relative_accuracy_drop']):.4f}"
        )


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def chunks(rows: list[dict], batch_size: int):
    for start in range(0, len(rows), batch_size):
        yield rows[start:start + batch_size]


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
