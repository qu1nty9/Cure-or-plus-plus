# Full-CURE-OR Challenge-Family Analysis v0.4

## Summary

This pass adds a challenge-family view over the eight usable Full-CURE-OR v0.4
baselines in `results/full_cure_or_probe_v04_with_prototypes_comparison.csv`.
It pairs native challenge types 02-09 with their grayscale counterparts 11-18:

- resize vs grayscale resize;
- underexposure vs grayscale underexposure;
- overexposure vs grayscale overexposure;
- gaussian blur vs grayscale gaussian blur;
- contrast vs grayscale contrast;
- dirty lens 1 vs grayscale dirty lens 1;
- dirty lens 2 vs grayscale dirty lens 2;
- salt and pepper noise vs grayscale salt and pepper noise.

The goal is to separate base distortion difficulty from grayscale/channel
interaction. This gives the writeup a stronger claim than a single worst-case
ranking.

All inputs are local aggregate CSVs. No external-disk reads or writes are
needed for this analysis.

## Level-5 Channel Effect

| Model | Color level-5 mean | Grayscale level-5 mean | Grayscale minus color |
| --- | ---: | ---: | ---: |
| ConvNeXt-Tiny Prototype | 0.2743 | 0.1734 | -0.1009 |
| OpenCLIP ViT-B/16 DataComp XL | 0.1791 | 0.1111 | -0.0680 |
| MobileNetV3-Small Prototype | 0.1274 | 0.0646 | -0.0629 |
| OpenCLIP ViT-B/32 LAION2B | 0.1203 | 0.0577 | -0.0626 |
| CLIP ViT-B/16 | 0.1306 | 0.0683 | -0.0623 |
| DINOv2 ViT-S/14 Prototype | 0.3071 | 0.2460 | -0.0611 |
| HGNetV2-B0 Prototype | 0.1506 | 0.0931 | -0.0574 |
| CLIP ViT-B/32 | 0.0963 | 0.0520 | -0.0443 |

Every usable model is worse on grayscale level-5 native challenges than on the
paired color level-5 challenges. DINOv2 remains the strongest model in absolute
accuracy, but it still loses 0.0611 accuracy when moving from color to paired
grayscale level-5 challenges. OpenCLIP ViT-B/16 DataComp XL lands between
ConvNeXt-Tiny and the smaller CLIP/OpenCLIP baselines by level-5 channel means,
but it still loses 0.0680 accuracy under paired grayscale level-5 challenges.
ConvNeXt-Tiny has the largest absolute grayscale penalty despite being the
second strongest prototype baseline.

This supports two claims:

1. grayscale/channel removal is a real interaction term, not only a separate
   control condition;
2. the hardest blur/noise cases can already be at floor in both color and
   grayscale, so a small paired gap does not mean the challenge is easy.

## Largest Paired Level-5 Grayscale Penalties

| Model | Base challenge | Color accuracy | Grayscale accuracy | Gap |
| --- | --- | ---: | ---: | ---: |
| ConvNeXt-Tiny Prototype | Dirty lens 2 | 0.4000 | 0.1940 | -0.2060 |
| OpenCLIP ViT-B/32 LAION2B | Contrast | 0.2720 | 0.1220 | -0.1500 |
| ConvNeXt-Tiny Prototype | Dirty lens 1 | 0.1920 | 0.0560 | -0.1360 |
| MobileNetV3-Small Prototype | Contrast | 0.2940 | 0.1580 | -0.1360 |
| ConvNeXt-Tiny Prototype | Overexposure | 0.3160 | 0.1820 | -0.1340 |
| HGNetV2-B0 Prototype | Contrast | 0.3940 | 0.2640 | -0.1300 |
| HGNetV2-B0 Prototype | Dirty lens 2 | 0.2480 | 0.1200 | -0.1280 |
| OpenCLIP ViT-B/16 DataComp XL | Contrast | 0.3620 | 0.2340 | -0.1280 |
| MobileNetV3-Small Prototype | Dirty lens 2 | 0.1900 | 0.0660 | -0.1240 |
| ConvNeXt-Tiny Prototype | Contrast | 0.4620 | 0.3440 | -0.1180 |
| CLIP ViT-B/16 | Dirty lens 2 | 0.1880 | 0.0720 | -0.1160 |
| CLIP ViT-B/16 | Contrast | 0.2680 | 0.1520 | -0.1160 |
| DINOv2 ViT-S/14 Prototype | Overexposure | 0.3540 | 0.2400 | -0.1140 |

The largest paired penalties are not only blur/noise. They often occur for
dirty-lens, contrast, and exposure distortions, where the color version still
leaves enough signal for a measurable grayscale drop.

## Floor Effects

Some paired gaps are small because both sides are already near chance:

| Model | Base challenge | Color accuracy | Grayscale accuracy | Gap |
| --- | --- | ---: | ---: | ---: |
| CLIP ViT-B/32 | Salt and pepper noise | 0.0060 | 0.0100 | 0.0040 |
| OpenCLIP ViT-B/16 DataComp XL | Salt and pepper noise | 0.0080 | 0.0100 | 0.0020 |
| DINOv2 ViT-S/14 Prototype | Gaussian blur | 0.0100 | 0.0100 | 0.0000 |
| CLIP ViT-B/16 | Salt and pepper noise | 0.0100 | 0.0100 | 0.0000 |
| MobileNetV3-Small Prototype | Salt and pepper noise | 0.0100 | 0.0100 | 0.0000 |
| HGNetV2-B0 Prototype | Salt and pepper noise | 0.0100 | 0.0100 | 0.0000 |
| DINOv2 ViT-S/14 Prototype | Salt and pepper noise | 0.0100 | 0.0080 | -0.0020 |
| OpenCLIP ViT-B/32 LAION2B | Salt and pepper noise | 0.0140 | 0.0080 | -0.0060 |

This matters for interpretation: grayscale salt-and-pepper noise is still one
of the strongest collapse cases, even when its paired gap is small.

## Stronger Baseline

- `configs/openclip_vit_b16_datacomp_xl_full_cure_or_probe_v04.json`
- model: OpenCLIP `ViT-B-16`;
- pretrained weights: `datacomp_xl_s13b_b90k`.

The Hugging Face CLI download stalled, so the weight file was downloaded via
the direct Hugging Face `resolve/main/open_clip_pytorch_model.bin` URL into the
local external-disk project folder and evaluated as a local checkpoint. The full
v0.4 native run produced:

- clean accuracy: 0.5460;
- mean native accuracy: 0.2561;
- mean level-5 native accuracy: 0.1451;
- worst level-5 native challenge: type 09, salt-and-pepper noise, at 0.0080.

This makes DataComp XL a reported baseline. It improves on smaller CLIP-family
zero-shot rows but does not remove the benchmark's severe level-5 failure
pattern.

## Artifacts

- `scripts/analyze_full_cure_or_challenge_families.py`
- `results/full_cure_or_probe_v04_with_prototypes_channel_effects.csv`
- `results/full_cure_or_probe_v04_with_prototypes_paired_channel_gaps.csv`
- `configs/openclip_vit_b16_datacomp_xl_full_cure_or_probe_v04.json`

## Verification

- `python scripts/analyze_full_cure_or_challenge_families.py`
- output rows:
  - channel effects: 80;
  - paired channel gaps: 312.

## Next Step

The next high-value step is the 180-output v0.2 real transfer validation block
or another stronger pretrained VLM family that is not just a nearby
CLIP/OpenCLIP variant.
