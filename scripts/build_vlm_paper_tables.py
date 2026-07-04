#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OUTPUT_FIELDS = [
    "slug",
    "display_name",
    "clean_accuracy",
    "real_accuracy",
    "accuracy_drop_vs_clean",
    "real_unparseable_rate",
    "video_call_frame_capture_accuracy",
    "hardest_pipeline",
    "hardest_label",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build paper-ready open-weight VLM v0.3 tables.")
    parser.add_argument("--comparison", default="reports/vlm_open_weight_full_v03_comparison.csv")
    parser.add_argument("--csv", default="reports/vlm_open_weight_full_v03_paper_table.csv")
    parser.add_argument("--markdown", default="reports/vlm_open_weight_full_v03_paper_table.md")
    parser.add_argument("--latex", default="reports/vlm_open_weight_full_v03_paper_table.tex")
    args = parser.parse_args()

    rows = load_csv(resolve_project_path(args.comparison))
    table_rows = build_table(rows)
    write_csv(resolve_project_path(args.csv), table_rows)
    write_markdown(resolve_project_path(args.markdown), table_rows)
    write_latex(resolve_project_path(args.latex), table_rows)

    print(f"Rows: {len(table_rows)}")
    print(f"Wrote {resolve_project_path(args.csv)}")
    print(f"Wrote {resolve_project_path(args.markdown)}")
    print(f"Wrote {resolve_project_path(args.latex)}")
    return 0


def build_table(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    output = []
    for row in rows:
        output.append(
            {
                "slug": row["slug"],
                "display_name": row["display_name"],
                "clean_accuracy": row["clean_accuracy"],
                "real_accuracy": row["real_accuracy"],
                "accuracy_drop_vs_clean": row["accuracy_drop_vs_clean"],
                "real_unparseable_rate": row["real_unparseable_rate"],
                "video_call_frame_capture_accuracy": row["video_call_frame_capture_accuracy"],
                "hardest_pipeline": row["hardest_pipeline"],
                "hardest_label": row["hardest_label"],
            }
        )
    return output


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        "# Open-Weight VLM Full v0.3 Paper Table",
        "",
        "Generated from `reports/vlm_open_weight_full_v03_comparison.csv`.",
        "",
        markdown_table(
            ["Model", "Clean", "Real", "Drop", "Unparseable", "FaceTime", "Hardest label"],
            [
                [
                    row["display_name"],
                    fmt4(row["clean_accuracy"]),
                    fmt4(row["real_accuracy"]),
                    fmt4(row["accuracy_drop_vs_clean"]),
                    fmt4(row["real_unparseable_rate"]),
                    fmt4(row["video_call_frame_capture_accuracy"]),
                    row["hardest_label"],
                ]
                for row in rows
            ],
        ),
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_latex(path: Path, rows: list[dict[str, str]]) -> None:
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Open-weight VLM full v0.3 real-transfer benchmark.}",
        r"\label{tab:vlm-open-weight-full-v03}",
        r"\resizebox{\linewidth}{!}{%",
        r"\begin{tabular}{lrrrrrl}",
        r"\hline",
        r"Model & Clean & Real & Drop & Unparseable & FaceTime & Hardest label \\",
        r"\hline",
    ]
    for row in rows:
        lines.append(
            " & ".join(
                [
                    latex_escape(row["display_name"]),
                    fmt4(row["clean_accuracy"]),
                    fmt4(row["real_accuracy"]),
                    fmt4(row["accuracy_drop_vs_clean"]),
                    fmt4(row["real_unparseable_rate"]),
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
        "| " + " | ".join("---" if index == 0 else "---:" for index, _ in enumerate(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(map(str, row)) + " |")
    return "\n".join(lines)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def resolve_project_path(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def fmt4(value: str) -> str:
    return f"{float(value):.4f}"


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
