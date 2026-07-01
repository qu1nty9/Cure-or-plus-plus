# Open-Weight VLM Matrix Smoke Run v0.3

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 27
- Device: Kaggle GPU, Tesla P100, CUDA
- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Prompt pack size: 900 rows, 100 clean and 800 real-transfer
- Run mode: smoke, 6 rows per model
- Smoke split: 2 clean rows and 4 real-transfer rows per model

## Models

| slug | model | clean n | clean acc | real n | real acc | unparseable |
|---|---|---:|---:|---:|---:|---:|
| `qwen2_5_vl_7b` | `Qwen/Qwen2.5-VL-7B-Instruct` | 2 | 1.0000 | 4 | 1.0000 | 0.0000 |
| `llava_onevision_qwen2_7b` | `llava-hf/llava-onevision-qwen2-7b-ov-hf` | 2 | 1.0000 | 4 | 1.0000 | 0.0000 |

## Interpretation

This is an engineering smoke gate, not a benchmark result. It confirms that the
private CURE-OR++ v0.3 Kaggle dataset, runtime unpacking, image-path mapping,
Hugging Face model loading, VLM generation, response parsing, and evaluator all
work end-to-end on Kaggle GPU for the two 7B priority open-weight VLMs.

The result clears the next step: full 900-row v0.3 runs should be launched one
model at a time, starting with `qwen2_5_vl_7b` and
`llava_onevision_qwen2_7b`, then extending to the smaller open-weight family
contrast models.

## Artifacts

- `combined_model_summary.csv`: split-level smoke summary for both models.
- `combined_recipe_table.csv`: per-real-transfer-recipe smoke summary.
- `combined_label_table.csv`: label-level smoke summary.
- `run_manifest.csv`: successful Kaggle run directories.
- `qwen2_5_vl_7b/`: per-model responses, audit, and summary tables.
- `llava_onevision_qwen2_7b/`: per-model responses, audit, and summary tables.
- `kaggle_kernel.log`: Kaggle execution log for kernel version 27.
