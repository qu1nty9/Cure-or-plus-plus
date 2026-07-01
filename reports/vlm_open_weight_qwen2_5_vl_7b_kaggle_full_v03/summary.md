# Qwen2.5-VL-7B Full v0.3 Run

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 28
- Device: Kaggle GPU, Tesla P100, CUDA
- Model: `Qwen/Qwen2.5-VL-7B-Instruct`
- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Run mode: full
- Rows: 900 total, 100 clean and 800 real-transfer
- Unparseable rate: 0.0000
- Abstention rate: 0.0000

## Result

| split | n | accuracy |
|---|---:|---:|
| clean | 100 | 0.9800 |
| real-transfer | 800 | 0.9613 |

Overall real-transfer drop vs clean: `0.0188`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `social_app_resave` | 200 | 0.9800 | 0.0000 |
| `messenger_upload_download` | 200 | 0.9700 | 0.0100 |
| `phone_screenshot_resave` | 200 | 0.9650 | 0.0150 |
| `video_call_frame_capture` | 200 | 0.9300 | 0.0500 |

## Failure Concentration

The model made 31 real-transfer errors and 2 clean errors. The real-transfer
failure mass is concentrated in:

| label | real n | real accuracy | drop vs clean |
|---|---:|---:|---:|
| `canon_camera` | 80 | 0.8625 | 0.1375 |
| `calcium_bottle` | 80 | 0.8750 | 0.0250 |
| `training_marker_cone` | 80 | 0.9000 | 0.0000 |
| `lg_cell_phone` | 80 | 0.9750 | 0.0250 |

The hardest transfer pipeline for this model is `video_call_frame_capture`,
with 14 real-transfer errors and a 5.0 percentage-point drop relative to clean.

## Interpretation

This is the first completed 900-row open-weight VLM result on the v0.3
CURE-OR++ real-transfer protocol. It confirms that a strong 7B VLM remains
highly robust overall, but still shows a measurable degradation under real
capture and communication transforms, especially FaceTime video-call frame
capture.

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
- `kaggle_kernel.log`: Kaggle execution log for kernel version 28.
