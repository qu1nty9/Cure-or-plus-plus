# Full-CURE-OR Probe v0.4 Expanded Models

## Summary

This pass adds two locally available models to the same Full-CURE-OR v0.4
manifest:

- CLIP ViT-B/32;
- SigLIP Base P16 224 diagnostic.

The core v0.4 manifest is unchanged:

- 500 clean probe images;
- 38,999 native challenge images;
- challenge types 02-09 and 11-18;
- challenge levels 1-5 where available;
- five paired acquisition-condition samples per object/challenge/level, except
  one strict paired-source group with 4 usable samples.

All external-disk reads stayed under
`/Volumes/980PRO/CURE-OR++/archives`. No files were written to the external
disk.

## Headline Results

| Model | Clean accuracy | Mean native accuracy | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 | Worst level-5 challenge |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| CLIP ViT-B/16 | 0.4440 | 0.1929 | 0.2772 | 0.2245 | 0.1921 | 0.1596 | 0.0994 | type 09, salt and pepper noise; tied with type 18 |
| OpenCLIP ViT-B/32 LAION2B | 0.4120 | 0.1705 | 0.2473 | 0.2000 | 0.1659 | 0.1400 | 0.0890 | type 18, grayscale salt and pepper noise |
| CLIP ViT-B/32 | 0.3500 | 0.1532 | 0.2220 | 0.1825 | 0.1527 | 0.1249 | 0.0741 | type 09, salt and pepper noise |
| SigLIP Base P16 224 | 0.0120 | 0.0103 | 0.0105 | 0.0111 | 0.0114 | 0.0096 | 0.0084 | type 03, underexposure |

SigLIP is not a usable robustness baseline under the current zero-shot prompt
protocol because clean accuracy is 0.0120. It is retained as a negative
diagnostic result: the protocol can run, but the model-output interface or
prompting is not yet valid enough for robustness claims.

## Interpretation

The expanded pass strengthens the current v0.4 story in two ways.

First, the usable CLIP-family ordering is stable across the full native
challenge grid:

1. CLIP ViT-B/16;
2. OpenCLIP ViT-B/32 LAION2B;
3. CLIP ViT-B/32.

Second, the hardest level-5 native challenges remain near-collapse cases even
for the best current zero-shot model. For CLIP ViT-B/16, salt-and-pepper noise
and grayscale salt-and-pepper noise both reach 0.0100 accuracy. For OpenCLIP,
grayscale salt-and-pepper noise reaches 0.0080 accuracy.

This is still not enough for an arXiv-level final benchmark. CLIP ViT-B/32 is
an additional baseline, but not a new model family. SigLIP currently fails
clean recognition and should not be counted as a strong model. The next paper
level step is to add at least two more usable model families or stronger
pretrained variants, then extend the confidence-collapse/calibration analysis
on the same v0.4 manifest.

That next step has started with a separate non-CLIP prototype pass. HGNetV2-B0
and MobileNetV3-Small now run on the same v0.4 manifest using frozen ImageNet
features and a leave-clean-condition-out nearest-centroid protocol. Details are
in `reports/full_cure_or_prototype_v04.md`.

The first confidence/calibration pass is now complete for the three usable
zero-shot baselines. OpenCLIP is the clearest overconfidence case: at level 5,
mean accuracy is 0.0890 but mean confidence is 0.4781. See
`reports/full_cure_or_confidence_v04.md`.

## Artifacts

- `configs/clip_vit_b32_full_cure_or_probe_v04.json`
- `configs/siglip_base_p16_224_full_cure_or_probe_v04.json`
- `configs/full_cure_or_probe_summaries_v04_expanded.json`
- `results/clip_vit_b32_full_cure_or_probe_v04_predictions.csv`
- `results/clip_vit_b32_full_cure_or_probe_v04_summary.csv`
- `results/siglip_base_p16_224_full_cure_or_probe_v04_predictions.csv`
- `results/siglip_base_p16_224_full_cure_or_probe_v04_summary.csv`
- `results/full_cure_or_probe_v04_expanded_comparison.csv`
- `results/full_cure_or_probe_v04_expanded_level5_ranking.csv`
- `results/full_cure_or_probe_v04_expanded_level5_ranking.png`
- `results/full_cure_or_probe_v04_expanded_mean_accuracy_by_level.png`
- `results/full_cure_or_probe_v04_confidence_by_level.png`
- `results/full_cure_or_probe_v04_level5_overconfidence.png`
- `reports/full_cure_or_confidence_v04.md`

## Next Step

The next experiment should not simply scale row count. Use the same v0.4
manifest and add stronger usable baselines first:

1. a larger OpenCLIP, EVA-CLIP, or similar contrastive VLM if weights are
   available locally or can be downloaded with approval;
2. a non-CLIP classifier/prototype protocol adapted to the Full-CURE-OR
   100-object label space;
3. confidence-collapse and calibration tables for every new usable baseline.
