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

The v0.3 extension uses the same Kaggle GPU path on a larger 900-row prompt
pack: 100 clean rows and 800 real-transfer rows over WhatsApp transfer,
phone screenshot/resave, Instagram resave, and FaceTime frame capture. Two
full 7B v0.3 rows are complete and tracked under
`reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/` and
`reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/`.
Kaggle kernel version 30 completed the SmolVLM2-2.2B full v0.3 run, tracked in
`reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/`. Kaggle kernel version
31 completed the Qwen2.5-VL-3B full v0.3 run, tracked in
`reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/`; it preserves the
earlier generation-instability signal, with 0.2088 real-transfer unparseable
rate. Kaggle kernel version 32 completed the LLaVA-OneVision Qwen2 0.5B full
v0.3 run, tracked in
`reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/`, with
0.9300 clean accuracy, 0.9213 real-transfer accuracy, and zero unparseables.
Kaggle kernel version 33 completed the InternVL3-1B full v0.3 run, tracked in
`reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/`, with 0.9500 clean
accuracy, 0.9563 real-transfer accuracy, and zero unparseables.
Kaggle kernel version 34 completed the InternVL3-2B full v0.3 run, tracked in
`reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/`, with 0.9700 clean
accuracy, 0.9600 real-transfer accuracy, and zero unparseables.
The generated comparison in
`reports/vlm_open_weight_full_v03_comparison.md` is built from completed full
v0.3 result directories.

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
preprocessing. The same memory-safe path completed the 900-row v0.3 full run
at Kaggle kernel version 32.

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
