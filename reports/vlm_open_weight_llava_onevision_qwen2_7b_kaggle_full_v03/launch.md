# LLaVA-OneVision-Qwen2-7B Full v0.3 Run Launch

## Launch

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 29
- Status at launch check: `RUNNING`
- Model: `llava-hf/llava-onevision-qwen2-7b-ov-hf`
- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Run mode: full
- Expected rows: 900 total, 100 clean and 800 real-transfer
- Dataset source: `yaroslavkholmirzayev/cure-or-pp-vlm-real-transfer-v03-private`
- Result cache location in Kaggle runtime: `/kaggle/temp/cure_or_pp_vlm_cache/full`

## Expected Artifacts

When complete, the Kaggle output should contain:

- `vlm_open_weight_runs/full/llava_onevision_qwen2_7b/responses.jsonl`
- `vlm_open_weight_runs/full/llava_onevision_qwen2_7b/model_summary.csv`
- `vlm_open_weight_runs/full/llava_onevision_qwen2_7b/recipe_table.csv`
- `vlm_open_weight_runs/full/llava_onevision_qwen2_7b/label_table.csv`
- `vlm_open_weight_runs/full/llava_onevision_qwen2_7b/audit.csv`
- `vlm_open_weight_runs/full/combined_model_summary.csv`
- `vlm_open_weight_runs/full/combined_recipe_table.csv`
- `vlm_open_weight_runs/full/combined_label_table.csv`
- `vlm_open_weight_runs/full/run_manifest.csv`

## Next Step

After Kaggle reports `COMPLETE`, download the output, copy the result artifacts
into this directory, replace this launch note with a result summary, and update
`configs/vlm_open_weight_model_matrix_v03.json` from
`v03_full_running_kaggle_v29` to a completed or failed status.
