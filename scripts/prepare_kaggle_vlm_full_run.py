#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OWNER = "yaroslavkholmirzayev"
DEFAULT_KERNEL_SLUG = "cure-or-open-weight-vlm-real-transfer-gpu-pilot"
DEFAULT_DATASET_SLUG = "cure-or-pp-vlm-real-transfer-v03-private"
DEFAULT_MODEL_MATRIX = "configs/vlm_open_weight_model_matrix_v03.json"
DEFAULT_NOTEBOOK = "notebooks/cure-or-open-weight-vlm-real-transfer-gpu-pilot.ipynb"
DEFAULT_KAGGLE_DIR = "kaggle/vlm_kernel_v03"

EXPECTED_ARTIFACTS = [
    "{run_root}/{slug}/responses.jsonl",
    "{run_root}/{slug}/model_summary.csv",
    "{run_root}/{slug}/recipe_table.csv",
    "{run_root}/{slug}/label_table.csv",
    "{run_root}/{slug}/audit.csv",
    "{run_root}/combined_model_summary.csv",
    "{run_root}/combined_recipe_table.csv",
    "{run_root}/combined_label_table.csv",
    "{run_root}/run_manifest.csv",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a single-model Kaggle full v0.3 VLM run.")
    parser.add_argument("--slug", required=True, help="Model slug from configs/vlm_open_weight_model_matrix_v03.json.")
    parser.add_argument("--kernel-version", type=int, help="Known Kaggle kernel version after push.")
    parser.add_argument("--status-at-launch", default="PREPARED", help="Launch-note status, e.g. PREPARED, RUNNING.")
    parser.add_argument("--model-matrix", default=DEFAULT_MODEL_MATRIX)
    parser.add_argument("--dataset-slug", default=DEFAULT_DATASET_SLUG)
    parser.add_argument("--kaggle-owner", default=DEFAULT_OWNER)
    parser.add_argument("--kernel-slug", default=DEFAULT_KERNEL_SLUG)
    parser.add_argument("--notebook-path", default=DEFAULT_NOTEBOOK)
    parser.add_argument("--kaggle-dir", default=DEFAULT_KAGGLE_DIR)
    parser.add_argument("--title", default="CURE-OR++ Open-Weight VLM Real-Transfer GPU Pilot")
    parser.add_argument("--result-dir", default="")
    parser.add_argument("--no-update-matrix", action="store_true")
    args = parser.parse_args()

    matrix_path = resolve_path(args.model_matrix)
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    model = find_model(matrix, args.slug)
    prompt_pack = matrix["prompt_pack_path"]
    result_dir = resolve_path(args.result_dir or f"reports/vlm_open_weight_{args.slug}_kaggle_full_v03")

    write_notebook(args=args, prompt_pack=prompt_pack)
    write_launch_note(
        result_dir=result_dir,
        args=args,
        matrix=matrix,
        model=model,
        prompt_pack=prompt_pack,
    )
    if not args.no_update_matrix:
        update_matrix(
            matrix=matrix,
            matrix_path=matrix_path,
            slug=args.slug,
            result_dir=result_dir,
            kernel_version=args.kernel_version,
        )

    print(f"Prepared full v0.3 Kaggle run for {args.slug}")
    print(f"Notebook: {resolve_path(args.notebook_path)}")
    print(f"Kaggle dir: {resolve_path(args.kaggle_dir)}")
    print(f"Launch note: {result_dir / 'launch.md'}")
    return 0


def write_notebook(*, args: argparse.Namespace, prompt_pack: str) -> None:
    command = [
        sys.executable,
        str(ROOT / "scripts/write_kaggle_vlm_notebook.py"),
        "--kaggle-owner",
        args.kaggle_owner,
        "--kernel-slug",
        args.kernel_slug,
        "--dataset-slug",
        args.dataset_slug,
        "--title",
        args.title,
        "--run-mode",
        "full",
        "--selected-model-slug",
        args.slug,
        "--model-matrix",
        args.model_matrix,
        "--prompt-pack",
        prompt_pack,
        "--notebook-path",
        args.notebook_path,
        "--kaggle-dir",
        args.kaggle_dir,
        "--no-embed-runtime",
    ]
    subprocess.run(command, cwd=ROOT, check=True)


def write_launch_note(
    *,
    result_dir: Path,
    args: argparse.Namespace,
    matrix: dict,
    model: dict,
    prompt_pack: str,
) -> None:
    result_dir.mkdir(parents=True, exist_ok=True)
    run_root = "vlm_open_weight_runs/full"
    kernel_text = str(args.kernel_version) if args.kernel_version is not None else "TBD after push"
    lines = [
        f"# {model['slug']} Full v0.3 Run Launch",
        "",
        "## Launch",
        "",
        f"- Kaggle notebook: `{args.kaggle_owner}/{args.kernel_slug}`",
        f"- Kaggle kernel version: {kernel_text}",
        f"- Status at launch check: `{args.status_at_launch}`",
        f"- Model: `{model['model_id']}`",
        f"- Prompt pack: `{prompt_pack}`",
        "- Run mode: full",
        f"- Expected rows: {matrix.get('full_limit', 900)} total, 100 clean and 800 real-transfer",
        f"- Dataset source: `{args.kaggle_owner}/{args.dataset_slug}`",
        "- Result cache location in Kaggle runtime: `/kaggle/temp/cure_or_pp_vlm_cache/full`",
        "",
        "## Expected Artifacts",
        "",
        "When complete, the Kaggle output should contain:",
        "",
    ]
    lines.extend(f"- `{item.format(run_root=run_root, slug=model['slug'])}`" for item in EXPECTED_ARTIFACTS)
    lines.extend([
        "",
        "## Integration Command",
        "",
        "After Kaggle reports `COMPLETE`, download the output and run:",
        "",
        "```bash",
        f".venv/bin/python scripts/integrate_kaggle_vlm_output.py \\",
        "  --download-dir /private/tmp/cure_or_v03_output \\",
        f"  --slug {model['slug']} \\",
        f"  --result-dir {relative_text(result_dir)} \\",
        f"  --kernel-version {kernel_text} \\",
        "  --update-matrix",
        "",
        ".venv/bin/python scripts/build_vlm_open_weight_full_comparison.py",
        ".venv/bin/python scripts/run_release_checks.py",
        "```",
        "",
    ])
    (result_dir / "launch.md").write_text("\n".join(lines), encoding="utf-8")


def update_matrix(
    *,
    matrix: dict,
    matrix_path: Path,
    slug: str,
    result_dir: Path,
    kernel_version: int | None,
) -> None:
    model = find_model(matrix, slug)
    if kernel_version is not None:
        model["status"] = f"v03_full_running_kaggle_v{kernel_version}"
        model["active_v03_full_kernel_version"] = kernel_version
    else:
        model["status"] = "v03_full_prepared_for_kaggle_push"
        model.pop("active_v03_full_kernel_version", None)
    model["planned_v03_full_result_dir"] = relative_text(result_dir)
    matrix_path.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")


def find_model(matrix: dict, slug: str) -> dict:
    for model in matrix.get("models", []):
        if model.get("slug") == slug:
            return model
    raise ValueError(f"Unknown model slug: {slug}")


def resolve_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def relative_text(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
