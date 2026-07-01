# Qwen2.5-VL-7B Full Run v0.1

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 23
- Device: Kaggle GPU, Tesla P100, CUDA
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean and 180 real-transfer
- Model: `Qwen/Qwen2.5-VL-7B-Instruct`

## Memory-Controlled Configuration

This full run reused the successful Kaggle version 22 smoke settings:

- `processor_kwargs.min_pixels=50176`
- `processor_kwargs.max_pixels=262144`
- `image_max_side=512`
- `generate_kwargs.use_cache=false`
- `model_kwargs.low_cpu_mem_usage=true`

These settings were introduced because the earlier Kaggle version 21 smoke
attempt hit CUDA OOM on P100 with a larger visual-token budget.

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.9667 | 0.0000 | 0.0000 |
| real-transfer | 180 | 0.9333 | 0.0000 | 0.0000 |

Real-transfer recipe accuracy:

- `messenger_upload_download`: `0.9333`
- `phone_screenshot_resave`: `0.9333`
- `video_call_frame_capture`: `0.9333`

Label-level weakness is narrow:

- `calcium_bottle`: clean `0.6667`, real `0.6667`
- `canon_camera`: clean `1.0000`, real `0.6667`, drop `0.3333`

All other labels are perfect on both clean and real-transfer.

## Interpretation

This is a strong result. Under the reduced visual-token configuration needed to
fit Kaggle P100 memory, `Qwen2.5-VL-7B-Instruct` reaches the same headline
split-level performance as the strongest completed open-weight rows:

- clean `0.9667`
- real-transfer `0.9333`
- zero unparseable responses

That ties the completed `LLaVA-OneVision 0.5B` row on the current prompt pack
while remaining fully parseable across all 210 examples.

## Artifacts

- `model_summary.csv`
- `recipe_table.csv`
- `label_table.csv`
- `audit.csv`
- `responses.jsonl`
- `run_manifest.csv`
- `kaggle_kernel.log`
