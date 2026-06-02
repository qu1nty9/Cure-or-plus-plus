# CLIP ViT-B/32 Baseline v0.1

Model:

- `openai/clip-vit-base-patch32`

Dataset:

- mini-CURE-OR clean subset
- 250 clean source images
- 10 classes, 25 images per class
- 6,750 generated CURE-OR++ distorted images
- 7,000 evaluated images total

Outputs:

- Predictions: `results/clip_vit_b32_v01_predictions.csv`
- Summary: `results/clip_vit_b32_v01_summary.csv`
- High-severity chart: `results/clip_vit_b32_v01_high_severity.png`

## Headline Results

Clean accuracy:

- 0.8280

Family average accuracy:

| Family | Accuracy |
| --- | ---: |
| clean | 0.8280 |
| classic | 0.8076 |
| modern_transfer | 0.8064 |

High-severity accuracy:

| Family | Recipe | Accuracy | Drop vs clean |
| --- | --- | ---: | ---: |
| modern_transfer | low_light_upload | 0.6560 | 0.1720 |
| classic | blur_classic | 0.7440 | 0.0840 |
| modern_transfer | video_call_frame | 0.7680 | 0.0600 |
| modern_transfer | restoration_artifact | 0.7960 | 0.0320 |
| classic | resize_roundtrip | 0.8000 | 0.0280 |
| modern_transfer | dirty_lens_recompress | 0.8120 | 0.0160 |
| classic | jpeg_classic | 0.8160 | 0.0120 |
| modern_transfer | screenshot_chain | 0.8160 | 0.0120 |
| modern_transfer | messenger_chain | 0.8480 | -0.0200 |

## Initial Read

The first full mini-CURE-OR clean-subset run preserves the same signal we saw in
the smaller train-only pass. Modern transfer distortions are not uniformly
harder than classic corruptions, but `low_light_upload` creates the largest
drop for CLIP ViT-B/32: 17.2 percentage points below clean accuracy.

The Kaggle write-up should frame this as a measurement result rather than an
overclaim: realistic transfer chains produce a distinct robustness profile, and
some chains are substantially more damaging than simple JPEG or resize
corruptions.

## Next Checks

- Compare with completed CLIP ViT-B/16, OpenCLIP ViT-B/32 LAION2B, and SigLIP
  diagnostic baselines.
- Add per-class confusion analysis.
- Check whether low-light failures cluster around specific objects or
  backgrounds.
- Compare classic-vs-modern ranking shifts across at least two model families.
