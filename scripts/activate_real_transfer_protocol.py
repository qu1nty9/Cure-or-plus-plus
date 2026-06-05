#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

METADATA_FIELDS = ["capture_device", "capture_date", "pipeline_variant", "notes"]
DEFAULT_FIELDNAMES = [
    "source_path",
    "output_path",
    "recipe",
    "severity",
    "app_or_pipeline",
    "label",
    "capture_device",
    "capture_date",
    "repeat_id",
    "pipeline_variant",
    "source_selection_id",
    "notes",
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Materialize, validate, and manifest a real-transfer protocol after outputs are collected."
    )
    parser.add_argument("--pairs-template", default="data/real_transfer/v02/pairs_template.csv")
    parser.add_argument("--checklist", default="data/real_transfer/v02/collection_pack/collection_checklist.csv")
    parser.add_argument("--pairs", default="data/real_transfer/v02/pairs.csv")
    parser.add_argument("--validation-report", default="reports/real_transfer_pairs_v02_validation.json")
    parser.add_argument("--status-report", default="reports/real_transfer_v02_activation_status.json")
    parser.add_argument("--manifest", default="data/real_transfer/v02/manifest.csv")
    parser.add_argument("--clean-manifest", default="data/interim/cure_or_clean_test_manifest.csv")
    parser.add_argument("--min-rows", type=int, default=180)
    parser.add_argument("--min-recipes", type=int, default=3)
    parser.add_argument("--min-labels", type=int, default=10)
    parser.add_argument("--min-repeats-per-source-recipe", type=int, default=2)
    parser.add_argument("--max-warning-details", type=int, default=80)
    parser.add_argument(
        "--require-ready",
        action="store_true",
        help="Exit with a failure code unless validation says the protocol is ready for evaluation.",
    )
    args = parser.parse_args()

    pairs_template_path = resolve_project_path(args.pairs_template)
    checklist_path = resolve_project_path(args.checklist)
    pairs_path = resolve_project_path(args.pairs)
    validation_report_path = resolve_project_path(args.validation_report)
    status_report_path = resolve_project_path(args.status_report)
    manifest_path = resolve_project_path(args.manifest)
    clean_manifest_path = resolve_project_path(args.clean_manifest)

    pair_rows = read_csv(pairs_template_path)
    if not pair_rows:
        raise ValueError(f"Pairs template has no rows: {pairs_template_path}")

    checklist_metadata = read_checklist_metadata(checklist_path)
    merged_rows = merge_metadata(pair_rows, checklist_metadata)
    write_csv(pairs_path, merged_rows, fieldnames=list(pair_rows[0].keys()) or DEFAULT_FIELDNAMES)

    validation = run_validation(args, pairs_path, clean_manifest_path, validation_report_path)
    status = build_status(merged_rows, validation, pairs_path, validation_report_path, manifest_path)

    manifest_written = False
    if validation.get("ready_for_eval"):
        run_manifest_builder(pairs_path, clean_manifest_path, manifest_path)
        manifest_written = manifest_path.exists()
    status["manifest_written"] = manifest_written
    status["manifest_build_skipped_reason"] = "" if manifest_written else "validation is not ready_for_eval"

    write_json(status_report_path, status)
    print_summary(status, pairs_path, validation_report_path, status_report_path, manifest_path)

    if args.require_ready and not validation.get("ready_for_eval"):
        return 1
    return 0


def read_checklist_metadata(path: Path) -> dict[str, dict[str, str]]:
    if not path.exists():
        return {}

    metadata_by_output: dict[str, dict[str, str]] = {}
    for row in read_csv(path):
        output_path = value(row, "expected_output_path")
        if not output_path:
            continue
        metadata_by_output[output_path] = {field: value(row, field) for field in METADATA_FIELDS}
    return metadata_by_output


def merge_metadata(pair_rows: list[dict], checklist_metadata: dict[str, dict[str, str]]) -> list[dict]:
    merged_rows = []
    for row in pair_rows:
        output_path = value(row, "output_path")
        merged = dict(row)
        metadata = checklist_metadata.get(output_path, {})
        for field in METADATA_FIELDS:
            if metadata.get(field):
                merged[field] = metadata[field]
        merged_rows.append(merged)
    return merged_rows


def run_validation(args, pairs_path: Path, clean_manifest_path: Path, validation_report_path: Path) -> dict:
    command = [
        sys.executable,
        str(ROOT / "scripts/validate_real_transfer_pairs.py"),
        "--pairs",
        str(pairs_path),
        "--clean-manifest",
        str(clean_manifest_path),
        "--report",
        str(validation_report_path),
        "--min-rows",
        str(args.min_rows),
        "--min-recipes",
        str(args.min_recipes),
        "--min-labels",
        str(args.min_labels),
        "--min-repeats-per-source-recipe",
        str(args.min_repeats_per_source_recipe),
        "--max-warning-details",
        str(args.max_warning_details),
        "--allow-missing-files",
    ]
    subprocess.run(command, cwd=ROOT, check=True)
    return read_json(validation_report_path)


def run_manifest_builder(pairs_path: Path, clean_manifest_path: Path, manifest_path: Path) -> None:
    command = [
        sys.executable,
        str(ROOT / "scripts/build_real_transfer_manifest.py"),
        "--pairs",
        str(pairs_path),
        "--clean-manifest",
        str(clean_manifest_path),
        "--output",
        str(manifest_path),
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def build_status(
    rows: list[dict],
    validation: dict,
    pairs_path: Path,
    validation_report_path: Path,
    manifest_path: Path,
) -> dict:
    present_rows = [row for row in rows if resolve_project_path(value(row, "output_path")).exists()]
    missing_rows = [row for row in rows if not resolve_project_path(value(row, "output_path")).exists()]
    by_recipe = build_counter_status(rows, present_rows, "recipe")
    by_label = build_counter_status(rows, present_rows, "label")
    by_repeat = build_counter_status(rows, present_rows, "repeat_id")

    return {
        "ready_for_eval": bool(validation.get("ready_for_eval")),
        "schema_ready": bool(validation.get("schema_ready")),
        "files_ready": bool(validation.get("files_ready")),
        "expected_output_count": len(rows),
        "present_output_count": len(present_rows),
        "missing_output_count": len(missing_rows),
        "pairs_path": relative_text(pairs_path),
        "validation_report_path": relative_text(validation_report_path),
        "manifest_path": relative_text(manifest_path),
        "by_recipe": by_recipe,
        "by_label": by_label,
        "by_repeat": by_repeat,
        "first_missing_output_paths": [value(row, "output_path") for row in missing_rows[:30]],
    }


def build_counter_status(rows: list[dict], present_rows: list[dict], key: str) -> dict[str, dict[str, int]]:
    expected = Counter(value(row, key) for row in rows if value(row, key))
    present = Counter(value(row, key) for row in present_rows if value(row, key))
    output = {}
    for item in sorted(expected):
        output[item] = {
            "expected": expected[item],
            "present": present[item],
            "missing": expected[item] - present[item],
        }
    return output


def print_summary(status: dict, pairs_path: Path, validation_report_path: Path, status_report_path: Path, manifest_path: Path) -> None:
    print(f"Pairs: {pairs_path}")
    print(f"Validation report: {validation_report_path}")
    print(f"Status report: {status_report_path}")
    print(f"Expected outputs: {status['expected_output_count']}")
    print(f"Present outputs: {status['present_output_count']}")
    print(f"Missing outputs: {status['missing_output_count']}")
    print(f"Ready for eval: {status['ready_for_eval']}")
    if status["ready_for_eval"]:
        print(f"Manifest: {manifest_path}")
    else:
        print("Manifest: skipped until all expected output files exist.")


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def value(row: dict, key: str) -> str:
    return str(row.get(key, "") or "").strip()


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def relative_text(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
