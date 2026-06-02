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
from cure_or_pp.labels import load_labels_from_config  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate OpenCLIP zero-shot robustness on CURE-OR++.")
    parser.add_argument("--config", default="configs/openclip_vit_b32_laion2b_v01.json")
    parser.add_argument("--limit", type=int, default=None, help="Optional row limit for smoke tests.")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda", "mps"])
    args = parser.parse_args()

    import open_clip
    import torch
    import torch.nn.functional as F
    from tqdm import tqdm

    config = json.loads(resolve_project_path(args.config).read_text(encoding="utf-8"))
    clean_manifest_path = resolve_project_path(config["clean_manifest_path"])
    distorted_manifest_path = resolve_project_path(config["distorted_manifest_path"])
    predictions_path = resolve_project_path(config["predictions_path"])
    summary_path = resolve_project_path(config["summary_path"])
    batch_size = int(config.get("batch_size", 16))

    label_display = load_labels_from_config(config, ROOT)
    labels = list(label_display.keys())
    prompts = build_prompts(labels, label_display, config["prompt_templates"])

    rows = load_eval_rows(clean_manifest_path, distorted_manifest_path)
    if args.limit is not None:
        rows = rows[: args.limit]

    device = choose_device(args.device, torch)
    print(f"Loading {config['model_name']} {config['pretrained']} on {device}")
    model, _, preprocess = open_clip.create_model_and_transforms(
        config["model_name"],
        pretrained=config["pretrained"],
    )
    tokenizer = open_clip.get_tokenizer(config["model_name"])
    model = model.to(device)
    model.eval()

    text_features = encode_text_features(model, tokenizer, prompts, labels, device, torch, F)
    predictions = []

    for batch_rows in tqdm(list(chunks(rows, batch_size)), desc="Evaluating"):
        images = []
        valid_rows = []
        for row in batch_rows:
            try:
                with Image.open(resolve_project_path(row["image_path"])) as opened:
                    images.append(preprocess(opened.convert("RGB")))
                valid_rows.append(row)
            except (FileNotFoundError, UnidentifiedImageError, OSError) as exc:
                print(f"Skipping unreadable image {row['image_path']}: {exc}")

        if not valid_rows:
            continue

        batch = torch.stack(images).to(device)
        with torch.no_grad():
            image_features = F.normalize(model.encode_image(batch), dim=-1)
            logit_scale = model.logit_scale.exp()
            logits = logit_scale * image_features @ text_features.T
            probs = logits.softmax(dim=-1)
            predicted_indices = probs.argmax(dim=-1).tolist()
            confidences = probs.max(dim=-1).values.tolist()

        for row, pred_idx, confidence in zip(valid_rows, predicted_indices, confidences):
            predicted_label = labels[pred_idx]
            predictions.append(
                {
                    "image_path": row["image_path"],
                    "source_path": row["source_path"],
                    "label": row["label"],
                    "predicted_label": predicted_label,
                    "correct": int(predicted_label == row["label"]),
                    "confidence": float(confidence),
                    "family": row["family"],
                    "recipe": row["recipe"],
                    "severity": row["severity"],
                    "model_id": config["model_id"],
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


def build_prompts(labels: list[str], label_display: dict, templates: list[str]) -> dict[str, list[str]]:
    return {
        label: [template.format(label_display.get(label, label).replace("_", " ")) for template in templates]
        for label in labels
    }


def encode_text_features(model, tokenizer, prompts, labels, device, torch, F):
    per_label_features = []
    for label in labels:
        tokens = tokenizer(prompts[label]).to(device)
        with torch.no_grad():
            features = F.normalize(model.encode_text(tokens), dim=-1)
            features = F.normalize(features.mean(dim=0, keepdim=True), dim=-1)
        per_label_features.append(features)
    return torch.cat(per_label_features, dim=0)


def summarize(predictions: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str, str], list[dict]] = {}
    for row in predictions:
        groups.setdefault((row["family"], row["recipe"], row["severity"]), []).append(row)

    summary = []
    clean_acc = None
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
            }
        )

    if clean_acc is not None:
        for row in summary:
            row["relative_accuracy_drop"] = clean_acc - float(row["accuracy"])
    return summary


def print_key_results(summary: list[dict]) -> None:
    clean = [row for row in summary if row["family"] == "clean"]
    if clean:
        print(f"Clean accuracy: {float(clean[0]['accuracy']):.4f}")

    modern_high = [
        row
        for row in summary
        if row["family"] == "modern_transfer" and row["severity"] == "high"
    ]
    if modern_high:
        worst = sorted(modern_high, key=lambda row: float(row["accuracy"]))[:3]
        print("Worst high-severity modern transfer recipes:")
        for row in worst:
            drop = row["relative_accuracy_drop"]
            drop_text = "n/a" if drop == "" else f"{float(drop):.4f}"
            print(f"  {row['recipe']}: acc={float(row['accuracy']):.4f}, drop={drop_text}")


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
