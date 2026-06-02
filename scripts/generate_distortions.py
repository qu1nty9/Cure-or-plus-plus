#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cure_or_pp.corruptions import apply_recipe  # noqa: E402
from cure_or_pp.io import infer_label, iter_images, output_path_for  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate CURE-OR++ distorted images.")
    parser.add_argument("--config", default="configs/benchmark_v0.json", help="Path to JSON config.")
    parser.add_argument("--limit", type=int, default=None, help="Optional max number of source images.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned work without writing images.")
    args = parser.parse_args()

    config_path = resolve_project_path(args.config)
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    input_dir = resolve_project_path(config["input_dir"])
    output_dir = resolve_project_path(config["output_dir"])
    manifest_path = resolve_project_path(config["manifest_path"])
    seed = int(config.get("seed", 0))

    sources = load_sources(config, input_dir, args.limit)

    if not sources:
        print("No source images found.")
        return 0

    planned = len(sources) * sum(len(recipe["levels"]) for recipe in config["recipes"])
    print(f"Source images: {len(sources)}")
    print(f"Distorted outputs planned: {planned}")

    if args.dry_run:
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    with manifest_path.open("w", newline="", encoding="utf-8") as manifest_file:
        writer = csv.DictWriter(
            manifest_file,
            fieldnames=[
                "source_path",
                "output_path",
                "label",
                "family",
                "recipe",
                "severity",
                "params_json",
                "source_metadata_json",
            ],
        )
        writer.writeheader()

        written = 0
        skipped = 0
        for source_index, source in enumerate(sources):
            source_path = source["path"]
            try:
                with Image.open(source_path) as opened:
                    source_image = opened.convert("RGB")
            except (UnidentifiedImageError, OSError) as exc:
                skipped += 1
                print(f"Skipping unreadable image {source_path}: {exc}")
                continue

            for recipe in config["recipes"]:
                recipe_name = recipe["name"]
                family = recipe["family"]
                for severity, params in recipe["levels"].items():
                    rng = np.random.default_rng(stable_seed(seed, source_path, recipe_name, severity))
                    distorted = apply_recipe(source_image, recipe_name, params, rng)
                    target_path = target_path_for_source(
                        source_path,
                        input_dir,
                        output_dir,
                        recipe_name,
                        severity,
                        source_index,
                        source["metadata"],
                    )
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    distorted.save(target_path, format="JPEG", quality=95)

                    writer.writerow(
                        {
                            "source_path": display_path(source_path),
                            "output_path": display_path(target_path),
                            "label": source["label"],
                            "family": family,
                            "recipe": recipe_name,
                            "severity": severity,
                            "params_json": json.dumps(params, sort_keys=True),
                            "source_metadata_json": json.dumps(source["metadata"], sort_keys=True),
                        }
                    )
                    written += 1

    print(f"Wrote {written} distorted images.")
    print(f"Skipped {skipped} unreadable images.")
    print(f"Manifest: {manifest_path}")
    return 0


def resolve_project_path(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def load_sources(config: dict, input_dir: Path, limit: int | None) -> list[dict]:
    source_manifest = config.get("source_manifest_path")
    if source_manifest:
        manifest_path = resolve_project_path(source_manifest)
        if manifest_path.exists():
            sources = load_sources_from_manifest(manifest_path)
            return sources[:limit] if limit is not None else sources
        print(f"Source manifest does not exist yet: {manifest_path}")
        print("Falling back to recursive image scan.")

    if not input_dir.exists():
        print(f"Input directory does not exist yet: {input_dir}")
        return []

    image_paths = iter_images(input_dir, config["image_extensions"])
    if limit is not None:
        image_paths = image_paths[:limit]
    return [
        {
            "path": path,
            "label": infer_label(path, input_dir),
            "metadata": {},
        }
        for path in image_paths
    ]


def load_sources_from_manifest(manifest_path: Path) -> list[dict]:
    sources = []
    with manifest_path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if "image_path" not in (reader.fieldnames or []):
            raise ValueError(f"{manifest_path} must contain an image_path column.")

        for row in reader:
            source_path = resolve_project_path(row["image_path"])
            label = row.get("label") or row.get("class") or row.get("object_id") or ""
            sources.append(
                {
                    "path": source_path,
                    "label": label,
                    "metadata": dict(row),
                }
            )
    return sources


def target_path_for_source(
    source_path: Path,
    input_dir: Path,
    output_dir: Path,
    recipe_name: str,
    severity: str,
    source_index: int,
    metadata: dict,
) -> Path:
    try:
        return output_path_for(source_path, input_dir, output_dir, recipe_name, severity)
    except ValueError:
        image_id = metadata.get("image_id") or metadata.get("imageID") or source_path.name
        safe_stem = Path(str(image_id)).stem.replace(" ", "_")
        return output_dir / recipe_name / severity / f"{source_index:06d}_{safe_stem}.jpg"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def stable_seed(seed: int, source_path: Path, recipe_name: str, severity: str) -> int:
    payload = f"{seed}:{source_path}:{recipe_name}:{severity}".encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    return int(digest[:16], 16) % (2**32)


if __name__ == "__main__":
    raise SystemExit(main())
