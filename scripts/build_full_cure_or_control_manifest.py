#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_full_cure_or_probe_manifests import (  # noqa: E402
    NATIVE_FIELDNAMES,
    clean_key,
    iter_image_paths,
    parse_image_filename,
    select_candidates,
    write_csv,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build paired Full-CURE-OR no-challenge control manifest.")
    parser.add_argument("--archives-dir", default="/Volumes/980PRO/CURE-OR++/archives")
    parser.add_argument("--archive-config", default="configs/cure_or_dataport_archives_v01.json")
    parser.add_argument("--clean-manifest", default="data/interim/full_cure_or_clean_probe_v04_manifest.csv")
    parser.add_argument("--output", default="data/interim/full_cure_or_grayscale_control_v04_manifest.csv")
    parser.add_argument("--control-type", default="10")
    parser.add_argument("--max-per-object", type=int, default=5)
    parser.add_argument("--sampling-strategy", choices=["first", "spread"], default="spread")
    parser.add_argument("--verify-selected-images", action="store_true")
    args = parser.parse_args()

    archive_config = json.loads(resolve_project_path(args.archive_config).read_text(encoding="utf-8"))
    archive_by_type = {item["challenge_type"]: item for item in archive_config["archives"]}
    control_type = args.control_type.zfill(2)
    if control_type not in archive_by_type:
        raise ValueError(f"Control type {control_type} is not present in {args.archive_config}")

    clean_index = load_clean_index(resolve_project_path(args.clean_manifest))
    rows = build_control_rows(
        archives_dir=Path(args.archives_dir),
        archive=archive_by_type[control_type],
        clean_index=clean_index,
        control_type=control_type,
        max_per_object=args.max_per_object,
        sampling_strategy=args.sampling_strategy,
        verify_selected_images=args.verify_selected_images,
    )

    output_path = resolve_project_path(args.output)
    write_csv(output_path, NATIVE_FIELDNAMES, rows)
    print(f"Control rows: {len(rows)}")
    print(f"Control output: {output_path}")
    print_underfilled_groups(rows, args.max_per_object)
    return 0


def load_clean_index(path: Path) -> dict[tuple[str, str, str, str], dict]:
    clean_rows = {}
    with path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row["background"], row["device"], row["orientation"], row["object_id"])
            clean_rows[key] = row
    return clean_rows


def build_control_rows(
    *,
    archives_dir: Path,
    archive: dict,
    clean_index: dict[tuple[str, str, str, str], dict],
    control_type: str,
    max_per_object: int,
    sampling_strategy: str,
    verify_selected_images: bool,
) -> list[dict]:
    archive_dir = archives_dir / archive["filename"].replace(".tar.gz", "")
    candidates_by_object: dict[str, list[tuple[Path, dict[str, str]]]] = {}

    for path in iter_image_paths(archive_dir):
        metadata = parse_image_filename(path)
        if metadata is None or metadata["challenge_type"] != control_type:
            continue
        if clean_key(metadata) not in clean_index:
            continue
        candidates_by_object.setdefault(metadata["object_id"], []).append((path, metadata))

    rows = []
    for object_id in sorted(candidates_by_object):
        selected = select_candidates(
            candidates_by_object[object_id],
            max_per_object,
            sampling_strategy,
            verify_selected_images,
        )
        for path, metadata in selected:
            source = clean_index[clean_key(metadata)]
            source_metadata = {
                **metadata,
                "image_path": str(path),
                "label": source["label"],
                "challenge_name": archive["challenge_name"],
                "split": "full_probe",
            }
            rows.append(
                {
                    "source_path": source["image_path"],
                    "output_path": str(path),
                    "label": source["label"],
                    "family": "control_cure_or",
                    "recipe": "grayscale_no_challenge",
                    "severity": "control",
                    "params_json": json.dumps(
                        {
                            "challenge_type": control_type,
                            "challenge_name": archive["challenge_name"],
                            "challenge_level": metadata["challenge_level"],
                            "split": "full_probe",
                        },
                        sort_keys=True,
                    ),
                    "source_metadata_json": json.dumps(source_metadata, sort_keys=True),
                }
            )
    return rows


def print_underfilled_groups(rows: list[dict], expected: int) -> None:
    counts: dict[str, int] = {}
    for row in rows:
        metadata = json.loads(row["source_metadata_json"])
        counts[metadata["object_id"]] = counts.get(metadata["object_id"], 0) + 1

    underfilled = {object_id: count for object_id, count in counts.items() if count < expected}
    if not underfilled:
        return
    print("Underfilled object groups:")
    for object_id, count in sorted(underfilled.items()):
        print(f"  object_{object_id}: {count}/{expected}")


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
