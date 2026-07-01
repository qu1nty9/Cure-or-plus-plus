# Qwen2.5-VL-7B Full v0.3 Run Launch

## Launch

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 28
- Status at launch check: `RUNNING`
- Model: `Qwen/Qwen2.5-VL-7B-Instruct`
- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Run mode: full
- Expected rows: 900 total, 100 clean and 800 real-transfer
- Dataset source: `yaroslavkholmirzayev/cure-or-pp-vlm-real-transfer-v03-private`

## Expected Artifacts

When complete, the Kaggle output should contain:

- `vlm_open_weight_runs/full/qwen2_5_vl_7b/responses.jsonl`
- `vlm_open_weight_runs/full/qwen2_5_vl_7b/model_summary.csv`
- `vlm_open_weight_runs/full/qwen2_5_vl_7b/recipe_table.csv`
- `vlm_open_weight_runs/full/qwen2_5_vl_7b/label_table.csv`
- `vlm_open_weight_runs/full/qwen2_5_vl_7b/audit.csv`
- `vlm_open_weight_runs/full/combined_model_summary.csv`
- `vlm_open_weight_runs/full/combined_recipe_table.csv`
- `vlm_open_weight_runs/full/combined_label_table.csv`
- `vlm_open_weight_runs/full/run_manifest.csv`

## Next Step

After Kaggle reports `COMPLETE`, download the output, copy the result artifacts
into this directory, replace this launch note with a result summary, and update
`configs/vlm_open_weight_model_matrix_v03.json` from
`v03_full_running_kaggle_v28` to a completed or failed status.
