# Real Transfer Validation v0.1 Readiness

## Status

The real-transfer pilot is prepared but not yet evaluated because
`data/real_transfer/v01/pairs.csv` has not been filled with real transferred
outputs.

Prepared local assets:

- `data/real_transfer/v01/source_selection_v01.csv`
- `data/real_transfer/v01/pairs_template.csv`
- `scripts/validate_real_transfer_pairs.py`
- `scripts/build_real_transfer_manifest.py`
- `configs/clip_vit_b16_real_transfer_v01.json`
- `configs/openclip_vit_b32_laion2b_real_transfer_v01.json`

The source selection pins 10 clean mini-CURE-OR test images, one per object
class. The minimum useful pilot is 20 rows: the same 10 sources through at least
2 real transfer pipelines.

## Go/No-Go Gate

The validation script uses these default thresholds:

| Check | Threshold |
| --- | ---: |
| Real transfer rows | 20 |
| Distinct recipes | 2 |
| Distinct labels | 10 |
| Duplicate source/output/recipe rows | 0 |
| Missing source/output files | 0 |

The pilot is ready for model evaluation only when
`scripts/validate_real_transfer_pairs.py` reports `Ready for eval: True`.

## Reproduction

After transferred images are collected under
`data/real_transfer/v01/images/<recipe>/`, fill
`data/real_transfer/v01/pairs.csv`, then run:

```bash
.venv/bin/python scripts/validate_real_transfer_pairs.py \
  --pairs data/real_transfer/v01/pairs.csv

.venv/bin/python scripts/build_real_transfer_manifest.py \
  --pairs data/real_transfer/v01/pairs.csv \
  --output data/real_transfer/v01/manifest.csv

HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  .venv/bin/python scripts/evaluate_clip_zero_shot.py \
  --config configs/clip_vit_b16_real_transfer_v01.json \
  --device cpu

.venv/bin/python scripts/evaluate_openclip_zero_shot.py \
  --config configs/openclip_vit_b32_laion2b_real_transfer_v01.json \
  --device cpu
```

## Interpretation Target

The first real-transfer pilot should answer one narrow question:

> Do actual app or capture pipelines reproduce the direction of the simulated
> CURE-OR failure signal?

It does not need to be large enough for final claims. It only needs to show
whether real messenger/screenshot/video-call degradation agrees with the
existing simulated failure ranking enough to justify scaling the collection.
