# Real Transfer Validation v0.2 Status

## Status

The stronger v0.2 real-transfer block is collected, activated, and evaluated.
The evaluated design is:

- 30 clean mini-CURE-OR test sources;
- 10 labels;
- 3 sources per label;
- 3 real transfer pipelines;
- 2 repeats per source and pipeline;
- 180 collected real transferred output images.

Current activation validation:

- rows: 180;
- recipes: 3;
- labels: 10;
- schema ready: true;
- files ready: true;
- ready for eval: true.

The local collection pack was generated at
`data/real_transfer/v02/collection_pack/`. It contains the 30 selected source
images, an HTML index, a contact sheet, and a 180-row collection checklist. The
pack, real-transfer image payloads, `pairs.csv`, `manifest.csv`, and per-image
prediction dumps are intentionally ignored by Git.

## Artifacts

- `docs/real_transfer_validation_protocol_v02.md`
- `scripts/prepare_real_transfer_protocol.py`
- `scripts/build_real_transfer_collection_pack.py`
- `scripts/import_real_transfer_clean_pack.py`
- `scripts/activate_real_transfer_protocol.py`
- `scripts/validate_real_transfer_pairs.py`
- `scripts/build_real_transfer_manifest.py`
- `scripts/build_real_transfer_report.py`
- `data/real_transfer/v02/source_selection_v02.csv`
- `data/real_transfer/v02/recipe_plan_v02.csv`
- `data/real_transfer/v02/pairs_template.csv`
- `reports/real_transfer_pairs_v02_template_validation.json`
- `reports/real_transfer_v02_clean_pack_import_report.json`
- `reports/real_transfer_pairs_v02_validation.json`
- `reports/real_transfer_v02_activation_status.json`
- `reports/real_transfer_v02_results.md`
- `reports/real_transfer_v02_model_pipeline_table.csv`
- `reports/real_transfer_v02_pipeline_consensus_table.csv`
- `reports/real_transfer_v02_label_failure_table.csv`
- `configs/clip_vit_b16_real_transfer_v02.json`
- `configs/clip_vit_b32_real_transfer_v02.json`
- `configs/openclip_vit_b32_laion2b_real_transfer_v02.json`
- `configs/openclip_vit_b16_datacomp_xl_real_transfer_v02.json`
- `results/clip_vit_b16_real_transfer_v02_summary.csv`
- `results/clip_vit_b32_real_transfer_v02_summary.csv`
- `results/openclip_vit_b32_laion2b_real_transfer_v02_summary.csv`
- `results/openclip_vit_b16_datacomp_xl_real_transfer_v02_summary.csv`

## Why This Is The Stronger Path

This closes the largest remaining external-validity gap. The current Full-CURE-OR
work already has broad native challenge coverage, consensus analysis,
confidence/calibration analysis, and stronger baseline rows. The v0.2 block now
adds direct evidence from actual app/device transfer pipelines.

The v0.2 protocol is strong enough to support a serious validation section
because it is balanced by class, includes multiple real pipelines, and includes
repeat captures rather than a single fragile sample per source. It now provides
direct evidence about whether actual app/device transfers produce related
failure behavior.

## Result Summary

The source-matched report in `reports/real_transfer_v02_results.md` compares
each real-transfer pipeline against the same 30 clean source images used for
collection. The effects are moderate, not catastrophic:

- collector-supplied metadata: iPhone 15 Pro capture device, WhatsApp
  messenger upload/download, iPhone screenshot/resave, and FaceTime
  video-call/screen-share frame capture;
- video-call frame capture: 79.6% mean real accuracy, 2.1 percentage-point mean
  drop, 5.0 point max drop;
- messenger upload/download: 80.0% mean real accuracy, 1.7 point mean drop;
- phone screenshot/resave: 82.5% mean real accuracy, -0.8 point mean drop.

The model-pipeline table includes source-level bootstrap confidence intervals,
and `results/real_transfer_v02_source_matched_drops.png` plus
`results/real_transfer_v02_accuracy_heatmap.png` provide paper-ready figures.
The intervals are wide because v0.2 uses 30 source images, so the right claim is
external-validity guardrail rather than precise small-effect ranking.

This is best interpreted as an external-validity guardrail for the larger
simulated and native CURE-OR findings. It should not be overclaimed as broad
real-world transfer robustness.

## Next Step

Integrate the real-transfer v0.2 results into the technical draft and LaTeX
paper source. Per-file capture dates are not manually asserted; extract them
from image metadata where present if needed for final public packaging.
