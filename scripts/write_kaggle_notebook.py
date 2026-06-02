#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = ROOT / "notebooks/cure_or_pp_kaggle_v01.ipynb"
KAGGLE_NOTEBOOK_PATH = ROOT / "kaggle/kernel/cure_or_pp_kaggle_v01.ipynb"


def main() -> int:
    notebook = json.loads(NOTEBOOK_PATH.read_text(encoding="utf-8"))
    notebook["cells"] = cells()
    NOTEBOOK_PATH.write_text(json.dumps(notebook, indent=1) + "\n", encoding="utf-8")
    KAGGLE_NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(NOTEBOOK_PATH, KAGGLE_NOTEBOOK_PATH)
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


def cells() -> list[dict]:
    return [
        md(
            """
# CURE-OR++ v0.1: Modern Transfer Distortion Baseline

This notebook is the first public-facing CURE-OR++ experiment. The goal is to
test whether modern digital transfer chains create a different robustness
profile from classic single-step corruptions.

We use a compact derived dataset from mini-CURE-OR: 250 clean source images,
6,750 generated distorted images, two OpenAI CLIP zero-shot baselines, an
OpenCLIP zero-shot baseline, a SigLIP diagnostic baseline, and two clean-train
prototype baselines for cross-model comparison.
"""
        ),
        code(
            """
from pathlib import Path
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

CANDIDATE_ROOTS = [
    Path('/kaggle/input/cure-or-plus-plus-v01'),
    Path('/kaggle/input/cure-or-modern-transfer-distortions-v01'),
    Path('../kaggle/cure-or-plus-plus-v01'),
    Path('kaggle/cure-or-plus-plus-v01'),
    Path('.'),
]

DATA_ROOT = next((path for path in CANDIDATE_ROOTS if (path / 'metadata/distortion_manifest.csv').exists()), None)
if DATA_ROOT is None:
    raise FileNotFoundError('Could not find CURE-OR++ dataset root. Update CANDIDATE_ROOTS.')

DATA_ROOT
"""
        ),
        md(
            """
## Load Metadata

The manifests preserve the original mini-CURE-OR labels and the generated
distortion recipe for every image.
"""
        ),
        code(
            """
clean = pd.read_csv(DATA_ROOT / 'metadata/clean_manifest.csv')
distorted = pd.read_csv(DATA_ROOT / 'metadata/distortion_manifest.csv')
summary = pd.read_csv(DATA_ROOT / 'results/clip_vit_b32_v01_summary.csv')
predictions = pd.read_csv(DATA_ROOT / 'results/clip_vit_b32_v01_predictions.csv')

comparison_path = DATA_ROOT / 'results/model_comparison_v01.csv'
ranking_path = DATA_ROOT / 'results/model_ranking_shift_v01.csv'
per_class_path = DATA_ROOT / 'results/per_class_failures_v01.csv'
confidence_path = DATA_ROOT / 'results/confidence_shift_v01.csv'
model_comparison = pd.read_csv(comparison_path) if comparison_path.exists() else None
model_ranking = pd.read_csv(ranking_path) if ranking_path.exists() else None
per_class = pd.read_csv(per_class_path) if per_class_path.exists() else None
confidence = pd.read_csv(confidence_path) if confidence_path.exists() else None

print(f'clean images: {len(clean):,}')
print(f'distorted images: {len(distorted):,}')
print(f'evaluated images: {len(predictions):,}')
print(f\"classes: {clean['label'].nunique()}\")

clean['label'].value_counts().sort_index()
"""
        ),
        md(
            """
## Distortion Families

CURE-OR++ v0.1 separates classic corruptions from modern transfer chains. The
first group is a sanity anchor; the second group is the main research direction.
"""
        ),
        code(
            """
distorted.groupby(['family', 'recipe', 'severity']).size().rename('n').reset_index().head(20)
"""
        ),
        md(
            """
## Visual Check

A quick look at one source image across recipes helps catch obvious generation
issues before interpreting metrics.
"""
        ),
        code(
            """
sample_source = distorted['source_path'].iloc[0]
recipes = [
    'jpeg_classic',
    'resize_roundtrip',
    'screenshot_chain',
    'messenger_chain',
    'video_call_frame',
    'low_light_upload',
    'dirty_lens_recompress',
    'restoration_artifact',
]
items = [('clean', DATA_ROOT / sample_source)]
for recipe in recipes:
    row = distorted[
        (distorted['source_path'] == sample_source)
        & (distorted['recipe'] == recipe)
        & (distorted['severity'] == 'high')
    ].iloc[0]
    items.append((recipe, DATA_ROOT / row['output_path']))

fig, axes = plt.subplots(3, 3, figsize=(9, 9))
for ax, (title, path) in zip(axes.ravel(), items):
    ax.imshow(Image.open(path).convert('RGB'))
    ax.set_title(title, fontsize=9)
    ax.axis('off')
plt.tight_layout()
"""
        ),
        md(
            """
## First CLIP Baseline

The first baseline uses `openai/clip-vit-base-patch32` in zero-shot mode with
simple class prompts. The cross-model section below adds CLIP ViT-B/16,
OpenCLIP ViT-B/32 LAION2B, SigLIP, and two prototype image backbones on the
fair test split.
"""
        ),
        code(
            """
clean_acc = summary.query(\"family == 'clean'\")['accuracy'].iloc[0]
family_avg = summary.groupby('family', as_index=False)['accuracy'].mean().sort_values('accuracy', ascending=False)

print(f'Clean accuracy: {clean_acc:.4f}')
family_avg
"""
        ),
        md(
            """
## High-Severity Result

The headline finding is not that every modern transfer recipe is harder. The
useful signal is that specific transfer chains create a distinct failure
profile.
"""
        ),
        code(
            """
high = summary[summary['severity'].isin(['clean', 'high'])].copy()
high = high.sort_values('accuracy')

colors = high['family'].map({
    'classic': '#2f6fb2',
    'modern_transfer': '#c25c42',
    'clean': '#469650',
}).fillna('#999999')

fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(high['recipe'] + ' (' + high['family'] + ')', high['accuracy'], color=colors)
ax.set_xlabel('Zero-shot accuracy')
ax.set_title('CLIP ViT-B/32 accuracy: clean vs high-severity distortions')
ax.set_xlim(0, 1)
for i, value in enumerate(high['accuracy']):
    ax.text(value + 0.01, i, f'{value:.3f}', va='center')
plt.tight_layout()

high[['family', 'recipe', 'severity', 'n', 'accuracy', 'relative_accuracy_drop']]
"""
        ),
        md(
            """
## Cross-Model Comparison

The fair comparison uses the mini-CURE-OR test split only: 100 clean images and
2,700 distorted variants. CLIP ViT-B/32, CLIP ViT-B/16, OpenCLIP ViT-B/32
LAION2B, and SigLIP are evaluated zero-shot; HGNetV2-B0 and MobileNetV3-Small
use clean-train prototype classifiers.
"""
        ),
        code(
            """
if model_comparison is None or model_ranking is None:
    print('Cross-model result tables are not included in this dataset package.')
else:
    clean_rows = (
        model_comparison[model_comparison['family'].eq('clean')]
        [['model_name', 'accuracy']]
        .rename(columns={'accuracy': 'clean_accuracy'})
    )
    worst_rows = (
        model_ranking[model_ranking['rank_most_damaging'].eq(1)]
        [['model_name', 'recipe', 'accuracy', 'relative_accuracy_drop']]
        .rename(columns={
            'recipe': 'worst_high_recipe',
            'accuracy': 'worst_high_accuracy',
            'relative_accuracy_drop': 'worst_high_drop',
        })
    )
    headline = clean_rows.merge(worst_rows, on='model_name').sort_values('clean_accuracy', ascending=False)
    headline
"""
        ),
        code(
            """
if model_comparison is not None:
    high_models = model_comparison[
        (model_comparison['severity'] == 'high')
        & (model_comparison['family'] != 'clean')
    ].copy()
    recipe_order = (
        high_models[['family', 'recipe']]
        .drop_duplicates()
        .sort_values(['family', 'recipe'])['recipe']
        .tolist()
    )
    pivot = high_models.pivot_table(
        index='recipe',
        columns='model_name',
        values='accuracy',
        aggfunc='first',
    ).reindex(recipe_order)

    fig, ax = plt.subplots(figsize=(11, 5.5))
    colors = ['#2f6f73', '#c44e52', '#4c72b0', '#8172b3', '#dd8452', '#55a868']
    for idx, model_name in enumerate(pivot.columns):
        ax.plot(
            range(len(pivot.index)),
            pivot[model_name],
            marker='o',
            linewidth=2.2,
            color=colors[idx % len(colors)],
            label=model_name,
        )
    ax.set_title('High-severity accuracy by model and recipe')
    ax.set_ylabel('Accuracy')
    ax.set_xticks(range(len(pivot.index)))
    ax.set_xticklabels([name.replace('_', ' ') for name in pivot.index], rotation=25, ha='right')
    ax.grid(axis='y', alpha=0.35)
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend(frameon=False)
    plt.tight_layout()
"""
        ),
        md(
            """
## Confidence Shift

Accuracy drop is only part of the robustness story. Confidence shift helps
separate graceful uncertainty from confident failure.
"""
        ),
        code(
            """
if confidence is None:
    print('Confidence shift table is not included in this dataset package.')
else:
    confidence_high = confidence[
        (confidence['severity'] == 'high')
        & (confidence['family'] != 'clean')
    ].copy()
    confidence_high = confidence_high.sort_values('accuracy_drop', ascending=False)
    confidence_high[
        [
            'model_name',
            'recipe',
            'accuracy_drop',
            'confidence_drop',
            'mean_confidence',
            'mean_confidence_incorrect',
            'high_conf_wrong_rate',
        ]
    ].head(10)
"""
        ),
        code(
            """
if confidence is not None:
    confidence_high = confidence[
        (confidence['severity'] == 'high')
        & (confidence['family'] != 'clean')
    ].copy()
    confidence_high['accuracy_drop'] = confidence_high['accuracy_drop'].astype(float)
    confidence_high['confidence_drop'] = confidence_high['confidence_drop'].astype(float)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for model_name, group in confidence_high.groupby('model_name'):
        ax.scatter(
            group['accuracy_drop'],
            group['confidence_drop'],
            s=54,
            alpha=0.82,
            label=model_name,
        )
    ax.axhline(0, color='#777777', linewidth=1, alpha=0.5)
    ax.axvline(0, color='#777777', linewidth=1, alpha=0.5)
    ax.set_xlabel('Accuracy drop vs clean')
    ax.set_ylabel('Mean confidence drop vs clean')
    ax.set_title('High-severity confidence shifts')
    ax.grid(alpha=0.25)
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend(frameon=False, fontsize=8)
    plt.tight_layout()
"""
        ),
        md(
            """
## Per-Class Failures

The object-level view is important because aggregate accuracy can hide a small
number of severe class collapses.
"""
        ),
        code(
            """
if per_class is None:
    print('Per-class result table is not included in this dataset package.')
else:
    class_drops = per_class[
        (per_class['severity'] == 'high')
        & (per_class['family'] != 'clean')
        & per_class['drop_vs_clean_label'].notna()
    ].copy()
    class_drops['drop_vs_clean_label'] = class_drops['drop_vs_clean_label'].astype(float)
    class_drops = class_drops.sort_values('drop_vs_clean_label', ascending=False)
    class_drops[['model_name', 'recipe', 'label', 'n', 'accuracy', 'drop_vs_clean_label']].head(10)
"""
        ),
        md(
            """
## Severity Curves

A degradation curve is more informative than a single high-severity score
because it shows whether the model degrades smoothly or collapses under
specific recipes.
"""
        ),
        code(
            """
severity_order = {'low': 1, 'mid': 2, 'high': 3}
curves = summary[summary['severity'].isin(severity_order)].copy()
curves['severity_idx'] = curves['severity'].map(severity_order)

fig, ax = plt.subplots(figsize=(10, 6))
for recipe, group in curves.sort_values('severity_idx').groupby('recipe'):
    ax.plot(group['severity_idx'], group['accuracy'], marker='o', label=recipe)
ax.axhline(clean_acc, color='black', linestyle='--', linewidth=1, label='clean')
ax.set_xticks([1, 2, 3], ['low', 'mid', 'high'])
ax.set_ylabel('Zero-shot accuracy')
ax.set_title('Accuracy by severity level')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
"""
        ),
        md(
            """
## First Interpretation

The full v0.1 run keeps the same signal as the smaller train-only pass:

- clean accuracy is 0.8280;
- classic and modern-transfer family averages are close;
- `low_light_upload` is the largest high-severity failure mode, with a 0.1720
  drop vs clean;
- `video_call_frame` is the second strongest modern-transfer degradation;
- `messenger_chain` is not harmful in this setup, which is useful negative
  evidence.

The corrected cross-model comparison makes the story stronger:
`low_light_upload` is the worst high-severity recipe for both CLIP variants,
OpenCLIP, and HGNetV2-B0, while MobileNetV3-Small ranks `video_call_frame` as
its worst case. That means the benchmark is already producing ranking shifts
across model families. OpenCLIP gives us a usable non-OpenAI contrastive
baseline. SigLIP is retained as a diagnostic run, but its clean accuracy is low
under this prompt protocol, so its robustness ranking should be read cautiously.
"""
        ),
        code(
            """
worst = high[high['family'] == 'modern_transfer'].sort_values('accuracy').head(3)
worst[['recipe', 'accuracy', 'relative_accuracy_drop', 'mean_confidence']]
"""
        ),
        md(
            """
## Related Work Positioning

Recent robustness benchmarks already cover broad VLM and MLLM degradation:
R-Bench models a capture-to-reception corruption sequence for large multimodal
models; MLLM-IC evaluates MLLMs across many corruption types and low-level
capabilities; VLM-RobustBench spans many augmentation settings on MMBench and
MMMU-Pro; CLEAR/MMD-Bench studies degraded-image understanding across standard
multimodal benchmarks.

CURE-OR++ should therefore make a narrower claim. It complements those suites
with a compact object-recognition setup, paired clean/distorted metadata,
transparent transfer-chain recipes, and recipe/class-level ranking shifts that
are easy to reproduce and inspect.

Sources:

- R-Bench: https://arxiv.org/abs/2410.05474
- MLLM-IC: https://openaccess.thecvf.com/content/ICCV2025/html/Qiu_Benchmarking_Multimodal_Large_Language_Models_Against_Image_Corruptions_ICCV_2025_paper.html
- VLM-RobustBench: https://arxiv.org/abs/2603.06148
- CLEAR / MMD-Bench: https://arxiv.org/abs/2604.04780
"""
        ),
        md(
            """
## Limitations

This is a first Kaggle-ready benchmark artifact, not a final paper claim.

- SigLIP has low clean accuracy under the current prompt protocol.
- The source dataset has only 10 object classes.
- Transfer chains are simulated, not captured from actual app uploads yet.
- The next version should add at least one real app-transfer validation sample
  and expand beyond this compact 10-class subset.
"""
        ),
    ]


if __name__ == "__main__":
    raise SystemExit(main())
