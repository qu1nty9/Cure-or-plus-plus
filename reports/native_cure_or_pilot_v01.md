# Native mini-CURE-OR Pilot v0.1

## Purpose

This is the first bridge from CURE-OR++ simulated transfer chains toward a
broader CURE-OR evaluation. It does not use the full original CURE-OR release.
It uses the locally available mini-CURE-OR challenge grid:

- 16,500 total local mini-CURE-OR rows;
- 250 clean images;
- 16,250 native challenge images;
- 10 object classes.

The pilot evaluates a small native test-split slice:

- 100 clean test images;
- challenge types 2, 8, and 14;
- challenge levels 1 through 4;
- 1,200 native challenge images.

Challenge type names are pinned in `docs/native_challenge_mapping_v01.md`.

## Models

| Model | Clean test accuracy |
| --- | ---: |
| CLIP ViT-B/16 | 0.9000 |
| OpenCLIP ViT-B/32 LAION2B | 0.8500 |

## Level-4 Native Challenge Results

| Model | Native challenge | Accuracy | Drop vs clean | Mean confidence |
| --- | --- | ---: | ---: | ---: |
| CLIP ViT-B/16 | type 14, grayscale gaussian blur | 0.1000 | 0.8000 | 0.4607 |
| CLIP ViT-B/16 | type 8, dirty lens 2 | 0.4200 | 0.4800 | 0.6696 |
| CLIP ViT-B/16 | type 2, resize | 0.8800 | 0.0200 | 0.8746 |
| OpenCLIP ViT-B/32 LAION2B | type 14, grayscale gaussian blur | 0.1000 | 0.7500 | 0.8570 |
| OpenCLIP ViT-B/32 LAION2B | type 8, dirty lens 2 | 0.4400 | 0.4100 | 0.8182 |
| OpenCLIP ViT-B/32 LAION2B | type 2, resize | 0.8600 | -0.0100 | 0.8865 |

## Interpretation

The native pilot shows a much sharper degradation regime than the CURE-OR++
transfer-chain benchmark. Grayscale gaussian blur collapses both contrastive
models to 0.1000 accuracy at level 4. Dirty lens 2 degrades both models
substantially, while resize remains close to clean accuracy.

This is useful for the serious writeup because it separates two claims:

- CURE-OR++ transfer chains expose realistic digital-transfer failures such as
  `low_light_upload`.
- Native CURE-OR challenges can be far harsher and should be treated as a
  broader stress-test layer, not as the same phenomenon.

The expanded local native test-grid result is tracked in
`reports/native_cure_or_test_v01.md`.

## Generated Artifacts

- `reports/mini_cure_or_scope_v01.csv`
- `data/interim/cure_or_clean_test_manifest.csv`
- `data/interim/mini_cure_or_native_pilot_v01_manifest.csv`
- `results/clip_vit_b16_native_pilot_v01_predictions.csv`
- `results/clip_vit_b16_native_pilot_v01_summary.csv`
- `results/openclip_vit_b32_laion2b_native_pilot_v01_predictions.csv`
- `results/openclip_vit_b32_laion2b_native_pilot_v01_summary.csv`
- `results/native_pilot_v01_comparison.csv`
- `results/native_pilot_v01_level4_ranking.csv`
- `results/native_pilot_v01_severity_curves.png`
