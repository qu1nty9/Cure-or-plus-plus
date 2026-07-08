#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "results/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png"
OUTPUTS = [
    (ROOT / "results/kaggle_writeup_media_v041.png", (640, 360)),
    (ROOT / "results/kaggle_writeup_card_thumbnail_v041.png", (560, 280)),
]


def center_crop_to_aspect(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    source_width, source_height = image.size
    target_aspect = target_width / target_height
    source_aspect = source_width / source_height

    if source_aspect > target_aspect:
        crop_width = int(round(source_height * target_aspect))
        left = (source_width - crop_width) // 2
        box = (left, 0, left + crop_width, source_height)
    else:
        crop_height = int(round(source_width / target_aspect))
        top = (source_height - crop_height) // 2
        box = (0, top, source_width, top + crop_height)

    return image.crop(box)


def main() -> int:
    source = Image.open(SOURCE).convert("RGB")
    for output_path, size in OUTPUTS:
        cropped = center_crop_to_aspect(source, *size)
        resized = cropped.resize(size, Image.Resampling.LANCZOS)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        resized.save(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
