#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot Full-CURE-OR confidence and calibration by challenge level.")
    parser.add_argument("--input", default="results/full_cure_or_probe_v04_confidence_by_level.csv")
    parser.add_argument("--output", default="results/full_cure_or_probe_v04_confidence_by_level.png")
    parser.add_argument("--title", default="Full-CURE-OR v0.4: accuracy, confidence, and calibration by level")
    args = parser.parse_args()

    df = pd.read_csv(resolve_project_path(args.input))
    native = df[df["family"].eq("native_cure_or")].copy()
    native["level"] = native["severity"].map(parse_level)
    native = native.dropna(subset=["level"]).copy()
    native["level"] = native["level"].astype(int)
    for column in ["accuracy", "mean_confidence", "calibration_gap"]:
        native[column] = native[column].astype(float)

    import matplotlib.pyplot as plt

    colors = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd", "#ff7f0e"]
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(9.4, 7.0), sharex=True)

    for color, (model_name, rows) in zip(colors, native.groupby("model_name", sort=False)):
        rows = rows.sort_values("level")
        axes[0].plot(rows["level"], rows["accuracy"], marker="o", linewidth=2.2, color=color, label=f"{model_name} accuracy")
        axes[0].plot(
            rows["level"],
            rows["mean_confidence"],
            marker="s",
            linewidth=1.8,
            linestyle="--",
            color=color,
            alpha=0.78,
            label=f"{model_name} confidence",
        )
        axes[1].plot(rows["level"], rows["calibration_gap"], marker="o", linewidth=2.2, color=color, label=model_name)

    axes[0].set_ylabel("Weighted mean")
    axes[0].set_ylim(0.0, 1.0)
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].spines[["top", "right"]].set_visible(False)
    axes[0].legend(frameon=False, fontsize=8, ncols=2, loc="upper right")

    axes[1].axhline(0, color="#777777", linewidth=1.0, alpha=0.55)
    axes[1].set_xlabel("Native CURE-OR challenge level")
    axes[1].set_ylabel("Mean confidence - accuracy")
    axes[1].set_xticks(sorted(native["level"].unique()))
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].spines[["top", "right"]].set_visible(False)
    axes[1].legend(frameon=False, fontsize=8, loc="upper right")

    fig.suptitle(args.title)
    fig.tight_layout()
    output_path = resolve_project_path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    print(f"Wrote {output_path}")
    return 0


def parse_level(value: str) -> int | None:
    match = re.fullmatch(r"level_(\d+)", str(value))
    if not match:
        return None
    return int(match.group(1))


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
