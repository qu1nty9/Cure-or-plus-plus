#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPE_RE = re.compile(r"native_challenge_type_(\d{2})$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze consensus native CURE-OR failures across models.")
    parser.add_argument(
        "--comparison",
        default="results/full_cure_or_probe_v04_with_prototypes_comparison.csv",
        help="Comparison CSV produced by compare_native_pilot.py.",
    )
    parser.add_argument(
        "--challenge-types",
        default="configs/cure_or_challenge_types_v01.json",
        help="Official challenge type mapping.",
    )
    parser.add_argument("--severity", default="level_5")
    parser.add_argument(
        "--consensus-output",
        default="results/full_cure_or_probe_v04_with_prototypes_level5_consensus.csv",
    )
    parser.add_argument(
        "--correlation-output",
        default="results/full_cure_or_probe_v04_with_prototypes_level5_rank_correlations.csv",
    )
    parser.add_argument(
        "--floor-threshold",
        type=float,
        default=0.02,
        help="Accuracy threshold treated as floor/near-chance.",
    )
    parser.add_argument(
        "--near-floor-threshold",
        type=float,
        default=0.05,
        help="Accuracy threshold treated as near-floor.",
    )
    args = parser.parse_args()

    challenge_types = load_challenge_types(resolve_project_path(args.challenge_types))
    rows = load_rows(resolve_project_path(args.comparison), challenge_types, args.severity)
    if not rows:
        raise ValueError(f"No native rows found for severity {args.severity}")

    rankings = build_model_rankings(rows)
    consensus_rows = build_consensus_rows(
        rows,
        rankings,
        floor_threshold=args.floor_threshold,
        near_floor_threshold=args.near_floor_threshold,
    )
    correlation_rows = build_rank_correlation_rows(rankings, args.severity)

    write_csv(resolve_project_path(args.consensus_output), consensus_rows)
    write_csv(resolve_project_path(args.correlation_output), correlation_rows)

    print(f"Consensus rows: {len(consensus_rows)}")
    print(f"Rank-correlation rows: {len(correlation_rows)}")
    print_headline(consensus_rows, correlation_rows)
    return 0


def load_challenge_types(path: Path) -> dict[str, dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))["challenge_types"]
    output = {}
    for key, value in raw.items():
        output[f"native_challenge_type_{key}"] = {
            "challenge_type": key,
            "challenge_name": value["name"],
            "display_name": value["display_name"],
        }
    return output


def load_rows(path: Path, challenge_types: dict[str, dict], severity: str) -> list[dict]:
    rows = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["family"] != "native_cure_or" or row["severity"] != severity:
                continue
            match = TYPE_RE.match(row["recipe"])
            if not match:
                continue
            meta = challenge_types.get(row["recipe"], {})
            rows.append(
                {
                    "model_name": row["model_name"],
                    "model_slug": row["model_slug"],
                    "recipe": row["recipe"],
                    "severity": row["severity"],
                    "accuracy": float(row["accuracy"]),
                    "mean_confidence": float(row["mean_confidence"]),
                    "relative_accuracy_drop": float(row["relative_accuracy_drop"]),
                    "challenge_type": meta.get("challenge_type", match.group(1)),
                    "challenge_name": meta.get("challenge_name", row["recipe"]),
                    "display_name": meta.get("display_name", row["recipe"]),
                }
            )
    return rows


def build_model_rankings(rows: list[dict]) -> dict[str, dict]:
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["model_name"], []).append(row)

    rankings = {}
    for model_name, model_rows in grouped.items():
        ranks = average_ranks(model_rows, value_key="accuracy", id_key="recipe")
        rankings[model_name] = {
            row["recipe"]: {
                "rank": ranks[row["recipe"]],
                "accuracy": row["accuracy"],
                "display_name": row["display_name"],
            }
            for row in model_rows
        }
    return rankings


def average_ranks(rows: list[dict], value_key: str, id_key: str) -> dict[str, float]:
    ordered = sorted(rows, key=lambda row: (float(row[value_key]), row[id_key]))
    ranks = {}
    index = 0
    while index < len(ordered):
        start = index
        value = float(ordered[index][value_key])
        while index < len(ordered) and float(ordered[index][value_key]) == value:
            index += 1
        end = index
        rank = (start + 1 + end) / 2
        for row in ordered[start:end]:
            ranks[row[id_key]] = rank
    return ranks


def build_consensus_rows(
    rows: list[dict],
    rankings: dict[str, dict],
    floor_threshold: float,
    near_floor_threshold: float,
) -> list[dict]:
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["recipe"], []).append(row)

    output = []
    for recipe, recipe_rows in grouped.items():
        accuracies = [row["accuracy"] for row in recipe_rows]
        confidences = [row["mean_confidence"] for row in recipe_rows]
        ranks = [rankings[row["model_name"]][recipe]["rank"] for row in recipe_rows]
        floor_models = [row["model_name"] for row in recipe_rows if row["accuracy"] <= floor_threshold]
        near_floor_models = [row["model_name"] for row in recipe_rows if row["accuracy"] <= near_floor_threshold]
        meta = recipe_rows[0]
        output.append(
            {
                "recipe": recipe,
                "challenge_type": meta["challenge_type"],
                "display_name": meta["display_name"],
                "severity": meta["severity"],
                "model_count": len(recipe_rows),
                "mean_accuracy": statistics.fmean(accuracies),
                "median_accuracy": statistics.median(accuracies),
                "min_accuracy": min(accuracies),
                "max_accuracy": max(accuracies),
                "accuracy_std": pstdev(accuracies),
                "mean_confidence": statistics.fmean(confidences),
                "mean_rank_most_damaging": statistics.fmean(ranks),
                "median_rank_most_damaging": statistics.median(ranks),
                "rank_std": pstdev(ranks),
                "top3_count": sum(1 for rank in ranks if rank <= 3),
                "top5_count": sum(1 for rank in ranks if rank <= 5),
                "floor_count": len(floor_models),
                "near_floor_count": len(near_floor_models),
                "floor_models": "; ".join(floor_models),
                "near_floor_models": "; ".join(near_floor_models),
            }
        )
    return sorted(output, key=lambda row: (float(row["mean_rank_most_damaging"]), float(row["mean_accuracy"])))


def build_rank_correlation_rows(rankings: dict[str, dict], severity: str) -> list[dict]:
    models = sorted(rankings)
    output = []
    for left_index, model_a in enumerate(models):
        for model_b in models[left_index + 1 :]:
            shared = sorted(set(rankings[model_a]) & set(rankings[model_b]))
            left_ranks = [float(rankings[model_a][recipe]["rank"]) for recipe in shared]
            right_ranks = [float(rankings[model_b][recipe]["rank"]) for recipe in shared]
            deltas = [abs(left - right) for left, right in zip(left_ranks, right_ranks)]
            output.append(
                {
                    "model_a": model_a,
                    "model_b": model_b,
                    "severity": severity,
                    "shared_challenges": len(shared),
                    "spearman_rank_correlation": pearson(left_ranks, right_ranks),
                    "mean_abs_rank_delta": statistics.fmean(deltas),
                    "max_abs_rank_delta": max(deltas),
                }
            )
    return sorted(output, key=lambda row: float(row["spearman_rank_correlation"]))


def pearson(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or not left:
        return 0.0
    mean_left = statistics.fmean(left)
    mean_right = statistics.fmean(right)
    centered_left = [value - mean_left for value in left]
    centered_right = [value - mean_right for value in right]
    numerator = sum(a * b for a, b in zip(centered_left, centered_right))
    left_norm = math.sqrt(sum(value * value for value in centered_left))
    right_norm = math.sqrt(sum(value * value for value in centered_right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


def pstdev(values: list[float]) -> float:
    if len(values) <= 1:
        return 0.0
    return statistics.pstdev(values)


def print_headline(consensus_rows: list[dict], correlation_rows: list[dict]) -> None:
    print("Consensus most damaging challenges:")
    for row in consensus_rows[:5]:
        print(
            f"  {row['display_name']}: mean_rank={float(row['mean_rank_most_damaging']):.2f}, "
            f"mean_acc={float(row['mean_accuracy']):.4f}, floor={row['floor_count']}/{row['model_count']}"
        )

    print("Lowest rank correlations:")
    for row in correlation_rows[:5]:
        print(
            f"  {row['model_a']} vs {row['model_b']}: "
            f"rho={float(row['spearman_rank_correlation']):.3f}, "
            f"mean_abs_delta={float(row['mean_abs_rank_delta']):.2f}"
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
