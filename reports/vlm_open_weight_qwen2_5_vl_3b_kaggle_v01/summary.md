# Open-Weight VLM Kaggle Run v0.3

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 13
- Model: `Qwen/Qwen2.5-VL-3B-Instruct`
- Backend: Hugging Face Transformers with `qwen-vl-utils`
- Model class: `Qwen2_5_VLForConditionalGeneration`
- Device: Kaggle GPU, Tesla P100, CUDA
- Runtime pins: `torch==2.5.1+cu121`, `torchvision==0.20.1+cu121`, `transformers>=4.57,<5`
- Numeric dtype: `float16`
- Processor bounds: `min_pixels=200704`, `max_pixels=1003520`
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean, 180 real-transfer

## Main Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.900000 | 0.033333 | 0.000000 |
| real-transfer | 180 | 0.638889 | 0.327778 | 0.000000 |

Accuracy drop vs clean: `0.261111`.

## Real-Transfer Recipes

| recipe | n | accuracy | 95% CI low | 95% CI high | unparseable | drop vs clean |
|---|---:|---:|---:|---:|---:|---:|
| messenger_upload_download | 60 | 0.716667 | 0.550000 | 0.866667 | 0.250000 | 0.183333 |
| phone_screenshot_resave | 60 | 0.566667 | 0.416667 | 0.716667 | 0.383333 | 0.333333 |
| video_call_frame_capture | 60 | 0.633333 | 0.483333 | 0.766667 | 0.350000 | 0.266667 |

## Artifacts

- `responses.jsonl`: sanitized model responses.
- `model_summary.csv`: split-level summary.
- `recipe_table.csv`: real-transfer recipe table with source-matched bootstrap intervals.
- `label_table.csv`: label-level clean vs real-transfer table.
- `audit.csv`: per-sample parsed-response audit.
- `kaggle_kernel.log`: Kaggle execution log.

## Notes

This row is scientifically useful but not a simple leaderboard win. Qwen2.5-VL
3B has strong clean-source accuracy, but many real-transfer images trigger the
literal response `!!!!!!!!`, which is recorded as unparseable rather than
silently coerced into an answer. This exposes a generation-stability failure
under transfer pipelines, especially phone screenshot/resave and video-call
frame capture.
