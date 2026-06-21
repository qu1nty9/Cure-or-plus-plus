# Kaggle GPU VLM Plan v0.1

## Goal

Run the CURE-OR++ real-transfer v0.2 VLM prompt pack on Kaggle GPU with a
tiered open-weight model matrix. Completed full rows now include
`HuggingFaceTB/SmolVLM2-500M-Video-Instruct` and
`OpenGVLab/InternVL3-1B-hf`; the next step is promoting selected remaining
smoke-passed candidates from `configs/vlm_open_weight_model_matrix_v01.json`.

This path avoids paid frontier APIs and avoids local CPU runtime bottlenecks.

Status: complete for two open-weight full rows. Kaggle kernel version 7 ran the
SmolVLM2-500M 210-row prompt pack and wrote tracked artifacts under
`reports/vlm_open_weight_smolvlm2_kaggle_v01/`. Kaggle kernel version 12 ran
the InternVL3-1B 210-row prompt pack and wrote tracked artifacts under
`reports/vlm_open_weight_internvl3_1b_kaggle_v01/`. The current notebook now
defaults to smoke mode for the remaining tier-1 queue:

- `HuggingFaceTB/SmolVLM2-2.2B-Instruct`
- `llava-hf/llava-onevision-qwen2-0.5b-ov-hf`
- `Qwen/Qwen2.5-VL-3B-Instruct`

`llava-hf/llava-onevision-qwen2-0.5b-ov-hf` passed smoke but hit CUDA OOM in
full mode on Kaggle P100, so it should be retried only after memory-specific
tuning.

## What Codex Can Prepare Locally

- Build a private Kaggle dataset folder with prompt pack, scripts, and image
  payloads:

```bash
.venv/bin/python scripts/build_kaggle_vlm_package.py \
  --output-dir /Volumes/980PRO/CURE-OR++/kaggle_vlm/cure-or-pp-vlm-real-transfer-v02-private \
  --kaggle-id yaroslavkholmirzayev/cure-or-pp-vlm-real-transfer-v02-private
```

- Generate the GPU notebook and Kaggle kernel metadata:

```bash
.venv/bin/python scripts/write_kaggle_vlm_notebook.py
```

Generated files:

- `notebooks/cure_or_pp_vlm_open_weight_kaggle_v01.ipynb`
- `kaggle/vlm_kernel/cure_or_pp_vlm_open_weight_kaggle_v01.ipynb`
- `kaggle/vlm_kernel/kernel-metadata.json`

The notebook pins `torch==2.5.1+cu121` and `torchvision==0.20.1+cu121`
because the default Kaggle GPU resolved to Tesla P100, while newer Kaggle
PyTorch images no longer supported P100 `sm_60`. The runner uses `float16` for
that GPU.

Default notebook settings:

```python
RUN_MODE = "smoke"
SELECTED_MODEL_SLUGS = []
```

This runs enabled tier-1 models with fixed mixed clean/real-transfer smoke rows.
After smoke succeeds, promote models one at a time:

```python
RUN_MODE = "full"
SELECTED_MODEL_SLUGS = ["smolvlm2_2b"]
```

Do not run all large/stretch candidates in one session. Full 210-row runs
should be model-by-model so one memory failure does not destroy successful
rows.

## What Requires The User's Kaggle Account

Codex cannot push or run the notebook unless Kaggle CLI credentials are
configured locally.

Required local credential state, either OAuth cache:

```text
~/.kaggle/credentials.json
~/.kaggle/access_token
```

or the legacy API token file:

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

If the CLI reports `Authentication required`, refresh the local OAuth session:

```bash
kaggle auth login
```

## Privacy Boundary

The VLM real-transfer Kaggle dataset should stay private unless upstream CURE-OR
and local real-transfer image terms explicitly permit public redistribution.

Do not upload API keys or raw paid-provider response payloads.
