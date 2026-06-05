#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MODEL_TABLE_FIELDS = [
    "model_name",
    "model_slug",
    "clean_accuracy",
    "native_mean_accuracy",
    "native_level_1_accuracy",
    "native_level_5_accuracy",
    "level_5_drop_vs_clean",
    "worst_level_5_recipe",
    "worst_level_5_challenge",
    "worst_level_5_accuracy",
]

FAILURE_TABLE_FIELDS = [
    "rank",
    "challenge_type",
    "display_name",
    "mean_accuracy",
    "median_accuracy",
    "floor_count",
    "near_floor_count",
    "top3_count",
    "model_count",
    "mean_rank_most_damaging",
]

CONTROL_TABLE_FIELDS = [
    "model_name",
    "model_slug",
    "clean_accuracy",
    "grayscale_control_accuracy",
    "native_level_5_accuracy",
    "control_minus_native_level_5",
    "control_drop_vs_clean",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build paper-ready benchmark tables for the Full-CURE-OR v0.4 track.")
    parser.add_argument(
        "--comparison",
        default="results/full_cure_or_probe_v04_with_prototypes_comparison.csv",
        help="Model comparison CSV with clean and native CURE-OR rows.",
    )
    parser.add_argument(
        "--level5-ranking",
        default="results/full_cure_or_probe_v04_with_prototypes_level5_ranking.csv",
        help="Per-model level-5 most-damaging ranking CSV.",
    )
    parser.add_argument(
        "--consensus",
        default="results/full_cure_or_probe_v04_with_prototypes_level5_consensus.csv",
        help="Cross-model level-5 consensus failure CSV.",
    )
    parser.add_argument(
        "--control",
        default="results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.csv",
        help="Grayscale control comparison CSV.",
    )
    parser.add_argument(
        "--challenge-types",
        default="configs/cure_or_challenge_types_v01.json",
        help="Official challenge type mapping for display names.",
    )
    parser.add_argument("--model-table", default="reports/full_cure_or_paper_model_table_v04.csv")
    parser.add_argument("--failure-table", default="reports/full_cure_or_paper_failure_table_v04.csv")
    parser.add_argument("--control-table", default="reports/full_cure_or_paper_control_table_v04.csv")
    parser.add_argument("--markdown", default="reports/full_cure_or_paper_tables_v04.md")
    parser.add_argument("--latex", default="reports/full_cure_or_paper_tables_v04.tex")
    parser.add_argument("--top-failures", type=int, default=6)
    args = parser.parse_args()

    comparison_rows = load_csv(resolve_project_path(args.comparison))
    ranking_rows = load_csv(resolve_project_path(args.level5_ranking))
    consensus_rows = load_csv(resolve_project_path(args.consensus))
    control_rows = load_csv(resolve_project_path(args.control))
    challenge_display = load_challenge_display(resolve_project_path(args.challenge_types))

    model_table = build_model_table(comparison_rows, ranking_rows, challenge_display)
    failure_table = build_failure_table(consensus_rows, args.top_failures)
    control_table = build_control_table(control_rows)

    write_csv(resolve_project_path(args.model_table), model_table, MODEL_TABLE_FIELDS)
    write_csv(resolve_project_path(args.failure_table), failure_table, FAILURE_TABLE_FIELDS)
    write_csv(resolve_project_path(args.control_table), control_table, CONTROL_TABLE_FIELDS)
    write_markdown(resolve_project_path(args.markdown), model_table, failure_table, control_table)
    write_latex(resolve_project_path(args.latex), model_table, failure_table, control_table)

    print(f"Model rows: {len(model_table)}")
    print(f"Failure rows: {len(failure_table)}")
    print(f"Control rows: {len(control_table)}")
    print(f"Wrote {resolve_project_path(args.markdown)}")
    print_headline(model_table, failure_table, control_table)
    return 0


def build_model_table(
    comparison_rows: list[dict],
    ranking_rows: list[dict],
    challenge_display: dict[str, str],
) -> list[dict]:
    grouped = group_by(comparison_rows, "model_slug")
    ranking_by_model = {row["model_slug"]: row for row in ranking_rows if int(row["rank_most_damaging"]) == 1}
    output = []
    for model_slug, rows in grouped.items():
        clean_rows = [row for row in rows if row["family"] == "clean" and row["severity"] == "clean"]
        native_rows = [row for row in rows if row["family"] == "native_cure_or"]
        if len(clean_rows) != 1 or not native_rows:
            continue

        clean_accuracy = float(clean_rows[0]["accuracy"])
        level_1_accuracy = weighted_accuracy(row for row in native_rows if row["severity"] == "level_1")
        level_5_accuracy = weighted_accuracy(row for row in native_rows if row["severity"] == "level_5")
        worst = ranking_by_model.get(model_slug, {})
        worst_recipe = worst.get("recipe", "")
        output.append(
            {
                "model_name": clean_rows[0]["model_name"],
                "model_slug": model_slug,
                "clean_accuracy": clean_accuracy,
                "native_mean_accuracy": weighted_accuracy(native_rows),
                "native_level_1_accuracy": level_1_accuracy,
                "native_level_5_accuracy": level_5_accuracy,
                "level_5_drop_vs_clean": clean_accuracy - level_5_accuracy,
                "worst_level_5_recipe": worst_recipe,
                "worst_level_5_challenge": challenge_display.get(worst_recipe, worst_recipe),
                "worst_level_5_accuracy": float_or_blank(worst.get("accuracy", "")),
            }
        )
    return sorted(output, key=lambda row: float(row["native_level_5_accuracy"]), reverse=True)


def build_failure_table(consensus_rows: list[dict], top_n: int) -> list[dict]:
    output = []
    for rank, row in enumerate(consensus_rows[:top_n], start=1):
        output.append(
            {
                "rank": rank,
                "challenge_type": row["challenge_type"],
                "display_name": row["display_name"],
                "mean_accuracy": float(row["mean_accuracy"]),
                "median_accuracy": float(row["median_accuracy"]),
                "floor_count": int(row["floor_count"]),
                "near_floor_count": int(row["near_floor_count"]),
                "top3_count": int(row["top3_count"]),
                "model_count": int(row["model_count"]),
                "mean_rank_most_damaging": float(row["mean_rank_most_damaging"]),
            }
        )
    return output


def build_control_table(control_rows: list[dict]) -> list[dict]:
    output = []
    for row in control_rows:
        output.append(
            {
                "model_name": row["model_name"],
                "model_slug": row["model_slug"],
                "clean_accuracy": float(row["clean_accuracy"]),
                "grayscale_control_accuracy": float(row["control_accuracy"]),
                "native_level_5_accuracy": float(row["native_level_5_accuracy"]),
                "control_minus_native_level_5": float(row["control_minus_native_level_5"]),
                "control_drop_vs_clean": float(row["control_drop_vs_clean"]),
            }
        )
    return sorted(output, key=lambda row: float(row["native_level_5_accuracy"]), reverse=True)


def write_markdown(path: Path, model_table: list[dict], failure_table: list[dict], control_table: list[dict]) -> None:
    lines = [
        "# Full-CURE-OR v0.4 Paper Tables",
        "",
        "These tables are generated from tracked aggregate result CSVs, not from per-image prediction dumps.",
        "",
        "## Model Leaderboard",
        "",
        markdown_table(
            ["Model", "Clean", "Native mean", "Level 1", "Level 5", "L5 drop", "Worst L5"],
            [
                [
                    row["model_name"],
                    fmt_pct(row["clean_accuracy"]),
                    fmt_pct(row["native_mean_accuracy"]),
                    fmt_pct(row["native_level_1_accuracy"]),
                    fmt_pct(row["native_level_5_accuracy"]),
                    fmt_pct(row["level_5_drop_vs_clean"]),
                    f"{row['worst_level_5_challenge']} ({fmt_pct(row['worst_level_5_accuracy'])})",
                ]
                for row in model_table
            ],
        ),
        "",
        "## Consensus Level-5 Failures",
        "",
        markdown_table(
            ["Rank", "Type", "Challenge", "Mean acc.", "Median acc.", "Floor", "Top-3"],
            [
                [
                    row["rank"],
                    row["challenge_type"],
                    row["display_name"],
                    fmt_pct(row["mean_accuracy"]),
                    fmt_pct(row["median_accuracy"]),
                    f"{row['floor_count']}/{row['model_count']}",
                    f"{row['top3_count']}/{row['model_count']}",
                ]
                for row in failure_table
            ],
        ),
        "",
        "## Grayscale Control Guardrail",
        "",
        markdown_table(
            ["Model", "Clean", "Gray control", "Native L5", "Control - L5", "Control drop"],
            [
                [
                    row["model_name"],
                    fmt_pct(row["clean_accuracy"]),
                    fmt_pct(row["grayscale_control_accuracy"]),
                    fmt_pct(row["native_level_5_accuracy"]),
                    fmt_pct(row["control_minus_native_level_5"]),
                    fmt_pct(row["control_drop_vs_clean"]),
                ]
                for row in control_table
            ],
        ),
        "",
        "## Notes",
        "",
        "- The model leaderboard excludes the SigLIP diagnostic failure row.",
        "- Native means are weighted by row count `n`.",
        "- The grayscale control is type 10/no-challenge grayscale, so it is a guardrail rather than a native challenge.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_latex(path: Path, model_table: list[dict], failure_table: list[dict], control_table: list[dict]) -> None:
    parts = [
        latex_table(
            "Full-CURE-OR v0.4 model leaderboard.",
            "tab:full-cure-or-model-leaderboard",
            ["Model", "Clean", "Native mean", "Level 5", "Worst L5"],
            [
                [
                    row["model_name"],
                    fmt_pct(row["clean_accuracy"]),
                    fmt_pct(row["native_mean_accuracy"]),
                    fmt_pct(row["native_level_5_accuracy"]),
                    f"{row['worst_level_5_challenge']} ({fmt_pct(row['worst_level_5_accuracy'])})",
                ]
                for row in model_table
            ],
        ),
        latex_table(
            "Consensus hardest level-5 native CURE-OR challenges.",
            "tab:full-cure-or-consensus-failures",
            ["Rank", "Type", "Challenge", "Mean acc.", "Floor"],
            [
                [
                    row["rank"],
                    row["challenge_type"],
                    row["display_name"],
                    fmt_pct(row["mean_accuracy"]),
                    f"{row['floor_count']}/{row['model_count']}",
                ]
                for row in failure_table
            ],
        ),
        latex_table(
            "Type-10 grayscale control versus native level-5 accuracy.",
            "tab:full-cure-or-grayscale-control",
            ["Model", "Gray control", "Native L5", "Control - L5"],
            [
                [
                    row["model_name"],
                    fmt_pct(row["grayscale_control_accuracy"]),
                    fmt_pct(row["native_level_5_accuracy"]),
                    fmt_pct(row["control_minus_native_level_5"]),
                ]
                for row in control_table
            ],
        ),
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def latex_table(caption: str, label: str, headers: list[str], rows: list[list]) -> str:
    column_spec = "l" * len(headers)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{latex_escape(caption)}}}",
        f"\\label{{{latex_escape(label)}}}",
        f"\\begin{{tabular}}{{{column_spec}}}",
        "\\hline",
        " & ".join(latex_escape(str(header)) for header in headers) + " \\\\",
        "\\hline",
    ]
    for row in rows:
        lines.append(" & ".join(latex_escape(str(value)) for value in row) + " \\\\")
    lines.extend(["\\hline", "\\end{tabular}", "\\end{table}"])
    return "\n".join(lines)


def markdown_table(headers: list[str], rows: list[list]) -> str:
    output = ["| " + " | ".join(str(header) for header in headers) + " |"]
    output.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        output.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(output)


def print_headline(model_table: list[dict], failure_table: list[dict], control_table: list[dict]) -> None:
    if model_table:
        best = model_table[0]
        print(
            "Best native level-5 row: "
            f"{best['model_name']} at {float(best['native_level_5_accuracy']):.4f}"
        )
    if failure_table:
        worst = failure_table[0]
        print(
            "Top consensus failure: "
            f"{worst['display_name']} at mean accuracy {float(worst['mean_accuracy']):.4f}"
        )
    if control_table:
        strongest_guardrail = max(control_table, key=lambda row: float(row["control_minus_native_level_5"]))
        print(
            "Largest grayscale-control vs native-L5 gap: "
            f"{strongest_guardrail['model_name']} at {float(strongest_guardrail['control_minus_native_level_5']):.4f}"
        )


def weighted_accuracy(rows_iter) -> float:
    rows = list(rows_iter)
    total = sum(int(row["n"]) for row in rows)
    if total == 0:
        return float("nan")
    return sum(float(row["accuracy"]) * int(row["n"]) for row in rows) / total


def group_by(rows: list[dict], key: str) -> dict[str, list[dict]]:
    output: dict[str, list[dict]] = {}
    for row in rows:
        output.setdefault(row[key], []).append(row)
    return output


def fmt_pct(value) -> str:
    numeric = float(value)
    if math.isnan(numeric):
        return "NA"
    return f"{numeric:.3f}"


def float_or_blank(value: str):
    if value == "":
        return ""
    return float(value)


def latex_escape(value: str) -> str:
    replacements = {
        "\\": "\\textbackslash{}",
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
        "{": "\\{",
        "}": "\\}",
        "~": "\\textasciitilde{}",
        "^": "\\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def load_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_challenge_display(path: Path) -> dict[str, str]:
    import json

    raw = json.loads(path.read_text(encoding="utf-8"))["challenge_types"]
    return {f"native_challenge_type_{key}": value["display_name"] for key, value in raw.items()}


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
