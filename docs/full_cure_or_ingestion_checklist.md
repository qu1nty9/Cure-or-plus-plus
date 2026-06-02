# Full-CURE-OR Ingestion Checklist v0.1

## Purpose

This checklist defines the first controlled move from local mini-CURE-OR to the
full CURE-OR release. The goal is to avoid turning the next step into a blind
large download. Full-CURE-OR should enter the project through the same probe,
manifest, and evaluation path that already works for mini-CURE-OR.

## Known Full Dataset Facts

From the official `olivesgatech/CURE-OR` README:

- 1,000,000 images;
- 100 objects;
- 5 backgrounds;
- 5 acquisition devices;
- 5 object orientations;
- challenging conditions encoded by `challengeType` and `challengeLevel`;
- filename pattern:
  `backgroundID_deviceID_objectOrientationID_objectID_challengeType_challengeLevel.jpg`.

The complete dataset requires submitting the official access form. The mini
version remains the local dry-run dataset.

IEEE DataPort now lists the complete release as 18 `.tar.gz` archives. The
archive manifest is pinned in `configs/cure_or_dataport_archives_v01.json`, and
the current download status is tracked in
`reports/cure_or_download_status_v01.md`.

## Local Storage Estimate

The local mini-CURE-OR unpacked image set is:

- 16,500 images;
- 3,455,399,222 bytes;
- 3.2181 GiB.

A linear estimate for 1,000,000 images is about 195 GiB unpacked. This is only
a planning estimate, not an official full-release size. Keep extra space for
archives, probes, manifests, predictions, and figures.

## Current External-Disk Layout

The first Full-CURE-OR probe subset is currently staged as extracted folders,
not compressed `.tar.gz` archives:

```text
/Volumes/980PRO/CURE-OR++/archives/
  01_no_challenge/
  02_resize/
  05_blur/
  09_saltpepper/
  14_grayscale_blur/
  18_grayscale_saltpepper/
```

This folder contains 312,500 usable image files after ignoring macOS
AppleDouble `._*` files.

## Target Full-Release Layout

```text
data/
  raw/
    full_cure_or/
      train.csv
      test.csv
      train/
      test/
```

If the official release arrives with a different directory layout, do not move
files by hand first. Run the probe with `--skip-image-scan`, inspect the CSV
schema, then adapt the path/index logic.

## Preflight Commands

Metadata-only probe:

```bash
python3 scripts/probe_cure_or_dataset.py \
  --dataset-dir data/raw/full_cure_or \
  --output reports/full_cure_or_probe_v01.json \
  --scope-output reports/full_cure_or_scope_v01.csv \
  --skip-image-scan
```

Full local image probe:

```bash
python3 scripts/probe_cure_or_dataset.py \
  --dataset-dir data/raw/full_cure_or \
  --output reports/full_cure_or_probe_v01.json \
  --scope-output reports/full_cure_or_scope_v01.csv
```

Success criteria:

- CSV files are found;
- challenge types map to `docs/native_challenge_mapping_v01.md`;
- full object IDs map to `configs/cure_or_objects_v01.json`;
- image scan finds the expected image count;
- missing image rows are zero or explainable;
- scope table has the expected challenge type/level coverage.

Build a Full-CURE-OR clean manifest with 100 object labels:

```bash
python3 scripts/build_cure_or_base_manifest.py \
  --dataset-dir data/raw/full_cure_or \
  --output data/interim/full_cure_or_clean_manifest.csv \
  --splits test \
  --label-map cure_or_objects
```

Validate the OpenCLIP probe config before running the model:

```bash
python3 scripts/validate_eval_config.py \
  --config configs/openclip_vit_b32_laion2b_full_cure_or_probe_v01.json
```

Before the manifests exist, use:

```bash
python3 scripts/validate_eval_config.py \
  --config configs/openclip_vit_b32_laion2b_full_cure_or_probe_v01.json \
  --allow-missing-manifests
```

Build the first native probe manifest:

```bash
python3 scripts/build_native_cure_or_manifest.py \
  --dataset-dir data/raw/full_cure_or \
  --output data/interim/full_cure_or_native_probe_v01_manifest.csv \
  --splits test \
  --challenge-types 2,5,9,14,18 \
  --challenge-levels 1,2,3,4 \
  --label-map cure_or_objects
```

For the extracted IEEE DataPort folder layout currently on the external disk,
use the archive-folder manifest builder instead:

```bash
python3 scripts/build_full_cure_or_probe_manifests.py \
  --archives-dir /Volumes/980PRO/CURE-OR++/archives \
  --challenge-types 2,5,9,14,18 \
  --challenge-levels 1,2,3,4 \
  --max-clean-per-object 1 \
  --max-native-per-object-group 1
```

This produces:

```text
data/interim/full_cure_or_clean_probe_v01_manifest.csv
data/interim/full_cure_or_native_probe_v01_manifest.csv
```

## First Evaluation Scope

The first Full-CURE-OR run should be a probe, not a full paper run.

Recommended first probe:

- split: test only;
- model: OpenCLIP ViT-B/32 LAION2B;
- challenge types: 02, 05, 09, 14, 18;
- levels: 1-4 where present;
- max per object/class/group: start small if runtime or storage is uncertain.

Why this scope:

- resize is a low-damage control in mini-CURE-OR;
- gaussian blur and grayscale gaussian blur are major failure modes;
- salt and pepper noise and grayscale salt and pepper noise expose
  high-confidence failure for OpenCLIP;
- the subset is aligned with the strongest mini-CURE-OR evidence.

## Gate Before Full-Scale Run

Do not run the full model suite until the probe has:

- a clean probe JSON;
- a clean scope CSV;
- one evaluated model;
- a runtime estimate per 10,000 images;
- a storage estimate for predictions and figures;
- a short note comparing Full-CURE-OR probe behavior with mini-CURE-OR.

Current status: the first extracted-folder probe has two evaluated models and
is documented in `reports/full_cure_or_probe_v01.md`. The remaining gate is to
expand sampling across more backgrounds/devices/orientations before calling the
result paper-scale.

## Label Caveat

Full-CURE-OR has 100 object IDs, but at least one display name appears more
than once: `Calculator` is used for object 034 and object 066. The configs
therefore use object-ID-aware label keys such as `object_034_calculator` and
`object_066_calculator`. Their zero-shot prompt text is still the same display
name, so object-instance disambiguation is a known limitation for this probe.
