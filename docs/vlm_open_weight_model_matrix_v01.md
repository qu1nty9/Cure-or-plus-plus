# Open-Weight VLM Model Matrix v0.1

This matrix turns the VLM/API track from a single SmolVLM2 result into a
repeatable open-weight benchmark block.

## Policy

Run the matrix in two passes:

1. Smoke mode: 5 fixed prompt-pack rows per enabled model, covering clean plus
   messenger, screenshot, and video-call real-transfer examples.
2. Full mode: 210 rows only for models that pass smoke without load/generation
   failures.

The completed baseline remains
`HuggingFaceTB/SmolVLM2-500M-Video-Instruct`. The next default smoke queue is:

| slug | model | tier | reason |
| --- | --- | --- | --- |
| `smolvlm2_2b` | `HuggingFaceTB/SmolVLM2-2.2B-Instruct` | tier_1_next | Same family as completed baseline, stronger size. |
| `llava_onevision_qwen2_0_5b` | `llava-hf/llava-onevision-qwen2-0.5b-ov-hf` | tier_1_next | Small LLaVA-OneVision family contrast. |
| `internvl3_1b` | `OpenGVLab/InternVL3-1B-hf` | tier_1_next | Compact InternVL-family contrast. |
| `qwen2_5_vl_3b` | `Qwen/Qwen2.5-VL-3B-Instruct` | tier_1_next | Strong 3B VLM candidate. |

Stretch rows are present but disabled by default:

| slug | model | reason |
| --- | --- | --- |
| `internvl3_2b` | `OpenGVLab/InternVL3-2B-hf` | Run after the 1B row succeeds. |
| `qwen2_5_vl_7b` | `Qwen/Qwen2.5-VL-7B-Instruct` | Strong row, but memory-sensitive on Kaggle P100. |
| `llava_onevision_qwen2_7b` | `llava-hf/llava-onevision-qwen2-7b-ov-hf` | Strong LLaVA row, but memory-sensitive on Kaggle P100. |

## Source Checks

The model IDs and high-level loading classes were checked against Hugging Face
model cards:

- `HuggingFaceTB/SmolVLM2-2.2B-Instruct`:
  <https://huggingface.co/HuggingFaceTB/SmolVLM2-2.2B-Instruct>
- `llava-hf/llava-onevision-qwen2-0.5b-ov-hf`:
  <https://huggingface.co/llava-hf/llava-onevision-qwen2-0.5b-ov-hf>
- `OpenGVLab/InternVL3-1B-hf`:
  <https://huggingface.co/OpenGVLab/InternVL3-1B-hf>
- `Qwen/Qwen2.5-VL-3B-Instruct`:
  <https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct>
- `Qwen/Qwen2.5-VL-7B-Instruct`:
  <https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct>

## Kaggle Usage

Generate the notebook and metadata:

```bash
.venv/bin/python scripts/write_kaggle_vlm_notebook.py
```

Push the notebook after the private VLM dataset is attached:

```bash
kaggle kernels push -p kaggle/vlm_kernel
```

Notebook defaults to smoke mode. For full runs, edit the first configuration
cell:

```python
RUN_MODE = "full"
SELECTED_MODEL_SLUGS = ["smolvlm2_2b"]
```

Do not run all stretch candidates in one Kaggle session. The full 210-row pass
should be model-by-model so failed large models do not invalidate successful
smaller rows.

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
