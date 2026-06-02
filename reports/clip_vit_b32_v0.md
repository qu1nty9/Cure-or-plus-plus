# CLIP ViT-B/32 Baseline v0

Model:

- `openai/clip-vit-base-patch32`

Dataset:

- mini-CURE-OR train clean subset only
- 150 clean source images
- 10 classes, 15 images per class
- 4,050 generated CURE-OR++ distorted images
- 4,200 evaluated images total

Outputs:

- Predictions: `results/clip_vit_b32_v0_predictions.csv`
- Summary: `results/clip_vit_b32_v0_summary.csv`
- High-severity chart: `results/clip_vit_b32_high_severity.png`

## Headline Results

Clean accuracy:

- 0.8533

Family average accuracy:

| Family | Accuracy |
| --- | ---: |
| clean | 0.8533 |
| classic | 0.8304 |
| modern_transfer | 0.8278 |

High-severity accuracy:

| Family | Recipe | Accuracy | Drop vs clean |
| --- | --- | ---: | ---: |
| modern_transfer | low_light_upload | 0.6667 | 0.1867 |
| classic | blur_classic | 0.7667 | 0.0867 |
| modern_transfer | video_call_frame | 0.7800 | 0.0733 |
| classic | resize_roundtrip | 0.8200 | 0.0333 |
| modern_transfer | restoration_artifact | 0.8200 | 0.0333 |
| modern_transfer | screenshot_chain | 0.8333 | 0.0200 |
| classic | jpeg_classic | 0.8400 | 0.0133 |
| modern_transfer | dirty_lens_recompress | 0.8400 | 0.0133 |
| modern_transfer | messenger_chain | 0.8667 | -0.0133 |

## Initial Read

The first result is promising but still preliminary. Modern transfer distortions
are not uniformly worse than classic distortions, but specific chains matter a
lot: `low_light_upload` is the strongest failure mode in this first run,
dropping CLIP ViT-B/32 by 18.67 percentage points from clean accuracy.

This is exactly the kind of signal the project needs: not "all modern
distortions are harder", but "realistic transfer chains create a distinct
failure profile that should be measured separately."

## Next Checks

- Add `test.zip` to move from 150 to 250 clean source images.
- Run at least one non-CLIP baseline.
- Add per-class confusion analysis.
- Compare recipe ranking across at least two model families.

