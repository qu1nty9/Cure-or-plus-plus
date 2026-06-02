#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Print compact CURE-OR++ result summaries.")
    parser.add_argument("summary_csv")
    args = parser.parse_args()

    rows = load_rows(Path(args.summary_csv))
    if not rows:
        print("No rows.")
        return 0

    print("Family averages:")
    for family in sorted({row["family"] for row in rows}):
        family_rows = [row for row in rows if row["family"] == family]
        print(f"{family}: {mean_acc(family_rows):.4f}")

    print("\nRecipes by high-severity accuracy:")
    high_rows = [row for row in rows if row["severity"] in {"clean", "high"}]
    for row in sorted(high_rows, key=lambda item: float(item["accuracy"])):
        drop = row.get("relative_accuracy_drop", "")
        drop_text = "" if drop == "" else f", drop={float(drop):.4f}"
        print(f"{row['family']}/{row['recipe']}/{row['severity']}: acc={float(row['accuracy']):.4f}{drop_text}")
    return 0


def load_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def mean_acc(rows: list[dict]) -> float:
    return sum(float(row["accuracy"]) for row in rows) / len(rows)


if __name__ == "__main__":
    raise SystemExit(main())

