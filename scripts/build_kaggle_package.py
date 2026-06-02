#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a local Kaggle dataset package for CURE-OR++.")
    parser.add_argument("--output-dir", default="kaggle/cure-or-plus-plus-v01")
    parser.add_argument("--kaggle-id", default="USERNAME/cure-or-plus-plus-v01")
    args = parser.parse_args()

    output_dir = resolve_project_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    clean_manifest = ROOT / "data/interim/cure_or_clean_manifest.csv"
    distortion_manifest = ROOT / "data/processed/cure_or_pp_v0/manifest.csv"

    copy_manifest(clean_manifest, output_dir / "metadata/clean_manifest.csv")
    copy_manifest(distortion_manifest, output_dir / "metadata/distortion_manifest.csv")
    copy_file(ROOT / "results/clip_vit_b32_v01_predictions.csv", output_dir / "results/clip_vit_b32_v01_predictions.csv")
    copy_file(ROOT / "results/clip_vit_b32_v01_summary.csv", output_dir / "results/clip_vit_b32_v01_summary.csv")
    copy_file(ROOT / "results/clip_vit_b32_v01_test_predictions.csv", output_dir / "results/clip_vit_b32_v01_test_predictions.csv")
    copy_file(ROOT / "results/clip_vit_b32_v01_test_summary.csv", output_dir / "results/clip_vit_b32_v01_test_summary.csv")
    copy_file(ROOT / "results/clip_vit_b16_v01_predictions.csv", output_dir / "results/clip_vit_b16_v01_predictions.csv")
    copy_file(ROOT / "results/clip_vit_b16_v01_summary.csv", output_dir / "results/clip_vit_b16_v01_summary.csv")
    copy_file(ROOT / "results/clip_vit_b16_v01_test_predictions.csv", output_dir / "results/clip_vit_b16_v01_test_predictions.csv")
    copy_file(ROOT / "results/clip_vit_b16_v01_test_summary.csv", output_dir / "results/clip_vit_b16_v01_test_summary.csv")
    copy_file(ROOT / "results/siglip_base_p16_224_v01_predictions.csv", output_dir / "results/siglip_base_p16_224_v01_predictions.csv")
    copy_file(ROOT / "results/siglip_base_p16_224_v01_summary.csv", output_dir / "results/siglip_base_p16_224_v01_summary.csv")
    copy_file(ROOT / "results/siglip_base_p16_224_v01_test_predictions.csv", output_dir / "results/siglip_base_p16_224_v01_test_predictions.csv")
    copy_file(ROOT / "results/siglip_base_p16_224_v01_test_summary.csv", output_dir / "results/siglip_base_p16_224_v01_test_summary.csv")
    copy_file(ROOT / "results/openclip_vit_b32_laion2b_v01_predictions.csv", output_dir / "results/openclip_vit_b32_laion2b_v01_predictions.csv")
    copy_file(ROOT / "results/openclip_vit_b32_laion2b_v01_summary.csv", output_dir / "results/openclip_vit_b32_laion2b_v01_summary.csv")
    copy_file(ROOT / "results/openclip_vit_b32_laion2b_v01_test_predictions.csv", output_dir / "results/openclip_vit_b32_laion2b_v01_test_predictions.csv")
    copy_file(ROOT / "results/openclip_vit_b32_laion2b_v01_test_summary.csv", output_dir / "results/openclip_vit_b32_laion2b_v01_test_summary.csv")
    copy_file(ROOT / "results/hgnetv2_b0_prototype_v01_predictions.csv", output_dir / "results/hgnetv2_b0_prototype_v01_predictions.csv")
    copy_file(ROOT / "results/hgnetv2_b0_prototype_v01_summary.csv", output_dir / "results/hgnetv2_b0_prototype_v01_summary.csv")
    copy_file(ROOT / "results/mobilenet_v3_small_prototype_v01_predictions.csv", output_dir / "results/mobilenet_v3_small_prototype_v01_predictions.csv")
    copy_file(ROOT / "results/mobilenet_v3_small_prototype_v01_summary.csv", output_dir / "results/mobilenet_v3_small_prototype_v01_summary.csv")
    copy_file(ROOT / "results/model_comparison_v01.csv", output_dir / "results/model_comparison_v01.csv")
    copy_file(ROOT / "results/model_ranking_shift_v01.csv", output_dir / "results/model_ranking_shift_v01.csv")
    copy_file(ROOT / "results/per_class_failures_v01.csv", output_dir / "results/per_class_failures_v01.csv")
    copy_file(ROOT / "results/confidence_shift_v01.csv", output_dir / "results/confidence_shift_v01.csv")
    copy_file(ROOT / "results/clip_vit_b32_v01_high_severity.png", output_dir / "figures/clip_vit_b32_v01_high_severity.png")
    copy_file(ROOT / "results/model_comparison_v01_high_severity.png", output_dir / "figures/model_comparison_v01_high_severity.png")
    copy_file(ROOT / "results/confidence_shift_v01_high_severity.png", output_dir / "figures/confidence_shift_v01_high_severity.png")
    copy_file(ROOT / "results/preview_v0.jpg", output_dir / "figures/preview_v01.jpg")

    linked_clean = link_manifest_images(clean_manifest, "image_path", output_dir)
    linked_distorted = link_manifest_images(distortion_manifest, "output_path", output_dir)

    write_dataset_metadata(output_dir / "dataset-metadata.json", args.kaggle_id)
    write_readme(output_dir / "README.md")
    write_citation(output_dir / "CITATION.md")

    print(f"Kaggle package: {output_dir}")
    print(f"Clean images linked/copied: {linked_clean}")
    print(f"Distorted images linked/copied: {linked_distorted}")
    return 0


def link_manifest_images(manifest_path: Path, column: str, output_dir: Path) -> int:
    count = 0
    with manifest_path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            source = resolve_project_path(row[column])
            target = output_dir / row[column]
            link_or_copy(source, target)
            count += 1
    return count


def copy_manifest(source: Path, target: Path) -> None:
    copy_file(source, target)


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def link_or_copy(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return
    try:
        os.link(source, target)
    except OSError:
        shutil.copy2(source, target)


def write_dataset_metadata(path: Path, kaggle_id: str) -> None:
    metadata = {
        "title": "CURE-OR++ v0.1: Modern Transfer Distortions",
        "id": kaggle_id,
        "licenses": [{"name": "CC-BY-4.0"}],
    }
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def write_readme(path: Path) -> None:
    path.write_text(
        """# CURE-OR++ v0.1: Modern Transfer Distortions

CURE-OR++ v0.1 is a small robustness benchmark built on the clean subset of
mini-CURE-OR. It evaluates how vision models behave under classic corruptions
and modern digital transfer chains.

## Contents

- `data/raw/mini_cure_or/`: 250 clean source images used by this release.
- `data/processed/cure_or_pp_v0/`: 6,750 generated distorted images.
- `metadata/clean_manifest.csv`: clean source metadata.
- `metadata/distortion_manifest.csv`: distortion metadata.
- `results/clip_vit_b32_v01_predictions.csv`: CLIP ViT-B/32 predictions on all 7,000 images.
- `results/clip_vit_b16_v01_predictions.csv`: CLIP ViT-B/16 predictions on all 7,000 images.
- `results/clip_vit_*_summary.csv`: aggregate CLIP metrics on all 7,000 images.
- `results/openclip_vit_b32_laion2b_*`: OpenCLIP ViT-B/32 LAION2B baseline outputs.
- `results/siglip_base_p16_224_*`: SigLIP diagnostic baseline outputs.
- `results/*_test_predictions.csv` and prototype prediction files: fair test-split baselines.
- `results/model_comparison_v01.csv`: cross-model comparison table.
- `results/model_ranking_shift_v01.csv`: high-severity recipe rankings by model.
- `results/per_class_failures_v01.csv`: per-class degradation table.
- `results/confidence_shift_v01.csv`: confidence degradation and overconfidence table.
- `figures/`: preview and result figures.

## Baselines

The zero-shot baselines use `openai/clip-vit-base-patch32`,
`openai/clip-vit-base-patch16`, `laion/CLIP-ViT-B-32-laion2B-s34B-b79K`, and
`google/siglip-base-patch16-224` with 10 mini-CURE-OR class prompts. The
test-split comparison also includes clean-train prototype classifiers using
HGNetV2-B0 and MobileNetV3-Small image backbones.

On the full 250-image clean subset, CLIP ViT-B/16 clean accuracy is 0.9160 and
CLIP ViT-B/32 clean accuracy is 0.8280. On the fair 100-image test split, the
strongest high-severity degradation is `low_light_upload` for both CLIP
variants, OpenCLIP, and HGNetV2-B0, while MobileNetV3-Small has its worst
high-severity result on `video_call_frame`. OpenCLIP provides a usable
non-OpenAI contrastive baseline; SigLIP is retained as a diagnostic run because
its clean test accuracy is low under this prompt protocol.

## Attribution

This dataset is derived from mini-CURE-OR, released by OLIVES Lab, Georgia Tech.
The original mini-CURE-OR Zenodo record is licensed under CC-BY-4.0.
""",
        encoding="utf-8",
    )


def write_citation(path: Path) -> None:
    path.write_text(
        """# Citation

If you use this derived benchmark, cite the original CURE-OR work:

```bibtex
@inproceedings{Temel2018_ICMLA,
  author    = {D. Temel and J. Lee and G. AlRegib},
  booktitle = {2018 17th IEEE International Conference on Machine Learning and Applications (ICMLA)},
  title     = {CURE-OR: Challenging unreal and real environments for object recognition},
  year      = {2018}
}

@inproceedings{Temel2019_ICIP,
  author    = {D. Temel and J. Lee and G. AlRegib},
  booktitle = {IEEE International Conference on Image Processing (ICIP)},
  title     = {Object Recognition Under Multifarious Conditions: A Reliability Analysis and A Feature Similarity-Based Performance Estimation},
  year      = {2019}
}
```

Original resources:

- https://github.com/olivesgatech/CURE-OR
- https://github.com/olivesgatech/mini-CURE-OR
- https://zenodo.org/record/4299330

mini-CURE-OR is distributed under CC-BY-4.0 according to its Zenodo metadata.
""",
        encoding="utf-8",
    )


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
