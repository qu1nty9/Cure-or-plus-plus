#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PIPELINE_ORDER = [
    "messenger_upload_download",
    "phone_screenshot_resave",
    "social_app_resave",
    "video_call_frame_capture",
]

PIPELINE_DISPLAY = {
    "messenger_upload_download": "WhatsApp",
    "phone_screenshot_resave": "screenshot/resave",
    "social_app_resave": "Instagram resave",
    "video_call_frame_capture": "FaceTime frame",
}

FIELDS = [
    "slug",
    "display_name",
    "model_id",
    "tier",
    "status",
    "result_dir",
    "clean_n",
    "clean_accuracy",
    "real_n",
    "real_accuracy",
    "accuracy_drop_vs_clean",
    "real_errors",
    "clean_errors",
    "real_unparseable_rate",
    "real_abstention_rate",
    "messenger_upload_download_accuracy",
    "phone_screenshot_resave_accuracy",
    "social_app_resave_accuracy",
    "video_call_frame_capture_accuracy",
    "hardest_pipeline",
    "hardest_pipeline_drop",
    "hardest_label",
    "hardest_label_real_accuracy",
]

DISPLAY_NAMES = {
    "smolvlm2_2b": "SmolVLM2-2.2B",
    "internvl3_1b": "InternVL3-1B",
    "internvl3_2b": "InternVL3-2B",
    "qwen2_5_vl_3b": "Qwen2.5-VL-3B",
    "qwen2_5_vl_7b": "Qwen2.5-VL-7B",
    "llava_onevision_qwen2_0_5b": "LLaVA-OneVision-Qwen2-0.5B",
    "llava_onevision_qwen2_7b": "LLaVA-OneVision-Qwen2-7B",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build full v0.3 open-weight VLM comparison tables.")
    parser.add_argument("--model-matrix", default="configs/vlm_open_weight_model_matrix_v03.json")
    parser.add_argument("--csv", default="reports/vlm_open_weight_full_v03_comparison.csv")
    parser.add_argument("--markdown", default="reports/vlm_open_weight_full_v03_comparison.md")
    args = parser.parse_args()

    matrix = json.loads(resolve_path(args.model_matrix).read_text(encoding="utf-8"))
    rows = build_rows(matrix)
    if not rows:
        raise RuntimeError("No completed full v0.3 VLM result directories found.")
    write_csv(resolve_path(args.csv), rows)
    write_markdown(resolve_path(args.markdown), rows, matrix)
    print(f"Rows: {len(rows)}")
    print(f"Wrote {resolve_path(args.csv)}")
    print(f"Wrote {resolve_path(args.markdown)}")
    return 0


def build_rows(matrix: dict) -> list[dict[str, str]]:
    output = []
    for model in matrix.get("models", []):
        result_dir_text = model.get("known_v03_full_result_dir", "")
        if not result_dir_text:
            continue
        result_dir = resolve_path(result_dir_text)
        required = [
            result_dir / "model_summary.csv",
            result_dir / "recipe_table.csv",
            result_dir / "label_table.csv",
            result_dir / "audit.csv",
        ]
        if any(not path.exists() for path in required):
            continue
        output.append(build_model_row(model, result_dir))
    return sorted(output, key=lambda row: decimal_value(row["real_accuracy"]), reverse=True)


def build_model_row(model: dict, result_dir: Path) -> dict[str, str]:
    summary_rows = load_csv(result_dir / "model_summary.csv")
    recipe_rows = load_csv(result_dir / "recipe_table.csv")
    label_rows = load_csv(result_dir / "label_table.csv")
    audit_rows = load_csv(result_dir / "audit.csv")
    if len(summary_rows) != 1:
        raise ValueError(f"{result_dir}/model_summary.csv must contain exactly one row")

    summary = summary_rows[0]
    recipes = {row["recipe"]: row for row in recipe_rows}
    hardest_recipe = max(recipe_rows, key=lambda row: decimal_value(row.get("accuracy_drop_vs_clean", "0")))
    hardest_label = max(label_rows, key=lambda row: real_errors_for_label(row))
    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")

    row = {
        "slug": model["slug"],
        "display_name": DISPLAY_NAMES.get(model["slug"], model["slug"]),
        "model_id": summary.get("model_id") or model.get("model_id", ""),
        "tier": model.get("tier", ""),
        "status": model.get("status", ""),
        "result_dir": relative_text(result_dir),
        "clean_n": summary.get("clean_n", ""),
        "clean_accuracy": fmt5(summary.get("clean_accuracy")),
        "real_n": summary.get("real_n", ""),
        "real_accuracy": fmt5(summary.get("real_accuracy")),
        "accuracy_drop_vs_clean": fmt5(summary.get("accuracy_drop_vs_clean")),
        "real_errors": str(real_errors),
        "clean_errors": str(clean_errors),
        "real_unparseable_rate": fmt5(summary.get("real_unparseable_rate")),
        "real_abstention_rate": fmt5(summary.get("real_abstention_rate")),
        "hardest_pipeline": hardest_recipe.get("recipe", ""),
        "hardest_pipeline_drop": fmt5(hardest_recipe.get("accuracy_drop_vs_clean")),
        "hardest_label": hardest_label.get("label", ""),
        "hardest_label_real_accuracy": fmt5(hardest_label.get("real_accuracy")),
    }
    for pipeline in PIPELINE_ORDER:
        row[f"{pipeline}_accuracy"] = fmt5(recipes.get(pipeline, {}).get("accuracy"))
    return row


def write_markdown(path: Path, rows: list[dict[str, str]], matrix: dict) -> None:
    leader = rows[0]
    hardest_counts: dict[str, int] = {}
    for row in rows:
        hardest = row["hardest_pipeline"]
        hardest_counts[hardest] = hardest_counts.get(hardest, 0) + 1
    consensus_hardest = sorted(hardest_counts.items(), key=lambda item: (-item[1], item[0]))[0][0]

    lines = [
        "# Open-Weight VLM Full v0.3 Comparison",
        "",
        "## Scope",
        "",
        "This table is generated from completed 900-row open-weight VLM runs on the CURE-OR++ v0.3 real-transfer protocol.",
        f"Prompt pack: `{matrix.get('prompt_pack_path', 'reports/vlm_api_track_v03_prompt_pack.jsonl')}`.",
        "Launch-only or incomplete result directories are intentionally excluded.",
        "",
        "## Model-Level Results",
        "",
        markdown_table(
            ["model", "clean acc", "real-transfer acc", "drop", "real errors", "hardest pipeline", "hardest label"],
            [
                [
                    row["display_name"],
                    fmt4(row["clean_accuracy"]),
                    fmt4(row["real_accuracy"]),
                    fmt4(row["accuracy_drop_vs_clean"]),
                    row["real_errors"],
                    f"`{row['hardest_pipeline']}`",
                    f"`{row['hardest_label']}`",
                ]
                for row in rows
            ],
        ),
        "",
        "## Pipeline Results",
        "",
        markdown_table(
            ["model", "WhatsApp", "screenshot/resave", "Instagram resave", "FaceTime frame"],
            [
                [
                    row["display_name"],
                    fmt4(row["messenger_upload_download_accuracy"]),
                    fmt4(row["phone_screenshot_resave_accuracy"]),
                    fmt4(row["social_app_resave_accuracy"]),
                    fmt4(row["video_call_frame_capture_accuracy"]),
                ]
                for row in rows
            ],
        ),
        "",
        "## Interpretation",
        "",
        f"The current leader is `{leader['display_name']}` with real-transfer accuracy `{fmt4(leader['real_accuracy'])}`.",
        f"The consensus hardest pipeline across completed models is `{consensus_hardest}`.",
        "This generated table is the current main open-weight VLM benchmark block; optional additional full v0.3 runs extend it without changing the audit path.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" if index == 0 else "---:" for index, _ in enumerate(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(map(str, row)) + " |")
    return "\n".join(lines)


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def real_errors_for_label(row: dict[str, str]) -> Decimal:
    real_n = decimal_value(row.get("real_n", "0"))
    real_accuracy = decimal_value(row.get("real_accuracy", "0"))
    return real_n * (Decimal("1") - real_accuracy)


def decimal_value(value: str | None) -> Decimal:
    return Decimal(value or "0")


def fmt5(value: str | Decimal | None) -> str:
    return str(decimal_value(str(value) if value is not None else "0").quantize(Decimal("0.00001"), rounding=ROUND_HALF_UP))


def fmt4(value: str | Decimal | None) -> str:
    return str(decimal_value(str(value) if value is not None else "0").quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))


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
