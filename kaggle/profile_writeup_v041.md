# Kaggle Profile Writeup Draft: CURE-OR++ v0.4.1

This file is drafted for Kaggle's profile-level **New writeup** editor. It is
separate from the Kaggle dataset description and separate from the executable
Kaggle notebook.

Published URL:

https://www.kaggle.com/writeups/yaroslavkholmirzayev/cure-or-object-recognition-robustness-under-nat

## Title

CURE-OR++: Object Recognition Robustness Under Native and Real Transfer Stress

## Subtitle

A public aggregate benchmark for testing whether object-recognition models
share stable failures under severe CURE-OR challenges, phone/app transfer
pipelines, and VLM prompt-pack evaluation.

## Media Gallery

Upload:

- `results/kaggle_writeup_media_v041_01_mean_accuracy.png`
- `results/kaggle_writeup_media_v041_02_level5_ranking.png`
- `results/kaggle_writeup_media_v041_03_real_transfer_drops.png`
- `results/kaggle_writeup_media_v041_04_real_transfer_heatmap.png`
- `results/kaggle_writeup_media_v041_05_grayscale_control.png`
- `results/kaggle_writeup_media_v041_06_level5_overconfidence.png`

Required UI size:

- `640 x 360`

Compatibility alias:

- `results/kaggle_writeup_media_v041.png` is the same image as
  `results/kaggle_writeup_media_v041_01_mean_accuracy.png`.

## Card and Thumbnail Image

Upload:

- `results/kaggle_writeup_card_thumbnail_v041.png`

Required UI size:

- `560 x 280`

## Content

Modern object-recognition systems are strong on clean images, but clean-image
accuracy is only part of the story. CURE-OR++ asks a narrower robustness
question:

> When clean object images move into severe challenge conditions and real
> app/device transfer pipelines, do different recognition systems share stable
> failure patterns?

This writeup summarizes the public CURE-OR++ v0.4.1 aggregate release. The
release combines three views of the same problem:

- Full-CURE-OR native challenge evaluation.
- Real-transfer validation through phone/app workflows.
- Assistant-style VLM prompt-pack evaluation for open-weight and hosted models.

The public Kaggle package is intentionally aggregate-only. It includes tables,
figures, documentation, reproducibility notes, and citation metadata. It does
not redistribute raw CURE-OR images, local real-transfer photos, provider raw
JSONL responses, API caches, source archives, or credentials.

Dataset:
https://www.kaggle.com/datasets/yaroslavkholmirzayev/cure-or-plus-plus-v041-public-flat

Notebook:
https://www.kaggle.com/code/yaroslavkholmirzayev/cure-or-v0-4-1-public-benchmark-writeup

GitHub release:
https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1

Version DOI:
https://doi.org/10.5281/zenodo.21239828

## What Was Evaluated

The current evidence package contains:

- 500 clean Full-CURE-OR probe rows.
- 38,999 native CURE-OR challenge rows.
- Eight usable CLIP, OpenCLIP, and prototype baseline rows.
- A real-transfer v0.2 block with 30 source images, three pipelines, two repeats
  per source/pipeline, and 180 transferred outputs.
- Seven completed 900-row open-weight VLM prompt-pack runs.
- Hosted-provider VLM comparisons across OpenAI, xAI, Anthropic, and GigaChat.

The core design is source-matched where possible: real-transfer rows are
compared against the same clean source images, rather than against a broad clean
set with different composition.

## Result 1: Severe Native CURE-OR Failures Are Stable

The strongest current level-5 baseline is DINOv2 ViT-S/14 Prototype:

- clean accuracy: 0.7520
- native mean accuracy: 0.4393
- native level-5 mean accuracy: 0.2766

That is better than the CLIP/OpenCLIP baselines, but it does not remove the
severe-challenge collapse. Across all eight usable baselines, the same three
level-5 challenge families are the consensus floor:

- grayscale salt-and-pepper noise
- salt-and-pepper noise
- grayscale gaussian blur

This is the main Full-CURE-OR signal. The hardest failures are not random
per-model accidents; they are shared stress points across model families.

![Full-CURE-OR mean accuracy by level](https://raw.githubusercontent.com/qu1nty9/Cure-or-plus-plus/main/results/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png)

## Result 2: Grayscale Alone Does Not Explain the Collapse

A useful control is type-10 grayscale without an additional native challenge.
That control is damaging, but it remains much easier than severe native
challenge recipes. The benchmark therefore separates ordinary channel loss from
combined stressors such as blur, noise, compression, and grayscale variants.

This matters because a simple "models dislike grayscale" interpretation would
be too weak. The evidence points to severe challenge recipes that combine
multiple forms of visual degradation.

## Result 3: Real-Transfer Effects Are Moderate but Measurable

The real-transfer v0.2 block uses phone/app workflows rather than synthetic
distortions:

- WhatsApp upload/download
- iPhone screenshot/resave
- FaceTime video-call or screen-share frame capture

The block uses 30 clean source images, three pipelines, and two repeats per
source/pipeline. Effects are moderate rather than catastrophic. The largest mean
source-matched drop is currently from video-call frame capture:

- mean real-transfer accuracy: 79.6%
- mean source-matched drop: 2.1 percentage points

That makes this block a guardrail, not a leaderboard. It gives external-validity
pressure: real phone/app transfer changes the input distribution, but the
current 30-source block should be read cautiously rather than as a universal
estimate of every app-specific effect.

![Real-transfer source-matched drops](https://raw.githubusercontent.com/qu1nty9/Cure-or-plus-plus/main/results/real_transfer_v02_source_matched_drops.png)

## Result 4: VLM Evaluation Needs Accuracy and Parsing Stability

The open-weight VLM v0.3 track uses a 900-row prompt pack with 100 clean rows
and 800 real-transfer rows per model.

The strongest completed open-weight rows are:

| Model | Clean accuracy | Real-transfer accuracy | Drop |
| --- | ---: | ---: | ---: |
| LLaVA-OneVision-Qwen2-7B | 0.9800 | 0.9775 | 0.0025 |
| Qwen2.5-VL-7B | 0.9800 | 0.9613 | 0.0188 |
| InternVL3-2B | 0.9700 | 0.9600 | 0.0100 |
| SmolVLM2-2.2B | 0.9600 | 0.9575 | 0.0025 |

The most important VLM lesson is not only accuracy. Qwen2.5-VL-3B exposes a
different failure mode: many transferred-image responses become unparseable.
That means the VLM track audits both recognition and answer-format stability.

For an assistant-style object-recognition model, returning a stable parseable
answer is part of the benchmark.

## Result 5: Hosted-Provider Rows Should Be Reported Separately

Hosted-provider VLM rows use the same prompt, parser, and audit protocol, but
they should not be mixed into the open-weight leaderboard. Provider models have
externally managed versioning, pricing, caching, and data-handling behavior.

The current hosted-provider v0.1 block includes 210-row comparisons across
OpenAI, xAI, Anthropic, and GigaChat. A larger v0.3 hosted-provider row is also
tracked for xAI Grok 4.3:

- clean accuracy: 0.9900
- real-transfer accuracy: 0.9788
- hardest pipeline: FaceTime frame capture
- hardest label: toy

These rows are useful, but the interpretation is different from fully
reproducible open-weight runs.

## Why This Release Is Aggregate-Only

The public boundary is deliberate.

Public:

- project-authored aggregate tables
- generated figures
- dataset and evaluation cards
- reproducibility notes
- citation metadata
- sanitized parsed-response audits and summaries

Not public:

- raw CURE-OR or mini-CURE-OR images
- local real-transfer photos
- source dataset archives
- hosted-provider raw JSONL response dumps
- provider API caches
- API keys, OAuth files, `.env` files, or credentials

Users who need image-level reproduction should obtain upstream CURE-OR under
its own terms and rerun the documented pipeline from the GitHub release.

## What To Look At First

If you want the shortest route through the project:

1. Open the Kaggle notebook and run through the generated tables.
2. Check the Full-CURE-OR model leaderboard and consensus level-5 failures.
3. Compare the grayscale control against native level-5 rows.
4. Inspect the real-transfer source-matched drop plot.
5. Read the VLM open-weight and hosted-provider tables separately.

The main claim is narrow by design: CURE-OR++ shows stable, shared robustness
failures under native CURE-OR stress and gives an initial real-transfer/VLM
guardrail around those failures.

## Tags

Use:

- computer-vision
- robustness
- object-recognition
- vision-language-models
- benchmark
- openclip

## Attachments

Project links:

- Dataset: https://www.kaggle.com/datasets/yaroslavkholmirzayev/cure-or-plus-plus-v041-public-flat
- Notebook: https://www.kaggle.com/code/yaroslavkholmirzayev/cure-or-v0-4-1-public-benchmark-writeup
- GitHub release: https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1
- GitHub repository: https://github.com/qu1nty9/Cure-or-plus-plus
- Version DOI: https://doi.org/10.5281/zenodo.21239828

Files to attach only if Kaggle asks for optional supporting files:

- `results/kaggle_writeup_media_v041.png`
- `results/kaggle_writeup_media_v041_01_mean_accuracy.png`
- `results/kaggle_writeup_media_v041_02_level5_ranking.png`
- `results/kaggle_writeup_media_v041_03_real_transfer_drops.png`
- `results/kaggle_writeup_media_v041_04_real_transfer_heatmap.png`
- `results/kaggle_writeup_media_v041_05_grayscale_control.png`
- `results/kaggle_writeup_media_v041_06_level5_overconfidence.png`
- `results/kaggle_writeup_card_thumbnail_v041.png`

Do not attach:

- raw CURE-OR or mini-CURE-OR images
- local real-transfer photos
- hosted-provider raw JSONL files
- provider caches
- API keys, OAuth files, `.env` files, or credentials

## DOI Citation

Enable DOI citation if Kaggle offers it for this writeup.

Recommended citation metadata:

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
