#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SUPPORTED_SUFFIXES = [".jpg", ".jpeg", ".JPG", ".JPEG"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Import a numbered manual real-transfer collection pack into the "
            "pinned CURE-OR++ v02 output paths."
        )
    )
    parser.add_argument("--input-dir", required=True, help="Directory with numbered folders 1..N.")
    parser.add_argument(
        "--checklist",
        default="data/real_transfer/v02/collection_pack/collection_checklist.csv",
        help="Collection checklist that defines source order and expected output paths.",
    )
    parser.add_argument(
        "--report",
        default="reports/real_transfer_v02_clean_pack_import_report.json",
        help="JSON report path.",
    )
    parser.add_argument("--execute", action="store_true", help="Actually copy files. Default is dry-run.")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing existing output files.")
    args = parser.parse_args()

    input_dir = Path(args.input_dir).expanduser()
    checklist_path = resolve_project_path(args.checklist)
    report_path = resolve_project_path(args.report)

    rows = read_csv(checklist_path)
    groups = group_rows(rows)
    problems: list[str] = []
    mappings = build_mappings(input_dir, groups, problems)

    existing_outputs = []
    for mapping in mappings:
        output_path = resolve_project_path(mapping["expected_output_path"])
        if output_path.exists():
            existing_outputs.append(mapping["expected_output_path"])

    if existing_outputs and not args.overwrite:
        problems.append(
            f"{len(existing_outputs)} output files already exist; rerun with --overwrite if replacement is intended."
        )

    copied = []
    if args.execute and not problems:
        for mapping in mappings:
            source = Path(mapping["input_path"])
            target = resolve_project_path(mapping["expected_output_path"])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied.append(mapping["expected_output_path"])

    report = {
        "execute": args.execute,
        "input_dir": "<manual-clean-pack>",
        "checklist": relative_text(checklist_path),
        "report": relative_text(report_path),
        "source_group_count": len(groups),
        "expected_mapping_count": len(groups) * 6,
        "resolved_mapping_count": len(mappings),
        "existing_output_count": len(existing_outputs),
        "copied_count": len(copied),
        "problems": problems,
        "existing_outputs": existing_outputs[:50],
        "mappings_preview": sanitize_mapping_preview(mappings[:12], input_dir),
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Input dir: {input_dir}")
    print(f"Source groups: {len(groups)}")
    print(f"Resolved mappings: {len(mappings)}")
    print(f"Copied: {len(copied)}")
    print(f"Report: {report_path}")
    for problem in problems:
        print(f"ERROR: {problem}")

    return 1 if problems else 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def group_rows(rows: list[dict[str, str]]) -> list[list[dict[str, str]]]:
    groups: list[list[dict[str, str]]] = []
    current_key = None
    current: list[dict[str, str]] = []
    for row in rows:
        key = value(row, "source_selection_id")
        if key != current_key:
            if current:
                groups.append(current)
            current_key = key
            current = []
        current.append(row)
    if current:
        groups.append(current)
    return groups


def build_mappings(input_dir: Path, groups: list[list[dict[str, str]]], problems: list[str]) -> list[dict[str, str]]:
    mappings: list[dict[str, str]] = []
    if not input_dir.exists():
        problems.append(f"Input directory does not exist: {input_dir}")
        return mappings

    for group_index, rows in enumerate(groups, start=1):
        folder = input_dir / str(group_index)
        if not folder.exists():
            problems.append(f"Missing numbered source folder: {folder}")
            continue
        if len(rows) != 6:
            problems.append(f"Checklist source group {group_index} has {len(rows)} rows, expected 6.")
            continue
        for file_index, row in enumerate(rows, start=1):
            input_path = find_numbered_file(folder, file_index)
            if input_path is None:
                problems.append(f"Missing input image for folder {group_index}, file {file_index}.")
                continue
            mappings.append(
                {
                    "folder_index": str(group_index),
                    "file_index": str(file_index),
                    "source_selection_id": value(row, "source_selection_id"),
                    "label": value(row, "label"),
                    "source_image_id": value(row, "source_image_id"),
                    "recipe": value(row, "recipe"),
                    "repeat_id": value(row, "repeat_id"),
                    "input_path": str(input_path),
                    "expected_output_path": value(row, "expected_output_path"),
                }
            )
    return mappings


def find_numbered_file(folder: Path, index: int) -> Path | None:
    for suffix in SUPPORTED_SUFFIXES:
        candidate = folder / f"{index}{suffix}"
        if candidate.exists():
            return candidate
    return None


def sanitize_mapping_preview(mappings: list[dict[str, str]], input_dir: Path) -> list[dict[str, str]]:
    sanitized = []
    for mapping in mappings:
        row = dict(mapping)
        row["input_path"] = sanitize_input_path(Path(row["input_path"]), input_dir)
        sanitized.append(row)
    return sanitized


def sanitize_input_path(path: Path, input_dir: Path) -> str:
    try:
        return str(Path("<manual-clean-pack>") / path.resolve().relative_to(input_dir.resolve()))
    except ValueError:
        return "<manual-clean-pack>"


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


def value(row: dict[str, str], key: str) -> str:
    return str(row.get(key, "") or "").strip()


if __name__ == "__main__":
    raise SystemExit(main())
