# LLaVA-OneVision 7B Smoke Retry v0.1

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 25
- Device: Kaggle GPU, Tesla P100, CUDA
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 5 smoke rows, covering 2 clean examples and 3 real-transfer examples
- Model: `llava-hf/llava-onevision-qwen2-7b-ov-hf`

## Memory-Controlled Configuration

Kaggle kernel version 24 failed during the first smoke attempt with CUDA OOM on
P100. Version 25 passed after changing only inference memory controls:

- `device_map=auto`
- `model_kwargs.low_cpu_mem_usage=true`
- `generate_kwargs.use_cache=false`
- `image_max_side=384`
- `max_tokens=2`

The reduced token budget is acceptable for this prompt pack because the
expected answer is exactly one option letter.

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 2 | 1.0000 | 0.0000 | 0.0000 |
| real-transfer | 3 | 1.0000 | 0.0000 | 0.0000 |

Real-transfer recipe accuracy:

- `messenger_upload_download`: `1.0000`
- `phone_screenshot_resave`: `1.0000`
- `video_call_frame_capture`: `1.0000`

## Interpretation

The memory-controlled retry validates that the LLaVA-OneVision 7B row is
loadable and executable on Kaggle P100 for the CURE-OR++ prompt-pack path. This
is a smoke result only; it supports promotion to a 210-row full run, not a
headline benchmark claim.

## Artifacts

- `model_summary.csv`
- `recipe_table.csv`
- `label_table.csv`
- `audit.csv`
- `responses.jsonl`
- `run_manifest.csv`
- `kaggle_kernel.log`
