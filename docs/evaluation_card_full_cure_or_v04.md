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
- real-transfer v0.2 validation over messenger upload/download, phone
  screenshot/resave, and video-call frame capture.

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

Real-transfer validation:

- 180 real transferred outputs were collected from 30 source images, 10 labels,
  three pipelines, and two repeats per source/pipeline.
- Collector-supplied metadata identifies iPhone 15 Pro as the capture device,
  WhatsApp as the messenger pipeline, and FaceTime as the video-call pipeline.
- The source-matched consensus table shows moderate rather than catastrophic
  effects: video-call frame capture has the largest mean drop at 2.1 percentage
  points, messenger upload/download drops 1.7 points, and phone
  screenshot/resave is +0.8 points versus matched clean source accuracy.
- Source-level bootstrap intervals are reported in
  `reports/real_transfer_v02_model_pipeline_table.csv`; they are intentionally
  wide because the validation block uses 30 source images.
- The result is best treated as an external-validity guardrail for the larger
  simulated and native CURE-OR findings, not as a broad deployment claim.

VLM/API prompt-pack status:

- A separate multiple-choice VLM/API prompt pack is prepared for real-transfer
  v0.2.
- It contains 210 image-question rows per model: 30 clean source rows and 180
  transferred rows.
- Five open-weight full rows are complete: `SmolVLM2-500M-Video-Instruct`,
  `SmolVLM2-2.2B-Instruct`, `InternVL3-1B-hf`, `InternVL3-2B-hf`, and
  `Qwen2.5-VL-3B-Instruct`. Their tracked artifacts are in
  `reports/vlm_open_weight_smolvlm2_kaggle_v01/`,
  `reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/`,
  `reports/vlm_open_weight_internvl3_1b_kaggle_v01/`, and
  `reports/vlm_open_weight_internvl3_2b_kaggle_v01/`, plus
  `reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/`.
- The strongest open-weight rows are now SmolVLM2-2.2B and InternVL3-1B at
  93.3% on both clean-source and real-transfer splits, while InternVL3-2B
  remains fully parseable but lands slightly lower at 92.8% real-transfer
  accuracy.
- It is intentionally not mixed into the current CLIP/OpenCLIP/prototype
  leaderboard because provider VLMs require text-answer extraction, exact model
  versioning, and raw-response audit handling.

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
- `reports/real_transfer_v02_results.md`
- `reports/vlm_api_track_v01_prompt_pack_summary.json`

Primary scripts:

- `scripts/build_paper_tables.py`
- `scripts/analyze_full_cure_or_confidence.py`
- `scripts/analyze_full_cure_or_challenge_families.py`
- `scripts/analyze_full_cure_or_consensus.py`
- `scripts/compare_full_cure_or_control.py`
- `scripts/import_real_transfer_clean_pack.py`
- `scripts/build_real_transfer_report.py`
- `scripts/build_vlm_prompt_pack.py`
- `scripts/run_openai_compatible_vlm.py`
- `scripts/run_gemini_vlm.py`
- `scripts/run_hf_vlm.py`
- `scripts/evaluate_vlm_response_pack.py`

## Interpretation Rules

Safe interpretation:

- compare clean-to-native degradation within each model;
- compare consensus severe challenge failures across usable baselines;
- report that stronger baselines improve absolute level-5 accuracy but still
  fail near chance on salt-and-pepper and blur variants;
- use grayscale control as a guardrail, not as a replacement for native
  challenge analysis.
- use real-transfer v0.2 as a small external-validity guardrail, not as a claim
  that all app/device transfer behavior is covered.

Avoid:

- mixing SigLIP diagnostic results into the main robustness ranking;
- comparing prototype classifiers and zero-shot contrastive models as if they
  were the same training/evaluation protocol;
- claiming the v0.4 probe exhausts all Full-CURE-OR images.

## Remaining Evaluation Work

Before a final public paper:

1. Integrate real-transfer v0.2 results into the final paper prose.
2. Execute additional frontier/provider VLM rows if modern assistant
   comparisons are needed for the first public paper.
3. Add confidence/calibration tables for any further usable zero-shot or VLM
   families.
4. Decide whether to retry a memory-constrained open-weight row such as
   LLaVA-OneVision 0.5B or keep the current open-weight set and focus on paper
   polish.
