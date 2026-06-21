# Open-Weight VLM Kaggle Run v0.2

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 12
- Model: `OpenGVLab/InternVL3-1B-hf`
- Backend: Hugging Face Transformers
- Model class: `AutoModelForImageTextToText`
- Device: Kaggle GPU, Tesla P100, CUDA
- Runtime pins: `torch==2.5.1+cu121`, `torchvision==0.20.1+cu121`, `transformers>=4.57,<5`
- Numeric dtype: `float16`
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean, 180 real-transfer

## Main Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.933333 | 0.000000 | 0.000000 |
| real-transfer | 180 | 0.933333 | 0.000000 | 0.000000 |

Accuracy drop vs clean: `0.000000`.

## Real-Transfer Recipes

| recipe | n | accuracy | 95% CI low | 95% CI high | drop vs clean |
|---|---:|---:|---:|---:|---:|
| messenger_upload_download | 60 | 0.933333 | 0.833333 | 1.000000 | 0.000000 |
| phone_screenshot_resave | 60 | 0.933333 | 0.833333 | 1.000000 | 0.000000 |
| video_call_frame_capture | 60 | 0.933333 | 0.850000 | 1.000000 | 0.000000 |

## Artifacts

- `responses.jsonl`: sanitized model responses.
- `model_summary.csv`: split-level summary.
- `recipe_table.csv`: real-transfer recipe table with source-matched bootstrap intervals.
- `label_table.csv`: label-level clean vs real-transfer table.
- `audit.csv`: per-sample parsed-response audit.
- `kaggle_kernel.log`: Kaggle execution log.

## Notes

This is the first completed full 210-row non-SmolVLM open-weight VLM row in
the benchmark. It converts the VLM track from single-model infrastructure
validation into a model-family comparison: SmolVLM2-500M remains the weak
assistant-style baseline, while InternVL3-1B provides a much stronger
open-weight VLM row with no observed real-transfer drop on this prompt pack.
