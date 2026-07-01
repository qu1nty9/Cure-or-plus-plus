# LLaVA-OneVision Qwen2 7B Full Run v0.1

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 26
- Device: Kaggle GPU, Tesla P100, CUDA
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean and 180 real-transfer
- Model: `llava-hf/llava-onevision-qwen2-7b-ov-hf`

## Memory-Controlled Configuration

This full run reused the successful Kaggle version 25 smoke settings after the
version 24 smoke attempt hit CUDA OOM during generation on P100:

- `device_map=auto`
- `model_kwargs.low_cpu_mem_usage=true`
- `generate_kwargs.use_cache=false`
- `image_max_side=384`
- `max_tokens=2`

The reduced `max_tokens` is acceptable for this prompt pack because the
evaluator only needs a single option letter.

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.9667 | 0.0000 | 0.0000 |
| real-transfer | 180 | 0.9778 | 0.0000 | 0.0000 |

Accuracy drop vs clean: `-0.0111`.

Real-transfer recipe accuracy:

- `messenger_upload_download`: `1.0000`
- `phone_screenshot_resave`: `1.0000`
- `video_call_frame_capture`: `0.9333`

Label-level weakness is narrow:

- `canon_camera`: clean `0.6667`, real `0.8333`
- `calcium_bottle`: clean `1.0000`, real `0.9444`

All other labels are perfect on both clean and real-transfer.

## Interpretation

This is the strongest completed open-weight real-transfer row so far. Under the
memory-controlled P100 configuration, `llava-hf/llava-onevision-qwen2-7b-ov-hf`
reaches:

- clean `0.9667`
- real-transfer `0.9778`
- zero unparseable responses

The negative drop should not be interpreted as evidence that transfer improves
the model; it is a small-sample effect from the 30-source clean split and the
180 transferred outputs. The main takeaway is that the large LLaVA-OneVision
row completes on Kaggle P100, stays fully parseable, and raises the
open-weight real-transfer headline result.

## Artifacts

- `model_summary.csv`
- `recipe_table.csv`
- `label_table.csv`
- `audit.csv`
- `responses.jsonl`
- `run_manifest.csv`
- `kaggle_kernel.log`
