# Full-CURE-OR Consensus Failure Analysis v0.4

## Summary

This pass analyzes whether Full-CURE-OR level-5 failures are stable across the
eight usable v0.4 baselines or mostly model-specific. It uses
`results/full_cure_or_probe_v04_with_prototypes_comparison.csv` and focuses on
the 14 official challenge types that provide level-5 rows.

The key result is strong consensus: blur and salt-and-pepper noise variants are
near chance for every usable model, while pairwise level-5 rank correlations are
all high.

All inputs are local aggregate CSVs. No external-disk reads or writes are
needed for this analysis.

## Consensus Hardest Level-5 Challenges

The floor threshold is accuracy `<= 0.02`. With 100 object labels, chance is
approximately 0.01, so this threshold captures near-chance collapse.

| Rank | Challenge | Mean rank | Mean accuracy | Floor models |
| ---: | --- | ---: | ---: | ---: |
| 1 | Grayscale salt & pepper noise | 1.75 | 0.0092 | 8 / 8 |
| 2 | Salt & pepper noise | 2.44 | 0.0103 | 8 / 8 |
| 3 | Grayscale gaussian blur | 2.56 | 0.0115 | 8 / 8 |
| 4 | Gaussian blur | 3.62 | 0.0150 | 7 / 8 |
| 5 | Grayscale dirty lens 1 | 4.62 | 0.0255 | 5 / 8 |

This is a paper-level finding: the top three hardest level-5 challenges are not
only low on average, they are at the floor for every usable baseline, including
OpenCLIP ViT-B/16 DataComp XL, DINOv2 ViT-S/14, and ConvNeXt-Tiny. Gaussian
blur is also near-floor for all eight models, with seven of eight at the floor
threshold.

## Model-Ranking Stability

Pairwise Spearman rank correlations over the 14 level-5 challenges are high:

| Pair | Spearman rho | Mean absolute rank delta |
| --- | ---: | ---: |
| HGNetV2-B0 Prototype vs OpenCLIP ViT-B/32 LAION2B | 0.892 | 1.57 |
| MobileNetV3-Small Prototype vs OpenCLIP ViT-B/16 DataComp XL | 0.898 | 1.43 |
| DINOv2 ViT-S/14 Prototype vs MobileNetV3-Small Prototype | 0.900 | 1.36 |
| HGNetV2-B0 Prototype vs OpenCLIP ViT-B/16 DataComp XL | 0.902 | 1.43 |
| MobileNetV3-Small Prototype vs OpenCLIP ViT-B/32 LAION2B | 0.905 | 1.57 |

The lowest observed correlation is still 0.892. This means the benchmark is not
just producing arbitrary model-specific failure lists. There are model-family
differences, but the broad level-5 difficulty ordering is stable.

The strongest agreement is within closely related or similarly behaving
families:

| Pair | Spearman rho | Mean absolute rank delta |
| --- | ---: | ---: |
| CLIP ViT-B/16 vs CLIP ViT-B/32 | 0.988 | 0.43 |
| ConvNeXt-Tiny Prototype vs DINOv2 ViT-S/14 Prototype | 0.983 | 0.57 |
| CLIP ViT-B/32 vs MobileNetV3-Small Prototype | 0.981 | 0.50 |

## Interpretation

The consensus analysis strengthens the benchmark claim in two directions:

1. robust consensus failure exists: grayscale salt-and-pepper noise,
   salt-and-pepper noise, and grayscale gaussian blur collapse all eight usable
   baselines at level 5, while gaussian blur is near-floor for all eight;
2. model-family differences still matter: some middle-ranked challenges move
   by several rank positions, especially across CLIP/OpenCLIP and prototype
   backbones.

This is stronger than reporting only per-model worst cases. It shows that
CURE-OR level-5 has a stable core of universally hard corruptions plus a
secondary region where model-family robustness profiles diverge.

## Artifacts

- `scripts/analyze_full_cure_or_consensus.py`
- `results/full_cure_or_probe_v04_with_prototypes_level5_consensus.csv`
- `results/full_cure_or_probe_v04_with_prototypes_level5_rank_correlations.csv`

## Verification

- `python scripts/analyze_full_cure_or_consensus.py`
- output rows:
  - consensus rows: 14;
  - rank-correlation rows: 28.

## Next Step

The remaining paper-level gap is not more aggregate analysis on the same rows.
The next high-value step is either a real transfer validation sample or another
stronger pretrained VLM family that is not just a nearby CLIP/OpenCLIP variant.
