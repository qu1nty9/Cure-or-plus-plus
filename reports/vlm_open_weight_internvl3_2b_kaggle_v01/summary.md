# Open-Weight VLM Kaggle Run v0.5

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 16
- Model: `OpenGVLab/InternVL3-2B-hf`
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
| real-transfer | 180 | 0.927778 | 0.000000 | 0.000000 |

Accuracy drop vs clean: `0.005556`.

## Real-Transfer Recipes

| recipe | n | accuracy | 95% CI low | 95% CI high | drop vs clean |
|---|---:|---:|---:|---:|---:|
| messenger_upload_download | 60 | 0.966667 | 0.900000 | 1.000000 | -0.033333 |
| phone_screenshot_resave | 60 | 0.900000 | 0.800000 | 1.000000 | 0.033333 |
| video_call_frame_capture | 60 | 0.916667 | 0.816667 | 1.000000 | 0.016667 |

## Artifacts

- `responses.jsonl`: sanitized model responses.
- `model_summary.csv`: split-level summary.
- `recipe_table.csv`: real-transfer recipe table with source-matched bootstrap intervals.
- `label_table.csv`: label-level clean vs real-transfer table.
- `audit.csv`: per-sample parsed-response audit.
- `kaggle_kernel.log`: Kaggle execution log.

## Notes

This row extends the InternVL family comparison from 1B to 2B. The 2B model
stays fully parseable and remains a strong open-weight row, but unlike
InternVL3-1B it shows a small real-transfer drop and slightly weaker
`lg_cell_phone` and `calcium_bottle` label rows. On the current prompt pack,
InternVL family scaling is therefore strong but not monotonic.
