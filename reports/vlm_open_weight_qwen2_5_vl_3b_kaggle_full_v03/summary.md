# Qwen/Qwen2.5-VL-3B-Instruct Full v0.3 Run

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 31
- Device: Kaggle GPU
- Model: `Qwen/Qwen2.5-VL-3B-Instruct`
- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Run mode: full
- Rows: 900 total, 100 clean and 800 real-transfer
- Unparseable rate: clean=0.0900, real=0.2088
- Abstention rate: clean=0.0000, real=0.0000

## Result

| split | n | accuracy |
|---|---:|---:|
| clean | 100 | 0.8800 |
| real-transfer | 800 | 0.7650 |

Overall real-transfer drop vs clean: `0.1150`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `social_app_resave` | 200 | 0.8900 | -0.0100 |
| `messenger_upload_download` | 200 | 0.8650 | 0.0150 |
| `phone_screenshot_resave` | 200 | 0.6650 | 0.2150 |
| `video_call_frame_capture` | 200 | 0.6400 | 0.2400 |

## Failure Concentration

The model made 188 real-transfer errors and 12 clean errors.

| label | real n | real accuracy | drop vs clean |
|---|---:|---:|---:|
| `calcium_bottle` | 80 | 0.6500 | 0.2500 |
| `lg_cell_phone` | 80 | 0.6875 | 0.1125 |
| `training_marker_cone` | 80 | 0.7125 | 0.0875 |
| `canon_camera` | 80 | 0.7375 | 0.1625 |
| `hair_brush` | 80 | 0.7625 | 0.1375 |

The hardest transfer pipeline for this model is `video_call_frame_capture`, with 72 real-transfer errors and a 24.0 percentage-point drop relative to clean.

## Artifacts

- `responses.jsonl`: raw model responses.
- `audit.csv`: joined prompt/response correctness audit.
- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `combined_model_summary.csv`: combined Kaggle output summary.
- `combined_recipe_table.csv`: combined Kaggle output recipe table.
- `combined_label_table.csv`: combined Kaggle output label table.
- `run_manifest.csv`: successful Kaggle run directory.
- `kaggle_kernel.log`: Kaggle execution log, when available.
