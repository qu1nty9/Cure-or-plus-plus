# Full-CURE-OR v0.4 Evaluation Card

## Evaluation Summary

The Full-CURE-OR v0.4 evaluation measures how object-recognition baselines
degrade from clean images to native CURE-OR challenge rows. It is the current
serious benchmark track for CURE-OR++.

Core evaluated conditions:

- clean probe rows;
- native challenge types 02-09 and 11-18;
- severity levels 1-5 where available;
- type-10 grayscale no-challenge control;
- planned real-transfer v0.2 validation, not yet evaluated.

## Main Metrics

Tracked aggregate metrics:

- accuracy;
- mean max-class confidence;
- relative accuracy drop versus clean;
- confidence drop versus clean;
- calibration gap: `mean_confidence - accuracy`;
- expected calibration error with 10 bins;
- top-1 Brier score;
- high-confidence wrong rate.

Not every metric is computed for every model family. Confidence/calibration
analysis currently covers the usable CLIP/OpenCLIP-family zero-shot rows.

## Main Baselines

Usable rows in the current paper table:

- DINOv2 ViT-S/14 Prototype;
- ConvNeXt-Tiny Prototype;
- OpenCLIP ViT-B/16 DataComp XL;
- HGNetV2-B0 Prototype;
- CLIP ViT-B/16;
- MobileNetV3-Small Prototype;
- OpenCLIP ViT-B/32 LAION2B;
- CLIP ViT-B/32.

Diagnostic row:

- SigLIP Base P16 224 is excluded from the main interpretation because the
  current zero-shot prompt protocol produced a clean accuracy failure.

## Headline Results

Current strongest level-5 row:

- DINOv2 ViT-S/14 Prototype;
- clean accuracy: 0.7520;
- native mean accuracy: 0.4393;
- native level-5 accuracy: 0.2766.

Current strongest zero-shot contrastive row:

- OpenCLIP ViT-B/16 DataComp XL;
- clean accuracy: 0.5460;
- native mean accuracy: 0.2561;
- native level-5 accuracy: 0.1451.

Consensus severe failures:

- grayscale salt-and-pepper noise: mean level-5 accuracy 0.0092, floor 8/8;
- salt-and-pepper noise: mean level-5 accuracy 0.0103, floor 8/8;
- grayscale gaussian blur: mean level-5 accuracy 0.0115, floor 8/8.

Confidence finding:

- OpenCLIP ViT-B/16 DataComp XL level-5 accuracy is 0.1451 while mean confidence
  remains 0.4997.
- Its worst overconfidence case is grayscale salt-and-pepper noise: 0.0100
  accuracy, 0.7393 mean confidence, and 0.9760 high-confidence wrong rate.

Grayscale-control guardrail:

- DataComp XL grayscale no-challenge control accuracy is 0.3908 while native
  level-5 accuracy is 0.1451.
- This supports the claim that grayscale alone is damaging but does not explain
  the full native level-5 collapse.

## Reproducibility Artifacts

Paper-level outputs:

- `reports/full_cure_or_paper_tables_v04.md`
- `reports/full_cure_or_paper_tables_v04.tex`
- `reports/cure_or_pp_technical_report_draft_v04.md`

Primary aggregate reports:

- `reports/full_cure_or_probe_v04_status.md`
- `reports/full_cure_or_probe_v04_expanded_models.md`
- `reports/full_cure_or_prototype_v04.md`
- `reports/full_cure_or_confidence_v04.md`
- `reports/full_cure_or_grayscale_control_v04.md`
- `reports/full_cure_or_challenge_family_v04.md`
- `reports/full_cure_or_consensus_v04.md`

Primary scripts:

- `scripts/build_paper_tables.py`
- `scripts/analyze_full_cure_or_confidence.py`
- `scripts/analyze_full_cure_or_challenge_families.py`
- `scripts/analyze_full_cure_or_consensus.py`
- `scripts/compare_full_cure_or_control.py`

## Interpretation Rules

Safe interpretation:

- compare clean-to-native degradation within each model;
- compare consensus severe challenge failures across usable baselines;
- report that stronger baselines improve absolute level-5 accuracy but still
  fail near chance on salt-and-pepper and blur variants;
- use grayscale control as a guardrail, not as a replacement for native
  challenge analysis.

Avoid:

- claiming that real app-transfer failures are proven before v0.2 is evaluated;
- mixing SigLIP diagnostic results into the main robustness ranking;
- comparing prototype classifiers and zero-shot contrastive models as if they
  were the same training/evaluation protocol;
- claiming the v0.4 probe exhausts all Full-CURE-OR images.

## Remaining Evaluation Work

Before a final public paper:

1. Collect and evaluate real-transfer v0.2.
2. Add confidence/calibration tables for any further usable zero-shot or VLM
   families.
3. Decide whether to add one additional pretrained non-CLIP/OpenCLIP VLM family
   or keep the current model set and focus on real-transfer validation.
