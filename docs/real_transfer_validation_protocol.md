# Real Transfer Validation Protocol v0.1

The simulated CURE-OR++ recipes are useful, but the next release needs a small
real-transfer sanity check. The goal is not scale yet. The goal is to prove that
the simulated ranking is not completely detached from actual app pipelines.

## Minimum Useful Pilot

- 10 to 30 source images from the current mini-CURE-OR clean test subset.
- 2 or 3 real transfer pipelines.
- The same source image should be paired with every collected transfer output.
- Keep original files unchanged; store transferred outputs separately.

The v0.1 source selection is pinned in:

```text
data/real_transfer/v01/source_selection_v01.csv
```

It contains one clean test source image for each of the 10 mini-CURE-OR object
classes. A minimum useful pilot is therefore 20 rows: 10 source images across 2
real transfer pipelines.

Recommended first pipelines:

- `messenger_upload_download`: send image through a messenger and download it.
- `phone_screenshot_resave`: screenshot the source image on a phone and resave.
- `video_call_frame_capture`: show image in a call or screen share and capture a frame.

## Folder Layout

Store real outputs under:

```text
data/real_transfer/v01/images/<recipe>/<source_stem>.jpg
```

Keep the pairing table at:

```text
data/real_transfer/v01/pairs.csv
```

Use `data/real_transfer/v01/pairs_template.csv` as the starting schema.

## Pairing Columns

Required:

- `source_path`: path to the clean mini-CURE-OR source image.
- `output_path`: path to the real transferred image.
- `recipe`: pipeline slug.
- `severity`: use `real` unless a pipeline has multiple controlled levels.
- `app_or_pipeline`: human-readable pipeline name.

Optional but useful:

- `label`: override label if the source is outside the clean manifest.
- `capture_device`
- `capture_date`
- `notes`

## Build Manifest

```bash
.venv/bin/python scripts/validate_real_transfer_pairs.py \
  --pairs data/real_transfer/v01/pairs.csv

.venv/bin/python scripts/build_real_transfer_manifest.py \
  --pairs data/real_transfer/v01/pairs.csv \
  --output data/real_transfer/v01/manifest.csv
```

The output manifest uses the same core columns as the simulated distortion
manifest, so the existing zero-shot evaluators can consume it by pointing a
config's `distorted_manifest_path` at the real-transfer manifest.

Prepared evaluation configs:

- `configs/clip_vit_b16_real_transfer_v01.json`
- `configs/openclip_vit_b32_laion2b_real_transfer_v01.json`

## Success Criterion

The pilot is useful if it can answer one narrow question:

> Does at least one real transfer pipeline reproduce the direction of the
> simulated CURE-OR++ failure signal, especially around `low_light_upload`,
> screenshot/resave, or video-call style degradation?
