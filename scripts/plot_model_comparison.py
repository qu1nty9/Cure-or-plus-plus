#!/usr/bin/env python3
from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot high-severity CURE-OR++ model comparison.")
    parser.add_argument("--comparison", default="results/model_comparison_v01.csv")
    parser.add_argument("--output", default="results/model_comparison_v01_high_severity.png")
    args = parser.parse_args()

    comparison_path = resolve_project_path(args.comparison)
    output_path = resolve_project_path(args.output)

    rows = pd.read_csv(comparison_path)
    high = rows[(rows["severity"] == "high") & (rows["family"] != "clean")].copy()
    if high.empty:
        raise ValueError(f"No high-severity rows found in {comparison_path}")

    recipe_order = build_recipe_order(high)
    model_order = list(high["model_name"].drop_duplicates())
    pivot = high.pivot_table(index="recipe", columns="model_name", values="accuracy", aggfunc="first")
    pivot = pivot.reindex(recipe_order)

    fig, ax = plt.subplots(figsize=(12, 5.8))
    colors = ["#2f6f73", "#c44e52", "#4c72b0", "#8172b3", "#dd8452"]
    x = list(range(len(recipe_order)))

    for idx, model_name in enumerate(model_order):
        if model_name not in pivot.columns:
            continue
        ax.plot(
            x,
            pivot[model_name],
            marker="o",
            linewidth=2.2,
            markersize=6,
            color=colors[idx % len(colors)],
            label=model_name,
        )

    ax.set_title("CURE-OR++ v0.1 high-severity accuracy by recipe", pad=14)
    ax.set_ylabel("Accuracy")
    ax.set_xlabel("")
    ax.set_ylim(max(0.0, float(high["accuracy"].min()) - 0.08), min(1.0, float(high["accuracy"].max()) + 0.08))
    ax.set_xticks(x)
    ax.set_xticklabels([wrap_recipe(recipe) for recipe in recipe_order], rotation=0, ha="center")
    ax.grid(axis="y", color="#d9d9d9", linewidth=0.8, alpha=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=3)

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    print(f"Wrote {output_path}")
    return 0


def build_recipe_order(rows: pd.DataFrame) -> list[str]:
    family_order = {"classic": 0, "modern_transfer": 1}
    recipes = rows[["family", "recipe"]].drop_duplicates()
    recipes = recipes.sort_values(
        by=["family", "recipe"],
        key=lambda column: column.map(family_order).fillna(99) if column.name == "family" else column,
    )
    return recipes["recipe"].tolist()


def wrap_recipe(recipe: str) -> str:
    return "\n".join(textwrap.wrap(recipe.replace("_", " "), width=14))


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
