# CURE-OR++ v0.4.1 Public Kaggle Writeup Copy

## Short Description

CURE-OR++ v0.4.1 is a public aggregate benchmark package for auditing object
recognition robustness under native CURE-OR challenges, real app/device
transfer pipelines, and assistant-style VLM prompt-pack evaluations.

## Kaggle Summary

This package contains public aggregate tables, generated figures, release
metadata, and reproducibility notes for CURE-OR++ v0.4.1. It does not
redistribute raw CURE-OR images, mini-CURE-OR images, local real-transfer
photos, hosted-provider raw JSONL responses, provider caches, source archives,
or credentials.

The benchmark asks a narrow question: do object-recognition models share stable
failure patterns when clean object images move into severe native challenge
conditions and app/device transfer pipelines?

Main evidence blocks:

- Full-CURE-OR v0.4 native challenge probe: 500 clean probe rows and 38,999
  native challenge rows across eight usable baselines.
- Real-transfer v0.2 guardrail: 30 sources, three transfer pipelines, two
  repeats, and 180 transferred outputs.
- Open-weight VLM v0.3 prompt-pack: seven completed 900-row rows.
- Hosted-provider VLM rows: nine 210-row provider comparisons plus a 900-row
  xAI Grok 4.3 row and repeat tracked in the repository.

Key findings:

- All eight usable baselines hit the floor on grayscale salt-and-pepper noise,
  salt-and-pepper noise, and grayscale gaussian blur at level 5.
- Stronger features improve aggregate robustness but do not remove severe
  native challenge collapse.
- Real-transfer v0.2 effects are moderate and model-dependent, with video-call
  frame capture producing the largest mean source-matched drop in the current
  block.
- The VLM track separates object-recognition accuracy from response-generation
  stability.

Version DOI: https://doi.org/10.5281/zenodo.21239828

GitHub release: https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1

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
