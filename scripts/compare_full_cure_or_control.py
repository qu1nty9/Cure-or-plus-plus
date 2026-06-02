#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare Full-CURE-OR clean, grayscale control, and native severity.")
    parser.add_argument("--config", default="configs/full_cure_or_grayscale_control_summaries_v04.json")
    parser.add_argument("--native-comparison", default="results/full_cure_or_probe_v04_expanded_comparison.csv")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    config = json.loads(resolve_project_path(args.config).read_text(encoding="utf-8"))
    native_rows = load_rows(resolve_project_path(args.native_comparison))
    rows = []
    for model in config["models"]:
        control_summary = load_rows(resolve_project_path(model["summary_path"]))
        rows.append(build_model_row(model, control_summary, native_rows))

    output_path = resolve_project_path(args.output or config.get("comparison_path", "results/full_cure_or_grayscale_control_v04_comparison.csv"))
    write_csv(output_path, rows)
    print(f"Control comparison rows: {len(rows)}")
    print(f"Wrote {output_path}")
    print_headline(rows)
    return 0


def build_model_row(model: dict, control_summary: list[dict], native_rows: list[dict]) -> dict:
    clean = only_row(control_summary, family="clean", severity="clean")
    control = only_row(control_summary, family="control_cure_or", severity="control")
    native = [
        row
        for row in native_rows
        if row["model_slug"] == model["slug"] and row["family"] == "native_cure_or"
    ]
    if not native:
        raise ValueError(f"No native rows found for model slug {model['slug']}")

    levels = {f"level_{level}": weighted_accuracy(row for row in native if row["severity"] == f"level_{level}") for level in range(1, 6)}
    clean_accuracy = float(clean["accuracy"])
    control_accuracy = float(control["accuracy"])
    control_confidence = float(control["mean_confidence"])

    return {
        "model_name": model["name"],
        "model_slug": model["slug"],
        "clean_n": int(clean["n"]),
        "clean_accuracy": clean_accuracy,
        "clean_mean_confidence": float(clean["mean_confidence"]),
        "control_n": int(control["n"]),
        "control_accuracy": control_accuracy,
        "control_mean_confidence": control_confidence,
        "control_drop_vs_clean": clean_accuracy - control_accuracy,
        "control_confidence_drop_vs_clean": float(clean["mean_confidence"]) - control_confidence,
        "native_level_1_accuracy": levels["level_1"],
        "native_level_2_accuracy": levels["level_2"],
        "native_level_3_accuracy": levels["level_3"],
        "native_level_4_accuracy": levels["level_4"],
        "native_level_5_accuracy": levels["level_5"],
        "control_minus_native_level_1": control_accuracy - levels["level_1"],
        "control_minus_native_level_5": control_accuracy - levels["level_5"],
    }


def only_row(rows: list[dict], *, family: str, severity: str) -> dict:
    matches = [row for row in rows if row["family"] == family and row["severity"] == severity]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {family}/{severity} row, found {len(matches)}")
    return matches[0]


def weighted_accuracy(rows_iter) -> float:
    rows = list(rows_iter)
    if not rows:
        return float("nan")
    total = sum(int(row["n"]) for row in rows)
    return sum(float(row["accuracy"]) * int(row["n"]) for row in rows) / total


def load_rows(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def print_headline(rows: list[dict]) -> None:
    for row in rows:
        print(
            f"{row['model_name']}: clean={float(row['clean_accuracy']):.4f}, "
            f"grayscale={float(row['control_accuracy']):.4f}, "
            f"level5={float(row['native_level_5_accuracy']):.4f}"
        )


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
