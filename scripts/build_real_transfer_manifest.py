#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OUTPUT_FIELDNAMES = [
    "source_path",
    "output_path",
    "label",
    "family",
    "recipe",
    "severity",
    "params_json",
    "source_metadata_json",
    "app_or_pipeline",
    "capture_device",
    "capture_date",
    "notes",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a manifest for real CURE-OR++ transfer samples.")
    parser.add_argument("--pairs", default="data/real_transfer/v01/pairs.csv")
    parser.add_argument("--clean-manifest", default="data/interim/cure_or_clean_test_manifest.csv")
    parser.add_argument("--output", default="data/real_transfer/v01/manifest.csv")
    parser.add_argument("--allow-missing", action="store_true", help="Write rows even if referenced files are missing.")
    args = parser.parse_args()

    pairs_path = resolve_project_path(args.pairs)
    clean_manifest_path = resolve_project_path(args.clean_manifest)
    output_path = resolve_project_path(args.output)

    if not pairs_path.exists():
        print(f"Pairs CSV does not exist: {pairs_path}")
        print("Copy data/real_transfer/v01/pairs_template.csv to pairs.csv and add real transfer rows.")
        return 1

    clean_by_path = load_clean_manifest(clean_manifest_path)
    rows, problems = build_rows(pairs_path, clean_by_path)

    if problems and not args.allow_missing:
        for problem in problems:
            print(problem)
        print("Manifest was not written. Re-run with --allow-missing only for schema checks.")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(output_path, rows)
    print(f"Wrote {len(rows)} real transfer rows to {output_path}")
    if problems:
        print(f"Warnings: {len(problems)} missing or incomplete references")
    return 0


def load_clean_manifest(path: Path) -> dict[str, dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {normalize_path(row["image_path"]): row for row in rows}


def build_rows(pairs_path: Path, clean_by_path: dict[str, dict]) -> tuple[list[dict], list[str]]:
    rows = []
    problems = []
    with pairs_path.open("r", newline="", encoding="utf-8") as handle:
        for line_number, pair in enumerate(csv.DictReader(handle), start=2):
            source_path = value(pair, "source_path")
            output_path = value(pair, "output_path")
            recipe = value(pair, "recipe")
            severity = value(pair, "severity") or "real"
            app_or_pipeline = value(pair, "app_or_pipeline")

            if not source_path or not output_path or not recipe:
                problems.append(f"Line {line_number}: source_path, output_path, and recipe are required.")
                continue

            source_metadata = clean_by_path.get(normalize_path(source_path), {})
            label = value(pair, "label") or source_metadata.get("label", "")
            if not label:
                problems.append(f"Line {line_number}: label is required when source_path is not in clean manifest.")

            for column_name, path_text in [("source_path", source_path), ("output_path", output_path)]:
                if not resolve_project_path(path_text).exists():
                    problems.append(f"Line {line_number}: {column_name} does not exist: {path_text}")

            capture_device = value(pair, "capture_device")
            capture_date = value(pair, "capture_date")
            notes = value(pair, "notes")
            params = {
                "app_or_pipeline": app_or_pipeline,
                "capture_device": capture_device,
                "capture_date": capture_date,
                "notes": notes,
            }
            rows.append(
                {
                    "source_path": source_path,
                    "output_path": output_path,
                    "label": label,
                    "family": "real_transfer",
                    "recipe": recipe,
                    "severity": severity,
                    "params_json": json.dumps(params, sort_keys=True),
                    "source_metadata_json": json.dumps(source_metadata, sort_keys=True) if source_metadata else "",
                    "app_or_pipeline": app_or_pipeline,
                    "capture_device": capture_device,
                    "capture_date": capture_date,
                    "notes": notes,
                }
            )
    return rows, problems


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def value(row: dict, key: str) -> str:
    return str(row.get(key, "") or "").strip()


def normalize_path(path: str) -> str:
    return str(Path(path))


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
