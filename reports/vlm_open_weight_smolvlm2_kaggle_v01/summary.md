# Open-Weight VLM Kaggle Run v0.1

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 7
- Model: `HuggingFaceTB/SmolVLM2-500M-Video-Instruct`
- Backend: Hugging Face Transformers
- Device: Kaggle GPU, Tesla P100, CUDA
- Runtime pins: `torch==2.5.1+cu121`, `torchvision==0.20.1+cu121`, `transformers>=4.57,<5`
- Numeric dtype: `float16`
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean, 180 real-transfer

## Main Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.600000 | 0.000000 | 0.000000 |
| real-transfer | 180 | 0.555556 | 0.000000 | 0.000000 |

Accuracy drop vs clean: `0.044444`.

## Real-Transfer Recipes

| recipe | n | accuracy | 95% CI low | 95% CI high | drop vs clean |
|---|---:|---:|---:|---:|---:|
| messenger_upload_download | 60 | 0.633333 | 0.466667 | 0.800000 | -0.033333 |
| phone_screenshot_resave | 60 | 0.500000 | 0.333333 | 0.666667 | 0.100000 |
| video_call_frame_capture | 60 | 0.533333 | 0.366667 | 0.700000 | 0.066667 |

## Artifacts

- `responses.jsonl`: sanitized model responses.
- `model_summary.csv`: split-level summary.
- `recipe_table.csv`: real-transfer recipe table with source-matched bootstrap intervals.
- `label_table.csv`: label-level clean vs real-transfer table.
- `audit.csv`: per-sample parsed-response audit.
- `kaggle_kernel.log`: Kaggle execution log.

## Notes

The Kaggle default GPU resolved to Tesla P100. Current Kaggle PyTorch builds did
not support P100 `sm_60`, so the notebook pins a compatible CUDA 12.1 PyTorch
and matching torchvision wheel. The smoke run with five rows completed first;
the full 210-row run completed after that.
