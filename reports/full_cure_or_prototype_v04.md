# Full-CURE-OR Prototype Baselines v0.4

## Summary

This pass adds four non-CLIP feature backbones to the same Full-CURE-OR v0.4
manifest:

- HGNetV2-B0 Prototype;
- MobileNetV3-Small Prototype;
- ConvNeXt-Tiny Prototype;
- DINOv2 ViT-S/14 Prototype.

The goal is model-family diversity, not a new training benchmark. All four
models use frozen pretrained features and a nearest-centroid classifier over
the 100 Full-CURE-OR object labels.

Protocol:

1. extract features for the 500 clean v0.4 rows;
2. group clean rows by source acquisition condition
   `(background, device, orientation)`;
3. for each evaluated row, build class centroids from clean rows excluding the
   same source acquisition condition;
4. classify clean, native CURE-OR, and grayscale-control rows by cosine
   similarity to those held-out-condition centroids.

This is recorded as
`full_cure_or_leave_clean_condition_out_prototype` in the summary CSVs.

The protocol avoids training on the exact clean acquisition condition being
evaluated. It is still a lightweight prototype baseline: it is not comparable
to supervised fine-tuning and its `mean_confidence` values are centroid-softmax
diagnostics rather than calibrated model probabilities.

All external-disk reads stayed under
`/Volumes/980PRO/CURE-OR++/archives`. No files were written to the external
disk.

## Results

| Model | Clean | Grayscale control | Mean native | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| HGNetV2-B0 Prototype | 0.6240 | 0.4429 | 0.2547 | 0.3793 | 0.3006 | 0.2505 | 0.2045 | 0.1219 |
| MobileNetV3-Small Prototype | 0.5560 | 0.2846 | 0.1936 | 0.2855 | 0.2239 | 0.1872 | 0.1631 | 0.0960 |
| ConvNeXt-Tiny Prototype | 0.6160 | 0.4910 | 0.3436 | 0.4481 | 0.3914 | 0.3435 | 0.2965 | 0.2239 |
| DINOv2 ViT-S/14 Prototype | 0.7520 | 0.7415 | 0.4393 | 0.5884 | 0.4940 | 0.4354 | 0.3819 | 0.2766 |

For context, the strongest zero-shot baseline in the current v0.4 block is
CLIP ViT-B/16 with clean accuracy 0.4440 and mean level-5 native accuracy
0.0994. DINOv2 ViT-S/14 is the strongest current baseline on clean accuracy,
grayscale control, mean native accuracy, and every native challenge level.
ConvNeXt-Tiny is the second strongest prototype on mean native and level-5
native accuracy. MobileNetV3-Small is weaker than HGNetV2-B0, ConvNeXt-Tiny,
and DINOv2, but its mean native accuracy is close to CLIP ViT-B/16 while using a
different non-contrastive classifier protocol.

Level-5 worst-case ranking also changes by model family:

| Model | Worst level-5 challenge | Worst level-5 accuracy |
| --- | --- | ---: |
| OpenCLIP ViT-B/32 LAION2B | type 18, grayscale salt and pepper noise | 0.0080 |
| CLIP ViT-B/16 | type 09, salt and pepper noise; tied with type 18 | 0.0100 |
| CLIP ViT-B/32 | type 09, salt and pepper noise | 0.0060 |
| HGNetV2-B0 Prototype | type 05, gaussian blur; tied with types 09, 14, and 18 | 0.0100 |
| MobileNetV3-Small Prototype | type 05, gaussian blur; tied with types 09, 14, and 18 | 0.0100 |
| ConvNeXt-Tiny Prototype | type 18, grayscale salt and pepper noise | 0.0080 |
| DINOv2 ViT-S/14 Prototype | type 18, grayscale salt and pepper noise | 0.0080 |

That ranking shift is useful for the paper-level argument: CURE-OR is not just
measuring generic image difficulty. The most damaging native challenge depends
on the model family and decision protocol. DINOv2 changes the scale of the
baseline but not the existence of the native-collapse failure: type 18 remains
near chance, and types 05, 09, and 14 are also near chance at level 5.

## Artifacts

- `scripts/evaluate_full_cure_or_prototype.py`
- `configs/hgnetv2_b0_full_cure_or_prototype_v04.json`
- `configs/mobilenet_v3_small_full_cure_or_prototype_v04.json`
- `configs/convnext_tiny_fb_in1k_full_cure_or_prototype_v04.json`
- `configs/dinov2_vit_small_patch14_full_cure_or_prototype_v04.json`
- `configs/full_cure_or_probe_summaries_v04_with_prototypes.json`
- `configs/full_cure_or_grayscale_control_summaries_v04_with_prototypes.json`
- `results/hgnetv2_b0_full_cure_or_prototype_v04_predictions.csv`
- `results/hgnetv2_b0_full_cure_or_prototype_v04_summary.csv`
- `results/mobilenet_v3_small_full_cure_or_prototype_v04_predictions.csv`
- `results/mobilenet_v3_small_full_cure_or_prototype_v04_summary.csv`
- `results/convnext_tiny_fb_in1k_full_cure_or_prototype_v04_predictions.csv`
- `results/convnext_tiny_fb_in1k_full_cure_or_prototype_v04_summary.csv`
- `results/dinov2_vit_small_patch14_full_cure_or_prototype_v04_predictions.csv`
- `results/dinov2_vit_small_patch14_full_cure_or_prototype_v04_summary.csv`
- `results/full_cure_or_probe_v04_with_prototypes_comparison.csv`
- `results/full_cure_or_probe_v04_with_prototypes_level5_ranking.csv`
- `results/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png`
- `results/full_cure_or_probe_v04_with_prototypes_level5_ranking.png`
- `results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.csv`
- `results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.png`

## Verification

- `python -m compileall scripts src`
- `HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 python scripts/evaluate_full_cure_or_prototype.py --config configs/dinov2_vit_small_patch14_full_cure_or_prototype_v04.json --device cpu`
- `python scripts/compare_native_pilot.py --config configs/full_cure_or_probe_summaries_v04_with_prototypes.json`
- `python scripts/compare_full_cure_or_control.py --config configs/full_cure_or_grayscale_control_summaries_v04_with_prototypes.json --native-comparison results/full_cure_or_probe_v04_with_prototypes_comparison.csv`
- generated PNGs were opened and visually checked.

## Next Step

The prototype block makes the benchmark stronger, but it does not replace the
need for stronger pretrained VLMs or real transfer validation. The next
research step should be either:

1. evaluate one stronger pretrained contrastive/VLM family if weights are
   available;
2. collect the first real app-transfer validation sample and compare its
   ranking against native CURE-OR level-5 rankings.
