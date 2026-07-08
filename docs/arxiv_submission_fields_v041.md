# CURE-OR++ arXiv Submission Fields v0.4.1

Status date: 2026-07-08.

This file is a copy/paste guide for the first arXiv/workshop-style submission.
It is not a public claim that arXiv has accepted or posted the paper.

## Source Package

Upload this zip as the LaTeX source package:

```text
exports/arxiv_source_v0.4.1.zip
```

If using the verified temporary build from the current machine, the equivalent
test package path is:

```text
/private/tmp/cure-or-pp-arxiv-source-test.zip
```

## Title

CURE-OR++: Object Recognition Robustness Under Native CURE-OR Challenges and Digital Transfer Pipelines

## Authors

Yaroslav Kholmirzayev

## Affiliation

Independent Researcher

## Contact Email

yaric.kholm@gmail.com

## Abstract

Object-recognition systems are usually evaluated on clean images or isolated synthetic corruptions, but practical image use also includes app-mediated transfer, recompression, screenshots, and video-call capture. CURE-OR++ adds a compact, manifest-driven benchmark layer around CURE-OR to measure failures under native challenge conditions and documented real-transfer pipelines. On the Full-CURE-OR v0.4 probe, eight usable baselines show a stable severe-challenge failure core: the strongest level-5 row, DINOv2 ViT-S/14 Prototype, reaches only 0.2766 mean level-5 accuracy, and all usable baselines hit the floor on grayscale salt-and-pepper noise, salt-and-pepper noise, and grayscale gaussian blur. A 180-output real-transfer v0.2 block shows moderate source-matched drops, with video-call frame capture producing the largest mean drop at 2.1 percentage points. The VLM track extends the benchmark to assistant-style object recognition: seven open-weight VLMs run on a 900-row v0.3 prompt pack, where LLaVA-OneVision Qwen2 7B leads with 0.9775 real-transfer accuracy and Qwen2.5-VL-3B exposes a generation-instability failure mode. Hosted-provider runs add nine 210-row provider comparisons across OpenAI, xAI, Anthropic, and GigaChat, plus a 900-row xAI Grok 4.3 run and repeat. These results position CURE-OR++ as a small but auditable robustness artifact for measuring object-centric degradation, transfer sensitivity, and VLM response stability.

## Recommended arXiv Categories

Primary category:

```text
cs.CV
```

Recommended cross-lists:

```text
cs.LG
cs.AI
```

Rationale: the paper is primarily a computer-vision robustness benchmark, with
secondary relevance to machine learning evaluation and multimodal assistants.

## Comments

```text
9 pages, 2 figures. Code, aggregate artifacts, Kaggle public package, and reproducibility notes are available from the linked GitHub/Zenodo release.
```

## DOI / Related Public Artifacts

Version DOI:

```text
10.5281/zenodo.21239828
```

Concept DOI:

```text
10.5281/zenodo.21239827
```

GitHub release:

```text
https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1
```

Kaggle aggregate dataset:

```text
https://www.kaggle.com/datasets/yaroslavkholmirzayev/cure-or-plus-plus-v041-public-flat
```

Kaggle notebook:

```text
https://www.kaggle.com/code/yaroslavkholmirzayev/cure-or-v0-4-1-public-benchmark-writeup
```

Kaggle profile writeup:

```text
https://www.kaggle.com/writeups/yaroslavkholmirzayev/cure-or-object-recognition-robustness-under-nat
```

## License Choice

Recommended paper license for arXiv:

```text
CC BY 4.0
```

Use this if you are comfortable allowing redistribution and reuse with
attribution. The project-authored code and aggregate artifacts remain MIT as
documented in the repository.

## Submission Notes

- Do not upload raw CURE-OR images, mini-CURE-OR images, real-transfer photos,
  provider JSONL files, API caches, source dataset archives, or credentials.
- Upload the source zip, not the whole repository.
- After arXiv assigns an identifier, update `README.md`, `CITATION.cff`,
  `.zenodo.json`, and the Kaggle writeup links in a small follow-up release.
