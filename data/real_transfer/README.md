# Real Transfer Data

This folder is reserved for real app-transfer validation pilots.

Do not edit clean CURE-OR source images in place. Add transferred outputs under
the matching `data/real_transfer/<version>/images/` folder, then record
source/output pairs in `pairs.csv`.

Use v0.2 for the serious writeup path:

- `docs/real_transfer_validation_protocol_v02.md`
- `data/real_transfer/v02/source_selection_v02.csv`
- `data/real_transfer/v02/pairs_template.csv`
- `scripts/build_real_transfer_collection_pack.py`

v0.2 pins 30 clean mini-CURE-OR test images, three per object class, across
three real pipelines and two repeats. The older v0.1 folder remains as a
minimal pilot scaffold.

For collection, build the ignored local helper pack:

```bash
.venv/bin/python scripts/build_real_transfer_collection_pack.py \
  --source-selection data/real_transfer/v02/source_selection_v02.csv \
  --pairs-template data/real_transfer/v02/pairs_template.csv \
  --output-dir data/real_transfer/v02/collection_pack
```
