#!/usr/bin/env python3
from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

MODEL_ORDER = [
    "CLIP ViT-B/16",
    "CLIP ViT-B/32",
    "OpenCLIP ViT-B/32 LAION-2B",
    "OpenCLIP ViT-B/16 DataComp-XL",
]

PIPELINE_ORDER = [
    "Messenger upload/download",
    "Phone screenshot/resave",
    "Video-call frame capture",
]

MODEL_COLORS = {
    "CLIP ViT-B/16": "#2f6f73",
    "CLIP ViT-B/32": "#c44e52",
    "OpenCLIP ViT-B/32 LAION-2B": "#4c72b0",
    "OpenCLIP ViT-B/16 DataComp-XL": "#dd8452",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot Real-Transfer v0.2 paper-ready figures.")
    parser.add_argument("--model-table", default="reports/real_transfer_v02_model_pipeline_table.csv")
    parser.add_argument("--drop-output", default="results/real_transfer_v02_source_matched_drops.png")
    parser.add_argument("--heatmap-output", default="results/real_transfer_v02_accuracy_heatmap.png")
    args = parser.parse_args()

    rows = pd.read_csv(resolve_project_path(args.model_table))
    rows["model_name"] = pd.Categorical(rows["model_name"], MODEL_ORDER, ordered=True)
    rows["pipeline_name"] = pd.Categorical(rows["pipeline_name"], PIPELINE_ORDER, ordered=True)
    rows = rows.sort_values(["pipeline_name", "model_name"])

    plot_source_matched_drops(rows, resolve_project_path(args.drop_output))
    plot_accuracy_heatmap(rows, resolve_project_path(args.heatmap_output))
    return 0


def plot_source_matched_drops(rows: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10.2, 5.8))
    offsets = {
        "CLIP ViT-B/16": -0.27,
        "CLIP ViT-B/32": -0.09,
        "OpenCLIP ViT-B/32 LAION-2B": 0.09,
        "OpenCLIP ViT-B/16 DataComp-XL": 0.27,
    }
    pipeline_positions = {name: index for index, name in enumerate(PIPELINE_ORDER)}

    for model_name in MODEL_ORDER:
        subset = rows[rows["model_name"] == model_name]
        y = [pipeline_positions[row["pipeline_name"]] + offsets[model_name] for _, row in subset.iterrows()]
        x = subset["accuracy_drop_vs_matched_clean"].astype(float) * 100
        low = subset["accuracy_drop_ci_low"].astype(float) * 100
        high = subset["accuracy_drop_ci_high"].astype(float) * 100
        xerr = [x - low, high - x]
        ax.errorbar(
            x,
            y,
            xerr=xerr,
            fmt="o",
            markersize=6,
            capsize=3,
            linewidth=1.5,
            color=MODEL_COLORS[model_name],
            label=model_name,
        )

    ax.axvline(0, color="#5c5c5c", linewidth=1.1)
    ax.set_title("Real-transfer v0.2 source-matched accuracy drop", pad=12)
    ax.set_xlabel("Accuracy drop vs matched clean source images (percentage points)")
    ax.set_yticks(list(pipeline_positions.values()))
    ax.set_yticklabels([wrap_label(name, 26) for name in PIPELINE_ORDER])
    ax.grid(axis="x", color="#dedede", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=2)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {output_path}")


def plot_accuracy_heatmap(rows: pd.DataFrame, output_path: Path) -> None:
    pivot = rows.pivot(index="model_name", columns="pipeline_name", values="real_accuracy")
    pivot = pivot.reindex(index=MODEL_ORDER, columns=PIPELINE_ORDER)
    drops = rows.pivot(index="model_name", columns="pipeline_name", values="accuracy_drop_vs_matched_clean")
    drops = drops.reindex(index=MODEL_ORDER, columns=PIPELINE_ORDER)

    fig, ax = plt.subplots(figsize=(9.6, 4.9))
    image = ax.imshow(pivot.values.astype(float), cmap="viridis", vmin=0.65, vmax=0.9, aspect="auto")
    ax.set_title("Real-transfer v0.2 accuracy by model and pipeline", pad=12)
    ax.set_xticks(range(len(PIPELINE_ORDER)))
    ax.set_xticklabels([wrap_label(name, 18) for name in PIPELINE_ORDER])
    ax.set_yticks(range(len(MODEL_ORDER)))
    ax.set_yticklabels(MODEL_ORDER)

    for row_index, model_name in enumerate(MODEL_ORDER):
        for col_index, pipeline_name in enumerate(PIPELINE_ORDER):
            accuracy = float(pivot.loc[model_name, pipeline_name])
            drop = float(drops.loc[model_name, pipeline_name])
            color = "white" if accuracy < 0.77 else "#1f1f1f"
            ax.text(
                col_index,
                row_index,
                f"{accuracy * 100:.1f}%\n{drop * 100:+.1f} pp",
                ha="center",
                va="center",
                color=color,
                fontsize=9,
            )

    colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    colorbar.set_label("Real-transfer accuracy")
    ax.tick_params(axis="both", length=0)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {output_path}")


def wrap_label(label: str, width: int) -> str:
    return "\n".join(textwrap.wrap(label, width=width))


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
