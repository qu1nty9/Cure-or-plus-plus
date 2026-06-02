#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cure_or_pp.labels import object_label_key  # noqa: E402

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
CLEAN_FIELDNAMES = [
    "image_id",
    "image_path",
    "label",
    "object_id",
    "split",
    "background",
    "device",
    "orientation",
    "challenge_type",
    "challenge_level",
]
NATIVE_FIELDNAMES = [
    "source_path",
    "output_path",
    "label",
    "family",
    "recipe",
    "severity",
    "params_json",
    "source_metadata_json",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build small Full-CURE-OR probe manifests from extracted archives.")
    parser.add_argument("--archives-dir", default="/Volumes/980PRO/CURE-OR++/archives")
    parser.add_argument("--archive-config", default="configs/cure_or_dataport_archives_v01.json")
    parser.add_argument("--object-map", default="configs/cure_or_objects_v01.json")
    parser.add_argument("--clean-output", default="data/interim/full_cure_or_clean_probe_v01_manifest.csv")
    parser.add_argument("--native-output", default="data/interim/full_cure_or_native_probe_v01_manifest.csv")
    parser.add_argument("--challenge-types", default="2,5,9,14,18")
    parser.add_argument("--challenge-levels", default="1,2,3,4")
    parser.add_argument("--max-clean-per-object", type=int, default=1)
    parser.add_argument("--max-native-per-object-group", type=int, default=1)
    parser.add_argument("--sampling-strategy", choices=["first", "spread"], default="first")
    parser.add_argument("--verify-selected-images", action="store_true")
    parser.add_argument("--require-clean-source", action="store_true")
    args = parser.parse_args()

    archives_dir = Path(args.archives_dir)
    archive_config = json.loads(resolve_project_path(args.archive_config).read_text(encoding="utf-8"))
    object_map = json.loads(resolve_project_path(args.object_map).read_text(encoding="utf-8"))["objects"]
    challenge_types = {value.zfill(2) for value in parse_values(args.challenge_types)}
    challenge_levels = set(parse_values(args.challenge_levels))
    archive_by_type = {item["challenge_type"]: item for item in archive_config["archives"]}

    clean_rows, clean_index = build_clean_rows(
        archives_dir,
        archive_by_type["01"],
        object_map,
        args.max_clean_per_object,
        args.sampling_strategy,
        args.verify_selected_images,
    )
    native_rows = build_native_rows(
        archives_dir,
        archive_by_type,
        object_map,
        clean_index,
        challenge_types,
        challenge_levels,
        args.max_native_per_object_group,
        args.sampling_strategy,
        args.verify_selected_images,
        args.require_clean_source,
    )

    write_csv(resolve_project_path(args.clean_output), CLEAN_FIELDNAMES, clean_rows)
    write_csv(resolve_project_path(args.native_output), NATIVE_FIELDNAMES, native_rows)
    print(f"Clean rows: {len(clean_rows)}")
    print(f"Native rows: {len(native_rows)}")
    print(f"Clean output: {resolve_project_path(args.clean_output)}")
    print(f"Native output: {resolve_project_path(args.native_output)}")
    return 0


def build_clean_rows(
    archives_dir: Path,
    archive: dict,
    object_map: dict[str, str],
    max_per_object: int,
    sampling_strategy: str,
    verify_selected_images: bool,
) -> tuple[list[dict], dict[tuple[str, str, str, str], str]]:
    archive_dir = archives_dir / archive["filename"].replace(".tar.gz", "")
    rows = []
    clean_index = {}
    candidates_by_object: dict[str, list[tuple[Path, dict[str, str]]]] = {}

    for path in iter_image_paths(archive_dir):
        metadata = parse_image_filename(path)
        if metadata is None or metadata["challenge_type"] != "01":
            continue
        candidates_by_object.setdefault(metadata["object_id"], []).append((path, metadata))

    for object_id in sorted(candidates_by_object):
        for path, metadata in select_candidates(
            candidates_by_object[object_id],
            max_per_object,
            sampling_strategy,
            verify_selected_images,
        ):
            label = object_label_key(object_id, object_map[object_id])
            clean_index[clean_key(metadata)] = str(path)
            rows.append(
                {
                    "image_id": path.stem,
                    "image_path": str(path),
                    "label": label,
                    "object_id": object_id,
                    "split": "full_probe",
                    "background": metadata["background"],
                    "device": metadata["device"],
                    "orientation": metadata["orientation"],
                    "challenge_type": metadata["challenge_type"],
                    "challenge_level": metadata["challenge_level"],
                }
            )
    return rows, clean_index


def build_native_rows(
    archives_dir: Path,
    archive_by_type: dict[str, dict],
    object_map: dict[str, str],
    clean_index: dict[tuple[str, str, str, str], str],
    challenge_types: set[str],
    challenge_levels: set[str],
    max_per_object_group: int,
    sampling_strategy: str,
    verify_selected_images: bool,
    require_clean_source: bool,
) -> list[dict]:
    rows = []
    for challenge_type in sorted(challenge_types):
        archive = archive_by_type[challenge_type]
        archive_dir = archives_dir / archive["filename"].replace(".tar.gz", "")
        candidates_by_group: dict[tuple[str, str, str], list[tuple[Path, dict[str, str]]]] = {}
        for path in iter_image_paths(archive_dir):
            metadata = parse_image_filename(path)
            if metadata is None:
                continue
            if metadata["challenge_type"] != challenge_type:
                continue
            if metadata["challenge_level"] not in challenge_levels:
                continue
            if require_clean_source and clean_key(metadata) not in clean_index:
                continue

            object_id = metadata["object_id"]
            group_key = (challenge_type, metadata["challenge_level"], object_id)
            candidates_by_group.setdefault(group_key, []).append((path, metadata))

        for group_key in sorted(candidates_by_group):
            _, _, object_id = group_key
            for path, metadata in select_candidates(
                candidates_by_group[group_key],
                max_per_object_group,
                sampling_strategy,
                verify_selected_images,
            ):
                label = object_label_key(object_id, object_map[object_id])
                source_path = clean_index.get(clean_key(metadata), "")
                row_metadata = {
                    **metadata,
                    "image_path": str(path),
                    "label": label,
                    "challenge_name": archive["challenge_name"],
                    "split": "full_probe",
                }
                rows.append(
                    {
                        "source_path": source_path or str(path),
                        "output_path": str(path),
                        "label": label,
                        "family": "native_cure_or",
                        "recipe": f"native_challenge_type_{challenge_type}",
                        "severity": f"level_{metadata['challenge_level']}",
                        "params_json": json.dumps(
                            {
                                "challenge_type": challenge_type,
                                "challenge_name": archive["challenge_name"],
                                "challenge_level": metadata["challenge_level"],
                                "split": "full_probe",
                            },
                            sort_keys=True,
                        ),
                        "source_metadata_json": json.dumps(row_metadata, sort_keys=True),
                    }
                )
    return rows


def iter_image_paths(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name.startswith("._"):
            continue
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        yield path


def parse_image_filename(path: Path) -> dict[str, str] | None:
    parts = path.stem.split("_")
    if len(parts) != 6:
        return None
    background, device, orientation, object_id, challenge_type, challenge_level = parts
    return {
        "background": background,
        "device": device,
        "orientation": orientation,
        "object_id": object_id.zfill(3),
        "challenge_type": challenge_type.zfill(2),
        "challenge_level": challenge_level,
    }


def select_candidates(
    candidates: list[tuple[Path, dict[str, str]]],
    limit: int,
    sampling_strategy: str,
    verify_images: bool,
) -> list[tuple[Path, dict[str, str]]]:
    ordered = sorted(candidates, key=lambda item: metadata_sort_key(item[1], item[0]))
    if limit <= 0 or len(ordered) <= limit:
        selected = ordered
    else:
        if sampling_strategy == "first":
            selected = ordered[:limit]
        else:
            indexes = spread_indexes(len(ordered), limit)
            selected = [ordered[index] for index in indexes]
    if not verify_images:
        return selected
    return replace_unreadable_candidates(ordered, selected)


def replace_unreadable_candidates(
    ordered: list[tuple[Path, dict[str, str]]],
    selected: list[tuple[Path, dict[str, str]]],
) -> list[tuple[Path, dict[str, str]]]:
    selected_indexes = [ordered.index(item) for item in selected]
    output = []
    used: set[int] = set()
    for preferred_index in selected_indexes:
        for candidate_index in indexes_by_distance(len(ordered), preferred_index):
            if candidate_index in used:
                continue
            path, metadata = ordered[candidate_index]
            if not is_readable_image(path):
                continue
            output.append((path, metadata))
            used.add(candidate_index)
            break
    return output


def indexes_by_distance(total: int, preferred_index: int):
    indexes = range(total)
    return sorted(indexes, key=lambda index: (abs(index - preferred_index), index))


def spread_indexes(total: int, limit: int) -> list[int]:
    if limit == 1:
        return [0]
    indexes = []
    for position in range(limit):
        index = round(position * (total - 1) / (limit - 1))
        indexes.append(index)
    return indexes


def metadata_sort_key(metadata: dict[str, str], path: Path) -> tuple[int, int, int, int, str, str]:
    return (
        int(metadata["background"]),
        int(metadata["device"]),
        int(metadata["orientation"]),
        int(metadata["object_id"]),
        metadata["challenge_level"],
        str(path),
    )


def is_readable_image(path: Path) -> bool:
    try:
        with Image.open(path) as image:
            image.load()
        return True
    except (FileNotFoundError, UnidentifiedImageError, OSError):
        return False


def clean_key(metadata: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        metadata["background"],
        metadata["device"],
        metadata["orientation"],
        metadata["object_id"],
    )


def parse_values(raw: str) -> list[str]:
    return [value.strip() for value in raw.split(",") if value.strip()]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
