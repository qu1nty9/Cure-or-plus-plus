# Open-Weight VLM Kaggle Run v0.4

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 14
- Model: `HuggingFaceTB/SmolVLM2-2.2B-Instruct`
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
| phone_screenshot_resave | 60 | 0.916667 | 0.816667 | 1.000000 | 0.016667 |
| video_call_frame_capture | 60 | 0.950000 | 0.883333 | 1.000000 | -0.016667 |

## Artifacts

- `responses.jsonl`: sanitized model responses.
- `model_summary.csv`: split-level summary.
- `recipe_table.csv`: real-transfer recipe table with source-matched bootstrap intervals.
- `label_table.csv`: label-level clean vs real-transfer table.
- `audit.csv`: per-sample parsed-response audit.
- `kaggle_kernel.log`: Kaggle execution log.

## Notes

This row changes the interpretation of the open-weight VLM block. Scaling the
SmolVLM family from 500M to 2.2B removes the observed real-transfer drop on
the current prompt pack, reaching 0.9333 on both clean-source and
real-transfer splits with no unparseable responses. On this benchmark slice,
SmolVLM2-2.2B matches the strong InternVL3-1B row and shows that the
real-transfer guardrail is not uniformly difficult for modern open-weight VLMs.
