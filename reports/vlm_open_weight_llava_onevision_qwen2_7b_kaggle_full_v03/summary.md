# LLaVA-OneVision-Qwen2-7B Full v0.3 Run

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 29
- Device: Kaggle GPU, Tesla P100, CUDA
- Model: `llava-hf/llava-onevision-qwen2-7b-ov-hf`
- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Run mode: full
- Rows: 900 total, 100 clean and 800 real-transfer
- Unparseable rate: 0.0000
- Abstention rate: 0.0000

## Result

| split | n | accuracy |
|---|---:|---:|
| clean | 100 | 0.9800 |
| real-transfer | 800 | 0.9775 |

Overall real-transfer drop vs clean: `0.0025`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `messenger_upload_download` | 200 | 0.9900 | -0.0100 |
| `phone_screenshot_resave` | 200 | 0.9850 | -0.0050 |
| `social_app_resave` | 200 | 0.9800 | 0.0000 |
| `video_call_frame_capture` | 200 | 0.9550 | 0.0250 |

## Failure Concentration

The model made 18 real-transfer errors and 2 clean errors. The real-transfer
failure mass is concentrated in:

| label | real n | real accuracy | drop vs clean |
|---|---:|---:|---:|
| `canon_camera` | 80 | 0.8875 | 0.0125 |
| `lg_cell_phone` | 80 | 0.9125 | -0.0125 |
| `calcium_bottle` | 80 | 0.9875 | 0.0125 |
| `training_marker_cone` | 80 | 0.9875 | 0.0125 |

The hardest transfer pipeline for this model is `video_call_frame_capture`,
with 9 real-transfer errors and a 2.5 percentage-point drop relative to clean.

## Interpretation

This is the second completed 900-row open-weight 7B VLM result on the v0.3
CURE-OR++ real-transfer protocol. Relative to Qwen2.5-VL-7B, LLaVA-OneVision
shows a smaller overall real-transfer drop and fewer real-transfer errors, while
preserving the same qualitative pattern: FaceTime video-call frame capture is
the hardest real-transfer pipeline.

## Artifacts

- `responses.jsonl`: 900 raw model responses.
- `audit.csv`: joined prompt/response correctness audit.
- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `combined_model_summary.csv`: combined Kaggle output summary.
- `combined_recipe_table.csv`: combined Kaggle output recipe table.
- `combined_label_table.csv`: combined Kaggle output label table.
- `run_manifest.csv`: successful Kaggle run directory.
- `kaggle_kernel.log`: Kaggle execution log for kernel version 29.
