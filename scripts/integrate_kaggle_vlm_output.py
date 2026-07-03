#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import shutil
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODEL_FILES = [
    "responses.jsonl",
    "model_summary.csv",
    "recipe_table.csv",
    "label_table.csv",
    "audit.csv",
]
COMBINED_FILES = [
    "combined_model_summary.csv",
    "combined_recipe_table.csv",
    "combined_label_table.csv",
    "run_manifest.csv",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Integrate downloaded Kaggle VLM output into local reports.")
    parser.add_argument("--download-dir", required=True, help="Directory passed to `kaggle kernels output -p`.")
    parser.add_argument("--slug", required=True, help="Model slug, e.g. smolvlm2_2b.")
    parser.add_argument("--result-dir", required=True, help="Local report directory to populate.")
    parser.add_argument("--run-mode", default="full", choices=["smoke", "full"])
    parser.add_argument("--model-matrix", default="configs/vlm_open_weight_model_matrix_v03.json")
    parser.add_argument("--kernel-version", type=int)
    parser.add_argument("--expected-responses", type=int, default=900)
    parser.add_argument("--expected-clean", type=int, default=100)
    parser.add_argument("--expected-real", type=int, default=800)
    parser.add_argument("--expected-recipes", type=int, default=4)
    parser.add_argument("--expected-labels", type=int, default=10)
    parser.add_argument("--update-matrix", action="store_true")
    args = parser.parse_args()

    download_dir = resolve_path(args.download_dir)
    result_dir = resolve_path(args.result_dir)
    output_root = find_output_root(download_dir, args.run_mode)
    model_dir = output_root / args.slug
    if not model_dir.exists():
        raise FileNotFoundError(f"Missing model output directory: {model_dir}")

    copied = copy_artifacts(
        output_root=output_root,
        model_dir=model_dir,
        result_dir=result_dir,
        download_dir=download_dir,
    )
    validation = validate_result_dir(
        result_dir=result_dir,
        slug=args.slug,
        expected_responses=args.expected_responses,
        expected_clean=args.expected_clean,
        expected_real=args.expected_real,
        expected_recipes=args.expected_recipes,
        expected_labels=args.expected_labels,
    )
    write_summary(
        result_dir=result_dir,
        slug=args.slug,
        validation=validation,
        kernel_version=args.kernel_version,
    )
    if args.update_matrix:
        update_model_matrix(
            matrix_path=resolve_path(args.model_matrix),
            slug=args.slug,
            result_dir=result_dir,
            kernel_version=args.kernel_version,
        )

    print(f"Integrated {args.slug} from {output_root}")
    print(f"Result dir: {result_dir}")
    print(f"Copied files: {len(copied)}")
    print(f"Responses: {validation['response_count']}")
    return 0


def find_output_root(download_dir: Path, run_mode: str) -> Path:
    candidates = [
        download_dir / "vlm_open_weight_runs" / run_mode,
        download_dir / "working" / "vlm_open_weight_runs" / run_mode,
        download_dir / "kaggle" / "working" / "vlm_open_weight_runs" / run_mode,
        download_dir / run_mode,
    ]
    for candidate in candidates:
        if (candidate / "combined_model_summary.csv").exists() or any(candidate.glob("*/responses.jsonl")):
            return candidate
    raise FileNotFoundError(f"Could not find vlm_open_weight_runs/{run_mode} under {download_dir}")


def copy_artifacts(*, output_root: Path, model_dir: Path, result_dir: Path, download_dir: Path) -> list[Path]:
    result_dir.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for name in MODEL_FILES:
        copied.append(copy_required(model_dir / name, result_dir / name))
    for name in COMBINED_FILES:
        copied.append(copy_required(output_root / name, result_dir / name))

    log_files = sorted(download_dir.glob("*.log")) + sorted(download_dir.rglob("*.log"))
    unique_logs = []
    seen = set()
    for path in log_files:
        if path in seen:
            continue
        seen.add(path)
        unique_logs.append(path)
    if unique_logs:
        primary_log = unique_logs[0]
        copied.append(copy_required(primary_log, result_dir / "kaggle_kernel.log"))
        if primary_log.name != "kaggle_kernel.log":
            copied.append(copy_required(primary_log, result_dir / primary_log.name))
    return copied


def copy_required(source: Path, target: Path) -> Path:
    if not source.exists():
        raise FileNotFoundError(source)
    shutil.copy2(source, target)
    return target


def validate_result_dir(
    *,
    result_dir: Path,
    slug: str,
    expected_responses: int,
    expected_clean: int,
    expected_real: int,
    expected_recipes: int,
    expected_labels: int,
) -> dict:
    model_summary = load_csv(result_dir / "model_summary.csv")
    recipe_table = load_csv(result_dir / "recipe_table.csv")
    label_table = load_csv(result_dir / "label_table.csv")
    audit_table = load_csv(result_dir / "audit.csv")
    responses = load_jsonl(result_dir / "responses.jsonl")
    manifest = load_csv(result_dir / "run_manifest.csv")
    combined_summary = load_csv(result_dir / "combined_model_summary.csv")

    assert_count("model_summary rows", len(model_summary), 1)
    assert_count("recipe_table rows", len(recipe_table), expected_recipes)
    assert_count("label_table rows", len(label_table), expected_labels)
    assert_count("audit rows", len(audit_table), expected_responses)
    assert_count("responses rows", len(responses), expected_responses)
    assert_count("run_manifest rows", len(manifest), 1)
    assert_count("combined_model_summary rows", len(combined_summary), 1)
    if manifest[0].get("slug") != slug:
        raise ValueError(f"run_manifest slug={manifest[0].get('slug')!r}, expected {slug!r}")
    if combined_summary[0].get("slug") != slug:
        raise ValueError(f"combined_model_summary slug={combined_summary[0].get('slug')!r}, expected {slug!r}")

    summary = model_summary[0]
    assert_count("clean_n", int(summary.get("clean_n", "-1")), expected_clean)
    assert_count("real_n", int(summary.get("real_n", "-1")), expected_real)

    clean_errors = sum(1 for row in audit_table if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_table if row.get("family") == "real_transfer" and row.get("is_correct") != "True")
    pipeline_errors: dict[str, int] = {}
    for row in audit_table:
        if row.get("family") != "real_transfer" or row.get("is_correct") == "True":
            continue
        recipe = row.get("recipe", "")
        pipeline_errors[recipe] = pipeline_errors.get(recipe, 0) + 1

    return {
        "model_summary": summary,
        "recipe_table": recipe_table,
        "label_table": label_table,
        "audit_table": audit_table,
        "response_count": len(responses),
        "clean_errors": clean_errors,
        "real_errors": real_errors,
        "pipeline_errors": pipeline_errors,
    }


def write_summary(*, result_dir: Path, slug: str, validation: dict, kernel_version: int | None) -> None:
    summary = validation["model_summary"]
    recipes = sorted(
        validation["recipe_table"],
        key=lambda row: decimal_value(row.get("accuracy", "0")),
        reverse=True,
    )
    labels_with_failures = [
        row for row in validation["label_table"]
        if real_errors_for_label(row) > 0 or decimal_value(row.get("accuracy_drop_vs_clean", "0")) > 0
    ]
    labels = sorted(
        labels_with_failures or validation["label_table"],
        key=lambda row: (real_errors_for_label(row), decimal_value(row.get("accuracy_drop_vs_clean", "0"))),
        reverse=True,
    )
    hardest = max(
        validation["recipe_table"],
        key=lambda row: decimal_value(row.get("accuracy_drop_vs_clean", "0")),
    )
    title = summary.get("model_id") or slug
    kernel_text = str(kernel_version) if kernel_version is not None else "not recorded"

    lines = [
        f"# {title} Full v0.3 Run",
        "",
        "## Run",
        "",
        "- Kaggle notebook: `yaroslavkholmirzayev/cure-or-open-weight-vlm-real-transfer-gpu-pilot`",
        f"- Kaggle kernel version: {kernel_text}",
        "- Device: Kaggle GPU",
        f"- Model: `{summary.get('model_id', '')}`",
        "- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`",
        "- Run mode: full",
        f"- Rows: {validation['response_count']} total, {summary.get('clean_n')} clean and {summary.get('real_n')} real-transfer",
        f"- Unparseable rate: clean={fmt4(summary.get('clean_unparseable_rate'))}, real={fmt4(summary.get('real_unparseable_rate'))}",
        f"- Abstention rate: clean={fmt4(summary.get('clean_abstention_rate'))}, real={fmt4(summary.get('real_abstention_rate'))}",
        "",
        "## Result",
        "",
        "| split | n | accuracy |",
        "|---|---:|---:|",
        f"| clean | {summary.get('clean_n')} | {fmt4(summary.get('clean_accuracy'))} |",
        f"| real-transfer | {summary.get('real_n')} | {fmt4(summary.get('real_accuracy'))} |",
        "",
        f"Overall real-transfer drop vs clean: `{fmt4(summary.get('accuracy_drop_vs_clean'))}`.",
        "",
        "## Pipeline Results",
        "",
        "| pipeline | n | accuracy | drop vs clean |",
        "|---|---:|---:|---:|",
    ]
    for row in recipes:
        lines.append(
            f"| `{row.get('recipe')}` | {row.get('n')} | "
            f"{fmt4(row.get('accuracy'))} | "
            f"{fmt4(row.get('accuracy_drop_vs_clean'))} |"
        )

    lines.extend([
        "",
        "## Failure Concentration",
        "",
        f"The model made {validation['real_errors']} real-transfer errors and {validation['clean_errors']} clean errors.",
        "",
        "| label | real n | real accuracy | drop vs clean |",
        "|---|---:|---:|---:|",
    ])
    for row in labels[:5]:
        lines.append(
            f"| `{row.get('label')}` | {row.get('real_n')} | "
            f"{fmt4(row.get('real_accuracy'))} | "
            f"{fmt4(row.get('accuracy_drop_vs_clean'))} |"
        )

    hardest_errors = validation["pipeline_errors"].get(hardest.get("recipe", ""), 0)
    lines.extend([
        "",
        f"The hardest transfer pipeline for this model is `{hardest.get('recipe')}`, "
        f"with {hardest_errors} real-transfer errors and a "
        f"{fmt1(decimal_value(hardest.get('accuracy_drop_vs_clean', '0')) * Decimal('100'))} percentage-point drop relative to clean.",
        "",
        "## Artifacts",
        "",
        "- `responses.jsonl`: raw model responses.",
        "- `audit.csv`: joined prompt/response correctness audit.",
        "- `model_summary.csv`: clean vs real-transfer summary.",
        "- `recipe_table.csv`: per-pipeline summary.",
        "- `label_table.csv`: per-label summary.",
        "- `combined_model_summary.csv`: combined Kaggle output summary.",
        "- `combined_recipe_table.csv`: combined Kaggle output recipe table.",
        "- `combined_label_table.csv`: combined Kaggle output label table.",
        "- `run_manifest.csv`: successful Kaggle run directory.",
        "- `kaggle_kernel.log`: Kaggle execution log, when available.",
        "",
    ])
    (result_dir / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def update_model_matrix(*, matrix_path: Path, slug: str, result_dir: Path, kernel_version: int | None) -> None:
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    relative_result = str(result_dir.resolve().relative_to(ROOT))
    for model in matrix.get("models", []):
        if model.get("slug") != slug:
            continue
        status_version = f"_v{kernel_version}" if kernel_version is not None else ""
        model["status"] = f"v03_full_completed_kaggle{status_version}"
        model["known_v03_full_result_dir"] = relative_result
        model.pop("active_v03_full_kernel_version", None)
        model.pop("planned_v03_full_result_dir", None)
        matrix_path.write_text(json.dumps(matrix, indent=2) + "\n", encoding="utf-8")
        return
    raise ValueError(f"Model slug not found in matrix: {slug}")


def load_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def assert_count(label: str, actual: int, expected: int) -> None:
    if actual != expected:
        raise ValueError(f"{label}: actual={actual}, expected={expected}")


def real_errors_for_label(row: dict[str, str]) -> float:
    real_n = decimal_value(row.get("real_n", "0"))
    real_accuracy = decimal_value(row.get("real_accuracy", "0"))
    return real_n * (Decimal("1") - real_accuracy)


def decimal_value(value: str | None) -> Decimal:
    return Decimal(value or "0")


def fmt4(value: str | Decimal | None) -> str:
    return str(decimal_value(str(value) if value is not None else "0").quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


def fmt1(value: str | Decimal | None) -> str:
    return str(decimal_value(str(value) if value is not None else "0").quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def resolve_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())
