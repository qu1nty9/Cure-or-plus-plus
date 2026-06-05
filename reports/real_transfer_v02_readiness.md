# Real Transfer Validation v0.2 Readiness

## Status

The stronger v0.2 real-transfer scaffold is prepared but not evaluated yet.
The planned design is:

- 30 clean mini-CURE-OR test sources;
- 10 labels;
- 3 sources per label;
- 3 real transfer pipelines;
- 2 repeats per source and pipeline;
- 180 planned real transferred output images.

Current template validation:

- rows: 180;
- recipes: 3;
- labels: 10;
- schema ready: true;
- files ready: false;
- ready for eval: false.

`files_ready` is false because the actual real-transfer output images have not
been collected yet.

A local collection pack has been generated at
`data/real_transfer/v02/collection_pack/`. It contains the 30 selected source
images, an HTML index, a contact sheet, and a 180-row collection checklist. The
pack and future real-transfer image payloads are intentionally ignored by Git.

## Artifacts

- `docs/real_transfer_validation_protocol_v02.md`
- `scripts/prepare_real_transfer_protocol.py`
- `scripts/build_real_transfer_collection_pack.py`
- `scripts/validate_real_transfer_pairs.py`
- `scripts/build_real_transfer_manifest.py`
- `data/real_transfer/v02/source_selection_v02.csv`
- `data/real_transfer/v02/recipe_plan_v02.csv`
- `data/real_transfer/v02/pairs_template.csv`
- `reports/real_transfer_pairs_v02_template_validation.json`
- `configs/clip_vit_b16_real_transfer_v02.json`
- `configs/clip_vit_b32_real_transfer_v02.json`
- `configs/openclip_vit_b32_laion2b_real_transfer_v02.json`
- `configs/openclip_vit_b16_datacomp_xl_real_transfer_v02.json`

## Why This Is The Stronger Path

This closes the largest remaining external-validity gap. The current Full-CURE-OR
work already has broad native challenge coverage, consensus analysis,
confidence/calibration analysis, and stronger baseline rows. What it still lacks
is direct evidence that actual app/device transfer pipelines create related
failure modes.

The v0.2 protocol is strong enough to support a serious validation section
because it is balanced by class, includes multiple real pipelines, and includes
repeat captures rather than a single fragile sample per source.

## Next Step

Collect the 180 real transferred outputs at the paths pinned in
`data/real_transfer/v02/pairs_template.csv`, using
`data/real_transfer/v02/collection_pack/index.html` and
`data/real_transfer/v02/collection_pack/collection_checklist.csv` as the
collection guide. Then copy the template to `data/real_transfer/v02/pairs.csv`,
fill metadata columns, run strict validation, and run the four prepared
zero-shot configs.
