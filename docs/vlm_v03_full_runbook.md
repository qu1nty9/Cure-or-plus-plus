# VLM v0.3 Full-Run Runbook

This runbook covers the 900-row CURE-OR++ open-weight VLM v0.3 track.

## Scope

- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Rows per full run: 900 total
- Clean rows: 100
- Real-transfer rows: 800
- Pipelines: WhatsApp transfer, phone screenshot/resave, Instagram resave, FaceTime frame capture
- Kaggle dataset: `yaroslavkholmirzayev/cure-or-pp-vlm-real-transfer-v03-private`
- Kaggle kernel: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`

## Current State

Completed full v0.3 rows:

- `qwen2_5_vl_7b`: `reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/`
- `llava_onevision_qwen2_7b`: `reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/`
- `smolvlm2_2b`: `reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/`
- `internvl3_1b`: `reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/`
- `internvl3_2b`: `reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/`
- `llava_onevision_qwen2_0_5b`: `reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/`
- `qwen2_5_vl_3b`: `reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/`

Generated comparison:

- `reports/vlm_open_weight_full_v03_comparison.md`
- `reports/vlm_open_weight_full_v03_comparison.csv`

## Prepare A Full Run

Use one model per Kaggle kernel version.

```bash
.venv/bin/python scripts/prepare_kaggle_vlm_full_run.py \
  --slug smolvlm2_2b
```

After the Kaggle push reports a kernel version, rerun the prepare command with
that version so the matrix and launch note are exact:

```bash
.venv/bin/python scripts/prepare_kaggle_vlm_full_run.py \
  --slug smolvlm2_2b \
  --kernel-version 30 \
  --status-at-launch RUNNING
```

Then push the generated notebook:

```bash
.venv/bin/kaggle kernels push -p kaggle/vlm_kernel_v03 --accelerator gpu
```

## Integrate A Completed Run

Download Kaggle output to a temporary local directory:

```bash
.venv/bin/kaggle kernels output \
  yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot \
  -p /private/tmp/cure_or_v03_output
```

Integrate and validate:

```bash
.venv/bin/python scripts/integrate_kaggle_vlm_output.py \
  --download-dir /private/tmp/cure_or_v03_output \
  --slug smolvlm2_2b \
  --result-dir reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03 \
  --kernel-version 30 \
  --update-matrix

.venv/bin/python scripts/build_vlm_open_weight_full_comparison.py
.venv/bin/python scripts/run_release_checks.py
```

The integration script must see 900 responses, 100 clean rows, 800
real-transfer rows, four pipeline rows, and ten label rows.

## Next Model Order

After `internvl3_2b`, there is no remaining scheduled open-weight full v0.3
model in the current matrix.

Useful next extensions:

1. frontier/provider VLM rows with separate response-audit handling.
2. repeatability reruns for the strongest open-weight rows if final-release confidence requires them.

Keep frontier/provider API models in a separate block. They should not be mixed
into the open-weight Kaggle leaderboard because model versioning, API policy,
pricing, and response behavior differ.
