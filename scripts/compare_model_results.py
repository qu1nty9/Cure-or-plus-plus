#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare CURE-OR++ baseline summaries across models.")
    parser.add_argument("--config", default="configs/model_summaries_v01.json")
    args = parser.parse_args()

    config = json.loads(resolve_project_path(args.config).read_text(encoding="utf-8"))
    summaries = load_summaries(config["models"])
    comparison_rows = build_comparison_rows(summaries)
    ranking_rows = build_ranking_rows(summaries)
    per_class_rows = build_per_class_rows(config["models"])

    write_csv(resolve_project_path(config["comparison_path"]), comparison_rows)
    write_csv(resolve_project_path(config["ranking_path"]), ranking_rows)
    write_csv(resolve_project_path(config["per_class_path"]), per_class_rows)

    print(f"Comparison rows: {len(comparison_rows)}")
    print(f"Ranking rows: {len(ranking_rows)}")
    print(f"Per-class rows: {len(per_class_rows)}")
    print_headline(comparison_rows, ranking_rows)
    return 0


def load_summaries(models: list[dict]) -> list[dict]:
    rows = []
    for model in models:
        path = resolve_project_path(model["summary_path"])
        if not path.exists():
            print(f"Skipping missing summary for {model['name']}: {path}")
            continue
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


def build_ranking_rows(rows: list[dict]) -> list[dict]:
    output = []
    model_groups: dict[str, list[dict]] = {}
    for row in rows:
        if row["severity"] != "high" or row["family"] == "clean":
            continue
        model_groups.setdefault(row["model_slug"], []).append(row)

    for model_slug, model_rows in model_groups.items():
        ranked = sorted(model_rows, key=lambda row: float(row["accuracy"]))
        for rank, row in enumerate(ranked, start=1):
            output.append(
                {
                    "model_name": row["model_name"],
                    "model_slug": model_slug,
                    "rank_most_damaging": rank,
                    "family": row["family"],
                    "recipe": row["recipe"],
                    "accuracy": row["accuracy"],
                    "relative_accuracy_drop": row["relative_accuracy_drop"],
                }
            )
    return output


def build_per_class_rows(models: list[dict]) -> list[dict]:
    output = []
    for model in models:
        path = resolve_project_path(model["predictions_path"])
        if not path.exists():
            print(f"Skipping missing predictions for {model['name']}: {path}")
            continue

        groups: dict[tuple[str, str, str, str], list[dict]] = {}
        with path.open("r", newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                key = (row["family"], row["recipe"], row["severity"], row["label"])
                groups.setdefault(key, []).append(row)

        clean_by_label = {
            label: accuracy(rows)
            for (family, recipe, severity, label), rows in groups.items()
            if family == "clean" and recipe == "clean" and severity == "clean"
        }

        for (family, recipe, severity, label), rows in sorted(groups.items()):
            acc = accuracy(rows)
            clean_acc = clean_by_label.get(label)
            output.append(
                {
                    "model_name": model["name"],
                    "model_slug": model["slug"],
                    "family": family,
                    "recipe": recipe,
                    "severity": severity,
                    "label": label,
                    "n": len(rows),
                    "accuracy": acc,
                    "drop_vs_clean_label": "" if clean_acc is None else clean_acc - acc,
                }
            )
    return output


def accuracy(rows: list[dict]) -> float:
    return sum(int(row["correct"]) for row in rows) / len(rows)


def print_headline(comparison_rows: list[dict], ranking_rows: list[dict]) -> None:
    clean_rows = [row for row in comparison_rows if row["family"] == "clean"]
    for row in clean_rows:
        print(f"{row['model_name']} clean accuracy: {float(row['accuracy']):.4f}")

    for model_slug in sorted({row["model_slug"] for row in ranking_rows}):
        worst = [row for row in ranking_rows if row["model_slug"] == model_slug and row["rank_most_damaging"] == 1]
        if worst:
            row = worst[0]
            print(f"{row['model_name']} worst high-severity recipe: {row['recipe']} ({float(row['accuracy']):.4f})")


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())

