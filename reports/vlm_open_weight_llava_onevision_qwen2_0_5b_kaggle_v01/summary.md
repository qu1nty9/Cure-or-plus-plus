# Open-Weight VLM Kaggle Run v0.6

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 20
- Kaggle session id: `329304109`
- Model: `llava-hf/llava-onevision-qwen2-0.5b-ov-hf`
- Backend: Hugging Face Transformers
- Model class: `LlavaOnevisionForConditionalGeneration`
- Device: Kaggle GPU, Tesla P100, CUDA
- Runtime pins: `torch==2.5.1+cu121`, `torchvision==0.20.1+cu121`, `transformers>=4.57,<5`
- Numeric dtype: `float16`
- Memory-safe settings: `device_map=auto`, `use_cache=false`, per-image resize to `max_side=768`
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean, 180 real-transfer

## Main Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.966667 | 0.000000 | 0.000000 |
| real-transfer | 180 | 0.933333 | 0.000000 | 0.000000 |

Accuracy drop vs clean: `0.033333`.

## Real-Transfer Recipes

| recipe | n | accuracy | 95% CI low | 95% CI high | drop vs clean |
|---|---:|---:|---:|---:|---:|
| messenger_upload_download | 60 | 0.966667 | 0.900000 | 1.000000 | 0.000000 |
| phone_screenshot_resave | 60 | 0.933333 | 0.833333 | 1.000000 | 0.033333 |
| video_call_frame_capture | 60 | 0.900000 | 0.800000 | 0.983333 | 0.066667 |

## Artifacts

- `responses.jsonl`: sanitized model responses.
- `model_summary.csv`: split-level summary.
- `recipe_table.csv`: real-transfer recipe table with source-matched bootstrap intervals.
- `label_table.csv`: label-level clean vs real-transfer table.
- `audit.csv`: per-sample parsed-response audit.
- `kaggle_kernel.log`: extracted Kaggle execution-log highlights for the completed run.

## Notes

This is the first completed LLaVA-OneVision row on the CURE-OR++ prompt pack.
The earlier full-run attempt on Kaggle P100 failed with CUDA OOM, and a direct
`anyres` patch-space reduction then failed inside Transformers with a
`split_with_sizes` mismatch. The successful path kept default OneVision image
handling and instead resized each input image to `max_side=768` before
preprocessing.

Scientifically, this row is strong: it reaches the best executed real-transfer
accuracy so far (`0.9333`, tied with SmolVLM2-2.2B and InternVL3-1B) while also
setting the best clean split among completed open-weight rows (`0.9667`).
Failure concentration is narrow rather than broad: `dymo_label_maker` is the
clear weak label, and `video_call_frame_capture` is the weakest transfer recipe.
