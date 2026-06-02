#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Filter and summarize prediction CSV files.")
    parser.add_argument("--predictions", required=True)
    parser.add_argument("--out-predictions", required=True)
    parser.add_argument("--out-summary", required=True)
    parser.add_argument("--source-split", choices=["train", "test"], default=None)
    args = parser.parse_args()

    rows = read_csv(Path(args.predictions))
    if args.source_split:
        marker = f"/{args.source_split}/"
        rows = [row for row in rows if marker in row["source_path"]]

    write_csv(Path(args.out_predictions), rows)
    write_csv(Path(args.out_summary), summarize(rows))
    print(f"Predictions: {len(rows)}")
    print(f"Summary rows: {len(summarize(rows))}")
    return 0


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
            }
        )

    if clean_acc is not None:
        for row in summary:
            row["relative_accuracy_drop"] = clean_acc - float(row["accuracy"])
    return summary


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())

