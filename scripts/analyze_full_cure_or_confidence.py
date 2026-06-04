#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Full-CURE-OR confidence collapse and calibration.")
    parser.add_argument("--config", default="configs/full_cure_or_probe_confidence_v04.json")
    args = parser.parse_args()

    config = json.loads(resolve_project_path(args.config).read_text(encoding="utf-8"))
    threshold = float(config.get("high_confidence_threshold", 0.5))
    bins = int(config.get("ece_bins", 10))

    group_rows, severity_rows = build_rows(config["models"], threshold, bins)
    overconfidence_rows = build_overconfidence_rows(group_rows)

    write_csv(resolve_project_path(config["group_metrics_path"]), group_rows)
    write_csv(resolve_project_path(config["severity_metrics_path"]), severity_rows)
    write_csv(resolve_project_path(config["overconfidence_path"]), overconfidence_rows)

    print(f"Group confidence rows: {len(group_rows)}")
    print(f"Severity confidence rows: {len(severity_rows)}")
    print(f"Overconfidence ranking rows: {len(overconfidence_rows)}")
    print_headline(overconfidence_rows)
    return 0


def build_rows(models: list[dict], threshold: float, bins: int) -> tuple[list[dict], list[dict]]:
    group_output = []
    severity_output = []

    for model in models:
        predictions_path = resolve_project_path(model["predictions_path"])
        prediction_rows = load_prediction_rows(predictions_path)
        groups = group_by(prediction_rows, ["family", "recipe", "severity"])
        severity_groups = group_by(prediction_rows, ["family", "severity"])

        clean_rows = groups.get(("clean", "clean", "clean"), [])
        clean_metrics = metrics(clean_rows, threshold, bins) if clean_rows else None

        for (family, recipe, severity), rows in sorted(groups.items()):
            row_metrics = metrics(rows, threshold, bins)
            group_output.append(
                format_metric_row(
                    model=model,
                    family=family,
                    recipe=recipe,
                    severity=severity,
                    row_metrics=row_metrics,
                    clean_metrics=clean_metrics,
                )
            )

        for (family, severity), rows in sorted(severity_groups.items()):
            severity_metrics = metrics(rows, threshold, bins)
            severity_output.append(
                format_metric_row(
                    model=model,
                    family=family,
                    recipe="all" if family != "clean" else "clean",
                    severity=severity,
                    row_metrics=severity_metrics,
                    clean_metrics=clean_metrics,
                    extra={"cells": count_cells(rows)},
                )
            )

    return group_output, severity_output


def load_prediction_rows(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def group_by(rows: list[dict], keys: list[str]) -> dict[tuple[str, ...], list[dict]]:
    groups: dict[tuple[str, ...], list[dict]] = {}
    for row in rows:
        key = tuple(row[key] for key in keys)
        groups.setdefault(key, []).append(row)
    return groups


def metrics(rows: list[dict], threshold: float, bins: int) -> dict:
    if not rows:
        raise ValueError("Cannot compute metrics for an empty row group")

    confidences = [float(row["confidence"]) for row in rows]
    correct = [int(row["correct"]) for row in rows]
    n = len(rows)
    accuracy = mean(correct)
    mean_confidence = mean(confidences)
    incorrect_n = n - sum(correct)
    high_conf_wrong_n = sum(1 for conf, ok in zip(confidences, correct) if not ok and conf >= threshold)

    return {
        "n": n,
        "accuracy": accuracy,
        "mean_confidence": mean_confidence,
        "calibration_gap": mean_confidence - accuracy,
        "abs_calibration_gap": abs(mean_confidence - accuracy),
        "ece": expected_calibration_error(confidences, correct, bins),
        "brier_top1": mean((conf - ok) ** 2 for conf, ok in zip(confidences, correct)),
        "incorrect_n": incorrect_n,
        "mean_confidence_correct": "" if sum(correct) == 0 else mean(conf for conf, ok in zip(confidences, correct) if ok),
        "mean_confidence_incorrect": "" if incorrect_n == 0 else mean(
            conf for conf, ok in zip(confidences, correct) if not ok
        ),
        "high_conf_wrong_n": high_conf_wrong_n,
        "high_conf_wrong_rate": high_conf_wrong_n / n,
        "wrong_high_conf_share": "" if incorrect_n == 0 else high_conf_wrong_n / incorrect_n,
    }


def expected_calibration_error(confidences: list[float], correct: list[int], bins: int) -> float:
    if bins <= 0:
        raise ValueError("ece_bins must be positive")

    total = len(confidences)
    ece = 0.0
    for index in range(bins):
        lower = index / bins
        upper = (index + 1) / bins
        if index == bins - 1:
            bin_pairs = [(conf, ok) for conf, ok in zip(confidences, correct) if lower <= conf <= upper]
        else:
            bin_pairs = [(conf, ok) for conf, ok in zip(confidences, correct) if lower <= conf < upper]
        if not bin_pairs:
            continue
        bin_conf = mean(conf for conf, _ in bin_pairs)
        bin_acc = mean(ok for _, ok in bin_pairs)
        ece += (len(bin_pairs) / total) * abs(bin_conf - bin_acc)
    return ece


def format_metric_row(
    *,
    model: dict,
    family: str,
    recipe: str,
    severity: str,
    row_metrics: dict,
    clean_metrics: dict | None,
    extra: dict | None = None,
) -> dict:
    clean_accuracy = "" if clean_metrics is None else clean_metrics["accuracy"]
    clean_confidence = "" if clean_metrics is None else clean_metrics["mean_confidence"]
    row = {
        "model_name": model["name"],
        "model_slug": model["slug"],
        "family": family,
        "recipe": recipe,
        "severity": severity,
        "n": row_metrics["n"],
        "accuracy": row_metrics["accuracy"],
        "mean_confidence": row_metrics["mean_confidence"],
        "clean_accuracy": clean_accuracy,
        "clean_mean_confidence": clean_confidence,
        "accuracy_drop": "" if clean_metrics is None else clean_metrics["accuracy"] - row_metrics["accuracy"],
        "confidence_drop": "" if clean_metrics is None else clean_metrics["mean_confidence"] - row_metrics["mean_confidence"],
        "calibration_gap": row_metrics["calibration_gap"],
        "abs_calibration_gap": row_metrics["abs_calibration_gap"],
        "ece": row_metrics["ece"],
        "brier_top1": row_metrics["brier_top1"],
        "incorrect_n": row_metrics["incorrect_n"],
        "mean_confidence_correct": row_metrics["mean_confidence_correct"],
        "mean_confidence_incorrect": row_metrics["mean_confidence_incorrect"],
        "high_conf_wrong_n": row_metrics["high_conf_wrong_n"],
        "high_conf_wrong_rate": row_metrics["high_conf_wrong_rate"],
        "wrong_high_conf_share": row_metrics["wrong_high_conf_share"],
    }
    if extra:
        row.update(extra)
    return row


def count_cells(rows: list[dict]) -> int:
    return len({(row["recipe"], row["severity"]) for row in rows})


def build_overconfidence_rows(rows: list[dict]) -> list[dict]:
    native_rows = [row for row in rows if row["family"] == "native_cure_or"]
    output = []
    for model_slug in sorted({row["model_slug"] for row in native_rows}):
        model_rows = [row for row in native_rows if row["model_slug"] == model_slug]
        ranked = sorted(
            model_rows,
            key=lambda row: (
                float(row["calibration_gap"]),
                float(row["high_conf_wrong_rate"]),
                float(row["mean_confidence"]),
            ),
            reverse=True,
        )
        for rank, row in enumerate(ranked, start=1):
            output.append({"rank_overconfidence": rank, **row})
    return output


def print_headline(rows: list[dict]) -> None:
    level5 = [row for row in rows if row["severity"] == "level_5" and row["rank_overconfidence"] <= 3]
    if not level5:
        return
    print("Top level-5 overconfidence gaps by model:")
    for row in level5:
        print(
            f"  {row['model_name']} / {row['recipe']}: "
            f"gap={float(row['calibration_gap']):.4f}, "
            f"accuracy={float(row['accuracy']):.4f}, "
            f"confidence={float(row['mean_confidence']):.4f}"
        )


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
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
