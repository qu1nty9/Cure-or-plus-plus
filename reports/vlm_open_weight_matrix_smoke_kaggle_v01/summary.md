# Open-Weight VLM Matrix Smoke Run v0.1

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 9
- Device: Kaggle GPU, Tesla P100, CUDA
- Runtime pins: `torch==2.5.1+cu121`, `torchvision==0.20.1+cu121`,
  `transformers>=4.57,<5`, `qwen-vl-utils>=0.0.8,<0.1`
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Smoke rows: 5 total, 2 clean and 3 real-transfer

## Models

| slug | model | clean n | clean acc | real n | real acc | unparseable |
|---|---|---:|---:|---:|---:|---:|
| `smolvlm2_2b` | `HuggingFaceTB/SmolVLM2-2.2B-Instruct` | 2 | 0.5000 | 3 | 1.0000 | 0.0000 |
| `llava_onevision_qwen2_0_5b` | `llava-hf/llava-onevision-qwen2-0.5b-ov-hf` | 2 | 1.0000 | 3 | 1.0000 | 0.0000 |
| `internvl3_1b` | `OpenGVLab/InternVL3-1B-hf` | 2 | 0.5000 | 3 | 1.0000 | 0.0000 |
| `qwen2_5_vl_3b` | `Qwen/Qwen2.5-VL-3B-Instruct` | 2 | 0.5000 | 3 | 1.0000 | 0.0000 |

## Interpretation

This is a smoke gate, not a benchmark result. It validates model loading,
image-path handling, generation, response parsing, and evaluator compatibility
for all four tier-1 open-weight VLM candidates. Full 210-row runs should now be
launched one model at a time and reported separately.

## Artifacts

- `model_summary.csv`: split-level smoke summary.
- `recipe_table.csv`: per-real-transfer-recipe smoke summary.
- `label_table.csv`: label-level smoke summary.
- `run_manifest.csv`: successful Kaggle run directories.
- `kaggle_kernel_v9.log`: Kaggle execution log for the smoke pass.
