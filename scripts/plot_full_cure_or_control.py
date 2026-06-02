#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot Full-CURE-OR grayscale control comparison.")
    parser.add_argument("--input", default="results/full_cure_or_grayscale_control_v04_comparison.csv")
    parser.add_argument("--output", default="results/full_cure_or_grayscale_control_v04_comparison.png")
    parser.add_argument("--title", default="Full-CURE-OR v0.4: grayscale control vs native severity")
    args = parser.parse_args()

    df = pd.read_csv(resolve_project_path(args.input))
    metrics = [
        ("clean_accuracy", "clean"),
        ("control_accuracy", "grayscale control"),
        ("native_level_1_accuracy", "native level 1"),
        ("native_level_5_accuracy", "native level 5"),
    ]

    plot_rows = []
    for _, row in df.iterrows():
        for column, label in metrics:
            plot_rows.append(
                {
                    "model_name": row["model_name"],
                    "condition": label,
                    "accuracy": float(row[column]),
                }
            )
    plot_df = pd.DataFrame(plot_rows)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(max(10.2, len(df) * 2.25), 5.4))
    colors = ["#4c78a8", "#f58518", "#54a24b", "#e45756"]
    models = list(df["model_name"])
    width = 0.18
    x_positions = range(len(models))

    for offset, ((_, label), color) in enumerate(zip(metrics, colors)):
        values = [
            plot_df[(plot_df["model_name"] == model) & (plot_df["condition"] == label)]["accuracy"].iloc[0]
            for model in models
        ]
        positions = [x + (offset - 1.5) * width for x in x_positions]
        ax.bar(positions, values, width=width, color=color, label=label)

    ax.set_title(args.title)
    ax.set_ylabel("Accuracy")
    max_accuracy = max(float(plot_df["accuracy"].max()), 0.5)
    ax.set_ylim(0.0, min(1.0, max_accuracy * 1.12))
    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(models, rotation=18, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()

    output_path = resolve_project_path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    print(f"Wrote {output_path}")
    return 0


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
