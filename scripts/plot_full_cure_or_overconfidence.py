#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot Full-CURE-OR overconfidence ranking by challenge.")
    parser.add_argument("--input", default="results/full_cure_or_probe_v04_overconfidence_ranking.csv")
    parser.add_argument("--output", default="results/full_cure_or_probe_v04_level5_overconfidence.png")
    parser.add_argument("--severity", default="level_5")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--title", default="Full-CURE-OR v0.4: level-5 overconfidence gaps")
    args = parser.parse_args()

    df = pd.read_csv(resolve_project_path(args.input))
    df = df[df["severity"].eq(args.severity)].copy()
    if df.empty:
        raise ValueError(f"No rows found for severity={args.severity}")

    for column in ["calibration_gap", "accuracy", "mean_confidence", "high_conf_wrong_rate"]:
        df[column] = df[column].astype(float)

    models = list(df["model_name"].drop_duplicates())

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(
        nrows=1,
        ncols=len(models),
        figsize=(12.0, 5.3),
        sharex=True,
        squeeze=False,
    )
    axes_flat = axes[0]

    for ax, model_name in zip(axes_flat, models):
        rows = df[df["model_name"].eq(model_name)].sort_values("calibration_gap", ascending=False).head(args.top_k)
        labels = rows["recipe"].str.replace("native_challenge_type_", "type ", regex=False)
        ax.barh(labels, rows["calibration_gap"], color="#b45f06")
        ax.set_title(model_name)
        ax.set_xlabel("Confidence - accuracy")
        ax.set_xlim(0, max(0.05, df["calibration_gap"].max() * 1.08))
        ax.grid(axis="x", alpha=0.25)
        ax.spines[["top", "right"]].set_visible(False)
        ax.invert_yaxis()

    axes_flat[0].set_ylabel(args.severity.replace("_", "-") + " native challenge")
    fig.suptitle(args.title, y=0.99)
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
