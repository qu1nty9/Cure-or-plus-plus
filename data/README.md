# Data Layout

This directory is intentionally lightweight in git.

Recommended local layout for the first experiments:

```text
data/
  raw/
    mini_cure_or/
      train.csv
      test.csv
      train/
      test/
    full_cure_or/
      train.csv
      test.csv
      train/
      test/
  interim/
    cure_or_clean_manifest.csv
  processed/
    cure_or_pp_v0/
      manifest.csv
```

The mini-CURE-OR dataset is described in the public repository:

https://github.com/olivesgatech/mini-CURE-OR

The public Zenodo record is:

https://zenodo.org/record/4299330

Download metadata only:

```bash
python3 scripts/download_mini_cure_or.py --files train.csv test.csv
```

Download image archives when ready:

```bash
python3 scripts/download_mini_cure_or.py --files train.zip test.zip
```

The first CURE-OR++ pass should use only clean source images:

- `challengeType = 1`
- `challengeLevel = 0`

Build the source manifest:

```bash
python3 scripts/build_cure_or_base_manifest.py \
  --dataset-dir data/raw/mini_cure_or \
  --output data/interim/cure_or_clean_manifest.csv
```

For the complete CURE-OR release, use the 100-object label map:

```bash
python3 scripts/build_cure_or_base_manifest.py \
  --dataset-dir data/raw/full_cure_or \
  --output data/interim/full_cure_or_clean_manifest.csv \
  --splits test \
  --label-map cure_or_objects
```

Full-CURE zero-shot probe configs can be validated before model loading:

```bash
python3 scripts/validate_eval_config.py \
  --config configs/openclip_vit_b32_laion2b_full_cure_or_probe_v01.json \
  --allow-missing-manifests
```

Generate CURE-OR++ distorted images:

```bash
python3 scripts/generate_distortions.py --config configs/benchmark_v0.json
```

Probe a local CURE-OR-style dataset before evaluation:

```bash
python3 scripts/probe_cure_or_dataset.py \
  --dataset-dir data/raw/mini_cure_or \
  --output reports/mini_cure_or_probe_v01.json \
  --scope-output reports/mini_cure_or_scope_v01.csv
```

For the complete CURE-OR release, start with
`docs/full_cure_or_ingestion_checklist.md`.
