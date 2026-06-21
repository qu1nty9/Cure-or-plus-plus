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
    "reports/real_transfer_v02_activation_status.json",
    "results/real_transfer_v02_source_matched_drops.png",
    "results/real_transfer_v02_accuracy_heatmap.png",
    "paper/main.tex",
    "docs/dataset_card_cure_or_pp_v04.md",
    "docs/evaluation_card_full_cure_or_v04.md",
    "reports/arxiv_readiness_matrix_v04.md",
    "configs/vlm_api_track_v01.json",
    "configs/vlm_open_weight_model_matrix_v01.json",
    "docs/vlm_api_track_plan_v01.md",
    "docs/vlm_open_weight_model_matrix_v01.md",
    "reports/vlm_api_track_v01_prompt_pack.jsonl",
    "reports/vlm_api_track_v01_prompt_pack_summary.json",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v01/summary.md",
    "reports/vlm_open_weight_matrix_smoke_kaggle_v01/model_summary.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/summary.md",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/model_summary.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/recipe_table.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/label_table.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/audit.csv",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/responses.jsonl",
    "reports/vlm_open_weight_internvl3_1b_kaggle_v01/kaggle_kernel.log",
    "scripts/build_vlm_prompt_pack.py",
    "scripts/run_openai_compatible_vlm.py",
    "scripts/run_gemini_vlm.py",
    "scripts/run_hf_vlm.py",
    "scripts/evaluate_vlm_response_pack.py",
    "scripts/build_kaggle_vlm_package.py",
    "scripts/write_kaggle_vlm_notebook.py",
    "scripts/check_paper_build.py",
    "notebooks/cure_or_pp_vlm_open_weight_kaggle_v01.ipynb",
    "kaggle/vlm_kernel/cure_or_pp_vlm_open_weight_kaggle_v01.ipynb",
    "kaggle/vlm_kernel/kernel-metadata.json",
]

SUMMARY_FILES = [
    "results/clip_vit_b16_real_transfer_v02_summary.csv",
    "results/clip_vit_b32_real_transfer_v02_summary.csv",
    "results/openclip_vit_b32_laion2b_real_transfer_v02_summary.csv",
    "results/openclip_vit_b16_datacomp_xl_real_transfer_v02_summary.csv",
]

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
    return checks


def check_summary_files() -> list[dict]:
    checks = []
    for path_text in SUMMARY_FILES:
        rows = load_csv(resolve_project_path(path_text))
        checks.append(check(f"summary_rows:{path_text}", len(rows) == 4, f"rows={len(rows)} expected=4"))
    return checks


def check_paper_links() -> list[dict]:
    paper = resolve_project_path("paper/main.tex").read_text(encoding="utf-8")
    required = [
        "real_transfer_v02_source_matched_drops.png",
        "real_transfer_v02_accuracy_heatmap.png",
        "source-level bootstrap confidence intervals",
        "SmolVLM2-500M",
        "InternVL3-1B",
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
    summary_path = resolve_project_path("reports/vlm_api_track_v01_prompt_pack_summary.json")
    pack_path = resolve_project_path("reports/vlm_api_track_v01_prompt_pack.jsonl")
    if not summary_path.exists() or not pack_path.exists():
        return [check("vlm_prompt_pack", False, "missing prompt pack or summary")]

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    prompt_rows = load_jsonl(pack_path)
    checks = [
        check("vlm_prompt_pack_rows", len(prompt_rows) == 210, f"rows={len(prompt_rows)} expected=210"),
        check("vlm_prompt_pack_summary_rows", summary.get("row_count") == 210, f"row_count={summary.get('row_count')} expected=210"),
        check("vlm_prompt_pack_clean_rows", summary.get("family_counts", {}).get("clean") == 30, f"clean={summary.get('family_counts', {}).get('clean')} expected=30"),
        check("vlm_prompt_pack_real_rows", summary.get("family_counts", {}).get("real_transfer") == 180, f"real_transfer={summary.get('family_counts', {}).get('real_transfer')} expected=180"),
        check("vlm_prompt_pack_option_count", summary.get("option_count") == 10, f"option_count={summary.get('option_count')} expected=10"),
    ]
    required_fields = {"sample_id", "image_path", "label", "answer_letter", "prompt", "options"}
    present_fields = set(prompt_rows[0].keys()) if prompt_rows else set()
    checks.append(check("vlm_prompt_pack_fields", required_fields.issubset(present_fields), f"missing={sorted(required_fields - present_fields)}"))
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
