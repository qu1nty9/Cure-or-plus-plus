# Native mini-CURE-OR Test Grid v0.1

## Purpose

This report extends the 3-type native pilot to all native mini-CURE-OR
challenge types currently available in the local test split. It is the strongest
bridge so far from CURE-OR++ simulated transfer chains toward a controlled
Full-CURE-OR evaluation.

Challenge type names are pinned from the official `olivesgatech/CURE-OR`
README and tracked in `docs/native_challenge_mapping_v01.md`.

## Scope

- 100 clean test images.
- 6,400 native challenge images.
- 16 available native challenge types: 2-9 and 11-18.
- 4 challenge levels per type.
- 64 challenge type/level cells, with 100 images per cell.

## Models

| Model | Clean test accuracy |
| --- | ---: |
| CLIP ViT-B/16 | 0.9000 |
| OpenCLIP ViT-B/32 LAION2B | 0.8500 |

## Level-4 Summary

| Model | Mean level-4 accuracy | Worst challenge | Worst accuracy | Largest drop |
| --- | ---: | --- | ---: | ---: |
| CLIP ViT-B/16 | 0.5163 | type 14, grayscale gaussian blur | 0.1000 | 0.8000 |
| OpenCLIP ViT-B/32 LAION2B | 0.4325 | type 14, grayscale gaussian blur | 0.1000 | 0.7500 |

## Most Damaging Level-4 Challenges

| Model | Challenge | Accuracy | Drop vs clean | Mean confidence |
| --- | --- | ---: | ---: | ---: |
| CLIP ViT-B/16 | type 14, grayscale gaussian blur | 0.1000 | 0.8000 | 0.4607 |
| CLIP ViT-B/16 | type 18, grayscale salt & pepper noise | 0.1100 | 0.7900 | 0.3477 |
| CLIP ViT-B/16 | type 05, gaussian blur | 0.1200 | 0.7800 | 0.4541 |
| CLIP ViT-B/16 | type 09, salt & pepper noise | 0.2100 | 0.6900 | 0.4014 |
| CLIP ViT-B/16 | type 16, grayscale dirty lens 1 | 0.2700 | 0.6300 | 0.4338 |
| OpenCLIP ViT-B/32 LAION2B | type 14, grayscale gaussian blur | 0.1000 | 0.7500 | 0.8570 |
| OpenCLIP ViT-B/32 LAION2B | type 18, grayscale salt & pepper noise | 0.1000 | 0.7500 | 0.9730 |
| OpenCLIP ViT-B/32 LAION2B | type 09, salt & pepper noise | 0.1100 | 0.7400 | 0.6949 |
| OpenCLIP ViT-B/32 LAION2B | type 05, gaussian blur | 0.1400 | 0.7100 | 0.5877 |
| OpenCLIP ViT-B/32 LAION2B | type 16, grayscale dirty lens 1 | 0.1600 | 0.6900 | 0.8468 |

## Interpretation

The expanded native grid confirms that the pilot result was not a one-off.
Native CURE-OR grayscale gaussian blur remains the clearest collapse case for
both contrastive models, and several other level-4 challenges produce much
stronger degradation than the generated CURE-OR++ transfer-chain recipes.

This gives us two separate experimental layers:

- CURE-OR++ generated transfer chains: smaller, reproducible, and directly
  tied to modern image-transfer workflows.
- Native mini-CURE-OR challenge grid: harsher original stress tests that help
  bridge the project toward Full-CURE-OR.

The OpenCLIP confidence pattern is especially useful for a serious writeup:
grayscale salt and pepper noise reaches 0.1000 accuracy at level 4 with 0.9730
mean confidence. That is not merely confidence collapse; it is high-confidence
failure.

## Generated Artifacts

- `data/interim/mini_cure_or_native_test_v01_manifest.csv`
- `results/clip_vit_b16_native_test_v01_predictions.csv`
- `results/clip_vit_b16_native_test_v01_summary.csv`
- `results/openclip_vit_b32_laion2b_native_test_v01_predictions.csv`
- `results/openclip_vit_b32_laion2b_native_test_v01_summary.csv`
- `results/native_test_v01_comparison.csv`
- `results/native_test_v01_level4_ranking.csv`
- `results/native_test_v01_severity_curves.png`
- `results/native_test_v01_level4_ranking.png`
- `results/native_challenge_level4_samples.png`
- `configs/clip_vit_b16_native_test_v01.json`
- `configs/openclip_vit_b32_laion2b_native_test_v01.json`
- `configs/native_test_summaries_v01.json`
- `configs/cure_or_challenge_types_v01.json`
