#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot native mini-CURE-OR severity curves.")
    parser.add_argument("--input", default="results/native_pilot_v01_comparison.csv")
    parser.add_argument("--output", default="results/native_pilot_v01_severity_curves.png")
    parser.add_argument("--title", default="Native mini-CURE-OR pilot: accuracy by challenge level")
    args = parser.parse_args()

    input_path = resolve_project_path(args.input)
    output_path = resolve_project_path(args.output)

    df = pd.read_csv(input_path)
    native = df[df["family"] == "native_cure_or"].copy()
    native["severity_idx"] = native["severity"].str.replace("level_", "", regex=False).astype(int)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    for (model_name, recipe), group in native.sort_values("severity_idx").groupby(["model_name", "recipe"]):
        label = f"{model_name} / {recipe.replace('native_challenge_type_', 'type ')}"
        ax.plot(
            group["severity_idx"],
            group["accuracy"],
            marker="o",
            linewidth=2.0,
            label=label,
        )

    ax.set_title(args.title)
    ax.set_xlabel("Native CURE-OR challenge level")
    ax.set_ylabel("Accuracy")
    ax.set_xticks([1, 2, 3, 4])
    ax.set_ylim(0, 1)
    ax.grid(axis="y", alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False, fontsize=8, ncols=2)
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
