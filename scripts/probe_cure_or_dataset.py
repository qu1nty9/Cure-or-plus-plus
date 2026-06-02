#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe a local CURE-OR style dataset before evaluation.")
    parser.add_argument("--dataset-dir", default="data/raw/mini_cure_or")
    parser.add_argument("--splits", default="train,test", help="Comma-separated split names.")
    parser.add_argument("--challenge-map", default="configs/cure_or_challenge_types_v01.json")
    parser.add_argument("--output", default="reports/cure_or_dataset_probe_v01.json")
    parser.add_argument("--scope-output", default="reports/cure_or_dataset_scope_v01.csv")
    parser.add_argument("--skip-image-scan", action="store_true")
    parser.add_argument("--max-missing-samples", type=int, default=20)
    args = parser.parse_args()

    dataset_dir = resolve_project_path(args.dataset_dir)
    output_path = resolve_project_path(args.output)
    scope_output_path = resolve_project_path(args.scope_output)
    split_names = parse_values(args.splits)
    challenge_names = load_challenge_names(resolve_project_path(args.challenge_map))

    rows = load_rows(dataset_dir, split_names)
    scope_rows = build_scope_rows(rows, challenge_names)
    image_index = {} if args.skip_image_scan else build_image_index(dataset_dir)
    file_stats = {} if args.skip_image_scan else build_file_stats(dataset_dir)
    image_check = (
        {"skipped": True}
        if args.skip_image_scan
        else check_images(rows, image_index, args.max_missing_samples)
    )

    summary = {
        "dataset_dir": display_path(dataset_dir),
        "splits": split_names,
        "csv_rows_total": len(rows),
        "csv_rows_by_split": dict(sorted(Counter(row["split"] for row in rows).items())),
        "clean_rows": count_rows(rows, challenge_type="1", challenge_level="0"),
        "grayscale_rows": count_rows(rows, challenge_type="10", challenge_level="0"),
        "native_challenge_rows": count_native_challenge_rows(rows),
        "challenge_types": sorted({normalized_value(row, "challengeType", "challenge_type").zfill(2) for row in rows}),
        "challenge_levels": sorted({normalized_value(row, "challengeLevel", "challenge_level") for row in rows}),
        "scope_rows": len(scope_rows),
        "image_scan": file_stats,
        "image_check": image_check,
        "scope_output": display_path(scope_output_path),
    }

    write_csv(scope_output_path, scope_rows)
    write_json(output_path, summary)
    print(f"Rows: {summary['csv_rows_total']}")
    print(f"Clean rows: {summary['clean_rows']}")
    print(f"Native challenge rows: {summary['native_challenge_rows']}")
    if not args.skip_image_scan:
        print(f"Image files: {file_stats['image_files']}")
        print(f"Image bytes: {file_stats['image_bytes']}")
        print(f"Missing image rows: {image_check['missing_rows']}")
    print(f"Wrote {output_path}")
    print(f"Wrote {scope_output_path}")
    return 0


def parse_values(raw: str) -> list[str]:
    return [value.strip() for value in raw.split(",") if value.strip()]


def load_challenge_names(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {
        key: value["display_name"]
        for key, value in raw.get("challenge_types", {}).items()
        if isinstance(value, dict) and "display_name" in value
    }


def load_rows(dataset_dir: Path, split_names: list[str]) -> list[dict]:
    rows = []
    for split in split_names:
        csv_path = dataset_dir / f"{split}.csv"
        if not csv_path.exists():
            print(f"Skipping missing split CSV: {csv_path}")
            continue
        with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                row["split"] = split
                rows.append(row)
    return rows


def build_scope_rows(rows: list[dict], challenge_names: dict[str, str]) -> list[dict]:
    counts = Counter()
    for row in rows:
        challenge_type = normalized_value(row, "challengeType", "challenge_type")
        challenge_level = normalized_value(row, "challengeLevel", "challenge_level")
        key = (row["split"], challenge_type.zfill(2), challenge_level)
        counts[key] += 1

    return [
        {
            "split": split,
            "challenge_type": challenge_type,
            "challenge_name": challenge_names.get(challenge_type, ""),
            "challenge_level": challenge_level,
            "n": count,
        }
        for (split, challenge_type, challenge_level), count in sorted(counts.items())
    ]


def build_image_index(dataset_dir: Path) -> dict[str, Path]:
    index = {}
    for path in dataset_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        index.setdefault(path.name, path)
        index.setdefault(path.stem, path)
    return index


def build_file_stats(dataset_dir: Path) -> dict:
    image_files = 0
    image_bytes = 0
    for path in dataset_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        image_files += 1
        image_bytes += path.stat().st_size
    return {
        "skipped": False,
        "image_files": image_files,
        "image_bytes": image_bytes,
        "image_gb": round(image_bytes / (1024**3), 4),
    }


def check_images(rows: list[dict], image_index: dict[str, Path], max_missing_samples: int) -> dict:
    missing_samples = []
    found_rows = 0
    for row in rows:
        image_id = normalized_value(row, "imageID", "image_id")
        image_path = find_image_path(image_index, image_id)
        if image_path is None:
            if len(missing_samples) < max_missing_samples:
                missing_samples.append(
                    {
                        "split": row["split"],
                        "image_id": image_id,
                        "challenge_type": normalized_value(row, "challengeType", "challenge_type"),
                        "challenge_level": normalized_value(row, "challengeLevel", "challenge_level"),
                    }
                )
            continue
        found_rows += 1

    return {
        "skipped": False,
        "found_rows": found_rows,
        "missing_rows": len(rows) - found_rows,
        "missing_samples": missing_samples,
    }


def find_image_path(image_index: dict[str, Path], image_id: str) -> Path | None:
    candidates = [image_id, Path(image_id).stem]
    if image_id.isdigit():
        candidates.extend([image_id.zfill(5), image_id.zfill(6)])

    for candidate_id in candidates:
        if candidate_id in image_index:
            return image_index[candidate_id]

    for extension in IMAGE_EXTENSIONS:
        for candidate_id in candidates:
            candidate = f"{candidate_id}{extension}"
            if candidate in image_index:
                return image_index[candidate]
    return None


def count_rows(rows: list[dict], challenge_type: str, challenge_level: str) -> int:
    return sum(
        1
        for row in rows
        if normalized_value(row, "challengeType", "challenge_type") == challenge_type
        and normalized_value(row, "challengeLevel", "challenge_level") == challenge_level
    )


def count_native_challenge_rows(rows: list[dict]) -> int:
    return sum(
        1
        for row in rows
        if not (
            normalized_value(row, "challengeType", "challenge_type") == "1"
            and normalized_value(row, "challengeLevel", "challenge_level") == "0"
        )
    )


def normalized_value(row: dict, *keys: str) -> str:
    for key in keys:
        if key in row and row[key] is not None:
            return str(row[key]).strip()
    return ""


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
