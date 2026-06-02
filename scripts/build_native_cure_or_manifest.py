#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cure_or_pp.labels import normalize_label, object_label_key  # noqa: E402

MINI_CURE_OR_CLASSES = {
    "1": "canon_camera",
    "2": "training_marker_cone",
    "3": "baseball",
    "4": "pan",
    "5": "toy",
    "6": "lg_cell_phone",
    "7": "hair_brush",
    "8": "dymo_label_maker",
    "9": "calcium_bottle",
    "10": "shoes",
}

CURE_OR_CHALLENGE_TYPES = {
    "01": "no_challenge",
    "02": "resize",
    "03": "underexposure",
    "04": "overexposure",
    "05": "gaussian_blur",
    "06": "contrast",
    "07": "dirty_lens_1",
    "08": "dirty_lens_2",
    "09": "salt_pepper_noise",
    "10": "grayscale",
    "11": "grayscale_resize",
    "12": "grayscale_underexposure",
    "13": "grayscale_overexposure",
    "14": "grayscale_gaussian_blur",
    "15": "grayscale_contrast",
    "16": "grayscale_dirty_lens_1",
    "17": "grayscale_dirty_lens_2",
    "18": "grayscale_salt_pepper_noise",
}

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

FIELDNAMES = [
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
    parser = argparse.ArgumentParser(description="Build a native mini-CURE-OR challenge manifest.")
    parser.add_argument("--dataset-dir", default="data/raw/mini_cure_or")
    parser.add_argument("--output", default="data/interim/mini_cure_or_native_manifest.csv")
    parser.add_argument("--splits", default="test", help="Comma-separated split names.")
    parser.add_argument("--challenge-types", default="2,8,14", help="Comma-separated challengeType values, or all.")
    parser.add_argument("--challenge-levels", default="1,2,3,4", help="Comma-separated challengeLevel values, or all.")
    parser.add_argument("--label-map", choices=["mini_classes", "cure_or_objects", "raw"], default="mini_classes")
    parser.add_argument("--object-map", default="configs/cure_or_objects_v01.json")
    parser.add_argument("--max-per-class-per-group", type=int, default=None)
    args = parser.parse_args()

    dataset_dir = resolve_project_path(args.dataset_dir)
    output_path = resolve_project_path(args.output)
    split_names = parse_values(args.splits)
    challenge_types = None if args.challenge_types == "all" else set(parse_values(args.challenge_types))
    challenge_levels = None if args.challenge_levels == "all" else set(parse_values(args.challenge_levels))
    label_map = load_label_map(args.label_map, resolve_project_path(args.object_map))

    image_index = build_image_index(dataset_dir)
    rows = []
    counts: dict[tuple[str, str, str, str], int] = defaultdict(int)

    for split in split_names:
        csv_path = dataset_dir / f"{split}.csv"
        if not csv_path.exists():
            print(f"Skipping missing split CSV: {csv_path}")
            continue

        with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                challenge_type = normalized_value(row, "challengeType", "challenge_type")
                challenge_level = normalized_value(row, "challengeLevel", "challenge_level")
                if challenge_types is not None and challenge_type not in challenge_types:
                    continue
                if challenge_levels is not None and challenge_level not in challenge_levels:
                    continue

                image_id = normalized_value(row, "imageID", "image_id")
                raw_class = normalized_value(row, "class", "object_id", "objectID", "objectId")
                label = label_from_raw_value(raw_class, label_map)
                challenge_type_key = challenge_type.zfill(2)
                challenge_name = CURE_OR_CHALLENGE_TYPES.get(challenge_type_key, f"unknown_{challenge_type_key}")
                group_key = (split, challenge_type, challenge_level, label)
                if args.max_per_class_per_group is not None and counts[group_key] >= args.max_per_class_per_group:
                    continue

                image_path = find_image_path(image_index, image_id)
                if image_path is None:
                    print(f"Image listed in CSV was not found: {image_id}")
                    continue

                metadata = {
                    "image_id": image_id,
                    "image_path": display_path(image_path),
                    "label": label,
                    "object_id": raw_class,
                    "split": split,
                    "background": normalized_value(row, "background"),
                    "perspective": normalized_value(row, "perspective"),
                    "challenge_type": challenge_type,
                    "challenge_name": challenge_name,
                    "challenge_level": challenge_level,
                }
                rows.append(
                    {
                        "source_path": display_path(image_path),
                        "output_path": display_path(image_path),
                        "label": label,
                        "family": "native_cure_or",
                        "recipe": f"native_challenge_type_{int(challenge_type):02d}",
                        "severity": f"level_{challenge_level}",
                        "params_json": json.dumps(
                            {
                                "challenge_type": challenge_type,
                                "challenge_name": challenge_name,
                                "challenge_level": challenge_level,
                                "split": split,
                            },
                            sort_keys=True,
                        ),
                        "source_metadata_json": json.dumps(metadata, sort_keys=True),
                    }
                )
                counts[group_key] += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(output_path, rows)
    print(f"Wrote {len(rows)} native challenge rows to {output_path}")
    for (split, challenge_type, challenge_level), count in sorted(group_counts(rows).items()):
        print(f"{split} challengeType={challenge_type} challengeLevel={challenge_level}: {count}")
    return 0


def parse_values(raw: str) -> list[str]:
    return [value.strip() for value in raw.split(",") if value.strip()]


def load_label_map(label_map_name: str, object_map_path: Path) -> dict[str, str]:
    if label_map_name == "mini_classes":
        return MINI_CURE_OR_CLASSES
    if label_map_name == "raw":
        return {}
    raw = json.loads(object_map_path.read_text(encoding="utf-8"))
    return {
        key: object_label_key(key, value)
        for key, value in raw["objects"].items()
    }


def label_from_raw_value(raw_value: str, label_map: dict[str, str]) -> str:
    if not label_map:
        return raw_value
    candidates = [raw_value]
    if raw_value.isdigit():
        candidates.extend([raw_value.zfill(2), raw_value.zfill(3)])
    for candidate in candidates:
        if candidate in label_map:
            return label_map[candidate]
    return raw_value


def build_image_index(dataset_dir: Path) -> dict[str, Path]:
    index = {}
    for path in dataset_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        index.setdefault(path.name, path)
        index.setdefault(path.stem, path)
    return index


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


def group_counts(rows: list[dict]) -> dict[tuple[str, str, str], int]:
    counts: dict[tuple[str, str, str], int] = defaultdict(int)
    for row in rows:
        metadata = json.loads(row["source_metadata_json"])
        key = (metadata["split"], metadata["challenge_type"], metadata["challenge_level"])
        counts[key] += 1
    return counts


def normalized_value(row: dict, *keys: str) -> str:
    for key in keys:
        if key in row and row[key] is not None:
            return str(row[key]).strip()
    return ""


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


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
