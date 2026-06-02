from __future__ import annotations

import csv
import json
from pathlib import Path


def load_eval_rows(clean_manifest_path: Path, distorted_manifest_path: Path) -> list[dict]:
    rows: list[dict] = []

    with clean_manifest_path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "image_path": row["image_path"],
                    "source_path": row["image_path"],
                    "label": row["label"],
                    "family": "clean",
                    "recipe": "clean",
                    "severity": "clean",
                    "source_metadata_json": json.dumps(row, sort_keys=True),
                }
            )

    with distorted_manifest_path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                {
                    "image_path": row["output_path"],
                    "source_path": row["source_path"],
                    "label": row["label"],
                    "family": row["family"],
                    "recipe": row["recipe"],
                    "severity": row["severity"],
                    "source_metadata_json": row.get("source_metadata_json", ""),
                }
            )

    return rows
