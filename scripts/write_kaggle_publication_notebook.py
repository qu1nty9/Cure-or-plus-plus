#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "notebooks/cure_or_pp_kaggle_v041_public.ipynb"
KAGGLE_DIR = ROOT / "kaggle/public_kernel_v041"
KAGGLE_NOTEBOOK_PATH = KAGGLE_DIR / "cure_or_pp_kaggle_v041_public.ipynb"


def main() -> int:
    notebook = {
        "cells": with_cell_ids(cells()),
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=1) + "\n", encoding="utf-8")
    KAGGLE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(NOTEBOOK_PATH, KAGGLE_NOTEBOOK_PATH)
    write_kernel_metadata(KAGGLE_DIR / "kernel-metadata.json")
    print(NOTEBOOK_PATH)
    print(KAGGLE_NOTEBOOK_PATH)
    return 0


def md(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")],
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in text.strip().split("\n")],
    }


def with_cell_ids(notebook_cells: list[dict]) -> list[dict]:
    for index, cell in enumerate(notebook_cells, start=1):
        cell["id"] = f"cure-or-pp-v041-{index:02d}"
    return notebook_cells


def cells() -> list[dict]:
    return [
        md(
            """
# CURE-OR++ v0.4.1: Object Recognition Robustness Under Native and Real Transfer Stress

This notebook is the public Kaggle writeup for the CURE-OR++ v0.4.1 aggregate
release. It reads only public aggregate tables and generated figures; it does
not require raw CURE-OR images, local real-transfer photos, hosted-provider raw
JSONL responses, provider caches, or API keys.

The benchmark asks a narrow robustness question: do object-recognition systems
share stable failure patterns when clean object images move into severe native
challenge conditions and real digital transfer pipelines?

TL;DR:

- Severe native CURE-OR failures are stable across model families.
- Grayscale alone does not explain the level-5 collapse.
- Real-transfer v0.2 is a small external-validity guardrail, not a leaderboard.
- VLM rows measure both recognition accuracy and generation stability.
- Hosted-provider rows are useful but should be interpreted separately because
  providers control model versioning and data handling.

Version DOI: https://doi.org/10.5281/zenodo.21239828

GitHub release: https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1
"""
        ),
        code(
            """
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_columns', 120)
plt.rcParams['figure.dpi'] = 120

CANDIDATE_ROOTS = [
    Path('/kaggle/input/cure-or-plus-plus-v041-public'),
    Path('/kaggle/input/cure-or-plus-plus-v041-public-flat'),
    Path('/kaggle/input/cure-or-plus-plus-v041-public-benchmark-aggregates'),
    Path('../kaggle/cure-or-plus-plus-v041-public'),
    Path('../kaggle/cure-or-plus-plus-v041-public-flat'),
    Path('kaggle/cure-or-plus-plus-v041-public'),
    Path('kaggle/cure-or-plus-plus-v041-public-flat'),
    Path('.'),
]

def artifact_path(relative_path):
    direct = DATA_ROOT / relative_path
    if direct.exists():
        return direct
    flat = DATA_ROOT / str(relative_path).replace('/', '__')
    if flat.exists():
        return flat
    raise FileNotFoundError(f'Missing artifact: {relative_path}')

DATA_ROOT = next(
    (
        path
        for path in CANDIDATE_ROOTS
        if (path / 'reports/full_cure_or_paper_model_table_v04.csv').exists()
        or (path / 'reports__full_cure_or_paper_model_table_v04.csv').exists()
    ),
    None,
)
if DATA_ROOT is None:
    raise FileNotFoundError('Could not find the CURE-OR++ v0.4.1 public aggregate package.')

print(DATA_ROOT)
"""
        ),
        md(
            """
## Load the Public Aggregate Tables

The package has four evidence blocks:

- Full-CURE-OR native challenge probe.
- Real-transfer v0.2 source-matched validation.
- Open-weight VLM v0.3 prompt-pack runs.
- Hosted-provider VLM comparison rows.
"""
        ),
        code(
            """
full_models = pd.read_csv(artifact_path('reports/full_cure_or_paper_model_table_v04.csv'))
full_failures = pd.read_csv(artifact_path('reports/full_cure_or_paper_failure_table_v04.csv'))
full_control = pd.read_csv(artifact_path('reports/full_cure_or_paper_control_table_v04.csv'))

real_transfer = pd.read_csv(artifact_path('reports/real_transfer_v02_model_pipeline_table.csv'))
real_transfer_consensus = pd.read_csv(artifact_path('reports/real_transfer_v02_pipeline_consensus_table.csv'))

vlm_open = pd.read_csv(artifact_path('reports/vlm_open_weight_full_v03_paper_table.csv'))
vlm_provider_v03 = pd.read_csv(artifact_path('reports/vlm_provider_full_v03_comparison.csv'))
vlm_provider_v01 = pd.read_csv(artifact_path('reports/vlm_provider_full_v01_comparison.csv'))

print(f'Full-CURE-OR baseline rows: {len(full_models)}')
print(f'Real-transfer model/pipeline rows: {len(real_transfer)}')
print(f'Open-weight VLM rows: {len(vlm_open)}')
print(f'Hosted-provider v0.1 rows: {len(vlm_provider_v01)}')
print(f'Hosted-provider v0.3 rows: {len(vlm_provider_v03)}')
"""
        ),
        md(
            """
## Native CURE-OR Stress Test

The strongest level-5 row is DINOv2 ViT-S/14 Prototype, but all usable
baselines still collapse on the hardest native challenge families. The point is
not a single winner; it is the stable severe-challenge failure structure across
model families.
"""
        ),
        code(
            """
cols = [
    'model_name',
    'clean_accuracy',
    'native_mean_accuracy',
    'native_level_5_accuracy',
    'level_5_drop_vs_clean',
    'worst_level_5_challenge',
]
full_models[cols].sort_values('native_level_5_accuracy', ascending=False)
"""
        ),
        code(
            """
plot_df = full_models.sort_values('native_level_5_accuracy')

fig, ax = plt.subplots(figsize=(8.5, 4.8))
ax.barh(plot_df['model_name'], plot_df['native_level_5_accuracy'], color='#2f6f73')
ax.set_xlabel('Native level-5 accuracy')
ax.set_title('Full-CURE-OR v0.4 severe native challenge accuracy')
ax.set_xlim(0, max(0.32, plot_df['native_level_5_accuracy'].max() + 0.04))
ax.grid(axis='x', alpha=0.25)
ax.spines[['top', 'right']].set_visible(False)
for i, value in enumerate(plot_df['native_level_5_accuracy']):
    ax.text(value + 0.006, i, f'{value:.3f}', va='center', fontsize=8)
plt.tight_layout()
"""
        ),
        md(
            """
## Consensus Failure Core

The hardest level-5 conditions are not model-specific accidents. Grayscale
salt-and-pepper noise, salt-and-pepper noise, and grayscale gaussian blur are
floor-level failures for all eight usable baselines.
"""
        ),
        code(
            """
full_failures[['rank', 'display_name', 'mean_accuracy', 'floor_count', 'top3_count', 'model_count']]
"""
        ),
        md(
            """
## Grayscale Control

The type-10 grayscale no-challenge control is damaging, but it does not explain
the full severe native collapse. For every usable model, native level-5
accuracy is much lower than grayscale-control accuracy.
"""
        ),
        code(
            """
full_control[
    [
        'model_name',
        'clean_accuracy',
        'grayscale_control_accuracy',
        'native_level_5_accuracy',
        'control_minus_native_level_5',
    ]
].sort_values('control_minus_native_level_5', ascending=False)
"""
        ),
        md(
            """
## Real-Transfer v0.2 Guardrail

Real-transfer v0.2 uses 30 clean sources, three app/device transfer pipelines,
and two repeats per source/pipeline. The measured effects are moderate, not
catastrophic. Video-call frame capture is the largest mean source-matched drop
in this block.
"""
        ),
        code(
            """
real_transfer_consensus[
    [
        'pipeline_name',
        'model_count',
        'mean_real_accuracy',
        'mean_accuracy_drop_vs_matched_clean',
        'worst_model',
    ]
].sort_values('mean_accuracy_drop_vs_matched_clean', ascending=False)
"""
        ),
        code(
            """
rt_plot = real_transfer_consensus.sort_values('mean_accuracy_drop_vs_matched_clean')

fig, ax = plt.subplots(figsize=(8, 3.8))
ax.barh(rt_plot['pipeline_name'], 100 * rt_plot['mean_accuracy_drop_vs_matched_clean'], color='#c44e52')
ax.axvline(0, color='#333333', linewidth=1)
ax.set_xlabel('Mean accuracy drop vs matched clean source images (percentage points)')
ax.set_title('Real-transfer v0.2 source-matched drop by pipeline')
ax.grid(axis='x', alpha=0.25)
ax.spines[['top', 'right']].set_visible(False)
for i, value in enumerate(100 * rt_plot['mean_accuracy_drop_vs_matched_clean']):
    ax.text(value + 0.15, i, f'{value:.1f}', va='center', fontsize=8)
plt.tight_layout()
"""
        ),
        md(
            """
## Open-Weight VLM Prompt-Pack Runs

The open-weight VLM track uses a 900-row prompt pack with 100 clean rows and
800 real-transfer rows per model. It measures both recognition accuracy and
generation stability, because unparseable answers are a real failure mode for
assistant-style object recognition.
"""
        ),
        code(
            """
vlm_open[
    [
        'display_name',
        'clean_accuracy',
        'real_accuracy',
        'accuracy_drop_vs_clean',
        'real_unparseable_rate',
        'hardest_pipeline',
        'hardest_label',
    ]
].sort_values('real_accuracy', ascending=False)
"""
        ),
        code(
            """
open_plot = vlm_open.sort_values('real_accuracy')

fig, ax = plt.subplots(figsize=(8.5, 4.2))
ax.barh(open_plot['display_name'], open_plot['real_accuracy'], color='#4c72b0')
ax.set_xlabel('Real-transfer accuracy')
ax.set_title('Open-weight VLM v0.3 real-transfer accuracy')
ax.set_xlim(0.80, 1.0)
ax.grid(axis='x', alpha=0.25)
ax.spines[['top', 'right']].set_visible(False)
for i, value in enumerate(open_plot['real_accuracy']):
    ax.text(value + 0.002, i, f'{value:.3f}', va='center', fontsize=8)
plt.tight_layout()
"""
        ),
        md(
            """
## Hosted-Provider VLM Rows

Hosted-provider rows are reported separately because external providers control
model versioning, pricing, caching, and data-handling behavior. The 900-row
v0.3 hosted row currently contains xAI Grok 4.3 with a repeat run tracked in
the repository; the 210-row v0.1 comparison covers OpenAI, xAI, Anthropic, and
GigaChat rows.
"""
        ),
        code(
            """
vlm_provider_v03[
    [
        'display_name',
        'provider',
        'clean_accuracy',
        'real_accuracy',
        'accuracy_drop_vs_clean',
        'real_unparseable_rate',
        'hardest_pipeline',
        'hardest_label',
    ]
]
"""
        ),
        code(
            """
vlm_provider_v01[
    [
        'display_name',
        'provider',
        'clean_accuracy',
        'real_accuracy',
        'accuracy_drop_vs_clean',
        'real_unparseable_rate',
        'hardest_pipeline',
        'hardest_label',
    ]
].sort_values('real_accuracy', ascending=False)
"""
        ),
        md(
            """
## What This Gives Us

The current evidence package supports a serious benchmark claim:

- native CURE-OR severe challenge failures are stable across model families;
- grayscale alone does not explain the severe challenge collapse;
- real app/device transfer produces moderate but model-dependent drops;
- open-weight VLMs can be strong while still exposing generation-stability
  failures;
- hosted-provider VLMs can be evaluated under the same prompt, parser, and
  audit protocol, but should remain separated from open-weight rows.

The important release boundary is also part of the result: this public package
is auditable without redistributing raw upstream images or private provider
payloads. That boundary is not a limitation to hide; it is what makes the
Kaggle package publishable while keeping the full source and DOI trail
available through GitHub and Zenodo.
"""
        ),
        md(
            """
## Reproducibility and Data Boundary

Use the GitHub release and DOI for the complete source package, paper, release
checks, and reproducibility notes.

- Version DOI: https://doi.org/10.5281/zenodo.21239828
- GitHub release: https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1

Raw CURE-OR images, mini-CURE-OR images, local real-transfer photos, hosted
provider raw JSONL files, provider caches, and credentials are intentionally
excluded from this Kaggle package. Users should obtain upstream CURE-OR under
its own terms and rerun the documented pipeline if they need image-level
reproduction.
"""
        ),
    ]


def write_kernel_metadata(path: Path) -> None:
    metadata = {
        "id": "yaroslavkholmirzayev/cure-or-v0-4-1-public-benchmark-writeup",
        "title": "CURE-OR++ v0.4.1 Public Benchmark Writeup",
        "code_file": "cure_or_pp_kaggle_v041_public.ipynb",
        "language": "python",
        "kernel_type": "notebook",
        "is_private": False,
        "enable_gpu": False,
        "enable_internet": False,
        "dataset_sources": [
            "yaroslavkholmirzayev/cure-or-plus-plus-v041-public-flat",
        ],
    }
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
