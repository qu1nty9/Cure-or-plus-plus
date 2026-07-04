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
    "reports/full_cure_or_paper_tables_v04.md",
    "reports/full_cure_or_paper_tables_v04.tex",
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
    "paper/main.tex",
    "docs/dataset_card_cure_or_pp_v04.md",
    "docs/evaluation_card_full_cure_or_v04.md",
    "reports/arxiv_readiness_matrix_v04.md",
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
    "scripts/run_hf_vlm.py",
    "scripts/integrate_kaggle_vlm_output.py",
    "scripts/build_vlm_open_weight_full_comparison.py",
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
    "docs",
    "paper",
    "reports",
    "scripts",
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
    checks.extend(check_vlm_open_weight_smoke_v03())
    checks.extend(check_vlm_open_weight_qwen3b_full_v03())
    checks.extend(check_vlm_open_weight_qwen_full_v03())
    checks.extend(check_vlm_open_weight_internvl3_1b_full_v03())
    checks.extend(check_vlm_open_weight_internvl3_2b_full_v03())
    checks.extend(check_vlm_open_weight_llava_05b_full_v03())
    checks.extend(check_vlm_open_weight_llava_full_v03())
    checks.extend(check_vlm_open_weight_smolvlm2_full_v03())
    checks.extend(check_vlm_open_weight_full_comparison_v03())
    checks.extend(check_vlm_open_weight_7b_comparison_v03())
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
