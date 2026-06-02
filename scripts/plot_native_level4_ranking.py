#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot native mini-CURE-OR level-4 challenge ranking.")
    parser.add_argument("--input", default="results/native_test_v01_level4_ranking.csv")
    parser.add_argument("--output", default="results/native_test_v01_level4_ranking.png")
    parser.add_argument("--title", default="Native mini-CURE-OR test grid: level-4 accuracy by challenge")
    parser.add_argument("--ylabel", default="Level-4 native challenge")
    parser.add_argument("--xmax", type=float, default=1.0)
    args = parser.parse_args()

    input_path = resolve_project_path(args.input)
    output_path = resolve_project_path(args.output)

    df = pd.read_csv(input_path)
    if df.empty:
        raise ValueError(f"No rows found in {input_path}")

    df["accuracy"] = df["accuracy"].astype(float)
    models = list(df["model_name"].drop_duplicates())

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(
        nrows=1,
        ncols=len(models),
        figsize=(max(11.5, len(models) * 3.0), 5.8),
        sharex=True,
        squeeze=False,
    )
    axes_flat = axes[0]

    for ax, model_name in zip(axes_flat, models):
        model_rows = df[df["model_name"] == model_name].sort_values("accuracy", ascending=True).copy()
        labels = model_rows["recipe"].str.replace("native_challenge_type_", "type ", regex=False)
        ax.barh(labels, model_rows["accuracy"], color="#4c78a8")
        ax.set_title(model_name)
        ax.set_xlim(0, args.xmax)
        ax.grid(axis="x", alpha=0.25)
        ax.spines[["top", "right"]].set_visible(False)
        ax.invert_yaxis()
        ax.set_xlabel("Accuracy")

    axes_flat[0].set_ylabel(args.ylabel)
    fig.suptitle(args.title, y=0.99)
    plt.tight_layout()
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
