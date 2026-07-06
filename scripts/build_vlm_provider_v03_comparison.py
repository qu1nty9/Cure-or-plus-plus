#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PIPELINE_ORDER = [
    "messenger_upload_download",
    "phone_screenshot_resave",
    "social_app_resave",
    "video_call_frame_capture",
]

FIELDS = [
    "slug",
    "display_name",
    "provider",
    "model_id",
    "result_dir",
    "clean_n",
    "clean_accuracy",
    "real_n",
    "real_accuracy",
    "accuracy_drop_vs_clean",
    "clean_errors",
    "real_errors",
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

PROVIDER_RUNS = [
    {
        "slug": "xai_grok_4_3",
        "display_name": "xAI Grok 4.3",
        "provider": "xai",
        "model_id": "grok-4.3",
        "result_dir": "reports/vlm_provider_xai_grok_4_3_full_v03",
    }
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build hosted-provider VLM v0.3 comparison tables.")
    parser.add_argument("--csv", default="reports/vlm_provider_full_v03_comparison.csv")
    parser.add_argument("--markdown", default="reports/vlm_provider_full_v03_comparison.md")
    parser.add_argument("--latex", default="reports/vlm_provider_full_v03_comparison.tex")
    args = parser.parse_args()

    rows = build_rows()
    if not rows:
        raise RuntimeError("No completed hosted-provider v0.3 result directories found.")
    write_csv(resolve_path(args.csv), rows)
    write_markdown(resolve_path(args.markdown), rows)
    write_latex(resolve_path(args.latex), rows)
    print(f"Rows: {len(rows)}")
    print(f"Wrote {resolve_path(args.csv)}")
    print(f"Wrote {resolve_path(args.markdown)}")
    print(f"Wrote {resolve_path(args.latex)}")
    return 0


def build_rows() -> list[dict[str, str]]:
    rows = []
    for run in PROVIDER_RUNS:
        result_dir = resolve_path(run["result_dir"])
        required = [
            result_dir / "model_summary.csv",
            result_dir / "recipe_table.csv",
            result_dir / "label_table.csv",
            result_dir / "audit.csv",
        ]
        if any(not path.exists() for path in required):
            continue
        rows.append(build_row(run, result_dir))
    return sorted(rows, key=lambda row: decimal_value(row["real_accuracy"]), reverse=True)


def build_row(run: dict[str, str], result_dir: Path) -> dict[str, str]:
    summary_rows = load_csv(result_dir / "model_summary.csv")
    recipe_rows = load_csv(result_dir / "recipe_table.csv")
    label_rows = load_csv(result_dir / "label_table.csv")
    audit_rows = load_csv(result_dir / "audit.csv")
    if len(summary_rows) != 1:
        raise ValueError(f"{result_dir}/model_summary.csv must contain exactly one row")

    summary = summary_rows[0]
    recipes = {row["recipe"]: row for row in recipe_rows}
    hardest_recipe = max(recipe_rows, key=lambda row: decimal_value(row.get("accuracy_drop_vs_clean", "0")))
    hardest_label = max(label_rows, key=real_errors_for_label)
    clean_errors = sum(1 for row in audit_rows if row.get("family") == "clean" and row.get("is_correct") != "True")
    real_errors = sum(1 for row in audit_rows if row.get("family") == "real_transfer" and row.get("is_correct") != "True")

    row = {
        "slug": run["slug"],
        "display_name": run["display_name"],
        "provider": run["provider"],
        "model_id": summary.get("model_id") or run["model_id"],
        "result_dir": relative_text(result_dir),
        "clean_n": summary.get("clean_n", ""),
        "clean_accuracy": fmt5(summary.get("clean_accuracy")),
        "real_n": summary.get("real_n", ""),
        "real_accuracy": fmt5(summary.get("real_accuracy")),
        "accuracy_drop_vs_clean": fmt5(summary.get("accuracy_drop_vs_clean")),
        "clean_errors": str(clean_errors),
        "real_errors": str(real_errors),
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


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    leader = rows[0]
    lines = [
        "# Hosted-Provider VLM Full v0.3 Comparison",
        "",
        "## Scope",
        "",
        "This table is generated from completed hosted-provider VLM runs on the CURE-OR++ 900-row v0.3 real-transfer prompt pack.",
        "Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`.",
        "Raw provider response JSONL files and caches are local artifacts; tracked tables contain only sanitized aggregates and audits.",
        "",
        "## Model-Level Results",
        "",
        markdown_table(
            ["model", "provider", "clean acc", "real-transfer acc", "drop", "real errors", "hardest pipeline", "hardest label"],
            [
                [
                    row["display_name"],
                    row["provider"],
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
        f"The current hosted-provider v0.3 leader is `{leader['display_name']}` with real-transfer accuracy `{fmt4(leader['real_accuracy'])}`.",
        "This table should be interpreted separately from the open-weight v0.3 table because hosted providers have externally managed versioning, pricing, caching, and data-handling policies.",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_latex(path: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Hosted-provider VLM full v0.3 real-transfer benchmark.}",
        r"\label{tab:vlm-provider-full-v03}",
        r"\resizebox{\linewidth}{!}{%",
        r"\begin{tabular}{llrrrrl}",
        r"\hline",
        r"Model & Provider & Clean & Real & Drop & FaceTime & Hardest label \\",
        r"\hline",
    ]
    for row in rows:
        lines.append(
            " & ".join(
                [
                    latex_escape(row["display_name"]),
                    latex_escape(row["provider"]),
                    fmt4(row["clean_accuracy"]),
                    fmt4(row["real_accuracy"]),
                    fmt4(row["accuracy_drop_vs_clean"]),
                    fmt4(row["video_call_frame_capture_accuracy"]),
                    latex_escape(row["hardest_label"].replace("_", " ")),
                ]
            )
            + r" \\"
        )
    lines.extend([
        r"\hline",
        r"\end{tabular}",
        r"}",
        r"\end{table}",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" if index in {0, 1} else "---:" for index, _ in enumerate(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(map(str, row)) + " |")
    return "\n".join(lines)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
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


def latex_escape(text: str) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


if __name__ == "__main__":
    raise SystemExit(main())
