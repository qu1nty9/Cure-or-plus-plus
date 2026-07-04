# internvl3_2b Full v0.3 Run Launch

## Launch

- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`
- Kaggle kernel version: 34
- Status at launch check: `RUNNING`
- Model: `OpenGVLab/InternVL3-2B-hf`
- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Run mode: full
- Expected rows: 900 total, 100 clean and 800 real-transfer
- Dataset source: `yaroslavkholmirzayev/cure-or-pp-vlm-real-transfer-v03-private`
- Result cache location in Kaggle runtime: `/kaggle/temp/cure_or_pp_vlm_cache/full`

## Expected Artifacts

When complete, the Kaggle output should contain:

- `vlm_open_weight_runs/full/internvl3_2b/responses.jsonl`
- `vlm_open_weight_runs/full/internvl3_2b/model_summary.csv`
- `vlm_open_weight_runs/full/internvl3_2b/recipe_table.csv`
- `vlm_open_weight_runs/full/internvl3_2b/label_table.csv`
- `vlm_open_weight_runs/full/internvl3_2b/audit.csv`
- `vlm_open_weight_runs/full/combined_model_summary.csv`
- `vlm_open_weight_runs/full/combined_recipe_table.csv`
- `vlm_open_weight_runs/full/combined_label_table.csv`
- `vlm_open_weight_runs/full/run_manifest.csv`

## Integration Command

After Kaggle reports `COMPLETE`, download the output and run:

```bash
.venv/bin/python scripts/integrate_kaggle_vlm_output.py \
  --download-dir /private/tmp/cure_or_v03_output \
  --slug internvl3_2b \
  --result-dir reports/vlm_open_weight_internvl3_2b_kaggle_full_v03 \
  --kernel-version 34 \
  --update-matrix

.venv/bin/python scripts/build_vlm_open_weight_full_comparison.py
.venv/bin/python scripts/run_release_checks.py
```
