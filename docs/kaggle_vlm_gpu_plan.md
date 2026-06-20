# Kaggle GPU VLM Plan v0.1

## Goal

Run the CURE-OR++ real-transfer v0.2 VLM prompt pack on Kaggle GPU with an
open-weight model, starting with `HuggingFaceTB/SmolVLM2-500M-Video-Instruct`.

This path avoids paid frontier APIs and avoids local CPU runtime bottlenecks.

## What Codex Can Prepare Locally

- Build a private Kaggle dataset folder with prompt pack, scripts, and image
  payloads:

```bash
.venv/bin/python scripts/build_kaggle_vlm_package.py \
  --output-dir /Volumes/980PRO/CURE-OR++/kaggle_vlm/cure-or-pp-vlm-real-transfer-v02-private \
  --kaggle-id YOUR_KAGGLE_USERNAME/cure-or-pp-vlm-real-transfer-v02-private
```

- Generate the GPU notebook and Kaggle kernel metadata:

```bash
.venv/bin/python scripts/write_kaggle_vlm_notebook.py
```

Generated files:

- `notebooks/cure_or_pp_vlm_open_weight_kaggle_v01.ipynb`
- `kaggle/vlm_kernel/cure_or_pp_vlm_open_weight_kaggle_v01.ipynb`
- `kaggle/vlm_kernel/kernel-metadata.json`

## What Requires The User's Kaggle Account

Codex cannot push or run the notebook unless Kaggle CLI credentials are
configured locally.

Required local credential file:

```text
~/.kaggle/kaggle.json
```

Required CLI:

```bash
pip install kaggle
```

After that, upload the private dataset:

```bash
kaggle datasets create -p /Volumes/980PRO/CURE-OR++/kaggle_vlm/cure-or-pp-vlm-real-transfer-v02-private
```

Then push the GPU notebook:

```bash
kaggle kernels push -p kaggle/vlm_kernel
```

## Privacy Boundary

The VLM real-transfer Kaggle dataset should stay private unless upstream CURE-OR
and local real-transfer image terms explicitly permit public redistribution.

Do not upload API keys or raw paid-provider response payloads.
