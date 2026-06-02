# Failure Analysis v0.1

## Model Coverage

Completed:

- CLIP ViT-B/32
- CLIP ViT-B/16
- OpenCLIP ViT-B/32 LAION2B
- SigLIP Base P16 224 diagnostic baseline
- HGNetV2-B0 prototype classifier
- MobileNetV3-Small prototype classifier

Still missing:

- at least one real app-transfer validation sample;
- a Full-CURE-OR pilot after the local native mini-CURE-OR story is frozen;
- stronger related-work framing against recent VLM robustness benchmarks.

Validation note:

- prototype baselines now preserve distorted `image_path` values and only copy
  safe split/class metadata from `source_metadata_json`;
- corrected HGNetV2 and MobileNetV3 results below use the generated distorted
  image files, not the clean source paths.

## Test-Split Comparison

For a fair comparison, all models below are evaluated on the mini-CURE-OR test
split:

- 100 clean test images;
- 2,700 distorted test images;
- 10 classes.

| Model | Protocol | Clean accuracy | Worst high-severity recipe | Worst accuracy | Worst drop |
| --- | --- | ---: | --- | ---: | ---: |
| CLIP ViT-B/16 | zero-shot | 0.9000 | low_light_upload | 0.7800 | 0.1200 |
| OpenCLIP ViT-B/32 LAION2B | zero-shot | 0.8500 | low_light_upload | 0.6300 | 0.2200 |
| HGNetV2-B0 Prototype | clean-train prototype | 0.8400 | low_light_upload | 0.6400 | 0.2000 |
| CLIP ViT-B/32 | zero-shot | 0.7900 | low_light_upload | 0.6400 | 0.1500 |
| MobileNetV3-Small Prototype | clean-train prototype | 0.5600 | video_call_frame | 0.4600 | 0.1000 |
| SigLIP Base P16 224 | zero-shot diagnostic | 0.1900 | video_call_frame | 0.1500 | 0.0400 |

This is the strongest result so far: the same distortion suite creates a clear
low-light failure for both CLIP variants, OpenCLIP, and HGNetV2, while
MobileNetV3 has a different worst-case ranking. The benchmark is now showing
model-family-specific robustness profiles rather than a single universal
degradation order.

OpenCLIP gives the comparison a usable non-OpenAI contrastive baseline. SigLIP
is still included as a diagnostic run, but its clean accuracy is too low under
the current prompt protocol. Its distortion ranking should not be interpreted
as a strong robustness result until prompt/model alignment is improved.

## CLIP ViT-B/32 Summary

Full clean-subset accuracy:

- 0.8280

Test-split clean accuracy:

- 0.7900

Test-split worst high-severity recipes:

| Rank | Family | Recipe | Accuracy | Drop vs clean |
| ---: | --- | --- | ---: | ---: |
| 1 | modern_transfer | low_light_upload | 0.6400 | 0.1500 |
| 2 | classic | blur_classic | 0.7100 | 0.0800 |
| 3 | modern_transfer | video_call_frame | 0.7500 | 0.0400 |
| 4 | modern_transfer | restoration_artifact | 0.7600 | 0.0300 |
| 5 | classic | resize_roundtrip | 0.7700 | 0.0200 |

## CLIP ViT-B/16 Summary

Full clean-subset accuracy:

- 0.9160

Test-split clean accuracy:

- 0.9000

Test-split worst high-severity recipes:

| Rank | Family | Recipe | Accuracy | Drop vs clean |
| ---: | --- | --- | ---: | ---: |
| 1 | modern_transfer | low_light_upload | 0.7800 | 0.1200 |
| 2 | classic | blur_classic | 0.7900 | 0.1100 |
| 3 | modern_transfer | restoration_artifact | 0.8200 | 0.0800 |
| 4 | modern_transfer | screenshot_chain | 0.8200 | 0.0800 |
| 5 | modern_transfer | video_call_frame | 0.8200 | 0.0800 |

## SigLIP Base P16 224 Diagnostic

Full clean-subset accuracy:

- 0.1960

Test-split clean accuracy:

- 0.1900

Prediction distribution on the full clean subset is heavily concentrated:

- `hair_brush`: 172 / 250 predictions;
- `training_marker_cone`: 32 / 250 predictions;
- `baseball`: 19 / 250 predictions.

This suggests a prompt/model alignment issue rather than a meaningful object
recognition baseline for this 10-class CURE-OR subset.

## OpenCLIP ViT-B/32 LAION2B Summary

Full clean-subset accuracy:

- 0.8800

Test-split clean accuracy:

- 0.8500

Test-split worst high-severity recipes:

| Rank | Family | Recipe | Accuracy | Drop vs clean |
| ---: | --- | --- | ---: | ---: |
| 1 | modern_transfer | low_light_upload | 0.6300 | 0.2200 |
| 2 | classic | blur_classic | 0.7400 | 0.1100 |
| 3 | modern_transfer | video_call_frame | 0.7600 | 0.0900 |
| 4 | classic | resize_roundtrip | 0.8000 | 0.0500 |
| 5 | modern_transfer | restoration_artifact | 0.8100 | 0.0400 |

OpenCLIP has lower clean accuracy than CLIP ViT-B/16 but gives a stronger
stress signal: `low_light_upload` drops 0.2200 below clean on the test split.
That makes it a useful independent contrastive baseline rather than just a
diagnostic run.

## Confidence Shift

The confidence table adds a useful calibration-oriented view. The largest
high-severity accuracy drops are:

| Model | Recipe | Accuracy drop | Confidence drop | High-confidence wrong rate |
| --- | --- | ---: | ---: | ---: |
| OpenCLIP ViT-B/32 LAION2B | low_light_upload | 0.2200 | 0.0422 | 0.3200 |
| HGNetV2-B0 Prototype | low_light_upload | 0.2000 | 0.0087 | 0.0000 |
| CLIP ViT-B/32 | low_light_upload | 0.1500 | 0.1058 | 0.2100 |
| CLIP ViT-B/16 | low_light_upload | 0.1200 | 0.0739 | 0.1100 |
| OpenCLIP ViT-B/32 LAION2B | blur_classic | 0.1100 | 0.0342 | 0.1800 |

This suggests that the strongest transfer failures are not all alike. CLIP
ViT-B/32 loses confidence strongly on `low_light_upload`, while OpenCLIP keeps
relatively high confidence despite a larger accuracy drop. HGNetV2-B0 has low
prototype confidence overall, so its accuracy drop should not be read as
high-confidence misclassification.

## Prediction Stability

High-severity prediction changes relative to clean:

| Model | Recipe | Changed predictions |
| --- | --- | ---: |
| CLIP ViT-B/32 | low_light_upload | 36 / 100 |
| CLIP ViT-B/32 | video_call_frame | 17 / 100 |
| CLIP ViT-B/32 | blur_classic | 16 / 100 |
| CLIP ViT-B/16 | low_light_upload | 21 / 100 |
| CLIP ViT-B/16 | blur_classic | 17 / 100 |
| CLIP ViT-B/16 | restoration_artifact | 13 / 100 |
| OpenCLIP ViT-B/32 LAION2B | low_light_upload | 34 / 100 |
| OpenCLIP ViT-B/32 LAION2B | blur_classic | 21 / 100 |
| OpenCLIP ViT-B/32 LAION2B | video_call_frame | 21 / 100 |
| SigLIP Base P16 224 | low_light_upload | 22 / 100 |
| SigLIP Base P16 224 | blur_classic | 16 / 100 |
| SigLIP Base P16 224 | video_call_frame | 10 / 100 |
| HGNetV2-B0 Prototype | low_light_upload | 43 / 100 |
| HGNetV2-B0 Prototype | blur_classic | 24 / 100 |
| HGNetV2-B0 Prototype | video_call_frame | 14 / 100 |
| MobileNetV3-Small Prototype | low_light_upload | 36 / 100 |
| MobileNetV3-Small Prototype | video_call_frame | 19 / 100 |
| MobileNetV3-Small Prototype | blur_classic | 18 / 100 |

## Largest Per-Class Drops

Across the qualified five-model comparison, excluding low-clean-accuracy
SigLIP, the strongest high-severity class-level drops are concentrated in
`low_light_upload`, especially for CLIP ViT-B/16, OpenCLIP, and HGNetV2-B0.

| Model | Recipe | Label | Accuracy | Drop vs clean label |
| --- | --- | --- | ---: | ---: |
| CLIP ViT-B/16 | low_light_upload | dymo_label_maker | 0.100 | 0.700 |
| HGNetV2-B0 Prototype | low_light_upload | baseball | 0.300 | 0.700 |
| HGNetV2-B0 Prototype | low_light_upload | canon_camera | 0.200 | 0.600 |
| CLIP ViT-B/16 | video_call_frame | dymo_label_maker | 0.200 | 0.600 |
| OpenCLIP ViT-B/32 LAION2B | low_light_upload | canon_camera | 0.100 | 0.600 |
| CLIP ViT-B/16 | blur_classic | canon_camera | 0.000 | 0.600 |
| OpenCLIP ViT-B/32 LAION2B | low_light_upload | dymo_label_maker | 0.300 | 0.500 |
| MobileNetV3-Small Prototype | blur_classic | baseball | 0.000 | 0.500 |
| MobileNetV3-Small Prototype | low_light_upload | baseball | 0.000 | 0.500 |

## Interpretation

The strongest current claim is now cross-family, but still appropriately
limited:

> Low-light upload is the worst high-severity recipe for both CLIP variants,
> OpenCLIP, and HGNetV2-B0, while MobileNetV3-Small has a different worst-case
> recipe. This suggests that CURE-OR++ can expose model-family-specific
> robustness rankings, not just generic image difficulty.

This should not yet be framed as a universal VLM finding. It becomes stronger
after adding a real app-transfer validation sample and a larger Full-CURE-OR
pilot.

The related-work positioning is tracked in `docs/related_work_v01.md`. The
real-transfer pilot protocol is tracked in
`docs/real_transfer_validation_protocol.md`.

## Native CURE-OR Pilot Link

The native mini-CURE-OR challenge work is tracked separately in
`reports/native_cure_or_pilot_v01.md` and `reports/native_cure_or_test_v01.md`.
The expanded test grid uses 6,400 original mini-CURE-OR challenge images from
the test split. Both CLIP ViT-B/16 and OpenCLIP ViT-B/32 LAION2B collapse to
0.1000 accuracy on native grayscale gaussian blur at level 4; OpenCLIP also
reaches 0.1000 on grayscale salt and pepper noise with 0.9730 mean confidence.

## Generated Tables

- `results/model_comparison_v01.csv`
- `results/model_ranking_shift_v01.csv`
- `results/per_class_failures_v01.csv`
- `results/confidence_shift_v01.csv`
- `results/model_comparison_v01_high_severity.png`
- `results/confidence_shift_v01_high_severity.png`
- `scripts/plot_model_comparison.py`
- `scripts/analyze_confidence_shift.py`
- `scripts/plot_confidence_shift.py`
