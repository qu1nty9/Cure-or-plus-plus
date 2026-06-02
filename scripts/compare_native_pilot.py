#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare native mini-CURE-OR pilot summaries.")
    parser.add_argument("--config", default="configs/native_pilot_summaries_v01.json")
    args = parser.parse_args()

    config = json.loads(resolve_project_path(args.config).read_text(encoding="utf-8"))
    ranking_severity = config.get("ranking_severity", "level_4")
    rows = load_rows(config["models"])
    comparison_rows = build_comparison_rows(rows)
    ranking_rows = build_level_ranking(comparison_rows, ranking_severity)

    write_csv(resolve_project_path(config["comparison_path"]), comparison_rows)
    write_csv(resolve_project_path(config["ranking_path"]), ranking_rows)
    print(f"Comparison rows: {len(comparison_rows)}")
    print(f"{ranking_severity} ranking rows: {len(ranking_rows)}")
    print_headline(ranking_rows, ranking_severity)
    return 0


def load_rows(models: list[dict]) -> list[dict]:
    rows = []
    for model in models:
        path = resolve_project_path(model["summary_path"])
        with path.open("r", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                row["model_name"] = model["name"]
                row["model_slug"] = model["slug"]
                rows.append(row)
    return rows


def build_comparison_rows(rows: list[dict]) -> list[dict]:
    output = []
    for row in rows:
        output.append(
            {
                "model_name": row["model_name"],
                "model_slug": row["model_slug"],
                "family": row["family"],
                "recipe": row["recipe"],
                "severity": row["severity"],
                "n": row["n"],
                "accuracy": row["accuracy"],
                "mean_confidence": row["mean_confidence"],
                "relative_accuracy_drop": row["relative_accuracy_drop"],
            }
        )
    return output


def build_level_ranking(rows: list[dict], severity: str) -> list[dict]:
    output = []
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        if row["family"] != "native_cure_or" or row["severity"] != severity:
            continue
        grouped.setdefault(row["model_slug"], []).append(row)

    for model_slug, model_rows in grouped.items():
        ranked = sorted(model_rows, key=lambda row: float(row["accuracy"]))
        for rank, row in enumerate(ranked, start=1):
            output.append(
                {
                    "model_name": row["model_name"],
                    "model_slug": model_slug,
                    "rank_most_damaging": rank,
                    "recipe": row["recipe"],
                    "accuracy": row["accuracy"],
                    "relative_accuracy_drop": row["relative_accuracy_drop"],
                    "mean_confidence": row["mean_confidence"],
                }
            )
    return output


def print_headline(rows: list[dict], severity: str) -> None:
    for row in rows:
        if row["rank_most_damaging"] != 1:
            continue
        print(
            f"{row['model_name']} worst {severity} native challenge: "
            f"{row['recipe']} ({float(row['accuracy']):.4f})"
        )


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
