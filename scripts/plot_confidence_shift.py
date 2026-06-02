#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot CURE-OR++ high-severity confidence shifts.")
    parser.add_argument("--input", default="results/confidence_shift_v01.csv")
    parser.add_argument("--output", default="results/confidence_shift_v01_high_severity.png")
    args = parser.parse_args()

    input_path = resolve_project_path(args.input)
    output_path = resolve_project_path(args.output)

    df = pd.read_csv(input_path)
    high = df[(df["severity"] == "high") & (df["family"] != "clean")].copy()
    high = high[high["accuracy_drop"].notna() & high["confidence_drop"].notna()]
    high["accuracy_drop"] = high["accuracy_drop"].astype(float)
    high["confidence_drop"] = high["confidence_drop"].astype(float)

    import matplotlib.pyplot as plt

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9.5, 6))
    for model_name, group in high.groupby("model_name"):
        ax.scatter(group["accuracy_drop"], group["confidence_drop"], s=58, alpha=0.82, label=model_name)

    worst = high.sort_values("accuracy_drop", ascending=False).head(6)
    for _, row in worst.iterrows():
        ax.annotate(
            row["recipe"].replace("_", " "),
            (row["accuracy_drop"], row["confidence_drop"]),
            xytext=(5, 4),
            textcoords="offset points",
            fontsize=8,
        )

    ax.axhline(0, color="#777777", linewidth=1, alpha=0.5)
    ax.axvline(0, color="#777777", linewidth=1, alpha=0.5)
    ax.set_xlabel("Accuracy drop vs clean")
    ax.set_ylabel("Mean confidence drop vs clean")
    ax.set_title("CURE-OR++ v0.1 high-severity confidence shifts")
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8, loc="best")
    plt.tight_layout()
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
