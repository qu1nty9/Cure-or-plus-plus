#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot weighted mean native CURE-OR accuracy by challenge level.")
    parser.add_argument("--input", default="results/full_cure_or_probe_v04_comparison.csv")
    parser.add_argument("--output", default="results/full_cure_or_probe_v04_mean_accuracy_by_level.png")
    parser.add_argument("--title", default="Full-CURE-OR probe: mean accuracy by native challenge level")
    args = parser.parse_args()

    input_path = resolve_project_path(args.input)
    output_path = resolve_project_path(args.output)

    df = pd.read_csv(input_path)
    native = df[df["family"].eq("native_cure_or")].copy()
    if native.empty:
        raise ValueError(f"No native_cure_or rows found in {input_path}")

    native["n"] = native["n"].astype(int)
    native["accuracy"] = native["accuracy"].astype(float)
    native["level"] = native["severity"].map(parse_level)
    native = native.dropna(subset=["level"]).copy()
    native["level"] = native["level"].astype(int)

    grouped = (
        native.groupby(["model_name", "level"], as_index=False)
        .apply(weighted_accuracy, include_groups=False)
        .reset_index(drop=True)
    )

    clean = df[df["family"].eq("clean")].copy()
    clean["accuracy"] = clean["accuracy"].astype(float)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9.4, 5.4))
    colors = ["#1f77b4", "#d62728", "#2ca02c", "#9467bd", "#ff7f0e", "#17becf", "#8c564b", "#7f7f7f"]

    for color, (model_name, model_rows) in zip(colors, grouped.groupby("model_name")):
        model_rows = model_rows.sort_values("level")
        ax.plot(
            model_rows["level"],
            model_rows["weighted_accuracy"],
            marker="o",
            linewidth=2.4,
            color=color,
            label=model_name,
        )
        clean_rows = clean[clean["model_name"].eq(model_name)]
        if not clean_rows.empty:
            ax.axhline(
                clean_rows["accuracy"].iloc[0],
                color=color,
                linestyle="--",
                linewidth=1.2,
                alpha=0.45,
            )

    ax.set_title(args.title)
    ax.set_xlabel("Native CURE-OR challenge level")
    ax.set_ylabel("Weighted mean accuracy")
    ax.set_xticks(sorted(grouped["level"].unique()))
    max_accuracy = max(float(grouped["weighted_accuracy"].max()), float(clean["accuracy"].max()))
    ax.set_ylim(0.0, min(1.0, max(0.5, max_accuracy * 1.12)))
    ax.grid(axis="y", alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    print(f"Wrote {output_path}")
    return 0


def weighted_accuracy(group: pd.DataFrame) -> pd.Series:
    weight_sum = group["n"].sum()
    if weight_sum <= 0:
        raise ValueError("Cannot compute weighted accuracy with non-positive total n")
    return pd.Series(
        {
            "weighted_accuracy": (group["accuracy"] * group["n"]).sum() / weight_sum,
            "n": weight_sum,
            "cells": len(group),
        }
    )


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
