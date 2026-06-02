#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect local mini-CURE-OR challenge scope.")
    parser.add_argument("--dataset-dir", default="data/raw/mini_cure_or")
    parser.add_argument("--output", default="reports/mini_cure_or_scope_v01.csv")
    args = parser.parse_args()

    dataset_dir = resolve_project_path(args.dataset_dir)
    output_path = resolve_project_path(args.output)
    rows = load_rows(dataset_dir)
    counts = Counter(
        (row["split"], row["challengeType"], row["challengeLevel"])
        for row in rows
    )
    output_rows = [
        {
            "split": split,
            "challenge_type": challenge_type,
            "challenge_level": challenge_level,
            "n": count,
        }
        for (split, challenge_type, challenge_level), count in sorted(counts.items())
    ]
    write_csv(output_path, output_rows)
    print(f"Rows: {len(rows)}")
    print(f"Scope rows: {len(output_rows)}")
    print(f"Wrote {output_path}")
    return 0


def load_rows(dataset_dir: Path) -> list[dict]:
    rows = []
    for split in ["train", "test"]:
        csv_path = dataset_dir / f"{split}.csv"
        with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                row["split"] = split
                rows.append(row)
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
