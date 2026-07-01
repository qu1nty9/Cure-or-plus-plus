# Open-Weight VLM Model Matrix v0.1

This matrix turns the VLM/API track from a single SmolVLM2 result into a
repeatable open-weight benchmark block.

## Policy

Run the matrix in two passes:

1. Smoke mode: 5 fixed prompt-pack rows per enabled model, covering clean plus
   messenger, screenshot, and video-call real-transfer examples.
2. Full mode: 210 rows only for models that pass smoke without load/generation
   failures.

Completed full rows:

| slug | model | result dir | clean | real-transfer | note |
| --- | --- | --- | ---: | ---: | --- |
| `smolvlm2_500m` | `HuggingFaceTB/SmolVLM2-500M-Video-Instruct` | `reports/vlm_open_weight_smolvlm2_kaggle_v01/` | 0.6000 | 0.5556 | Initial weak open-weight baseline. |
| `smolvlm2_2b` | `HuggingFaceTB/SmolVLM2-2.2B-Instruct` | `reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/` | 0.9333 | 0.9333 | Same-family scale-up that removes the observed real-transfer drop. |
| `internvl3_1b` | `OpenGVLab/InternVL3-1B-hf` | `reports/vlm_open_weight_internvl3_1b_kaggle_v01/` | 0.9333 | 0.9333 | First completed non-SmolVLM family-contrast row. |
| `internvl3_2b` | `OpenGVLab/InternVL3-2B-hf` | `reports/vlm_open_weight_internvl3_2b_kaggle_v01/` | 0.9333 | 0.9278 | Strong InternVL follow-up with a small real-transfer drop versus the 1B row. |
| `llava_onevision_qwen2_0_5b` | `llava-hf/llava-onevision-qwen2-0.5b-ov-hf` | `reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/` | 0.9667 | 0.9333 | First completed LLaVA-OneVision row; tied-best clean split among completed open-weight runs. |
| `qwen2_5_vl_3b` | `Qwen/Qwen2.5-VL-3B-Instruct` | `reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/` | 0.9000 | 0.6389 | Strong clean row with high real-transfer unparseable rate. |
| `qwen2_5_vl_7b` | `Qwen/Qwen2.5-VL-7B-Instruct` | `reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/` | 0.9667 | 0.9333 | Memory-controlled Kaggle P100 completion with zero unparseables; ties the strongest completed headline split metrics. |
| `llava_onevision_qwen2_7b` | `llava-hf/llava-onevision-qwen2-7b-ov-hf` | `reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/` | 0.9667 | 0.9778 | Memory-controlled large LLaVA-OneVision row; strongest completed real-transfer split so far. |

The open-weight queue is now clear for the current matrix. Further work should
use the same prompt-pack/evaluator path for selected frontier/provider VLM rows
or for repeatability reruns of completed open-weight rows.

No completed model is enabled by default in the checked-in smoke notebook.

## Source Checks

The model IDs and high-level loading classes were checked against Hugging Face
model cards:

- `HuggingFaceTB/SmolVLM2-2.2B-Instruct`:
  <https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct>
- `llava-hf/llava-onevision-qwen2-0.5b-ov-hf`:
  <https://huggingface.co/llava-hf/llava-onevision-qwen2-0.5b-ov-hf>
- `OpenGVLab/InternVL3-1B-hf`:
  <https://huggingface.co/OpenGVLab/InternVL3-1B-hf>
- `OpenGVLab/InternVL3-2B-hf`:
  <https://huggingface.co/OpenGVLab/InternVL3-2B-hf>
- `Qwen/Qwen2.5-VL-3B-Instruct`:
  <https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct>
- `Qwen/Qwen2.5-VL-7B-Instruct`:
  <https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct>
- `llava-hf/llava-onevision-qwen2-7b-ov-hf`:
  <https://huggingface.co/llava-hf/llava-onevision-qwen2-7b-ov-hf>

## Kaggle Usage

Generate the notebook and metadata:

```bash
.venv/bin/python scripts/write_kaggle_vlm_notebook.py
```

Push the notebook after the private VLM dataset is attached:

```bash
kaggle kernels push -p kaggle/vlm_kernel
```

Notebook defaults to smoke mode. For full model-by-model runs, generate a
temporary full notebook:

```bash
.venv/bin/python scripts/write_kaggle_vlm_notebook.py \
  --run-mode full \
  --selected-model-slug llava_onevision_qwen2_7b
```

Do not run all stretch candidates in one Kaggle session. The full 210-row pass
should be model-by-model so failed large models do not invalidate successful
smaller rows.

After pushing a full-run notebook, regenerate the default smoke notebook before
committing:

```bash
.venv/bin/python scripts/write_kaggle_vlm_notebook.py
```

## Version 12 Full Result

Kaggle kernel version 12 completed the first non-SmolVLM full row:

- model: `OpenGVLab/InternVL3-1B-hf`
- rows: 210 total, 30 clean and 180 real-transfer
- clean accuracy: 0.9333
- real-transfer accuracy: 0.9333
- unparseable rate: 0.0000

The tracked full result is in
`reports/vlm_open_weight_internvl3_1b_kaggle_v01/summary.md`.

## Version 13 Full Result

Kaggle kernel version 13 completed the Qwen 3B full row:

- model: `Qwen/Qwen2.5-VL-3B-Instruct`
- rows: 210 total, 30 clean and 180 real-transfer
- clean accuracy: 0.9000
- real-transfer accuracy: 0.6389
- real-transfer unparseable rate: 0.3278

The tracked full result is in
`reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/summary.md`. The high
unparseable rate is caused by literal `!!!!!!!!` generations on many
real-transfer images, so this row is evidence of generation instability under
transfer rather than a parser failure.

## Version 14 Full Result

Kaggle kernel version 14 completed the SmolVLM2 2.2B full row:

- model: `HuggingFaceTB/SmolVLM2-2.2B-Instruct`
- rows: 210 total, 30 clean and 180 real-transfer
- clean accuracy: 0.9333
- real-transfer accuracy: 0.9333
- unparseable rate: 0.0000

The tracked full result is in
`reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/summary.md`. This is the
strongest same-family scaling result so far: compared with SmolVLM2-500M,
moving to 2.2B removes the observed real-transfer drop on the current prompt
pack and ties the strongest executed open-weight row.

## Version 16 Full Result

Kaggle kernel version 16 completed the InternVL3 2B full row:

- model: `OpenGVLab/InternVL3-2B-hf`
- rows: 210 total, 30 clean and 180 real-transfer
- clean accuracy: 0.9333
- real-transfer accuracy: 0.9278
- unparseable rate: 0.0000

The tracked full result is in
`reports/vlm_open_weight_internvl3_2b_kaggle_v01/summary.md`. This extends the
InternVL family comparison beyond the strong 1B row. The 2B variant remains
fully parseable and very strong, but it does not improve monotonically on the
current prompt pack: messenger upload/download rises to 0.9667, while phone
screenshot/resave and video-call frame capture land at 0.9000 and 0.9167.

## Version 20 Full Result

Kaggle kernel version 20 completed the LLaVA-OneVision 0.5B full row:

- model: `llava-hf/llava-onevision-qwen2-0.5b-ov-hf`
- rows: 210 total, 30 clean and 180 real-transfer
- clean accuracy: 0.9667
- real-transfer accuracy: 0.9333
- unparseable rate: 0.0000

The tracked full result is in
`reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/summary.md`.
This is the first completed LLaVA-OneVision row and one of the strongest
completed open-weight rows. The successful retry kept the default OneVision
image handling and instead resized each input image to `max_side=768` before
preprocessing; messenger upload/download stayed at 0.9667, phone
screenshot/resave landed at 0.9333, and video-call frame capture was the
weakest recipe at 0.9000.

## Version 23 Full Result

Kaggle kernel version 23 completed the Qwen2.5-VL-7B full row:

- model: `Qwen/Qwen2.5-VL-7B-Instruct`
- rows: 210 total, 30 clean and 180 real-transfer
- clean accuracy: 0.9667
- real-transfer accuracy: 0.9333
- unparseable rate: 0.0000

The tracked full result is in
`reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/summary.md`. This full run
reused the successful version 22 smoke settings after the version 21 CUDA OOM:
`min_pixels=50176`, `max_pixels=262144`, `image_max_side=512`,
`use_cache=false`, and `low_cpu_mem_usage=true`. Under those memory controls,
Qwen2.5-VL-7B ties the strongest completed open-weight headline result with
0.9667 clean accuracy, 0.9333 real-transfer accuracy, and zero unparseables.

## Version 25 Smoke Result

Kaggle kernel version 25 passed the memory-controlled smoke retry for
`llava-hf/llava-onevision-qwen2-7b-ov-hf` after the version 24 smoke attempt
hit CUDA OOM during generation on the Tesla P100. The retry keeps the same
prompt-pack rows and answer parser, but changes only inference memory controls:

- `device_map=auto`
- `model_kwargs.low_cpu_mem_usage=true`
- `generate_kwargs.use_cache=false`
- `image_max_side=384`
- `max_tokens=2`

The reduced `max_tokens` is acceptable for this prompt pack because evaluation
expects a single option letter. The tracked smoke result is in
`reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_smoke_v01/summary.md`:
2/2 clean rows and 3/3 real-transfer rows were correct, with zero unparseables.

## Version 26 Full Run

Kaggle kernel version 26 completed the LLaVA-OneVision Qwen2 7B full row:

- model: `llava-hf/llava-onevision-qwen2-7b-ov-hf`
- rows: 210 total, 30 clean and 180 real-transfer
- clean accuracy: 0.9667
- real-transfer accuracy: 0.9778
- unparseable rate: 0.0000

The tracked full result is in
`reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/summary.md`. This
full run reused the successful version 25 smoke settings after the version 24
CUDA OOM: `device_map=auto`, `low_cpu_mem_usage=true`, `use_cache=false`,
input resize to `max_side=384`, and `max_tokens=2`. It is the strongest
completed open-weight real-transfer row so far, with messenger upload/download
and phone screenshot/resave both at 1.0000 and video-call frame capture at
0.9333.

## Version 24 Smoke Notes

Kaggle kernel version 24 attempted the first smoke run for
`llava-hf/llava-onevision-qwen2-7b-ov-hf`, but failed with CUDA OOM during
generation. The log showed the model using almost all 16 GB of P100 memory and
failing to allocate an additional 74 MB inside the Qwen2 language-model
attention path. No full run should be attempted for this row until a smoke run
passes under memory controls.

## Version 19 Full Notes

Kaggle kernel version 19 attempted a direct `anyres` memory-reduction retry for
`llava-hf/llava-onevision-qwen2-0.5b-ov-hf`, but failed inside Transformers
with a `split_with_sizes` mismatch during image-feature processing. This showed
that shrinking OneVision patch-space through processor overrides was not a safe
path on the current runtime; the successful version 20 run used input resizing
instead.

## Version 11 Full Notes

Kaggle kernel version 11 attempted a full run for
`llava-hf/llava-onevision-qwen2-0.5b-ov-hf`, but failed with CUDA OOM on the
Tesla P100 during generation. The smoke result remains valid, but the model
should not be promoted to full mode again without memory-specific tuning. That
issue is now resolved by the version 20 input-resize retry path.

## Version 9 Smoke Result

Kaggle kernel version 9 passed the tier-1 smoke gate for all four enabled
models:

- `smolvlm2_2b`
- `llava_onevision_qwen2_0_5b`
- `internvl3_1b`
- `qwen2_5_vl_3b`

The tracked smoke summary is in
`reports/vlm_open_weight_matrix_smoke_kaggle_v01/summary.md`. This validates
the runner path only; it is not a full benchmark result.

## Version 8 Smoke Notes

Kaggle kernel version 8 validated the matrix runner path and produced a
successful smoke artifact for `smolvlm2_2b`, but exposed three infrastructure
issues:

- the smoke sample was clean-only because it used the first 5 prompt-pack rows;
- `AutoModelForMultimodalLM` was not available in the Kaggle Transformers
  runtime;
- InternVL rejected `file://` image URLs and needs local path strings.

The current matrix fixes these by using fixed mixed smoke sample IDs, concrete
model classes for LLaVA/Qwen, `qwen-vl-utils` for Qwen, and path-string image
references for InternVL/LLaVA.
