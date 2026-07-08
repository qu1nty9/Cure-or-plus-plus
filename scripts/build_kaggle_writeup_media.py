#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MEDIA_OUTPUTS = [
    (
        ROOT / "results/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png",
        ROOT / "results/kaggle_writeup_media_v041.png",
        (640, 360),
    ),
    (
        ROOT / "results/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png",
        ROOT / "results/kaggle_writeup_media_v041_01_mean_accuracy.png",
        (640, 360),
    ),
    (
        ROOT / "results/full_cure_or_probe_v04_with_prototypes_level5_ranking.png",
        ROOT / "results/kaggle_writeup_media_v041_02_level5_ranking.png",
        (640, 360),
    ),
    (
        ROOT / "results/real_transfer_v02_source_matched_drops.png",
        ROOT / "results/kaggle_writeup_media_v041_03_real_transfer_drops.png",
        (640, 360),
    ),
    (
        ROOT / "results/real_transfer_v02_accuracy_heatmap.png",
        ROOT / "results/kaggle_writeup_media_v041_04_real_transfer_heatmap.png",
        (640, 360),
    ),
    (
        ROOT / "results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.png",
        ROOT / "results/kaggle_writeup_media_v041_05_grayscale_control.png",
        (640, 360),
    ),
    (
        ROOT / "results/full_cure_or_probe_v04_level5_overconfidence.png",
        ROOT / "results/kaggle_writeup_media_v041_06_level5_overconfidence.png",
        (640, 360),
    ),
]
CARD_OUTPUTS = [
    (
        ROOT / "results/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png",
        ROOT / "results/kaggle_writeup_card_thumbnail_v041.png",
        (560, 280),
    ),
]


def fit_on_canvas(image: Image.Image, target_width: int, target_height: int) -> Image.Image:
    image.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (target_width, target_height), "white")
    left = (target_width - image.width) // 2
    top = (target_height - image.height) // 2
    canvas.paste(image, (left, top))
    return canvas


def center_crop_to_aspect(
    image: Image.Image,
    target_width: int,
    target_height: int,
) -> Image.Image:
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
    for source_path, output_path, size in MEDIA_OUTPUTS:
        source = Image.open(source_path).convert("RGB")
        resized = fit_on_canvas(source, *size)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        resized.save(output_path)

    for source_path, output_path, size in CARD_OUTPUTS:
        source = Image.open(source_path).convert("RGB")
        cropped = center_crop_to_aspect(source, *size)
        resized = cropped.resize(size, Image.Resampling.LANCZOS)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        resized.save(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
