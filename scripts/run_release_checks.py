#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    ".zenodo.json",
    "reports/full_cure_or_paper_tables_v04.md",
    "reports/full_cure_or_paper_tables_v04.tex",
    "reports/vlm_open_weight_full_v03_paper_table.csv",
    "reports/vlm_open_weight_full_v03_paper_table.md",
    "reports/vlm_open_weight_full_v03_paper_table.tex",
    "reports/vlm_provider_full_v01_comparison.csv",
    "reports/vlm_provider_full_v01_comparison.md",
    "reports/vlm_provider_full_v01_comparison.tex",
    "reports/vlm_provider_full_v03_comparison.csv",
    "reports/vlm_provider_full_v03_comparison.md",
    "reports/vlm_provider_full_v03_comparison.tex",
    "reports/vlm_provider_openai_gpt_5_4_mini_full_v01/summary.md",
    "reports/vlm_provider_openai_gpt_5_4_mini_full_v01/model_summary.csv",
    "reports/vlm_provider_openai_gpt_5_4_mini_full_v01/recipe_table.csv",
    "reports/vlm_provider_openai_gpt_5_4_mini_full_v01/label_table.csv",
    "reports/vlm_provider_openai_gpt_5_4_mini_full_v01/audit.csv",
    "reports/vlm_provider_openai_gpt_5_4_full_v01/summary.md",
    "reports/vlm_provider_openai_gpt_5_4_full_v01/model_summary.csv",
    "reports/vlm_provider_openai_gpt_5_4_full_v01/recipe_table.csv",
    "reports/vlm_provider_openai_gpt_5_4_full_v01/label_table.csv",
    "reports/vlm_provider_openai_gpt_5_4_full_v01/audit.csv",
    "reports/vlm_provider_openai_gpt_5_5_full_v01/summary.md",
    "reports/vlm_provider_openai_gpt_5_5_full_v01/model_summary.csv",
    "reports/vlm_provider_openai_gpt_5_5_full_v01/recipe_table.csv",
    "reports/vlm_provider_openai_gpt_5_5_full_v01/label_table.csv",
    "reports/vlm_provider_openai_gpt_5_5_full_v01/audit.csv",
    "reports/vlm_provider_anthropic_claude_sonnet_5_full_v01/summary.md",
    "reports/vlm_provider_anthropic_claude_sonnet_5_full_v01/model_summary.csv",
    "reports/vlm_provider_anthropic_claude_sonnet_5_full_v01/recipe_table.csv",
    "reports/vlm_provider_anthropic_claude_sonnet_5_full_v01/label_table.csv",
    "reports/vlm_provider_anthropic_claude_sonnet_5_full_v01/audit.csv",
    "reports/vlm_provider_anthropic_claude_fable_5_full_v01/summary.md",
    "reports/vlm_provider_anthropic_claude_fable_5_full_v01/model_summary.csv",
    "reports/vlm_provider_anthropic_claude_fable_5_full_v01/recipe_table.csv",
    "reports/vlm_provider_anthropic_claude_fable_5_full_v01/label_table.csv",
    "reports/vlm_provider_anthropic_claude_fable_5_full_v01/audit.csv",
    "reports/vlm_provider_anthropic_claude_haiku_4_5_full_v01/summary.md",
    "reports/vlm_provider_anthropic_claude_haiku_4_5_full_v01/model_summary.csv",
    "reports/vlm_provider_anthropic_claude_haiku_4_5_full_v01/recipe_table.csv",
    "reports/vlm_provider_anthropic_claude_haiku_4_5_full_v01/label_table.csv",
    "reports/vlm_provider_anthropic_claude_haiku_4_5_full_v01/audit.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v01/summary.md",
    "reports/vlm_provider_xai_grok_4_3_full_v01/model_summary.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v01/recipe_table.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v01/label_table.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v01/audit.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v03/summary.md",
    "reports/vlm_provider_xai_grok_4_3_full_v03/model_summary.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v03/recipe_table.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v03/label_table.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v03/audit.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v03_repeat_01/summary.md",
    "reports/vlm_provider_xai_grok_4_3_full_v03_repeat_01/model_summary.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v03_repeat_01/recipe_table.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v03_repeat_01/label_table.csv",
    "reports/vlm_provider_xai_grok_4_3_full_v03_repeat_01/audit.csv",
    "reports/real_transfer_v02_results.md",
    "reports/real_transfer_v02_model_pipeline_table.csv",
    "reports/real_transfer_v02_pipeline_consensus_table.csv",
    "reports/real_transfer_v02_label_failure_table.csv",
    "reports/real_transfer_v03_results.md",
    "reports/real_transfer_v03_model_pipeline_table.csv",
    "reports/real_transfer_v03_pipeline_consensus_table.csv",
    "reports/real_transfer_v03_label_failure_table.csv",
    "reports/real_transfer_v02_activation_status.json",
    "results/real_transfer_v02_source_matched_drops.png",
    "results/real_transfer_v02_accuracy_heatmap.png",
    "results/real_transfer_v03_source_matched_drops.png",
    "results/real_transfer_v03_accuracy_heatmap.png",
    "results/kaggle_writeup_media_v041.png",
    "results/kaggle_writeup_media_v041_01_mean_accuracy.png",
    "results/kaggle_writeup_media_v041_02_level5_ranking.png",
    "results/kaggle_writeup_media_v041_03_real_transfer_drops.png",
    "results/kaggle_writeup_media_v041_04_real_transfer_heatmap.png",
    "results/kaggle_writeup_media_v041_05_grayscale_control.png",
    "results/kaggle_writeup_media_v041_06_level5_overconfidence.png",
    "results/kaggle_writeup_card_thumbnail_v041.png",
    "paper/main.tex",
    "scripts/build_arxiv_source_package.py",
    "scripts/build_kaggle_writeup_media.py",
    "docs/dataset_card_cure_or_pp_v04.md",
    "docs/evaluation_card_full_cure_or_v04.md",
    "docs/public_release_checklist_v01.md",
    "docs/reproducibility_manifest_v01.md",
    "docs/arxiv_source_package_checklist_v01.md",
    "docs/github_release_notes_v0.4_preprint.md",
    "docs/publication_and_archival_plan_v01.md",
    "docs/kaggle_release_checklist.md",
    "reports/arxiv_readiness_matrix_v04.md",
    "scripts/build_kaggle_publication_package.py",
    "scripts/write_kaggle_publication_notebook.py",
    "notebooks/cure_or_pp_kaggle_v041_public.ipynb",
    "kaggle/public_kernel_v041/cure_or_pp_kaggle_v041_public.ipynb",
    "kaggle/public_kernel_v041/kernel-metadata.json",
    "kaggle/writeup_v041.md",
    "kaggle/profile_writeup_v041.md",
    "kaggle/cure-or-plus-plus-v041-public/README.md",
    "kaggle/cure-or-plus-plus-v041-public/WRITEUP.md",
    "kaggle/cure-or-plus-plus-v041-public/CITATION.md",
    "kaggle/cure-or-plus-plus-v041-public/MANIFEST.json",
    "kaggle/cure-or-plus-plus-v041-public/dataset-metadata.json",
    "kaggle/cure-or-plus-plus-v041-public/docs/public_boundary.md",
    "kaggle/cure-or-plus-plus-v041-public/docs/reproducibility_note.md",
    "kaggle/cure-or-plus-plus-v041-public/reports/full_cure_or_paper_model_table_v04.csv",
    "kaggle/cure-or-plus-plus-v041-public/reports/real_transfer_v02_pipeline_consensus_table.csv",
    "kaggle/cure-or-plus-plus-v041-public/reports/vlm_open_weight_full_v03_paper_table.csv",
    "kaggle/cure-or-plus-plus-v041-public/reports/vlm_provider_full_v01_comparison.csv",
    "kaggle/cure-or-plus-plus-v041-public/reports/vlm_provider_full_v03_comparison.csv",
    "kaggle/cure-or-plus-plus-v041-public/figures/real_transfer_v02_source_matched_drops.png",
    "kaggle/cure-or-plus-plus-v041-public-flat/README.md",
    "kaggle/cure-or-plus-plus-v041-public-flat/WRITEUP.md",
    "kaggle/cure-or-plus-plus-v041-public-flat/MANIFEST.json",
    "kaggle/cure-or-plus-plus-v041-public-flat/dataset-metadata.json",
    "kaggle/cure-or-plus-plus-v041-public-flat/reports__full_cure_or_paper_model_table_v04.csv",
    "kaggle/cure-or-plus-plus-v041-public-flat/reports__real_transfer_v02_pipeline_consensus_table.csv",
    "kaggle/cure-or-plus-plus-v041-public-flat/reports__vlm_open_weight_full_v03_paper_table.csv",
    "kaggle/cure-or-plus-plus-v041-public-flat/figures__real_transfer_v02_source_matched_drops.png",
    "configs/vlm_api_track_v01.json",
    "configs/vlm_api_track_v03.json",
    "configs/vlm_frontier_provider_matrix_v01.json",
    "configs/vlm_open_weight_model_matrix_v01.json",
    "configs/vlm_open_weight_model_matrix_v03.json",
    "docs/vlm_api_track_plan_v01.md",
    "docs/vlm_frontier_provider_block_v01.md",
    "docs/vlm_open_weight_model_matrix_v01.md",
    "docs/vlm_v03_full_runbook.md",
    "reports/vlm_api_track_v01_prompt_pack.jsonl",
    "reports/vlm_api_track_v01_prompt_pack_summary.json",
    "reports/vlm_api_track_v01_mixed_smoke_prompt_pack.jsonl",
    "reports/vlm_api_track_v03_prompt_pack.jsonl",
    "reports/vlm_api_track_v03_prompt_pack_summary.json",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/summary.md",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/combined_model_summary.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/combined_recipe_table.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/combined_label_table.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/run_manifest.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/kaggle_kernel.log",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/qwen2_5_vl_7b/model_summary.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/qwen2_5_vl_7b/recipe_table.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/qwen2_5_vl_7b/label_table.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/qwen2_5_vl_7b/audit.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/qwen2_5_vl_7b/responses.jsonl",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/llava_onevision_qwen2_7b/model_summary.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/llava_onevision_qwen2_7b/recipe_table.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/llava_onevision_qwen2_7b/label_table.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/llava_onevision_qwen2_7b/audit.csv",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v03/llava_onevision_qwen2_7b/responses.jsonl",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/summary.md",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/model_summary.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/recipe_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/label_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/audit.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/responses.jsonl",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/combined_model_summary.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/combined_recipe_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/combined_label_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/run_manifest.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/kaggle_kernel.log",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/summary.md",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/model_summary.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/recipe_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/label_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/audit.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/responses.jsonl",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/combined_model_summary.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/combined_recipe_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/combined_label_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/run_manifest.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/kaggle_kernel.log",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/summary.md",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/model_summary.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/recipe_table.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/label_table.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/audit.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/responses.jsonl",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/combined_model_summary.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/combined_recipe_table.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/combined_label_table.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/run_manifest.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/kaggle_kernel.log",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/summary.md",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/model_summary.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/recipe_table.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/label_table.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/audit.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/responses.jsonl",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/combined_model_summary.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/combined_recipe_table.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/combined_label_table.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/run_manifest.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/kaggle_kernel.log",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/summary.md",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/model_summary.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/recipe_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/label_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/audit.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/responses.jsonl",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/combined_model_summary.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/combined_recipe_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/combined_label_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/run_manifest.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/kaggle_kernel.log",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/summary.md",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/model_summary.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/recipe_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/label_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/audit.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/responses.jsonl",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/combined_model_summary.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/combined_recipe_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/combined_label_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/run_manifest.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/kaggle_kernel.log",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/summary.md",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/model_summary.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/recipe_table.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/label_table.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/audit.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/responses.jsonl",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/combined_model_summary.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/combined_recipe_table.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/combined_label_table.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/run_manifest.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/kaggle_kernel.log",
    "reports/vlm_open_weight_full_v03_comparison.csv",
    "reports/vlm_open_weight_full_v03_comparison.md",
    "reports/vlm_open_weight_7b_full_v03_comparison.csv",
    "reports/vlm_open_weight_7b_full_v03_comparison.md",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v01/summary.md",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v01/model_summary.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/summary.md",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/model_summary.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/recipe_table.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/label_table.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/audit.csv",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/responses.jsonl",
    "reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/kaggle_kernel.log",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/summary.md",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/model_summary.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/recipe_table.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/label_table.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/audit.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/responses.jsonl",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/kaggle_kernel.log",
    "reports/vlm_open_weight_internvl3_2b_kaggle_v01/summary.md",
    "reports/vlm_open_weight_internvl3_2b_kaggle_v01/model_summary.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_v01/recipe_table.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_v01/label_table.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_v01/audit.csv",
    "reports/vlm_open_weight_internvl3_2b_kaggle_v01/responses.jsonl",
    "reports/vlm_open_weight_internvl3_2b_kaggle_v01/kaggle_kernel.log",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/summary.md",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/model_summary.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/recipe_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/label_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/audit.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/responses.jsonl",
    "reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/kaggle_kernel.log",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/summary.md",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/model_summary.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/recipe_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/label_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/audit.csv",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/responses.jsonl",
    "reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/kaggle_kernel.log",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/summary.md",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/model_summary.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/recipe_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/label_table.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/audit.csv",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/responses.jsonl",
    "reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/kaggle_kernel.log",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/summary.md",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/model_summary.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/recipe_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/label_table.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/audit.csv",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/responses.jsonl",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/kaggle_kernel.log",
    "scripts/build_vlm_prompt_pack.py",
    "scripts/run_openai_compatible_vlm.py",
    "scripts/run_gemini_vlm.py",
    "scripts/run_anthropic_vlm.py",
    "scripts/run_gigachat_vlm.py",
    "scripts/run_hf_vlm.py",
    "scripts/integrate_kaggle_vlm_output.py",
    "scripts/build_vlm_open_weight_full_comparison.py",
    "scripts/build_vlm_paper_tables.py",
    "scripts/build_vlm_provider_comparison.py",
    "scripts/build_vlm_provider_v03_comparison.py",
    "scripts/merge_vlm_response_retries.py",
    "scripts/prepare_kaggle_vlm_full_run.py",
    "scripts/evaluate_vlm_response_pack.py",
    "scripts/build_kaggle_vlm_package.py",
    "scripts/write_kaggle_vlm_notebook.py",
    "scripts/check_paper_build.py",
    "notebooks/cure_or_pp_vlm_open_weight_kaggle_v01.ipynb",
    "kaggle/vlm_kernel/cure_or_pp_vlm_open_weight_kaggle_v01.ipynb",
    "kaggle/vlm_kernel/kernel-metadata.json",
    "notebooks/cure-or-open-weight-vlm-real-transfer-gpu-pilot.ipynb",
    "notebooks/cure_or_pp_vlm_open_weight_kaggle_v03.ipynb",
    "kaggle/vlm_kernel_v03/cure-or-open-weight-vlm-real-transfer-gpu-pilot.ipynb",
    "kaggle/vlm_kernel_v03/cure_or_pp_vlm_open_weight_kaggle_v03.ipynb",
    "kaggle/vlm_kernel_v03/kernel-metadata.json",
    "reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/launch.md",
]

SUMMARY_FILE_EXPECTATIONS = {
    "results/clip_vit_b16_real_transfer_v02_summary.csv": 4,
    "results/clip_vit_b32_real_transfer_v02_summary.csv": 4,
    "results/openclip_vit_b32_laion2b_real_transfer_v02_summary.csv": 4,
    "results/openclip_vit_b16_datacomp_xl_real_transfer_v02_summary.csv": 4,
    "results/clip_vit_b16_real_transfer_v03_summary.csv": 5,
    "results/clip_vit_b32_real_transfer_v03_summary.csv": 5,
    "results/openclip_vit_b32_laion2b_real_transfer_v03_summary.csv": 5,
    "results/openclip_vit_b16_datacomp_xl_real_transfer_v03_summary.csv": 5,
}

FORBIDDEN_PUBLIC_STRINGS = {
    "desktop_path": "/Users/" + "yaroslav/Desktop",
    "downloads_path": "/Users/" + "yaroslav/Downloads",
}

TEXT_SCAN_PATHS = [
    "README.md",
    "CITATION.cff",
    ".zenodo.json",
    "docs",
    "paper",
    "reports",
    "scripts",
    "kaggle/cure-or-plus-plus-v041-public",
    "kaggle/cure-or-plus-plus-v041-public-flat",
    "kaggle/public_kernel_v041",
    "kaggle/writeup_v041.md",
    "kaggle/profile_writeup_v041.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run release-readiness checks for the current CURE-OR++ draft state.")
    parser.add_argument("--report", default="reports/release_check_v04.json")
    args = parser.parse_args()

    checks = []
    checks.extend(check_required_files())
    checks.extend(check_real_transfer_status())
    checks.extend(check_real_transfer_tables())
    checks.extend(check_summary_files())
    checks.extend(check_paper_links())
    checks.extend(check_paper_preflight())
    checks.extend(check_vlm_prompt_pack())
    checks.extend(check_vlm_mixed_smoke_prompt_pack())
    checks.extend(check_vlm_open_weight_smoke_v03())
    checks.extend(check_vlm_open_weight_qwen3b_full_v03())
    checks.extend(check_vlm_open_weight_qwen_full_v03())
    checks.extend(check_vlm_open_weight_internvl3_1b_full_v03())
    checks.extend(check_vlm_open_weight_internvl3_2b_full_v03())
    checks.extend(check_vlm_open_weight_llava_05b_full_v03())
    checks.extend(check_vlm_open_weight_llava_full_v03())
    checks.extend(check_vlm_open_weight_smolvlm2_full_v03())
    checks.extend(check_vlm_open_weight_full_comparison_v03())
    checks.extend(check_vlm_open_weight_paper_table_v03())
    checks.extend(check_vlm_open_weight_7b_comparison_v03())
    checks.extend(check_vlm_provider_openai_full_v01())
    checks.extend(check_vlm_provider_openai_gpt54_full_v01())
    checks.extend(check_vlm_provider_openai_gpt55_full_v01())
    checks.extend(check_vlm_provider_anthropic_claude_sonnet5_full_v01())
    checks.extend(check_vlm_provider_anthropic_claude_fable5_full_v01())
    checks.extend(check_vlm_provider_anthropic_claude_haiku45_full_v01())
    checks.extend(check_vlm_provider_xai_grok43_full_v01())
    checks.extend(check_vlm_provider_xai_grok43_full_v03())
    checks.extend(check_vlm_provider_xai_grok43_full_v03_repeat_01())
    checks.extend(check_vlm_provider_comparison_v01())
    checks.extend(check_vlm_provider_comparison_v03())
    checks.extend(check_forbidden_public_strings())

    failed = [check for check in checks if not check["passed"]]
    report = {
        "passed": not failed,
        "check_count": len(checks),
        "failed_count": len(failed),
        "checks": checks,
    }
    report_path = resolve_project_path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Checks: {len(checks)}")
    print(f"Failed: {len(failed)}")
    print(f"Report: {report_path}")
    for check in failed:
        print(f"FAIL: {check['name']}: {check['detail']}")
    return 1 if failed else 0


def check_required_files() -> list[dict]:
    checks = []
    for path_text in REQUIRED_FILES:
        path = resolve_project_path(path_text)
        min_size = 10_000 if path.suffix.lower() == ".png" else 1
        checks.append(
            check(
                name=f"required_file:{path_text}",
                passed=path.exists() and path.stat().st_size >= min_size,
                detail=f"exists={path.exists()} size={path.stat().st_size if path.exists() else 0} min_size={min_size}",
            )
        )
    return checks


def check_real_transfer_status() -> list[dict]:
    path = resolve_project_path("reports/real_transfer_v02_activation_status.json")
    if not path.exists():
        return [check("real_transfer_status", False, "missing activation status")]
    status = json.loads(path.read_text(encoding="utf-8"))
    expected = {
        "ready_for_eval": True,
        "schema_ready": True,
        "files_ready": True,
        "expected_output_count": 180,
        "present_output_count": 180,
        "missing_output_count": 0,
    }
    return [
        check(
            name=f"real_transfer_status:{key}",
            passed=status.get(key) == expected_value,
            detail=f"actual={status.get(key)!r} expected={expected_value!r}",
        )
        for key, expected_value in expected.items()
    ]


def check_real_transfer_tables() -> list[dict]:
    checks = []
    table_expectations = {
        "reports/real_transfer_v02_model_pipeline_table.csv": 12,
        "reports/real_transfer_v02_pipeline_consensus_table.csv": 3,
        "reports/real_transfer_v02_label_failure_table.csv": 40,
        "reports/real_transfer_v03_model_pipeline_table.csv": 16,
        "reports/real_transfer_v03_pipeline_consensus_table.csv": 4,
        "reports/real_transfer_v03_label_failure_table.csv": 40,
    }
    for path_text, expected_rows in table_expectations.items():
        rows = load_csv(resolve_project_path(path_text))
        checks.append(check(f"row_count:{path_text}", len(rows) == expected_rows, f"rows={len(rows)} expected={expected_rows}"))

    model_rows = load_csv(resolve_project_path("reports/real_transfer_v02_model_pipeline_table.csv"))
    required_columns = {
        "matched_clean_accuracy_ci_low",
        "matched_clean_accuracy_ci_high",
        "real_accuracy_ci_low",
        "real_accuracy_ci_high",
        "accuracy_drop_ci_low",
        "accuracy_drop_ci_high",
    }
    columns = set(model_rows[0].keys()) if model_rows else set()
    checks.append(
        check(
            "real_transfer_bootstrap_columns",
            required_columns.issubset(columns),
            f"missing={sorted(required_columns - columns)}",
        )
    )
    v03_manifest_rows = load_csv(resolve_project_path("data/real_transfer/v03/manifest_full_4pipelines.csv"))
    checks.append(check("real_transfer_v03_manifest_rows", len(v03_manifest_rows) == 800, f"rows={len(v03_manifest_rows)} expected=800"))
    v03_recipes = sorted({row.get("recipe", "") for row in v03_manifest_rows})
    checks.append(
        check(
            "real_transfer_v03_manifest_recipes",
            v03_recipes == [
                "messenger_upload_download",
                "phone_screenshot_resave",
                "social_app_resave",
                "video_call_frame_capture",
            ],
            f"recipes={v03_recipes}",
        )
    )
    return checks


def check_summary_files() -> list[dict]:
    checks = []
    for path_text, expected_rows in SUMMARY_FILE_EXPECTATIONS.items():
        rows = load_csv(resolve_project_path(path_text))
        checks.append(check(f"summary_rows:{path_text}", len(rows) == expected_rows, f"rows={len(rows)} expected={expected_rows}"))
    return checks


def check_paper_links() -> list[dict]:
    paper = resolve_project_path("paper/main.tex").read_text(encoding="utf-8")
    required = [
        "real_transfer_v02_source_matched_drops.png",
        "real_transfer_v02_accuracy_heatmap.png",
        "source-level bootstrap confidence intervals",
        "SmolVLM2-500M",
        "SmolVLM2-2.2B",
        "InternVL3-1B",
        "InternVL3-2B",
        "LLaVA-OneVision 0.5B",
        "Qwen2.5-VL-3B",
        "Qwen2.5-VL-7B",
        "LLaVA-OneVision 7B",
        "OpenAI GPT-5.4-mini",
        "OpenAI GPT-5.5",
        "vlm_provider_full_v01_comparison.tex",
    ]
    return [
        check(f"paper_contains:{text}", text in paper, f"needle={text!r}")
        for text in required
    ]


def check_paper_preflight() -> list[dict]:
    script = resolve_project_path("scripts/check_paper_build.py")
    if not script.exists():
        return [check("paper_preflight", False, "missing scripts/check_paper_build.py")]

    result = subprocess.run(
        [sys.executable, str(script), "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    detail = f"exit_code={result.returncode}"
    if result.returncode != 0:
        detail += f" stderr={result.stderr[-500:]} stdout={result.stdout[-500:]}"
    return [check("paper_preflight", result.returncode == 0, detail)]


def check_vlm_prompt_pack() -> list[dict]:
    checks = []
    checks.extend(check_vlm_prompt_pack_file(
        prefix="vlm_prompt_pack_v01",
        summary_path=resolve_project_path("reports/vlm_api_track_v01_prompt_pack_summary.json"),
        pack_path=resolve_project_path("reports/vlm_api_track_v01_prompt_pack.jsonl"),
        expected_rows=210,
        expected_clean=30,
        expected_real=180,
    ))
    checks.extend(check_vlm_prompt_pack_file(
        prefix="vlm_prompt_pack_v03",
        summary_path=resolve_project_path("reports/vlm_api_track_v03_prompt_pack_summary.json"),
        pack_path=resolve_project_path("reports/vlm_api_track_v03_prompt_pack.jsonl"),
        expected_rows=900,
        expected_clean=100,
        expected_real=800,
    ))
    return checks


def check_vlm_prompt_pack_file(
    *,
    prefix: str,
    summary_path: Path,
    pack_path: Path,
    expected_rows: int,
    expected_clean: int,
    expected_real: int,
) -> list[dict]:
    if not summary_path.exists() or not pack_path.exists():
        return [check(prefix, False, "missing prompt pack or summary")]

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    prompt_rows = load_jsonl(pack_path)
    checks = [
        check(f"{prefix}_rows", len(prompt_rows) == expected_rows, f"rows={len(prompt_rows)} expected={expected_rows}"),
        check(f"{prefix}_summary_rows", summary.get("row_count") == expected_rows, f"row_count={summary.get('row_count')} expected={expected_rows}"),
        check(f"{prefix}_clean_rows", summary.get("family_counts", {}).get("clean") == expected_clean, f"clean={summary.get('family_counts', {}).get('clean')} expected={expected_clean}"),
        check(f"{prefix}_real_rows", summary.get("family_counts", {}).get("real_transfer") == expected_real, f"real_transfer={summary.get('family_counts', {}).get('real_transfer')} expected={expected_real}"),
        check(f"{prefix}_option_count", summary.get("option_count") == 10, f"option_count={summary.get('option_count')} expected=10"),
    ]
    required_fields = {"sample_id", "image_path", "label", "answer_letter", "prompt", "options"}
    present_fields = set(prompt_rows[0].keys()) if prompt_rows else set()
    checks.append(check(f"{prefix}_fields", required_fields.issubset(present_fields), f"missing={sorted(required_fields - present_fields)}"))
    return checks


def check_vlm_mixed_smoke_prompt_pack() -> list[dict]:
    smoke_rows = load_jsonl(resolve_project_path("reports/vlm_api_track_v01_mixed_smoke_prompt_pack.jsonl"))
    full_rows = load_jsonl(resolve_project_path("reports/vlm_api_track_v01_prompt_pack.jsonl"))
    full_by_id = {row["sample_id"]: row for row in full_rows}
    smoke_ids = [row.get("sample_id", "") for row in smoke_rows]
    expected_ids = [
        "clean__clean__clean__09904",
        "clean__clean__clean__10457",
        "real_transfer__messenger_upload_download__rep_01__10183",
        "real_transfer__phone_screenshot_resave__rep_01__10243",
        "real_transfer__video_call_frame_capture__rep_01__09958",
    ]
    family_counts = {}
    recipe_counts = {}
    labels = set()
    for row in smoke_rows:
        family_counts[row.get("family", "")] = family_counts.get(row.get("family", ""), 0) + 1
        recipe_counts[row.get("recipe", "")] = recipe_counts.get(row.get("recipe", ""), 0) + 1
        labels.add(row.get("label", ""))
    rows_match_full_pack = all(full_by_id.get(row.get("sample_id")) == row for row in smoke_rows)
    return [
        check("vlm_mixed_smoke_prompt_pack_rows", len(smoke_rows) == 5, f"rows={len(smoke_rows)} expected=5"),
        check("vlm_mixed_smoke_prompt_pack_ids", smoke_ids == expected_ids, f"sample_ids={smoke_ids}"),
        check("vlm_mixed_smoke_prompt_pack_families", family_counts == {"clean": 2, "real_transfer": 3}, f"family_counts={family_counts}"),
        check(
            "vlm_mixed_smoke_prompt_pack_recipes",
            recipe_counts == {
                "clean": 2,
                "messenger_upload_download": 1,
                "phone_screenshot_resave": 1,
                "video_call_frame_capture": 1,
            },
            f"recipe_counts={recipe_counts}",
        ),
        check("vlm_mixed_smoke_prompt_pack_labels", len(labels) == 5, f"labels={sorted(labels)}"),
        check("vlm_mixed_smoke_prompt_pack_matches_full_pack", rows_match_full_pack, "mixed smoke rows must be copied from v0.1 full prompt pack"),
    ]


def check_vlm_open_weight_smoke_v03() -> list[dict]:
    base = resolve_project_path("reports/vlm_open_weight_matrix_smoke_kaggle_v03")
    expected_slugs = {"llava_onevision_qwen2_7b", "qwen2_5_vl_7b"}

    combined_rows = load_csv(base / "combined_model_summary.csv")
    combined_slugs = {row.get("slug", "") for row in combined_rows}
    checks = [
        check(
            "vlm_open_weight_smoke_v03_combined_models",
            combined_slugs == expected_slugs,
            f"slugs={sorted(combined_slugs)} expected={sorted(expected_slugs)}",
        ),
        check(
            "vlm_open_weight_smoke_v03_combined_model_rows",
            len(combined_rows) == 2,
            f"rows={len(combined_rows)} expected=2",
        ),
        check(
            "vlm_open_weight_smoke_v03_recipe_rows",
            len(load_csv(base / "combined_recipe_table.csv")) == 8,
            f"rows={len(load_csv(base / 'combined_recipe_table.csv'))} expected=8",
        ),
        check(
            "vlm_open_weight_smoke_v03_manifest_rows",
            len(load_csv(base / "run_manifest.csv")) == 2,
            f"rows={len(load_csv(base / 'run_manifest.csv'))} expected=2",
        ),
    ]

    for slug in sorted(expected_slugs):
        model_dir = base / slug
        response_rows = load_jsonl(model_dir / "responses.jsonl")
        audit_rows = load_csv(model_dir / "audit.csv")
        summary_rows = load_csv(model_dir / "model_summary.csv")
        checks.extend([
            check(
                f"vlm_open_weight_smoke_v03_{slug}_responses",
                len(response_rows) == 6,
                f"rows={len(response_rows)} expected=6",
            ),
            check(
                f"vlm_open_weight_smoke_v03_{slug}_audit",
                len(audit_rows) == 6,
                f"rows={len(audit_rows)} expected=6",
            ),
            check(
                f"vlm_open_weight_smoke_v03_{slug}_summary",
                len(summary_rows) == 1,
                f"rows={len(summary_rows)} expected=1",
            ),
        ])

    return checks


def check_vlm_open_weight_qwen3b_full_v03() -> list[dict]:
    base = resolve_project_path("reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    response_rows = load_jsonl(base / "responses.jsonl")
    audit_rows = load_csv(base / "audit.csv")
    manifest_rows = load_csv(base / "run_manifest.csv")

    checks = [
        check(
            "vlm_open_weight_qwen3b_full_v03_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_open_weight_qwen3b_full_v03_recipe_rows",
            len(recipe_rows) == 4,
            f"rows={len(recipe_rows)} expected=4",
        ),
        check(
            "vlm_open_weight_qwen3b_full_v03_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_open_weight_qwen3b_full_v03_responses",
            len(response_rows) == 900,
            f"rows={len(response_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_qwen3b_full_v03_audit",
            len(audit_rows) == 900,
            f"rows={len(audit_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_qwen3b_full_v03_manifest",
            len(manifest_rows) == 1 and manifest_rows[0].get("slug") == "qwen2_5_vl_3b",
            f"rows={len(manifest_rows)} slugs={[row.get('slug') for row in manifest_rows]}",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_open_weight_qwen3b_full_v03_clean_n",
                row.get("clean_n") == "100",
                f"clean_n={row.get('clean_n')} expected=100",
            ),
            check(
                "vlm_open_weight_qwen3b_full_v03_real_n",
                row.get("real_n") == "800",
                f"real_n={row.get('real_n')} expected=800",
            ),
            check(
                "vlm_open_weight_qwen3b_full_v03_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.88),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.88",
            ),
            check(
                "vlm_open_weight_qwen3b_full_v03_real_accuracy",
                approx(row.get("real_accuracy"), 0.765),
                f"real_accuracy={row.get('real_accuracy')} expected=0.765",
            ),
            check(
                "vlm_open_weight_qwen3b_full_v03_real_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.20875),
                f"real_unparseable_rate={row.get('real_unparseable_rate')} expected=0.20875",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    recipe_unparseable = {row.get("recipe"): row.get("unparseable_rate") for row in recipe_rows}
    checks.extend([
        check(
            "vlm_open_weight_qwen3b_full_v03_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.64),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.64",
        ),
        check(
            "vlm_open_weight_qwen3b_full_v03_video_call_unparseable",
            approx(recipe_unparseable.get("video_call_frame_capture"), 0.32),
            f"unparseable={recipe_unparseable.get('video_call_frame_capture')} expected=0.32",
        ),
    ])
    return checks


def check_vlm_open_weight_qwen_full_v03() -> list[dict]:
    base = resolve_project_path("reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    response_rows = load_jsonl(base / "responses.jsonl")
    audit_rows = load_csv(base / "audit.csv")
    manifest_rows = load_csv(base / "run_manifest.csv")

    checks = [
        check(
            "vlm_open_weight_qwen_full_v03_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_open_weight_qwen_full_v03_recipe_rows",
            len(recipe_rows) == 4,
            f"rows={len(recipe_rows)} expected=4",
        ),
        check(
            "vlm_open_weight_qwen_full_v03_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_open_weight_qwen_full_v03_responses",
            len(response_rows) == 900,
            f"rows={len(response_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_qwen_full_v03_audit",
            len(audit_rows) == 900,
            f"rows={len(audit_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_qwen_full_v03_manifest",
            len(manifest_rows) == 1 and manifest_rows[0].get("slug") == "qwen2_5_vl_7b",
            f"rows={len(manifest_rows)} slugs={[row.get('slug') for row in manifest_rows]}",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_open_weight_qwen_full_v03_clean_n",
                row.get("clean_n") == "100",
                f"clean_n={row.get('clean_n')} expected=100",
            ),
            check(
                "vlm_open_weight_qwen_full_v03_real_n",
                row.get("real_n") == "800",
                f"real_n={row.get('real_n')} expected=800",
            ),
            check(
                "vlm_open_weight_qwen_full_v03_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.98),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.98",
            ),
            check(
                "vlm_open_weight_qwen_full_v03_real_accuracy",
                approx(row.get("real_accuracy"), 0.96125),
                f"real_accuracy={row.get('real_accuracy')} expected=0.96125",
            ),
            check(
                "vlm_open_weight_qwen_full_v03_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.append(
        check(
            "vlm_open_weight_qwen_full_v03_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.93),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.93",
        )
    )
    return checks


def check_vlm_open_weight_internvl3_1b_full_v03() -> list[dict]:
    base = resolve_project_path("reports/vlm_open_weight_internvl3_1b_kaggle_full_v03")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    response_rows = load_jsonl(base / "responses.jsonl")
    audit_rows = load_csv(base / "audit.csv")
    manifest_rows = load_csv(base / "run_manifest.csv")

    checks = [
        check(
            "vlm_open_weight_internvl3_1b_full_v03_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_open_weight_internvl3_1b_full_v03_recipe_rows",
            len(recipe_rows) == 4,
            f"rows={len(recipe_rows)} expected=4",
        ),
        check(
            "vlm_open_weight_internvl3_1b_full_v03_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_open_weight_internvl3_1b_full_v03_responses",
            len(response_rows) == 900,
            f"rows={len(response_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_internvl3_1b_full_v03_audit",
            len(audit_rows) == 900,
            f"rows={len(audit_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_internvl3_1b_full_v03_manifest",
            len(manifest_rows) == 1 and manifest_rows[0].get("slug") == "internvl3_1b",
            f"rows={len(manifest_rows)} slugs={[row.get('slug') for row in manifest_rows]}",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_open_weight_internvl3_1b_full_v03_clean_n",
                row.get("clean_n") == "100",
                f"clean_n={row.get('clean_n')} expected=100",
            ),
            check(
                "vlm_open_weight_internvl3_1b_full_v03_real_n",
                row.get("real_n") == "800",
                f"real_n={row.get('real_n')} expected=800",
            ),
            check(
                "vlm_open_weight_internvl3_1b_full_v03_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.95),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.95",
            ),
            check(
                "vlm_open_weight_internvl3_1b_full_v03_real_accuracy",
                approx(row.get("real_accuracy"), 0.95625),
                f"real_accuracy={row.get('real_accuracy')} expected=0.95625",
            ),
            check(
                "vlm_open_weight_internvl3_1b_full_v03_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.append(
        check(
            "vlm_open_weight_internvl3_1b_full_v03_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.945),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.945",
        )
    )
    return checks


def check_vlm_open_weight_internvl3_2b_full_v03() -> list[dict]:
    base = resolve_project_path("reports/vlm_open_weight_internvl3_2b_kaggle_full_v03")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    response_rows = load_jsonl(base / "responses.jsonl")
    audit_rows = load_csv(base / "audit.csv")
    manifest_rows = load_csv(base / "run_manifest.csv")

    checks = [
        check(
            "vlm_open_weight_internvl3_2b_full_v03_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_open_weight_internvl3_2b_full_v03_recipe_rows",
            len(recipe_rows) == 4,
            f"rows={len(recipe_rows)} expected=4",
        ),
        check(
            "vlm_open_weight_internvl3_2b_full_v03_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_open_weight_internvl3_2b_full_v03_responses",
            len(response_rows) == 900,
            f"rows={len(response_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_internvl3_2b_full_v03_audit",
            len(audit_rows) == 900,
            f"rows={len(audit_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_internvl3_2b_full_v03_manifest",
            len(manifest_rows) == 1 and manifest_rows[0].get("slug") == "internvl3_2b",
            f"rows={len(manifest_rows)} slugs={[row.get('slug') for row in manifest_rows]}",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_open_weight_internvl3_2b_full_v03_clean_n",
                row.get("clean_n") == "100",
                f"clean_n={row.get('clean_n')} expected=100",
            ),
            check(
                "vlm_open_weight_internvl3_2b_full_v03_real_n",
                row.get("real_n") == "800",
                f"real_n={row.get('real_n')} expected=800",
            ),
            check(
                "vlm_open_weight_internvl3_2b_full_v03_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.97),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.97",
            ),
            check(
                "vlm_open_weight_internvl3_2b_full_v03_real_accuracy",
                approx(row.get("real_accuracy"), 0.96),
                f"real_accuracy={row.get('real_accuracy')} expected=0.96",
            ),
            check(
                "vlm_open_weight_internvl3_2b_full_v03_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.append(
        check(
            "vlm_open_weight_internvl3_2b_full_v03_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.935),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.935",
        )
    )
    return checks


def check_vlm_open_weight_llava_05b_full_v03() -> list[dict]:
    base = resolve_project_path("reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    response_rows = load_jsonl(base / "responses.jsonl")
    audit_rows = load_csv(base / "audit.csv")
    manifest_rows = load_csv(base / "run_manifest.csv")

    checks = [
        check(
            "vlm_open_weight_llava_05b_full_v03_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_open_weight_llava_05b_full_v03_recipe_rows",
            len(recipe_rows) == 4,
            f"rows={len(recipe_rows)} expected=4",
        ),
        check(
            "vlm_open_weight_llava_05b_full_v03_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_open_weight_llava_05b_full_v03_responses",
            len(response_rows) == 900,
            f"rows={len(response_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_llava_05b_full_v03_audit",
            len(audit_rows) == 900,
            f"rows={len(audit_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_llava_05b_full_v03_manifest",
            len(manifest_rows) == 1 and manifest_rows[0].get("slug") == "llava_onevision_qwen2_0_5b",
            f"rows={len(manifest_rows)} slugs={[row.get('slug') for row in manifest_rows]}",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_open_weight_llava_05b_full_v03_clean_n",
                row.get("clean_n") == "100",
                f"clean_n={row.get('clean_n')} expected=100",
            ),
            check(
                "vlm_open_weight_llava_05b_full_v03_real_n",
                row.get("real_n") == "800",
                f"real_n={row.get('real_n')} expected=800",
            ),
            check(
                "vlm_open_weight_llava_05b_full_v03_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.93),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.93",
            ),
            check(
                "vlm_open_weight_llava_05b_full_v03_real_accuracy",
                approx(row.get("real_accuracy"), 0.92125),
                f"real_accuracy={row.get('real_accuracy')} expected=0.92125",
            ),
            check(
                "vlm_open_weight_llava_05b_full_v03_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.append(
        check(
            "vlm_open_weight_llava_05b_full_v03_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.895),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.895",
        )
    )
    return checks


def check_vlm_open_weight_llava_full_v03() -> list[dict]:
    base = resolve_project_path("reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    response_rows = load_jsonl(base / "responses.jsonl")
    audit_rows = load_csv(base / "audit.csv")
    manifest_rows = load_csv(base / "run_manifest.csv")

    checks = [
        check(
            "vlm_open_weight_llava_full_v03_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_open_weight_llava_full_v03_recipe_rows",
            len(recipe_rows) == 4,
            f"rows={len(recipe_rows)} expected=4",
        ),
        check(
            "vlm_open_weight_llava_full_v03_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_open_weight_llava_full_v03_responses",
            len(response_rows) == 900,
            f"rows={len(response_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_llava_full_v03_audit",
            len(audit_rows) == 900,
            f"rows={len(audit_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_llava_full_v03_manifest",
            len(manifest_rows) == 1 and manifest_rows[0].get("slug") == "llava_onevision_qwen2_7b",
            f"rows={len(manifest_rows)} slugs={[row.get('slug') for row in manifest_rows]}",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_open_weight_llava_full_v03_clean_n",
                row.get("clean_n") == "100",
                f"clean_n={row.get('clean_n')} expected=100",
            ),
            check(
                "vlm_open_weight_llava_full_v03_real_n",
                row.get("real_n") == "800",
                f"real_n={row.get('real_n')} expected=800",
            ),
            check(
                "vlm_open_weight_llava_full_v03_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.98),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.98",
            ),
            check(
                "vlm_open_weight_llava_full_v03_real_accuracy",
                approx(row.get("real_accuracy"), 0.9775),
                f"real_accuracy={row.get('real_accuracy')} expected=0.9775",
            ),
            check(
                "vlm_open_weight_llava_full_v03_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.append(
        check(
            "vlm_open_weight_llava_full_v03_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.955),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.955",
        )
    )
    return checks


def check_vlm_open_weight_smolvlm2_full_v03() -> list[dict]:
    base = resolve_project_path("reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    response_rows = load_jsonl(base / "responses.jsonl")
    audit_rows = load_csv(base / "audit.csv")
    manifest_rows = load_csv(base / "run_manifest.csv")

    checks = [
        check(
            "vlm_open_weight_smolvlm2_full_v03_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_open_weight_smolvlm2_full_v03_recipe_rows",
            len(recipe_rows) == 4,
            f"rows={len(recipe_rows)} expected=4",
        ),
        check(
            "vlm_open_weight_smolvlm2_full_v03_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_open_weight_smolvlm2_full_v03_responses",
            len(response_rows) == 900,
            f"rows={len(response_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_smolvlm2_full_v03_audit",
            len(audit_rows) == 900,
            f"rows={len(audit_rows)} expected=900",
        ),
        check(
            "vlm_open_weight_smolvlm2_full_v03_manifest",
            len(manifest_rows) == 1 and manifest_rows[0].get("slug") == "smolvlm2_2b",
            f"rows={len(manifest_rows)} slugs={[row.get('slug') for row in manifest_rows]}",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_open_weight_smolvlm2_full_v03_clean_n",
                row.get("clean_n") == "100",
                f"clean_n={row.get('clean_n')} expected=100",
            ),
            check(
                "vlm_open_weight_smolvlm2_full_v03_real_n",
                row.get("real_n") == "800",
                f"real_n={row.get('real_n')} expected=800",
            ),
            check(
                "vlm_open_weight_smolvlm2_full_v03_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.96),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.96",
            ),
            check(
                "vlm_open_weight_smolvlm2_full_v03_real_accuracy",
                approx(row.get("real_accuracy"), 0.9575),
                f"real_accuracy={row.get('real_accuracy')} expected=0.9575",
            ),
            check(
                "vlm_open_weight_smolvlm2_full_v03_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.append(
        check(
            "vlm_open_weight_smolvlm2_full_v03_social_app_accuracy",
            approx(recipe_accuracy.get("social_app_resave"), 0.95),
            f"accuracy={recipe_accuracy.get('social_app_resave')} expected=0.95",
        )
    )
    return checks


def check_vlm_open_weight_full_comparison_v03() -> list[dict]:
    rows = load_csv(resolve_project_path("reports/vlm_open_weight_full_v03_comparison.csv"))
    required_slugs = {
        "internvl3_1b",
        "internvl3_2b",
        "qwen2_5_vl_3b",
        "qwen2_5_vl_7b",
        "llava_onevision_qwen2_0_5b",
        "llava_onevision_qwen2_7b",
        "smolvlm2_2b",
    }
    slugs = {row.get("slug", "") for row in rows}
    checks = [
        check(
            "vlm_open_weight_full_comparison_v03_min_rows",
            len(rows) >= 7,
            f"rows={len(rows)} expected>=7",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_required_slugs",
            required_slugs.issubset(slugs),
            f"slugs={sorted(slugs)} required={sorted(required_slugs)}",
        ),
    ]
    if rows:
        checks.append(
            check(
                "vlm_open_weight_full_comparison_v03_leader",
                rows[0].get("slug") == "llava_onevision_qwen2_7b",
                f"leader={rows[0].get('slug')}",
            )
        )
    by_slug = {row.get("slug"): row for row in rows}
    checks.extend([
        check(
            "vlm_open_weight_full_comparison_v03_qwen_real_accuracy",
            approx(by_slug.get("qwen2_5_vl_7b", {}).get("real_accuracy"), 0.96125),
            f"accuracy={by_slug.get('qwen2_5_vl_7b', {}).get('real_accuracy')} expected=0.96125",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_qwen3b_real_accuracy",
            approx(by_slug.get("qwen2_5_vl_3b", {}).get("real_accuracy"), 0.765),
            f"accuracy={by_slug.get('qwen2_5_vl_3b', {}).get('real_accuracy')} expected=0.765",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_qwen3b_unparseable",
            approx(by_slug.get("qwen2_5_vl_3b", {}).get("real_unparseable_rate"), 0.20875),
            f"unparseable={by_slug.get('qwen2_5_vl_3b', {}).get('real_unparseable_rate')} expected=0.20875",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_llava_real_accuracy",
            approx(by_slug.get("llava_onevision_qwen2_7b", {}).get("real_accuracy"), 0.9775),
            f"accuracy={by_slug.get('llava_onevision_qwen2_7b', {}).get('real_accuracy')} expected=0.9775",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_internvl3_1b_real_accuracy",
            approx(by_slug.get("internvl3_1b", {}).get("real_accuracy"), 0.95625),
            f"accuracy={by_slug.get('internvl3_1b', {}).get('real_accuracy')} expected=0.95625",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_internvl3_1b_unparseable",
            approx(by_slug.get("internvl3_1b", {}).get("real_unparseable_rate"), 0.0),
            f"unparseable={by_slug.get('internvl3_1b', {}).get('real_unparseable_rate')} expected=0",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_internvl3_2b_real_accuracy",
            approx(by_slug.get("internvl3_2b", {}).get("real_accuracy"), 0.96),
            f"accuracy={by_slug.get('internvl3_2b', {}).get('real_accuracy')} expected=0.96",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_internvl3_2b_unparseable",
            approx(by_slug.get("internvl3_2b", {}).get("real_unparseable_rate"), 0.0),
            f"unparseable={by_slug.get('internvl3_2b', {}).get('real_unparseable_rate')} expected=0",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_llava05b_real_accuracy",
            approx(by_slug.get("llava_onevision_qwen2_0_5b", {}).get("real_accuracy"), 0.92125),
            f"accuracy={by_slug.get('llava_onevision_qwen2_0_5b', {}).get('real_accuracy')} expected=0.92125",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_llava05b_unparseable",
            approx(by_slug.get("llava_onevision_qwen2_0_5b", {}).get("real_unparseable_rate"), 0.0),
            f"unparseable={by_slug.get('llava_onevision_qwen2_0_5b', {}).get('real_unparseable_rate')} expected=0",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_smolvlm2_real_accuracy",
            approx(by_slug.get("smolvlm2_2b", {}).get("real_accuracy"), 0.9575),
            f"accuracy={by_slug.get('smolvlm2_2b', {}).get('real_accuracy')} expected=0.9575",
        ),
        check(
            "vlm_open_weight_full_comparison_v03_hardest_pipeline",
            all(
                row.get("hardest_pipeline") == "video_call_frame_capture"
                for row in rows
                if row.get("slug") in {"internvl3_1b", "internvl3_2b", "qwen2_5_vl_7b", "llava_onevision_qwen2_0_5b", "llava_onevision_qwen2_7b"}
            ),
            f"hardest={[(row.get('slug'), row.get('hardest_pipeline')) for row in rows]}",
        ),
    ])
    markdown = resolve_project_path("reports/vlm_open_weight_full_v03_comparison.md").read_text(encoding="utf-8")
    checks.append(
        check(
            "vlm_open_weight_full_comparison_v03_markdown_scope",
            "Launch-only or incomplete result directories are intentionally excluded." in markdown,
            "missing incomplete-result scope note",
        )
    )
    return checks


def check_vlm_open_weight_paper_table_v03() -> list[dict]:
    rows = load_csv(resolve_project_path("reports/vlm_open_weight_full_v03_paper_table.csv"))
    by_slug = {row.get("slug"): row for row in rows}
    markdown = resolve_project_path("reports/vlm_open_weight_full_v03_paper_table.md").read_text(encoding="utf-8")
    latex = resolve_project_path("reports/vlm_open_weight_full_v03_paper_table.tex").read_text(encoding="utf-8")
    paper = resolve_project_path("paper/main.tex").read_text(encoding="utf-8")
    return [
        check(
            "vlm_open_weight_paper_table_v03_rows",
            len(rows) == 7,
            f"rows={len(rows)} expected=7",
        ),
        check(
            "vlm_open_weight_paper_table_v03_leader",
            rows and rows[0].get("slug") == "llava_onevision_qwen2_7b",
            f"leader={rows[0].get('slug') if rows else None}",
        ),
        check(
            "vlm_open_weight_paper_table_v03_internvl3_2b",
            approx(by_slug.get("internvl3_2b", {}).get("real_accuracy"), 0.96),
            f"accuracy={by_slug.get('internvl3_2b', {}).get('real_accuracy')} expected=0.96",
        ),
        check(
            "vlm_open_weight_paper_table_v03_qwen3b_unparseable",
            approx(by_slug.get("qwen2_5_vl_3b", {}).get("real_unparseable_rate"), 0.20875),
            f"unparseable={by_slug.get('qwen2_5_vl_3b', {}).get('real_unparseable_rate')} expected=0.20875",
        ),
        check(
            "vlm_open_weight_paper_table_v03_markdown",
            "LLaVA-OneVision-Qwen2-7B" in markdown and "Qwen2.5-VL-3B" in markdown,
            "missing expected model names in markdown table",
        ),
        check(
            "vlm_open_weight_paper_table_v03_latex_label",
            r"\label{tab:vlm-open-weight-full-v03}" in latex,
            "missing latex table label",
        ),
        check(
            "vlm_open_weight_paper_table_v03_paper_input",
            r"\input{../reports/vlm_open_weight_full_v03_paper_table.tex}" in paper,
            "paper/main.tex does not input VLM v0.3 paper table",
        ),
    ]


def check_vlm_open_weight_7b_comparison_v03() -> list[dict]:
    rows = load_csv(resolve_project_path("reports/vlm_open_weight_7b_full_v03_comparison.csv"))
    slugs = {row.get("slug", "") for row in rows}
    checks = [
        check(
            "vlm_open_weight_7b_comparison_v03_rows",
            len(rows) == 2,
            f"rows={len(rows)} expected=2",
        ),
        check(
            "vlm_open_weight_7b_comparison_v03_slugs",
            slugs == {"qwen2_5_vl_7b", "llava_onevision_qwen2_7b"},
            f"slugs={sorted(slugs)}",
        ),
    ]
    real_accuracy = {row.get("slug"): row.get("real_accuracy") for row in rows}
    checks.extend([
        check(
            "vlm_open_weight_7b_comparison_v03_qwen_real_accuracy",
            approx(real_accuracy.get("qwen2_5_vl_7b"), 0.96125),
            f"accuracy={real_accuracy.get('qwen2_5_vl_7b')} expected=0.96125",
        ),
        check(
            "vlm_open_weight_7b_comparison_v03_llava_real_accuracy",
            approx(real_accuracy.get("llava_onevision_qwen2_7b"), 0.9775),
            f"accuracy={real_accuracy.get('llava_onevision_qwen2_7b')} expected=0.9775",
        ),
    ])
    return checks


def check_vlm_provider_openai_full_v01() -> list[dict]:
    base = resolve_project_path("reports/vlm_provider_openai_gpt_5_4_mini_full_v01")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    audit_rows = load_csv(base / "audit.csv")

    checks = [
        check(
            "vlm_provider_openai_full_v01_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_provider_openai_full_v01_recipe_rows",
            len(recipe_rows) == 3,
            f"rows={len(recipe_rows)} expected=3",
        ),
        check(
            "vlm_provider_openai_full_v01_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_provider_openai_full_v01_audit_rows",
            len(audit_rows) == 210,
            f"rows={len(audit_rows)} expected=210",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_provider_openai_full_v01_clean_n",
                row.get("clean_n") == "30",
                f"clean_n={row.get('clean_n')} expected=30",
            ),
            check(
                "vlm_provider_openai_full_v01_real_n",
                row.get("real_n") == "180",
                f"real_n={row.get('real_n')} expected=180",
            ),
            check(
                "vlm_provider_openai_full_v01_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.966667, tolerance=1e-6),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.966667",
            ),
            check(
                "vlm_provider_openai_full_v01_real_accuracy",
                approx(row.get("real_accuracy"), 0.961111, tolerance=1e-6),
                f"real_accuracy={row.get('real_accuracy')} expected=0.961111",
            ),
            check(
                "vlm_provider_openai_full_v01_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
            check(
                "vlm_provider_openai_full_v01_abstention_rate",
                approx(row.get("real_abstention_rate"), 0.0) and approx(row.get("clean_abstention_rate"), 0.0),
                f"clean={row.get('clean_abstention_rate')} real={row.get('real_abstention_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.extend([
        check(
            "vlm_provider_openai_full_v01_whatsapp_accuracy",
            approx(recipe_accuracy.get("messenger_upload_download"), 0.966667, tolerance=1e-6),
            f"accuracy={recipe_accuracy.get('messenger_upload_download')} expected=0.966667",
        ),
        check(
            "vlm_provider_openai_full_v01_screenshot_accuracy",
            approx(recipe_accuracy.get("phone_screenshot_resave"), 0.983333, tolerance=1e-6),
            f"accuracy={recipe_accuracy.get('phone_screenshot_resave')} expected=0.983333",
        ),
        check(
            "vlm_provider_openai_full_v01_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.933333, tolerance=1e-6),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.933333",
        ),
    ])

    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")
    unparseable = sum(1 for row in audit_rows if row.get("is_unparseable") == "True")
    abstentions = sum(1 for row in audit_rows if row.get("is_abstention") == "True")
    checks.extend([
        check("vlm_provider_openai_full_v01_clean_errors", clean_errors == 1, f"clean_errors={clean_errors} expected=1"),
        check("vlm_provider_openai_full_v01_real_errors", real_errors == 7, f"real_errors={real_errors} expected=7"),
        check("vlm_provider_openai_full_v01_audit_unparseable", unparseable == 0, f"unparseable={unparseable} expected=0"),
        check("vlm_provider_openai_full_v01_audit_abstentions", abstentions == 0, f"abstentions={abstentions} expected=0"),
    ])
    return checks


def check_vlm_provider_openai_gpt54_full_v01() -> list[dict]:
    base = resolve_project_path("reports/vlm_provider_openai_gpt_5_4_full_v01")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    audit_rows = load_csv(base / "audit.csv")

    checks = [
        check(
            "vlm_provider_openai_gpt54_full_v01_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_provider_openai_gpt54_full_v01_recipe_rows",
            len(recipe_rows) == 3,
            f"rows={len(recipe_rows)} expected=3",
        ),
        check(
            "vlm_provider_openai_gpt54_full_v01_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_provider_openai_gpt54_full_v01_audit_rows",
            len(audit_rows) == 210,
            f"rows={len(audit_rows)} expected=210",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_provider_openai_gpt54_full_v01_clean_n",
                row.get("clean_n") == "30",
                f"clean_n={row.get('clean_n')} expected=30",
            ),
            check(
                "vlm_provider_openai_gpt54_full_v01_real_n",
                row.get("real_n") == "180",
                f"real_n={row.get('real_n')} expected=180",
            ),
            check(
                "vlm_provider_openai_gpt54_full_v01_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.966667, tolerance=1e-6),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.966667",
            ),
            check(
                "vlm_provider_openai_gpt54_full_v01_real_accuracy",
                approx(row.get("real_accuracy"), 0.955556, tolerance=1e-6),
                f"real_accuracy={row.get('real_accuracy')} expected=0.955556",
            ),
            check(
                "vlm_provider_openai_gpt54_full_v01_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
            check(
                "vlm_provider_openai_gpt54_full_v01_abstention_rate",
                approx(row.get("real_abstention_rate"), 0.0) and approx(row.get("clean_abstention_rate"), 0.0),
                f"clean={row.get('clean_abstention_rate')} real={row.get('real_abstention_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.extend([
        check(
            "vlm_provider_openai_gpt54_full_v01_whatsapp_accuracy",
            approx(recipe_accuracy.get("messenger_upload_download"), 0.966667, tolerance=1e-6),
            f"accuracy={recipe_accuracy.get('messenger_upload_download')} expected=0.966667",
        ),
        check(
            "vlm_provider_openai_gpt54_full_v01_screenshot_accuracy",
            approx(recipe_accuracy.get("phone_screenshot_resave"), 0.95),
            f"accuracy={recipe_accuracy.get('phone_screenshot_resave')} expected=0.95",
        ),
        check(
            "vlm_provider_openai_gpt54_full_v01_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.95),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.95",
        ),
    ])

    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")
    unparseable = sum(1 for row in audit_rows if row.get("is_unparseable") == "True")
    abstentions = sum(1 for row in audit_rows if row.get("is_abstention") == "True")
    checks.extend([
        check("vlm_provider_openai_gpt54_full_v01_clean_errors", clean_errors == 1, f"clean_errors={clean_errors} expected=1"),
        check("vlm_provider_openai_gpt54_full_v01_real_errors", real_errors == 8, f"real_errors={real_errors} expected=8"),
        check("vlm_provider_openai_gpt54_full_v01_audit_unparseable", unparseable == 0, f"unparseable={unparseable} expected=0"),
        check("vlm_provider_openai_gpt54_full_v01_audit_abstentions", abstentions == 0, f"abstentions={abstentions} expected=0"),
    ])
    return checks


def check_vlm_provider_openai_gpt55_full_v01() -> list[dict]:
    base = resolve_project_path("reports/vlm_provider_openai_gpt_5_5_full_v01")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    audit_rows = load_csv(base / "audit.csv")

    checks = [
        check(
            "vlm_provider_openai_gpt55_full_v01_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_provider_openai_gpt55_full_v01_recipe_rows",
            len(recipe_rows) == 3,
            f"rows={len(recipe_rows)} expected=3",
        ),
        check(
            "vlm_provider_openai_gpt55_full_v01_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_provider_openai_gpt55_full_v01_audit_rows",
            len(audit_rows) == 210,
            f"rows={len(audit_rows)} expected=210",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_provider_openai_gpt55_full_v01_clean_n",
                row.get("clean_n") == "30",
                f"clean_n={row.get('clean_n')} expected=30",
            ),
            check(
                "vlm_provider_openai_gpt55_full_v01_real_n",
                row.get("real_n") == "180",
                f"real_n={row.get('real_n')} expected=180",
            ),
            check(
                "vlm_provider_openai_gpt55_full_v01_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.966667, tolerance=1e-6),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.966667",
            ),
            check(
                "vlm_provider_openai_gpt55_full_v01_real_accuracy",
                approx(row.get("real_accuracy"), 0.95),
                f"real_accuracy={row.get('real_accuracy')} expected=0.95",
            ),
            check(
                "vlm_provider_openai_gpt55_full_v01_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
            check(
                "vlm_provider_openai_gpt55_full_v01_abstention_rate",
                approx(row.get("real_abstention_rate"), 0.0) and approx(row.get("clean_abstention_rate"), 0.0),
                f"clean={row.get('clean_abstention_rate')} real={row.get('real_abstention_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.extend([
        check(
            "vlm_provider_openai_gpt55_full_v01_whatsapp_accuracy",
            approx(recipe_accuracy.get("messenger_upload_download"), 0.966667, tolerance=1e-6),
            f"accuracy={recipe_accuracy.get('messenger_upload_download')} expected=0.966667",
        ),
        check(
            "vlm_provider_openai_gpt55_full_v01_screenshot_accuracy",
            approx(recipe_accuracy.get("phone_screenshot_resave"), 0.95),
            f"accuracy={recipe_accuracy.get('phone_screenshot_resave')} expected=0.95",
        ),
        check(
            "vlm_provider_openai_gpt55_full_v01_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.933333, tolerance=1e-6),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.933333",
        ),
    ])

    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")
    unparseable = sum(1 for row in audit_rows if row.get("is_unparseable") == "True")
    abstentions = sum(1 for row in audit_rows if row.get("is_abstention") == "True")
    checks.extend([
        check("vlm_provider_openai_gpt55_full_v01_clean_errors", clean_errors == 1, f"clean_errors={clean_errors} expected=1"),
        check("vlm_provider_openai_gpt55_full_v01_real_errors", real_errors == 9, f"real_errors={real_errors} expected=9"),
        check("vlm_provider_openai_gpt55_full_v01_audit_unparseable", unparseable == 0, f"unparseable={unparseable} expected=0"),
        check("vlm_provider_openai_gpt55_full_v01_audit_abstentions", abstentions == 0, f"abstentions={abstentions} expected=0"),
    ])
    return checks


def check_vlm_provider_anthropic_claude_sonnet5_full_v01() -> list[dict]:
    base = resolve_project_path("reports/vlm_provider_anthropic_claude_sonnet_5_full_v01")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    audit_rows = load_csv(base / "audit.csv")

    checks = [
        check(
            "vlm_provider_anthropic_claude_sonnet5_full_v01_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_provider_anthropic_claude_sonnet5_full_v01_recipe_rows",
            len(recipe_rows) == 3,
            f"rows={len(recipe_rows)} expected=3",
        ),
        check(
            "vlm_provider_anthropic_claude_sonnet5_full_v01_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_provider_anthropic_claude_sonnet5_full_v01_audit_rows",
            len(audit_rows) == 210,
            f"rows={len(audit_rows)} expected=210",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_provider_anthropic_claude_sonnet5_full_v01_clean_n",
                row.get("clean_n") == "30",
                f"clean_n={row.get('clean_n')} expected=30",
            ),
            check(
                "vlm_provider_anthropic_claude_sonnet5_full_v01_real_n",
                row.get("real_n") == "180",
                f"real_n={row.get('real_n')} expected=180",
            ),
            check(
                "vlm_provider_anthropic_claude_sonnet5_full_v01_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.933333, tolerance=1e-6),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.933333",
            ),
            check(
                "vlm_provider_anthropic_claude_sonnet5_full_v01_real_accuracy",
                approx(row.get("real_accuracy"), 0.961111, tolerance=1e-6),
                f"real_accuracy={row.get('real_accuracy')} expected=0.961111",
            ),
            check(
                "vlm_provider_anthropic_claude_sonnet5_full_v01_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
            check(
                "vlm_provider_anthropic_claude_sonnet5_full_v01_abstention_rate",
                approx(row.get("real_abstention_rate"), 0.0) and approx(row.get("clean_abstention_rate"), 0.0),
                f"clean={row.get('clean_abstention_rate')} real={row.get('real_abstention_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.extend([
        check(
            "vlm_provider_anthropic_claude_sonnet5_full_v01_whatsapp_accuracy",
            approx(recipe_accuracy.get("messenger_upload_download"), 0.95),
            f"accuracy={recipe_accuracy.get('messenger_upload_download')} expected=0.95",
        ),
        check(
            "vlm_provider_anthropic_claude_sonnet5_full_v01_screenshot_accuracy",
            approx(recipe_accuracy.get("phone_screenshot_resave"), 0.983333, tolerance=1e-6),
            f"accuracy={recipe_accuracy.get('phone_screenshot_resave')} expected=0.983333",
        ),
        check(
            "vlm_provider_anthropic_claude_sonnet5_full_v01_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.95),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.95",
        ),
    ])

    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")
    unparseable = sum(1 for row in audit_rows if row.get("is_unparseable") == "True")
    abstentions = sum(1 for row in audit_rows if row.get("is_abstention") == "True")
    checks.extend([
        check("vlm_provider_anthropic_claude_sonnet5_full_v01_clean_errors", clean_errors == 2, f"clean_errors={clean_errors} expected=2"),
        check("vlm_provider_anthropic_claude_sonnet5_full_v01_real_errors", real_errors == 7, f"real_errors={real_errors} expected=7"),
        check("vlm_provider_anthropic_claude_sonnet5_full_v01_audit_unparseable", unparseable == 0, f"unparseable={unparseable} expected=0"),
        check("vlm_provider_anthropic_claude_sonnet5_full_v01_audit_abstentions", abstentions == 0, f"abstentions={abstentions} expected=0"),
    ])
    return checks


def check_vlm_provider_anthropic_claude_fable5_full_v01() -> list[dict]:
    base = resolve_project_path("reports/vlm_provider_anthropic_claude_fable_5_full_v01")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    audit_rows = load_csv(base / "audit.csv")

    checks = [
        check("vlm_provider_anthropic_claude_fable5_full_v01_summary_rows", len(summary_rows) == 1, f"rows={len(summary_rows)} expected=1"),
        check("vlm_provider_anthropic_claude_fable5_full_v01_recipe_rows", len(recipe_rows) == 3, f"rows={len(recipe_rows)} expected=3"),
        check("vlm_provider_anthropic_claude_fable5_full_v01_label_rows", len(label_rows) == 10, f"rows={len(label_rows)} expected=10"),
        check("vlm_provider_anthropic_claude_fable5_full_v01_audit_rows", len(audit_rows) == 210, f"rows={len(audit_rows)} expected=210"),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check("vlm_provider_anthropic_claude_fable5_full_v01_clean_n", row.get("clean_n") == "30", f"clean_n={row.get('clean_n')} expected=30"),
            check("vlm_provider_anthropic_claude_fable5_full_v01_real_n", row.get("real_n") == "180", f"real_n={row.get('real_n')} expected=180"),
            check("vlm_provider_anthropic_claude_fable5_full_v01_clean_accuracy", approx(row.get("clean_accuracy"), 0.966667, tolerance=1e-6), f"clean_accuracy={row.get('clean_accuracy')} expected=0.966667"),
            check("vlm_provider_anthropic_claude_fable5_full_v01_real_accuracy", approx(row.get("real_accuracy"), 0.961111, tolerance=1e-6), f"real_accuracy={row.get('real_accuracy')} expected=0.961111"),
            check("vlm_provider_anthropic_claude_fable5_full_v01_unparseable_rate", approx(row.get("clean_unparseable_rate"), 0.033333, tolerance=1e-6) and approx(row.get("real_unparseable_rate"), 0.005556, tolerance=1e-6), f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0.033333/0.005556"),
            check("vlm_provider_anthropic_claude_fable5_full_v01_abstention_rate", approx(row.get("real_abstention_rate"), 0.0) and approx(row.get("clean_abstention_rate"), 0.0), f"clean={row.get('clean_abstention_rate')} real={row.get('real_abstention_rate')} expected=0"),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.extend([
        check("vlm_provider_anthropic_claude_fable5_full_v01_whatsapp_accuracy", approx(recipe_accuracy.get("messenger_upload_download"), 0.966667, tolerance=1e-6), f"accuracy={recipe_accuracy.get('messenger_upload_download')} expected=0.966667"),
        check("vlm_provider_anthropic_claude_fable5_full_v01_screenshot_accuracy", approx(recipe_accuracy.get("phone_screenshot_resave"), 0.966667, tolerance=1e-6), f"accuracy={recipe_accuracy.get('phone_screenshot_resave')} expected=0.966667"),
        check("vlm_provider_anthropic_claude_fable5_full_v01_video_call_accuracy", approx(recipe_accuracy.get("video_call_frame_capture"), 0.95), f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.95"),
    ])

    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")
    unparseable = sum(1 for row in audit_rows if row.get("is_unparseable") == "True")
    abstentions = sum(1 for row in audit_rows if row.get("is_abstention") == "True")
    checks.extend([
        check("vlm_provider_anthropic_claude_fable5_full_v01_clean_errors", clean_errors == 1, f"clean_errors={clean_errors} expected=1"),
        check("vlm_provider_anthropic_claude_fable5_full_v01_real_errors", real_errors == 7, f"real_errors={real_errors} expected=7"),
        check("vlm_provider_anthropic_claude_fable5_full_v01_audit_unparseable", unparseable == 2, f"unparseable={unparseable} expected=2"),
        check("vlm_provider_anthropic_claude_fable5_full_v01_audit_abstentions", abstentions == 0, f"abstentions={abstentions} expected=0"),
    ])
    return checks


def check_vlm_provider_anthropic_claude_haiku45_full_v01() -> list[dict]:
    base = resolve_project_path("reports/vlm_provider_anthropic_claude_haiku_4_5_full_v01")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    audit_rows = load_csv(base / "audit.csv")

    checks = [
        check("vlm_provider_anthropic_claude_haiku45_full_v01_summary_rows", len(summary_rows) == 1, f"rows={len(summary_rows)} expected=1"),
        check("vlm_provider_anthropic_claude_haiku45_full_v01_recipe_rows", len(recipe_rows) == 3, f"rows={len(recipe_rows)} expected=3"),
        check("vlm_provider_anthropic_claude_haiku45_full_v01_label_rows", len(label_rows) == 10, f"rows={len(label_rows)} expected=10"),
        check("vlm_provider_anthropic_claude_haiku45_full_v01_audit_rows", len(audit_rows) == 210, f"rows={len(audit_rows)} expected=210"),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check("vlm_provider_anthropic_claude_haiku45_full_v01_clean_n", row.get("clean_n") == "30", f"clean_n={row.get('clean_n')} expected=30"),
            check("vlm_provider_anthropic_claude_haiku45_full_v01_real_n", row.get("real_n") == "180", f"real_n={row.get('real_n')} expected=180"),
            check("vlm_provider_anthropic_claude_haiku45_full_v01_clean_accuracy", approx(row.get("clean_accuracy"), 0.933333, tolerance=1e-6), f"clean_accuracy={row.get('clean_accuracy')} expected=0.933333"),
            check("vlm_provider_anthropic_claude_haiku45_full_v01_real_accuracy", approx(row.get("real_accuracy"), 0.95), f"real_accuracy={row.get('real_accuracy')} expected=0.95"),
            check("vlm_provider_anthropic_claude_haiku45_full_v01_unparseable_rate", approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0), f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0"),
            check("vlm_provider_anthropic_claude_haiku45_full_v01_abstention_rate", approx(row.get("real_abstention_rate"), 0.0) and approx(row.get("clean_abstention_rate"), 0.0), f"clean={row.get('clean_abstention_rate')} real={row.get('real_abstention_rate')} expected=0"),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.extend([
        check("vlm_provider_anthropic_claude_haiku45_full_v01_whatsapp_accuracy", approx(recipe_accuracy.get("messenger_upload_download"), 0.95), f"accuracy={recipe_accuracy.get('messenger_upload_download')} expected=0.95"),
        check("vlm_provider_anthropic_claude_haiku45_full_v01_screenshot_accuracy", approx(recipe_accuracy.get("phone_screenshot_resave"), 0.966667, tolerance=1e-6), f"accuracy={recipe_accuracy.get('phone_screenshot_resave')} expected=0.966667"),
        check("vlm_provider_anthropic_claude_haiku45_full_v01_video_call_accuracy", approx(recipe_accuracy.get("video_call_frame_capture"), 0.933333, tolerance=1e-6), f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.933333"),
    ])

    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")
    unparseable = sum(1 for row in audit_rows if row.get("is_unparseable") == "True")
    abstentions = sum(1 for row in audit_rows if row.get("is_abstention") == "True")
    checks.extend([
        check("vlm_provider_anthropic_claude_haiku45_full_v01_clean_errors", clean_errors == 2, f"clean_errors={clean_errors} expected=2"),
        check("vlm_provider_anthropic_claude_haiku45_full_v01_real_errors", real_errors == 9, f"real_errors={real_errors} expected=9"),
        check("vlm_provider_anthropic_claude_haiku45_full_v01_audit_unparseable", unparseable == 0, f"unparseable={unparseable} expected=0"),
        check("vlm_provider_anthropic_claude_haiku45_full_v01_audit_abstentions", abstentions == 0, f"abstentions={abstentions} expected=0"),
    ])
    return checks


def check_vlm_provider_xai_grok43_full_v01() -> list[dict]:
    base = resolve_project_path("reports/vlm_provider_xai_grok_4_3_full_v01")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    audit_rows = load_csv(base / "audit.csv")

    checks = [
        check(
            "vlm_provider_xai_grok43_full_v01_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_provider_xai_grok43_full_v01_recipe_rows",
            len(recipe_rows) == 3,
            f"rows={len(recipe_rows)} expected=3",
        ),
        check(
            "vlm_provider_xai_grok43_full_v01_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_provider_xai_grok43_full_v01_audit_rows",
            len(audit_rows) == 210,
            f"rows={len(audit_rows)} expected=210",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_provider_xai_grok43_full_v01_clean_n",
                row.get("clean_n") == "30",
                f"clean_n={row.get('clean_n')} expected=30",
            ),
            check(
                "vlm_provider_xai_grok43_full_v01_real_n",
                row.get("real_n") == "180",
                f"real_n={row.get('real_n')} expected=180",
            ),
            check(
                "vlm_provider_xai_grok43_full_v01_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.966667, tolerance=1e-6),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.966667",
            ),
            check(
                "vlm_provider_xai_grok43_full_v01_real_accuracy",
                approx(row.get("real_accuracy"), 0.983333, tolerance=1e-6),
                f"real_accuracy={row.get('real_accuracy')} expected=0.983333",
            ),
            check(
                "vlm_provider_xai_grok43_full_v01_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
            check(
                "vlm_provider_xai_grok43_full_v01_abstention_rate",
                approx(row.get("real_abstention_rate"), 0.0) and approx(row.get("clean_abstention_rate"), 0.0),
                f"clean={row.get('clean_abstention_rate')} real={row.get('real_abstention_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.extend([
        check(
            "vlm_provider_xai_grok43_full_v01_whatsapp_accuracy",
            approx(recipe_accuracy.get("messenger_upload_download"), 1.0),
            f"accuracy={recipe_accuracy.get('messenger_upload_download')} expected=1.0",
        ),
        check(
            "vlm_provider_xai_grok43_full_v01_screenshot_accuracy",
            approx(recipe_accuracy.get("phone_screenshot_resave"), 0.966667, tolerance=1e-6),
            f"accuracy={recipe_accuracy.get('phone_screenshot_resave')} expected=0.966667",
        ),
        check(
            "vlm_provider_xai_grok43_full_v01_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.983333, tolerance=1e-6),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.983333",
        ),
    ])

    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")
    unparseable = sum(1 for row in audit_rows if row.get("is_unparseable") == "True")
    abstentions = sum(1 for row in audit_rows if row.get("is_abstention") == "True")
    checks.extend([
        check("vlm_provider_xai_grok43_full_v01_clean_errors", clean_errors == 1, f"clean_errors={clean_errors} expected=1"),
        check("vlm_provider_xai_grok43_full_v01_real_errors", real_errors == 3, f"real_errors={real_errors} expected=3"),
        check("vlm_provider_xai_grok43_full_v01_audit_unparseable", unparseable == 0, f"unparseable={unparseable} expected=0"),
        check("vlm_provider_xai_grok43_full_v01_audit_abstentions", abstentions == 0, f"abstentions={abstentions} expected=0"),
    ])
    return checks


def check_vlm_provider_xai_grok43_full_v03() -> list[dict]:
    base = resolve_project_path("reports/vlm_provider_xai_grok_4_3_full_v03")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    audit_rows = load_csv(base / "audit.csv")

    checks = [
        check(
            "vlm_provider_xai_grok43_full_v03_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_recipe_rows",
            len(recipe_rows) == 4,
            f"rows={len(recipe_rows)} expected=4",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_audit_rows",
            len(audit_rows) == 900,
            f"rows={len(audit_rows)} expected=900",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_provider_xai_grok43_full_v03_clean_n",
                row.get("clean_n") == "100",
                f"clean_n={row.get('clean_n')} expected=100",
            ),
            check(
                "vlm_provider_xai_grok43_full_v03_real_n",
                row.get("real_n") == "800",
                f"real_n={row.get('real_n')} expected=800",
            ),
            check(
                "vlm_provider_xai_grok43_full_v03_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.99),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.99",
            ),
            check(
                "vlm_provider_xai_grok43_full_v03_real_accuracy",
                approx(row.get("real_accuracy"), 0.97875),
                f"real_accuracy={row.get('real_accuracy')} expected=0.97875",
            ),
            check(
                "vlm_provider_xai_grok43_full_v03_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
            check(
                "vlm_provider_xai_grok43_full_v03_abstention_rate",
                approx(row.get("real_abstention_rate"), 0.0) and approx(row.get("clean_abstention_rate"), 0.0),
                f"clean={row.get('clean_abstention_rate')} real={row.get('real_abstention_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.extend([
        check(
            "vlm_provider_xai_grok43_full_v03_whatsapp_accuracy",
            approx(recipe_accuracy.get("messenger_upload_download"), 0.995),
            f"accuracy={recipe_accuracy.get('messenger_upload_download')} expected=0.995",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_screenshot_accuracy",
            approx(recipe_accuracy.get("phone_screenshot_resave"), 0.98),
            f"accuracy={recipe_accuracy.get('phone_screenshot_resave')} expected=0.98",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_social_accuracy",
            approx(recipe_accuracy.get("social_app_resave"), 0.99),
            f"accuracy={recipe_accuracy.get('social_app_resave')} expected=0.99",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.95),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.95",
        ),
    ])

    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")
    unparseable = sum(1 for row in audit_rows if row.get("is_unparseable") == "True")
    abstentions = sum(1 for row in audit_rows if row.get("is_abstention") == "True")
    checks.extend([
        check("vlm_provider_xai_grok43_full_v03_clean_errors", clean_errors == 1, f"clean_errors={clean_errors} expected=1"),
        check("vlm_provider_xai_grok43_full_v03_real_errors", real_errors == 17, f"real_errors={real_errors} expected=17"),
        check("vlm_provider_xai_grok43_full_v03_audit_unparseable", unparseable == 0, f"unparseable={unparseable} expected=0"),
        check("vlm_provider_xai_grok43_full_v03_audit_abstentions", abstentions == 0, f"abstentions={abstentions} expected=0"),
    ])
    return checks


def check_vlm_provider_xai_grok43_full_v03_repeat_01() -> list[dict]:
    base = resolve_project_path("reports/vlm_provider_xai_grok_4_3_full_v03_repeat_01")
    summary_rows = load_csv(base / "model_summary.csv")
    recipe_rows = load_csv(base / "recipe_table.csv")
    label_rows = load_csv(base / "label_table.csv")
    audit_rows = load_csv(base / "audit.csv")

    checks = [
        check(
            "vlm_provider_xai_grok43_full_v03_repeat01_summary_rows",
            len(summary_rows) == 1,
            f"rows={len(summary_rows)} expected=1",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_repeat01_recipe_rows",
            len(recipe_rows) == 4,
            f"rows={len(recipe_rows)} expected=4",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_repeat01_label_rows",
            len(label_rows) == 10,
            f"rows={len(label_rows)} expected=10",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_repeat01_audit_rows",
            len(audit_rows) == 900,
            f"rows={len(audit_rows)} expected=900",
        ),
    ]

    if summary_rows:
        row = summary_rows[0]
        checks.extend([
            check(
                "vlm_provider_xai_grok43_full_v03_repeat01_clean_n",
                row.get("clean_n") == "100",
                f"clean_n={row.get('clean_n')} expected=100",
            ),
            check(
                "vlm_provider_xai_grok43_full_v03_repeat01_real_n",
                row.get("real_n") == "800",
                f"real_n={row.get('real_n')} expected=800",
            ),
            check(
                "vlm_provider_xai_grok43_full_v03_repeat01_clean_accuracy",
                approx(row.get("clean_accuracy"), 0.97),
                f"clean_accuracy={row.get('clean_accuracy')} expected=0.97",
            ),
            check(
                "vlm_provider_xai_grok43_full_v03_repeat01_real_accuracy",
                approx(row.get("real_accuracy"), 0.97875),
                f"real_accuracy={row.get('real_accuracy')} expected=0.97875",
            ),
            check(
                "vlm_provider_xai_grok43_full_v03_repeat01_unparseable_rate",
                approx(row.get("real_unparseable_rate"), 0.0) and approx(row.get("clean_unparseable_rate"), 0.0),
                f"clean={row.get('clean_unparseable_rate')} real={row.get('real_unparseable_rate')} expected=0",
            ),
            check(
                "vlm_provider_xai_grok43_full_v03_repeat01_abstention_rate",
                approx(row.get("real_abstention_rate"), 0.0) and approx(row.get("clean_abstention_rate"), 0.0),
                f"clean={row.get('clean_abstention_rate')} real={row.get('real_abstention_rate')} expected=0",
            ),
        ])

    recipe_accuracy = {row.get("recipe"): row.get("accuracy") for row in recipe_rows}
    checks.extend([
        check(
            "vlm_provider_xai_grok43_full_v03_repeat01_whatsapp_accuracy",
            approx(recipe_accuracy.get("messenger_upload_download"), 0.99),
            f"accuracy={recipe_accuracy.get('messenger_upload_download')} expected=0.99",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_repeat01_screenshot_accuracy",
            approx(recipe_accuracy.get("phone_screenshot_resave"), 0.98),
            f"accuracy={recipe_accuracy.get('phone_screenshot_resave')} expected=0.98",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_repeat01_social_accuracy",
            approx(recipe_accuracy.get("social_app_resave"), 0.99),
            f"accuracy={recipe_accuracy.get('social_app_resave')} expected=0.99",
        ),
        check(
            "vlm_provider_xai_grok43_full_v03_repeat01_video_call_accuracy",
            approx(recipe_accuracy.get("video_call_frame_capture"), 0.955),
            f"accuracy={recipe_accuracy.get('video_call_frame_capture')} expected=0.955",
        ),
    ])

    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")
    unparseable = sum(1 for row in audit_rows if row.get("is_unparseable") == "True")
    abstentions = sum(1 for row in audit_rows if row.get("is_abstention") == "True")
    checks.extend([
        check("vlm_provider_xai_grok43_full_v03_repeat01_clean_errors", clean_errors == 3, f"clean_errors={clean_errors} expected=3"),
        check("vlm_provider_xai_grok43_full_v03_repeat01_real_errors", real_errors == 17, f"real_errors={real_errors} expected=17"),
        check("vlm_provider_xai_grok43_full_v03_repeat01_audit_unparseable", unparseable == 0, f"unparseable={unparseable} expected=0"),
        check("vlm_provider_xai_grok43_full_v03_repeat01_audit_abstentions", abstentions == 0, f"abstentions={abstentions} expected=0"),
    ])
    return checks


def check_vlm_provider_comparison_v01() -> list[dict]:
    rows = load_csv(resolve_project_path("reports/vlm_provider_full_v01_comparison.csv"))
    markdown = resolve_project_path("reports/vlm_provider_full_v01_comparison.md").read_text(encoding="utf-8")
    latex = resolve_project_path("reports/vlm_provider_full_v01_comparison.tex").read_text(encoding="utf-8")
    paper = resolve_project_path("paper/main.tex").read_text(encoding="utf-8")
    by_slug = {row.get("slug"): row for row in rows}
    mini = by_slug.get("openai_gpt_5_4_mini", {})
    gpt54 = by_slug.get("openai_gpt_5_4", {})
    flagship = by_slug.get("openai_gpt_5_5", {})
    grok = by_slug.get("xai_grok_4_3", {})
    claude = by_slug.get("anthropic_claude_sonnet_5", {})
    fable = by_slug.get("anthropic_claude_fable_5", {})
    haiku = by_slug.get("anthropic_claude_haiku_4_5", {})
    gigachat_pro = by_slug.get("gigachat_2_pro", {})
    gigachat_max = by_slug.get("gigachat_2_max", {})
    return [
        check(
            "vlm_provider_comparison_v01_rows",
            len(rows) == 9,
            f"rows={len(rows)} expected=9",
        ),
        check(
            "vlm_provider_comparison_v01_grok_real_accuracy",
            approx(grok.get("real_accuracy"), 0.98333, tolerance=1e-5),
            f"real_accuracy={grok.get('real_accuracy')} expected=0.98333",
        ),
        check(
            "vlm_provider_comparison_v01_openai_real_accuracy",
            approx(mini.get("real_accuracy"), 0.96111, tolerance=1e-5),
            f"real_accuracy={mini.get('real_accuracy')} expected=0.96111",
        ),
        check(
            "vlm_provider_comparison_v01_gpt54_real_accuracy",
            approx(gpt54.get("real_accuracy"), 0.95556, tolerance=1e-5),
            f"real_accuracy={gpt54.get('real_accuracy')} expected=0.95556",
        ),
        check(
            "vlm_provider_comparison_v01_gpt55_real_accuracy",
            approx(flagship.get("real_accuracy"), 0.95),
            f"real_accuracy={flagship.get('real_accuracy')} expected=0.95",
        ),
        check(
            "vlm_provider_comparison_v01_claude_real_accuracy",
            approx(claude.get("real_accuracy"), 0.96111, tolerance=1e-5),
            f"real_accuracy={claude.get('real_accuracy')} expected=0.96111",
        ),
        check(
            "vlm_provider_comparison_v01_fable_real_accuracy",
            approx(fable.get("real_accuracy"), 0.96111, tolerance=1e-5),
            f"real_accuracy={fable.get('real_accuracy')} expected=0.96111",
        ),
        check(
            "vlm_provider_comparison_v01_haiku_real_accuracy",
            approx(haiku.get("real_accuracy"), 0.95),
            f"real_accuracy={haiku.get('real_accuracy')} expected=0.95",
        ),
        check(
            "vlm_provider_comparison_v01_gigachat_max_real_accuracy",
            approx(gigachat_max.get("real_accuracy"), 0.87778, tolerance=1e-5),
            f"real_accuracy={gigachat_max.get('real_accuracy')} expected=0.87778",
        ),
        check(
            "vlm_provider_comparison_v01_gigachat_pro_real_accuracy",
            approx(gigachat_pro.get("real_accuracy"), 0.87778, tolerance=1e-5),
            f"real_accuracy={gigachat_pro.get('real_accuracy')} expected=0.87778",
        ),
        check(
            "vlm_provider_comparison_v01_openai_hardest_pipeline",
            mini.get("hardest_pipeline") == "video_call_frame_capture"
            and gpt54.get("hardest_pipeline") in {"phone_screenshot_resave", "video_call_frame_capture"}
            and flagship.get("hardest_pipeline") == "video_call_frame_capture",
            f"hardest_pipeline={[row.get('hardest_pipeline') for row in rows]} expected known OpenAI provider pipelines",
        ),
        check(
            "vlm_provider_comparison_v01_openai_hardest_label",
            mini.get("hardest_label") == "calcium_bottle"
            and gpt54.get("hardest_label") == "calcium_bottle"
            and flagship.get("hardest_label") == "calcium_bottle",
            f"hardest_label={[row.get('hardest_label') for row in rows]} expected=calcium_bottle",
        ),
        check(
            "vlm_provider_comparison_v01_claude_hardest_label",
            claude.get("hardest_label") == "calcium_bottle",
            f"hardest_label={claude.get('hardest_label')} expected=calcium_bottle",
        ),
        check(
            "vlm_provider_comparison_v01_anthropic_hardest_label",
            fable.get("hardest_label") == "calcium_bottle"
            and haiku.get("hardest_label") == "calcium_bottle",
            f"hardest_label fable={fable.get('hardest_label')} haiku={haiku.get('hardest_label')} expected=calcium_bottle",
        ),
        check(
            "vlm_provider_comparison_v01_grok_hardest_label",
            grok.get("hardest_label") == "lg_cell_phone",
            f"hardest_label={grok.get('hardest_label')} expected=lg_cell_phone",
        ),
        check(
            "vlm_provider_comparison_v01_gigachat_hardest_label",
            gigachat_max.get("hardest_label") == "canon_camera"
            and gigachat_pro.get("hardest_label") == "canon_camera",
            f"hardest_label max={gigachat_max.get('hardest_label')} pro={gigachat_pro.get('hardest_label')} expected=canon_camera",
        ),
        check(
            "vlm_provider_comparison_v01_markdown",
            "xAI Grok 4.3" in markdown
            and "OpenAI GPT-5.4-mini" in markdown
            and "OpenAI GPT-5.4" in markdown
            and "OpenAI GPT-5.5" in markdown
            and "Anthropic Claude Sonnet 5" in markdown
            and "Anthropic Claude Fable 5" in markdown
            and "Anthropic Claude Haiku 4.5" in markdown
            and "GigaChat 2 Pro" in markdown
            and "GigaChat 2 Max" in markdown
            and "0.9833" in markdown
            and "0.9611" in markdown
            and "0.9556" in markdown
            and "0.9500" in markdown
            and "0.8778" in markdown,
            "missing expected model/result in markdown comparison",
        ),
        check(
            "vlm_provider_comparison_v01_latex_label",
            r"\label{tab:vlm-provider-full-v01}" in latex,
            "missing latex table label",
        ),
        check(
            "vlm_provider_comparison_v01_paper_input",
            r"\input{../reports/vlm_provider_full_v01_comparison.tex}" in paper,
            "paper/main.tex does not input provider VLM table",
        ),
    ]


def check_vlm_provider_comparison_v03() -> list[dict]:
    rows = load_csv(resolve_project_path("reports/vlm_provider_full_v03_comparison.csv"))
    markdown = resolve_project_path("reports/vlm_provider_full_v03_comparison.md").read_text(encoding="utf-8")
    latex = resolve_project_path("reports/vlm_provider_full_v03_comparison.tex").read_text(encoding="utf-8")
    paper = resolve_project_path("paper/main.tex").read_text(encoding="utf-8")
    by_slug = {row.get("slug"): row for row in rows}
    grok = by_slug.get("xai_grok_4_3", {})
    return [
        check(
            "vlm_provider_comparison_v03_rows",
            len(rows) == 1,
            f"rows={len(rows)} expected=1",
        ),
        check(
            "vlm_provider_comparison_v03_grok_real_accuracy",
            approx(grok.get("real_accuracy"), 0.97875),
            f"real_accuracy={grok.get('real_accuracy')} expected=0.97875",
        ),
        check(
            "vlm_provider_comparison_v03_grok_video_accuracy",
            approx(grok.get("video_call_frame_capture_accuracy"), 0.95),
            f"video_call_frame_capture_accuracy={grok.get('video_call_frame_capture_accuracy')} expected=0.95",
        ),
        check(
            "vlm_provider_comparison_v03_grok_hardest_label",
            grok.get("hardest_label") == "toy",
            f"hardest_label={grok.get('hardest_label')} expected=toy",
        ),
        check(
            "vlm_provider_comparison_v03_markdown",
            "xAI Grok 4.3" in markdown and "0.9788" in markdown and "video_call_frame_capture" in markdown,
            "missing expected model/result in markdown comparison",
        ),
        check(
            "vlm_provider_comparison_v03_latex_label",
            r"\label{tab:vlm-provider-full-v03}" in latex,
            "missing latex table label",
        ),
        check(
            "vlm_provider_comparison_v03_paper_input",
            r"\input{../reports/vlm_provider_full_v03_comparison.tex}" in paper,
            "paper/main.tex does not input provider VLM v0.3 table",
        ),
    ]


def check_forbidden_public_strings() -> list[dict]:
    files = []
    for base in TEXT_SCAN_PATHS:
        path = resolve_project_path(base)
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(item for item in path.rglob("*") if item.is_file() and item.suffix.lower() in {".md", ".tex", ".py", ".json", ".csv"})
    files = [path for path in files if relative_text(path) != "reports/release_check_v04.json"]

    checks = []
    for label, forbidden in FORBIDDEN_PUBLIC_STRINGS.items():
        hits = []
        for path in files:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if forbidden in text:
                hits.append(relative_text(path))
        checks.append(check(f"forbidden_string:{label}", not hits, f"hits={hits[:10]}"))
    return checks


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def check(name: str, passed: bool, detail: str) -> dict:
    return {"name": name, "passed": bool(passed), "detail": detail}


def approx(value: str | None, expected: float, tolerance: float = 1e-9) -> bool:
    if value is None or value == "":
        return False
    return abs(float(value) - expected) <= tolerance


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def relative_text(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
