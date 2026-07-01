#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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
    parser.add_argument("--model-specs-json", default="")
    parser.add_argument("--pipeline-specs-json", default="")
    parser.add_argument("--title-prefix", default="Real-transfer v0.2")
    args = parser.parse_args()

    model_order = load_model_order(args.model_specs_json)
    pipeline_order = load_pipeline_order(args.pipeline_specs_json)
    model_colors = build_model_colors(model_order)

    rows = pd.read_csv(resolve_project_path(args.model_table))
    rows["model_name"] = pd.Categorical(rows["model_name"], model_order, ordered=True)
    rows["pipeline_name"] = pd.Categorical(rows["pipeline_name"], pipeline_order, ordered=True)
    rows = rows.sort_values(["pipeline_name", "model_name"])

    plot_source_matched_drops(
        rows,
        resolve_project_path(args.drop_output),
        model_order,
        pipeline_order,
        model_colors,
        args.title_prefix,
    )
    plot_accuracy_heatmap(
        rows,
        resolve_project_path(args.heatmap_output),
        model_order,
        pipeline_order,
        args.title_prefix,
    )
    return 0


def plot_source_matched_drops(
    rows: pd.DataFrame,
    output_path: Path,
    model_order: list[str],
    pipeline_order: list[str],
    model_colors: dict[str, str],
    title_prefix: str,
) -> None:
    fig, ax = plt.subplots(figsize=(10.2, 5.8))
    offsets = build_offsets(model_order)
    pipeline_positions = {name: index for index, name in enumerate(pipeline_order)}

    for model_name in model_order:
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
    ax.set_title(f"{title_prefix} source-matched accuracy drop", pad=12)
    ax.set_xlabel("Accuracy drop vs matched clean source images (percentage points)")
    ax.set_yticks(list(pipeline_positions.values()))
    ax.set_yticklabels([wrap_label(name, 26) for name in pipeline_order])
    ax.grid(axis="x", color="#dedede", linewidth=0.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, -0.28), ncol=2)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {output_path}")


def plot_accuracy_heatmap(
    rows: pd.DataFrame,
    output_path: Path,
    model_order: list[str],
    pipeline_order: list[str],
    title_prefix: str,
) -> None:
    pivot = rows.pivot(index="model_name", columns="pipeline_name", values="real_accuracy")
    pivot = pivot.reindex(index=model_order, columns=pipeline_order)
    drops = rows.pivot(index="model_name", columns="pipeline_name", values="accuracy_drop_vs_matched_clean")
    drops = drops.reindex(index=model_order, columns=pipeline_order)

    fig, ax = plt.subplots(figsize=(9.6, 4.9))
    image = ax.imshow(pivot.values.astype(float), cmap="viridis", vmin=0.65, vmax=0.9, aspect="auto")
    ax.set_title(f"{title_prefix} accuracy by model and pipeline", pad=12)
    ax.set_xticks(range(len(pipeline_order)))
    ax.set_xticklabels([wrap_label(name, 18) for name in pipeline_order])
    ax.set_yticks(range(len(model_order)))
    ax.set_yticklabels(model_order)

    for row_index, model_name in enumerate(model_order):
        for col_index, pipeline_name in enumerate(pipeline_order):
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


def load_model_order(path: str) -> list[str]:
    if not path:
        return MODEL_ORDER
    specs = json.loads(resolve_project_path(path).read_text(encoding="utf-8"))
    return [row["model_name"] for row in specs]


def load_pipeline_order(path: str) -> list[str]:
    if not path:
        return PIPELINE_ORDER
    specs = json.loads(resolve_project_path(path).read_text(encoding="utf-8"))
    return [row["pipeline_name"] for row in specs]


def build_offsets(model_order: list[str]) -> dict[str, float]:
    if len(model_order) == 1:
        return {model_order[0]: 0.0}
    step = 0.54 / max(1, len(model_order) - 1)
    start = -0.27
    return {model_name: start + index * step for index, model_name in enumerate(model_order)}


def build_model_colors(model_order: list[str]) -> dict[str, str]:
    palette = [
        "#2f6f73",
        "#c44e52",
        "#4c72b0",
        "#dd8452",
        "#55a868",
        "#8172b2",
        "#937860",
        "#64b5cd",
    ]
    return {
        model_name: MODEL_COLORS.get(model_name, palette[index % len(palette)])
        for index, model_name in enumerate(model_order)
    }


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
