#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate real transfer pilot pairs before evaluation.")
    parser.add_argument("--pairs", default="data/real_transfer/v01/pairs.csv")
    parser.add_argument("--clean-manifest", default="data/interim/cure_or_clean_test_manifest.csv")
    parser.add_argument("--report", default="reports/real_transfer_pairs_v01_validation.json")
    parser.add_argument("--min-rows", type=int, default=20)
    parser.add_argument("--min-recipes", type=int, default=2)
    parser.add_argument("--min-labels", type=int, default=10)
    parser.add_argument("--min-repeats-per-source-recipe", type=int, default=1)
    parser.add_argument("--max-warning-details", type=int, default=50)
    parser.add_argument("--allow-empty", action="store_true", help="Allow empty or missing pairs for dry schema checks.")
    parser.add_argument("--allow-missing-files", action="store_true", help="Report missing files without failing.")
    args = parser.parse_args()

    pairs_path = resolve_project_path(args.pairs)
    clean_manifest_path = resolve_project_path(args.clean_manifest)
    report_path = resolve_project_path(args.report)

    clean_rows = load_clean_manifest(clean_manifest_path)
    clean_by_path = {normalize_path(row["image_path"]): row for row in clean_rows}
    problems: list[str] = []
    warnings: list[str] = []

    if not pairs_path.exists():
        problems.append(f"Pairs CSV does not exist: {relative(pairs_path)}")
        rows: list[dict] = []
    else:
        rows = load_pairs(pairs_path, problems)

    if rows:
        validate_rows(rows, clean_by_path, args, problems, warnings)
    elif not args.allow_empty:
        problems.append("Pairs CSV has no data rows.")

    recipe_counts = count_by(rows, "recipe")
    label_counts = count_labels(rows, clean_by_path)
    source_counts = count_by(rows, "source_path")
    output_counts = count_by(rows, "output_path")
    duplicate_pairs = duplicate_count(rows, ["source_path", "output_path", "recipe"])
    repeat_summary = summarize_repeats(rows)
    missing_source_file_count = count_missing_files(rows, "source_path")
    missing_output_file_count = count_missing_files(rows, "output_path")

    schema_ready = not problems and bool(rows)
    files_ready = missing_source_file_count == 0 and missing_output_file_count == 0
    ready = schema_ready and files_ready
    warning_details = warnings[: args.max_warning_details]
    report = {
        "ready_for_eval": ready,
        "schema_ready": schema_ready,
        "files_ready": files_ready,
        "pairs_path": str(relative(pairs_path)),
        "clean_manifest_path": str(relative(clean_manifest_path)),
        "row_count": len(rows),
        "recipe_count": len(recipe_counts),
        "label_count": len(label_counts),
        "source_count": len(source_counts),
        "output_count": len(output_counts),
        "duplicate_pair_count": duplicate_pairs,
        "missing_source_file_count": missing_source_file_count,
        "missing_output_file_count": missing_output_file_count,
        "source_recipe_count": repeat_summary["source_recipe_count"],
        "source_recipe_min_repeat_count": repeat_summary["min_repeat_count"],
        "source_recipe_max_repeat_count": repeat_summary["max_repeat_count"],
        "source_recipe_repeat_counts": repeat_summary["repeat_counts"],
        "recipe_counts": recipe_counts,
        "label_counts": label_counts,
        "problems": problems,
        "warnings": warning_details,
        "warning_count": len(warnings),
        "warnings_truncated_count": max(0, len(warnings) - len(warning_details)),
        "thresholds": {
            "min_rows": args.min_rows,
            "min_recipes": args.min_recipes,
            "min_labels": args.min_labels,
            "min_repeats_per_source_recipe": args.min_repeats_per_source_recipe,
            "max_warning_details": args.max_warning_details,
        },
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Rows: {len(rows)}")
    print(f"Recipes: {len(recipe_counts)}")
    print(f"Labels: {len(label_counts)}")
    print(f"Schema ready: {schema_ready}")
    print(f"Files ready: {files_ready}")
    print(f"Ready for eval: {ready}")
    print(f"Report: {report_path}")
    for problem in problems:
        print(f"ERROR: {problem}")
    for warning in warning_details:
        print(f"WARNING: {warning}")
    if len(warnings) > len(warning_details):
        print(f"WARNING: {len(warnings) - len(warning_details)} additional warnings omitted from console output.")
    return 0 if ready or args.allow_empty or args.allow_missing_files else 1


def load_clean_manifest(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_pairs(path: Path, problems: list[str]) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"source_path", "output_path", "recipe", "severity", "app_or_pipeline"}
        missing_columns = sorted(required - set(reader.fieldnames or []))
        if missing_columns:
            problems.append(f"Pairs CSV is missing required columns: {', '.join(missing_columns)}")
            return []
        return [{key: value(row, key) for key in reader.fieldnames or []} for row in reader]


def validate_rows(rows: list[dict], clean_by_path: dict[str, dict], args, problems: list[str], warnings: list[str]) -> None:
    if len(rows) < args.min_rows:
        problems.append(f"Expected at least {args.min_rows} rows, found {len(rows)}.")

    recipe_counts = count_by(rows, "recipe")
    if len(recipe_counts) < args.min_recipes:
        problems.append(f"Expected at least {args.min_recipes} recipes, found {len(recipe_counts)}.")

    label_counts = count_labels(rows, clean_by_path)
    if len(label_counts) < args.min_labels:
        problems.append(f"Expected at least {args.min_labels} labels, found {len(label_counts)}.")

    duplicate_pairs = duplicate_count(rows, ["source_path", "output_path", "recipe"])
    if duplicate_pairs:
        problems.append(f"Found {duplicate_pairs} duplicate source/output/recipe rows.")

    if args.min_repeats_per_source_recipe > 1:
        repeat_summary = summarize_repeats(rows)
        if repeat_summary["min_repeat_count"] < args.min_repeats_per_source_recipe:
            problems.append(
                "Expected at least "
                f"{args.min_repeats_per_source_recipe} repeats per source/recipe, "
                f"found a minimum of {repeat_summary['min_repeat_count']}."
            )

    for index, row in enumerate(rows, start=2):
        source_path = value(row, "source_path")
        output_path = value(row, "output_path")
        recipe = value(row, "recipe")
        severity = value(row, "severity")
        app_or_pipeline = value(row, "app_or_pipeline")
        label = value(row, "label")

        if not source_path or not output_path or not recipe:
            problems.append(f"Line {index}: source_path, output_path, and recipe are required.")
        if not severity:
            warnings.append(f"Line {index}: severity is empty; build script will default to real.")
        if not app_or_pipeline:
            warnings.append(f"Line {index}: app_or_pipeline is empty.")

        clean_row = clean_by_path.get(normalize_path(source_path))
        if clean_row is None and not label:
            problems.append(f"Line {index}: label is required when source_path is outside clean manifest.")
        if clean_row is not None and label and label != clean_row["label"]:
            problems.append(
                f"Line {index}: label mismatch for {source_path}: pair has {label}, clean manifest has {clean_row['label']}."
            )

        for column_name, path_text in [("source_path", source_path), ("output_path", output_path)]:
            if not path_text:
                continue
            if not resolve_project_path(path_text).exists():
                message = f"Line {index}: {column_name} does not exist: {path_text}"
                if args.allow_missing_files:
                    warnings.append(message)
                else:
                    problems.append(message)


def count_by(rows: list[dict], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        item = value(row, key)
        if item:
            counts[item] = counts.get(item, 0) + 1
    return dict(sorted(counts.items()))


def count_labels(rows: list[dict], clean_by_path: dict[str, dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        label = value(row, "label")
        if not label:
            label = clean_by_path.get(normalize_path(value(row, "source_path")), {}).get("label", "")
        if label:
            counts[label] = counts.get(label, 0) + 1
    return dict(sorted(counts.items()))


def duplicate_count(rows: list[dict], keys: list[str]) -> int:
    seen = set()
    duplicates = 0
    for row in rows:
        item = tuple(value(row, key) for key in keys)
        if item in seen:
            duplicates += 1
        seen.add(item)
    return duplicates


def count_missing_files(rows: list[dict], key: str) -> int:
    missing = 0
    for row in rows:
        path_text = value(row, key)
        if path_text and not resolve_project_path(path_text).exists():
            missing += 1
    return missing


def summarize_repeats(rows: list[dict]) -> dict:
    repeat_sets: dict[tuple[str, str], set[str]] = {}
    for row in rows:
        source_path = value(row, "source_path")
        recipe = value(row, "recipe")
        repeat_id = value(row, "repeat_id") or value(row, "output_path")
        if not source_path or not recipe:
            continue
        repeat_sets.setdefault((source_path, recipe), set()).add(repeat_id)

    counts = {f"{source_path}|{recipe}": len(repeats) for (source_path, recipe), repeats in repeat_sets.items()}
    values = list(counts.values())
    return {
        "source_recipe_count": len(counts),
        "min_repeat_count": min(values) if values else 0,
        "max_repeat_count": max(values) if values else 0,
        "repeat_counts": dict(sorted(counts.items())),
    }


def value(row: dict, key: str) -> str:
    return str(row.get(key, "") or "").strip()


def normalize_path(path: str) -> str:
    return str(Path(path))


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def relative(path: Path) -> Path:
    try:
        return path.resolve().relative_to(ROOT)
    except ValueError:
        return path


if __name__ == "__main__":
    raise SystemExit(main())
