# Qwen2.5-VL-7B Smoke Run v0.1

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 22
- Device: Kaggle GPU, Tesla P100, CUDA
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Run mode: smoke, 5 rows total
- Model: `Qwen/Qwen2.5-VL-7B-Instruct`

## Memory-Controlled Retry

The first Kaggle smoke attempt at version 21 still failed with CUDA OOM on P100
using `min_pixels=200704` and `max_pixels=802816`.

The successful version 22 retry used:

- `processor_kwargs.min_pixels=50176`
- `processor_kwargs.max_pixels=262144`
- `image_max_side=512`
- `generate_kwargs.use_cache=false`
- `model_kwargs.low_cpu_mem_usage=true`

## Result

| split | n | accuracy | unparseable |
|---|---:|---:|---:|
| clean | 2 | 1.0000 | 0.0000 |
| real-transfer | 3 | 1.0000 | 0.0000 |

Recipe-level smoke accuracy:

- `messenger_upload_download`: `1.0000`
- `phone_screenshot_resave`: `1.0000`
- `video_call_frame_capture`: `1.0000`

## Interpretation

This run clears the engineering question of whether `Qwen2.5-VL-7B-Instruct`
can be made to execute on Kaggle P100 at all. The answer is yes, but only after
aggressive visual-token and image-size reduction relative to the failed version
21 smoke configuration.

The next step is a full 210-row run with the same memory-controlled settings to
measure whether the model remains strong under the complete CURE-OR++ protocol.

## Artifacts

- `model_summary.csv`
- `recipe_table.csv`
- `label_table.csv`
- `audit.csv`
- `responses.jsonl`
- `kaggle_kernel.log`
