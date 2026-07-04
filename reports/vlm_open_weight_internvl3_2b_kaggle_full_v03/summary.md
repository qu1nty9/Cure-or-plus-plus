# OpenGVLab/InternVL3-2B-hf Full v0.3 Run

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 34
- Device: Kaggle GPU
- Model: `OpenGVLab/InternVL3-2B-hf`
- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Run mode: full
- Rows: 900 total, 100 clean and 800 real-transfer
- Unparseable rate: clean=0.0000, real=0.0000
- Abstention rate: clean=0.0000, real=0.0000

## Result

| split | n | accuracy |
|---|---:|---:|
| clean | 100 | 0.9700 |
| real-transfer | 800 | 0.9600 |

Overall real-transfer drop vs clean: `0.0100`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `messenger_upload_download` | 200 | 0.9800 | -0.0100 |
| `social_app_resave` | 200 | 0.9700 | 0.0000 |
| `phone_screenshot_resave` | 200 | 0.9550 | 0.0150 |
| `video_call_frame_capture` | 200 | 0.9350 | 0.0350 |

## Failure Concentration

The model made 32 real-transfer errors and 3 clean errors.

| label | real n | real accuracy | drop vs clean |
|---|---:|---:|---:|
| `lg_cell_phone` | 80 | 0.7625 | 0.0375 |
| `calcium_bottle` | 80 | 0.8625 | 0.0375 |
| `canon_camera` | 80 | 0.9750 | 0.0250 |

The hardest transfer pipeline for this model is `video_call_frame_capture`, with 13 real-transfer errors and a 3.5 percentage-point drop relative to clean.

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
