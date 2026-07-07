# CURE-OR++ v0.4.1: Public Benchmark Writeup

## Short Description

CURE-OR++ v0.4.1 is a public aggregate benchmark package for auditing object
recognition robustness under native CURE-OR challenge conditions, real
app/device transfer pipelines, and assistant-style VLM prompt-pack evaluation.

## TL;DR

CURE-OR++ asks a narrow robustness question: do object-recognition systems share
stable failure patterns when clean object images move into severe native
challenge conditions and real digital transfer pipelines?

The current public package gives a reproducible aggregate view of that question:

- eight usable Full-CURE-OR baselines over 500 clean probe rows and 38,999 native
  challenge rows;
- a source-matched real-transfer v0.2 guardrail over WhatsApp upload/download,
  phone screenshot/resave, and FaceTime frame-capture pipelines;
- seven completed 900-row open-weight VLM prompt-pack runs;
- hosted-provider VLM comparisons across OpenAI, xAI, Anthropic, and GigaChat.

This Kaggle package contains aggregate reports, generated figures, release
metadata, and reproducibility notes. It intentionally excludes raw CURE-OR
images, mini-CURE-OR images, local real-transfer photos, hosted-provider raw
JSONL responses, provider caches, source archives, and credentials.

## What Is Inside

The package is organized as a public evidence bundle:

- `reports/full_cure_or_paper_*`: Full-CURE-OR v0.4 paper tables.
- `reports/real_transfer_v02_*`: source-matched real-transfer validation.
- `reports/vlm_open_weight_full_v03_*`: 900-row open-weight VLM comparison.
- `reports/vlm_provider_full_v03_*`: 900-row hosted-provider VLM row.
- `reports/vlm_provider_full_v01_*`: 210-row hosted-provider comparison.
- `figures/`: generated paper/readout figures.
- `docs/`: dataset card, evaluation card, public-boundary, and reproducibility notes.
- `repository/`: README, citation metadata, and license from the GitHub release.
- `MANIFEST.json`: file hashes and release-boundary metadata.

## Key Results

### 1. Severe native CURE-OR failures are stable across model families.

The strongest current level-5 row is DINOv2 ViT-S/14 Prototype, with 0.7520
clean accuracy, 0.4393 native mean accuracy, and 0.2766 native level-5 mean
accuracy. Stronger features improve aggregate robustness, but they do not remove
the severe native challenge collapse.

All eight usable baselines hit the floor on the same three level-5 challenge
families:

- grayscale salt-and-pepper noise;
- salt-and-pepper noise;
- grayscale gaussian blur.

This is the core Full-CURE-OR signal: the hardest failures are not arbitrary
per-model accidents.

### 2. Grayscale alone does not explain the collapse.

The type-10 grayscale no-challenge control is damaging, but it remains much
easier than severe native challenge conditions. The benchmark therefore
separates ordinary channel loss from challenge recipes that combine blur, noise,
compression, or other stressors with grayscale variants.

### 3. Real-transfer v0.2 is a guardrail, not a leaderboard.

The real-transfer block uses 30 clean sources, three app/device pipelines, and
two repeats per source/pipeline. Effects are moderate rather than catastrophic.
Video-call frame capture is the largest mean source-matched drop in the current
block, with 79.6% mean real accuracy and a 2.1 percentage-point mean drop.

The important point is external validity: real app/device transfer changes the
input distribution, but the current small block should be interpreted as a
guardrail rather than a precise estimate of every app-specific effect.

### 4. VLM rows measure both recognition and generation stability.

The open-weight VLM v0.3 track uses a 900-row prompt pack with 100 clean rows
and 800 real-transfer rows per model. LLaVA-OneVision Qwen2 7B is the strongest
completed open-weight row, reaching 0.9775 real-transfer accuracy with zero
unparseable responses. Qwen2.5-VL-7B is also strong at 0.9613.

Qwen2.5-VL-3B exposes a separate failure mode: many transferred-image responses
are unparseable. That makes the VLM block more than a standard accuracy table;
it also audits whether a model can produce stable, parseable answers under the
same visual QA protocol.

### 5. Hosted-provider rows are useful, but should be separated.

Hosted-provider VLM rows use the same prompt, parser, and audit protocol, but
they are reported separately because providers control model versioning, pricing,
caching, and data-handling behavior. The package includes nine 210-row
provider comparisons plus a 900-row xAI Grok 4.3 v0.3 row and repeat tracked in
the GitHub repository.

## Why This Package Is Public-Aggregate Only

This Kaggle package is intentionally not a raw-image redistribution. It is an
auditable aggregate companion to the GitHub release and DOI.

Public:

- project-authored aggregate tables;
- generated figures;
- release and reproducibility documentation;
- dataset/evaluation cards;
- citation metadata.

Not public:

- raw CURE-OR or mini-CURE-OR images;
- local real-transfer photos or collection packs;
- source dataset archives;
- hosted-provider raw JSONL response dumps;
- provider API caches;
- API keys, OAuth material, `.env` files, or credentials.

Users who need image-level reproduction should obtain upstream CURE-OR under
its own terms and rerun the documented pipeline from the GitHub release.

## Reproducibility Route

Version DOI:

https://doi.org/10.5281/zenodo.21239828

GitHub release:

https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1

The GitHub release contains the source package, paper PDF, release checks,
scripts, configs, public data-boundary documentation, and citation metadata.
The Kaggle notebook reads this aggregate package and regenerates the main
reader-facing tables and plots.

## Citation

```bibtex
@misc{kholmirzayev2026cureorpp,
  title = {CURE-OR++: Object Recognition Robustness Under Native CURE-OR Challenges and Digital Transfer Pipelines},
  author = {Kholmirzayev, Yaroslav},
  year = {2026},
  note = {Archival metadata release v0.4.1; scientific preprint baseline v0.4-preprint},
  doi = {10.5281/zenodo.21239828},
  url = {https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1}
}
```
