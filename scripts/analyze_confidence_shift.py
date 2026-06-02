#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze confidence shifts across CURE-OR++ baselines.")
    parser.add_argument("--config", default="configs/model_summaries_v01.json")
    args = parser.parse_args()

    config = json.loads(resolve_project_path(args.config).read_text(encoding="utf-8"))
    output_path = resolve_project_path(config.get("confidence_path", "results/confidence_shift_v01.csv"))
    rows = build_confidence_rows(config["models"])
    write_csv(output_path, rows)
    print(f"Confidence rows: {len(rows)}")
    print(f"Wrote {output_path}")
    print_headline(rows)
    return 0


def build_confidence_rows(models: list[dict]) -> list[dict]:
    output = []
    for model in models:
        predictions_path = resolve_project_path(model["predictions_path"])
        if not predictions_path.exists():
            print(f"Skipping missing predictions for {model['name']}: {predictions_path}")
            continue

        groups = load_prediction_groups(predictions_path)
        clean_rows = groups.get(("clean", "clean", "clean"), [])
        clean_accuracy = accuracy(clean_rows) if clean_rows else None
        clean_confidence = mean_confidence(clean_rows) if clean_rows else None

        for (family, recipe, severity), rows in sorted(groups.items()):
            acc = accuracy(rows)
            conf = mean_confidence(rows)
            incorrect_rows = [row for row in rows if int(row["correct"]) == 0]
            correct_rows = [row for row in rows if int(row["correct"]) == 1]
            output.append(
                {
                    "model_name": model["name"],
                    "model_slug": model["slug"],
                    "family": family,
                    "recipe": recipe,
                    "severity": severity,
                    "n": len(rows),
                    "accuracy": acc,
                    "mean_confidence": conf,
                    "clean_accuracy": "" if clean_accuracy is None else clean_accuracy,
                    "clean_mean_confidence": "" if clean_confidence is None else clean_confidence,
                    "accuracy_drop": "" if clean_accuracy is None else clean_accuracy - acc,
                    "confidence_drop": "" if clean_confidence is None else clean_confidence - conf,
                    "incorrect_n": len(incorrect_rows),
                    "mean_confidence_correct": "" if not correct_rows else mean_confidence(correct_rows),
                    "mean_confidence_incorrect": "" if not incorrect_rows else mean_confidence(incorrect_rows),
                    "high_conf_wrong_rate": high_conf_wrong_rate(rows),
                }
            )
    return output


def load_prediction_groups(path: Path) -> dict[tuple[str, str, str], list[dict]]:
    groups: dict[tuple[str, str, str], list[dict]] = {}
    with path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row["family"], row["recipe"], row["severity"])
            groups.setdefault(key, []).append(row)
    return groups


def accuracy(rows: list[dict]) -> float:
    return sum(int(row["correct"]) for row in rows) / len(rows)


def mean_confidence(rows: list[dict]) -> float:
    return sum(float(row["confidence"]) for row in rows) / len(rows)


def high_conf_wrong_rate(rows: list[dict], threshold: float = 0.5) -> float:
    wrong = [row for row in rows if int(row["correct"]) == 0]
    if not wrong:
        return 0.0
    return sum(float(row["confidence"]) >= threshold for row in wrong) / len(rows)


def print_headline(rows: list[dict]) -> None:
    high_rows = [
        row
        for row in rows
        if row["severity"] == "high" and row["family"] != "clean" and row["accuracy_drop"] != ""
    ]
    if not high_rows:
        return

    worst_accuracy = sorted(high_rows, key=lambda row: float(row["accuracy_drop"]), reverse=True)[:5]
    print("Largest high-severity accuracy drops:")
    for row in worst_accuracy:
        print(
            f"  {row['model_name']} / {row['recipe']}: "
            f"accuracy_drop={float(row['accuracy_drop']):.4f}, "
            f"confidence_drop={float(row['confidence_drop']):.4f}"
        )


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
