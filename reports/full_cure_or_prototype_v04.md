# Full-CURE-OR Prototype Baselines v0.4

## Summary

This pass adds two non-CLIP classifier backbones to the same Full-CURE-OR v0.4
manifest:

- HGNetV2-B0 Prototype;
- MobileNetV3-Small Prototype.

The goal is model-family diversity, not a new training benchmark. Both models
use frozen ImageNet features and a nearest-centroid classifier over the 100
Full-CURE-OR object labels.

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

For context, the strongest zero-shot baseline in the current v0.4 block is
CLIP ViT-B/16 with clean accuracy 0.4440 and mean level-5 native accuracy
0.0994. HGNetV2-B0 is now the strongest local baseline on clean, grayscale
control, and every native challenge level. MobileNetV3-Small is weaker than
HGNetV2-B0, but its mean native accuracy is close to CLIP ViT-B/16 while using
a different non-contrastive classifier protocol.

Level-5 worst-case ranking also changes by model family:

| Model | Worst level-5 challenge | Worst level-5 accuracy |
| --- | --- | ---: |
| OpenCLIP ViT-B/32 LAION2B | type 18, grayscale salt and pepper noise | 0.0080 |
| CLIP ViT-B/16 | type 09, salt and pepper noise; tied with type 18 | 0.0100 |
| CLIP ViT-B/32 | type 09, salt and pepper noise | 0.0060 |
| HGNetV2-B0 Prototype | type 05, gaussian blur; tied with types 09, 14, and 18 | 0.0100 |
| MobileNetV3-Small Prototype | type 05, gaussian blur; tied with types 09, 14, and 18 | 0.0100 |

That ranking shift is useful for the paper-level argument: CURE-OR is not just
measuring generic image difficulty. The most damaging native challenge depends
on the model family and decision protocol.

## Artifacts

- `scripts/evaluate_full_cure_or_prototype.py`
- `configs/hgnetv2_b0_full_cure_or_prototype_v04.json`
- `configs/mobilenet_v3_small_full_cure_or_prototype_v04.json`
- `configs/full_cure_or_probe_summaries_v04_with_prototypes.json`
- `configs/full_cure_or_grayscale_control_summaries_v04_with_prototypes.json`
- `results/hgnetv2_b0_full_cure_or_prototype_v04_predictions.csv`
- `results/hgnetv2_b0_full_cure_or_prototype_v04_summary.csv`
- `results/mobilenet_v3_small_full_cure_or_prototype_v04_predictions.csv`
- `results/mobilenet_v3_small_full_cure_or_prototype_v04_summary.csv`
- `results/full_cure_or_probe_v04_with_prototypes_comparison.csv`
- `results/full_cure_or_probe_v04_with_prototypes_level5_ranking.csv`
- `results/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png`
- `results/full_cure_or_probe_v04_with_prototypes_level5_ranking.png`
- `results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.csv`
- `results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.png`

## Verification

- `python -m compileall scripts src`
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
