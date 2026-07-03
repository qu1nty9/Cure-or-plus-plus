# HuggingFaceTB/SmolVLM2-2.2B-Instruct Full v0.3 Run

## Run

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 30
- Device: Kaggle GPU
- Model: `HuggingFaceTB/SmolVLM2-2.2B-Instruct`
- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Run mode: full
- Rows: 900 total, 100 clean and 800 real-transfer
- Unparseable rate: clean=0.0000, real=0.0000
- Abstention rate: clean=0.0000, real=0.0000

## Result

| split | n | accuracy |
|---|---:|---:|
| clean | 100 | 0.9600 |
| real-transfer | 800 | 0.9575 |

Overall real-transfer drop vs clean: `0.0025`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `phone_screenshot_resave` | 200 | 0.9650 | -0.0050 |
| `messenger_upload_download` | 200 | 0.9600 | 0.0000 |
| `video_call_frame_capture` | 200 | 0.9550 | 0.0050 |
| `social_app_resave` | 200 | 0.9500 | 0.0100 |

## Failure Concentration

The model made 34 real-transfer errors and 4 clean errors.

| label | real n | real accuracy | drop vs clean |
|---|---:|---:|---:|
| `lg_cell_phone` | 80 | 0.7500 | 0.0500 |
| `calcium_bottle` | 80 | 0.8500 | -0.0500 |
| `canon_camera` | 80 | 0.9750 | 0.0250 |

The hardest transfer pipeline for this model is `social_app_resave`, with 10 real-transfer errors and a 1.0 percentage-point drop relative to clean.

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
