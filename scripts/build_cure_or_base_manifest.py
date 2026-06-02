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

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a clean-image manifest for mini-CURE-OR.")
    parser.add_argument("--dataset-dir", default="data/raw/mini_cure_or")
    parser.add_argument("--output", default="data/interim/cure_or_clean_manifest.csv")
    parser.add_argument("--splits", default="train,test", help="Comma-separated split names.")
    parser.add_argument("--challenge-type", default="1", help="CURE-OR challenge type to keep.")
    parser.add_argument("--challenge-level", default="0", help="CURE-OR challenge level to keep.")
    parser.add_argument("--label-map", choices=["mini_classes", "cure_or_objects", "raw"], default="mini_classes")
    parser.add_argument("--object-map", default="configs/cure_or_objects_v01.json")
    parser.add_argument("--max-per-class", type=int, default=None)
    args = parser.parse_args()

    dataset_dir = resolve_project_path(args.dataset_dir)
    output_path = resolve_project_path(args.output)
    split_names = [split.strip() for split in args.splits.split(",") if split.strip()]
    label_map = load_label_map(args.label_map, resolve_project_path(args.object_map))

    if not dataset_dir.exists():
        print(f"Dataset directory does not exist: {dataset_dir}")
        print("Expected mini-CURE-OR files under data/raw/mini_cure_or.")
        return 0

    image_index = build_image_index(dataset_dir)
    rows = []
    per_class_counts = defaultdict(int)

    for split in split_names:
        csv_path = dataset_dir / f"{split}.csv"
        if not csv_path.exists():
            print(f"Skipping missing split CSV: {csv_path}")
            continue

        with csv_path.open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                challenge_type = normalized_value(row, "challengeType", "challenge_type")
                challenge_level = normalized_value(row, "challengeLevel", "challenge_level")
                if challenge_type != args.challenge_type or challenge_level != args.challenge_level:
                    continue

                image_id = normalized_value(row, "imageID", "image_id")
                raw_class = normalized_value(row, "class", "object_id", "objectID", "objectId")
                label = label_from_raw_value(raw_class, label_map)
                if args.max_per_class is not None and per_class_counts[label] >= args.max_per_class:
                    continue

                image_path = find_image_path(image_index, image_id)
                if image_path is None:
                    print(f"Image listed in CSV was not found: {image_id}")
                    continue

                rows.append(
                    {
                        "image_id": image_id,
                        "image_path": display_path(image_path),
                        "label": label,
                        "object_id": raw_class,
                        "split": split,
                        "background": normalized_value(row, "background"),
                        "perspective": normalized_value(row, "perspective"),
                        "challenge_type": challenge_type,
                        "challenge_level": challenge_level,
                    }
                )
                per_class_counts[label] += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "image_id",
            "image_path",
            "label",
            "object_id",
            "split",
            "background",
            "perspective",
            "challenge_type",
            "challenge_level",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} clean source images to {output_path}")
    for label in sorted(per_class_counts):
        print(f"{label}: {per_class_counts[label]}")
    return 0


def build_image_index(dataset_dir: Path) -> dict[str, Path]:
    index = {}
    for path in dataset_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        index.setdefault(path.name, path)
        index.setdefault(path.stem, path)
    return index


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


def normalized_value(row: dict, *keys: str) -> str:
    for key in keys:
        if key in row and row[key] is not None:
            return str(row[key]).strip()
    return ""


def resolve_project_path(path: str) -> Path:
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
