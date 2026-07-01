# Kaggle GPU VLM Plan v0.1

## Goal

Run the CURE-OR++ real-transfer v0.2 VLM prompt pack on Kaggle GPU with a
tiered open-weight model matrix. Completed full rows now include
`HuggingFaceTB/SmolVLM2-500M-Video-Instruct` and
`HuggingFaceTB/SmolVLM2-2.2B-Instruct`, `OpenGVLab/InternVL3-1B-hf`,
`OpenGVLab/InternVL3-2B-hf`, `llava-hf/llava-onevision-qwen2-0.5b-ov-hf`, and
`Qwen/Qwen2.5-VL-3B-Instruct`, plus
`Qwen/Qwen2.5-VL-7B-Instruct` and
`llava-hf/llava-onevision-qwen2-7b-ov-hf`. The next step is using the same
prompt-pack/evaluator path for selected frontier/provider VLM rows or
repeatability reruns.

This path avoids paid frontier APIs and avoids local CPU runtime bottlenecks.

Status: complete for eight open-weight full rows. Kaggle kernel version 7 ran
the SmolVLM2-500M 210-row prompt pack and wrote tracked artifacts under
`reports/vlm_open_weight_smolvlm2_kaggle_v01/`. Kaggle kernel version 12 ran
the InternVL3-1B 210-row prompt pack and wrote tracked artifacts under
`reports/vlm_open_weight_internvl3_1b_kaggle_v01/`. Kaggle kernel version 13
ran the Qwen2.5-VL-3B 210-row prompt pack and wrote tracked artifacts under
`reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/`. Kaggle kernel version 14
ran the SmolVLM2-2.2B 210-row prompt pack and wrote tracked artifacts under
`reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/`. Kaggle kernel version 16
ran the InternVL3-2B 210-row prompt pack and wrote tracked artifacts under
`reports/vlm_open_weight_internvl3_2b_kaggle_v01/`. Kaggle kernel version 20
ran the LLaVA-OneVision 0.5B 210-row prompt pack and wrote tracked artifacts
under `reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/`. The
Qwen2.5-VL-7B then failed an initial smoke attempt at Kaggle kernel version 21
with CUDA OOM, passed a memory-controlled smoke retry at Kaggle kernel version
22, and completed a full 210-row pass at Kaggle kernel version 23 under
`reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/`.

`llava-hf/llava-onevision-qwen2-7b-ov-hf` failed the first smoke attempt at
Kaggle kernel version 24 with CUDA OOM during generation on P100. Kernel
version 25 passed a memory-controlled smoke retry with `device_map=auto`,
`low_cpu_mem_usage=true`, `use_cache=false`, input resize to `max_side=384`,
and `max_tokens=2`. Kaggle kernel version 26 completed the corresponding
model-by-model full run under
`reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/`.

`llava-hf/llava-onevision-qwen2-0.5b-ov-hf` originally passed smoke, then hit
CUDA OOM in full mode on Kaggle P100, and then failed once more under unsafe
`anyres` processor overrides. The successful completion path keeps default
OneVision processing and resizes each input image to `max_side=768` before
preprocessing.

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
SELECTED_MODEL_SLUGS = ["llava_onevision_qwen2_7b"]
```

Do not run all large/stretch candidates in one session. Full 210-row runs
should be model-by-model so one memory failure does not destroy successful
rows.

For Qwen2.5-VL-7B specifically, the successful path on Kaggle P100 required:

- `processor_kwargs.min_pixels=50176`
- `processor_kwargs.max_pixels=262144`
- `image_max_side=512`
- `generate_kwargs.use_cache=false`
- `model_kwargs.low_cpu_mem_usage=true`

For LLaVA-OneVision Qwen2 7B specifically, the successful path on Kaggle P100
required:

- `device_map=auto`
- `model_kwargs.low_cpu_mem_usage=true`
- `generate_kwargs.use_cache=false`
- `image_max_side=384`
- `max_tokens=2`

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
