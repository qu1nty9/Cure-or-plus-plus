# CURE-OR++ Dataset Card v0.4

## Dataset Summary

CURE-OR++ is a benchmark layer for evaluating object-recognition robustness
under clean images, simulated transfer distortions, native CURE-OR challenge
conditions, and real app/device transfer pipelines.

This repository does not redistribute raw CURE-OR or mini-CURE-OR images. It
contains code, configs, manifests where appropriate, aggregate reports, and
generated evaluation artifacts that can be reproduced locally when the source
datasets are available under their original terms.

## Source Data

- mini-CURE-OR: used for the first Kaggle-ready CURE-OR++ v0.1 package and for
  selecting clean source images for real-transfer validation.
- Full-CURE-OR: used for the v0.4 all-challenge controlled probe across official
  object labels and native challenge types.

Raw source datasets remain governed by their upstream licenses and access
conditions. The repository's MIT license applies to code, configs, reports, and
tracked aggregate result artifacts only.

## Public Release Boundary

The current public package is intended to include code, configs, non-sensitive
manifests, aggregate reports, parsed-response audits, generated figures, paper
source, and documentation. It is not intended to include raw CURE-OR images,
mini-CURE-OR images, local real-transfer photos, local collection packs, raw
hosted-provider JSONL responses, provider API caches, or credentials.

This boundary is deliberately conservative: it keeps the benchmark auditable
through tracked aggregate artifacts while avoiding redistribution of upstream
raw datasets, private transfer payloads, and provider response dumps.

## Current Benchmark Versions

### CURE-OR++ v0.1

Local Kaggle-ready artifact:

- 250 mini-CURE-OR clean source images;
- 6,750 generated distorted images;
- 7,000 evaluated rows for the original CLIP ViT-B/32 benchmark package;
- later local test-split comparisons across CLIP, OpenCLIP, SigLIP diagnostic,
  HGNetV2-B0, and MobileNetV3-Small.

This is suitable for a small public notebook/writeup, but it is no longer the
strongest research track.

### Full-CURE-OR v0.4

Current serious benchmark track:

- 500 clean probe rows;
- 38,999 native challenge probe rows;
- official challenge types 02-09 and 11-18;
- 100 official object labels;
- type-10 grayscale no-challenge control;
- eight usable baseline rows in the main paper tables.

The v0.4 track is a controlled probe rather than an exhaustive pass over every
available Full-CURE-OR image.

### Real-Transfer v0.2

Current real-transfer validation block:

- 30 clean mini-CURE-OR source images;
- 3 real transfer pipelines;
- 2 repeats per source and pipeline;
- 180 collected real transferred output images;
- four zero-shot CLIP/OpenCLIP-family baselines evaluated;
- collector-supplied metadata identifies iPhone 15 Pro as the capture device,
  WhatsApp as the messenger pipeline, and FaceTime as the video-call pipeline.

The raw transferred image payloads, `pairs.csv`, and `manifest.csv` are local
ignored artifacts. Tracked aggregate outputs include the validation reports,
summary CSVs, and `reports/real_transfer_v02_results.md`.

## Data Fields

The project uses manifest-style rows. Depending on the track, common fields are:

- `source_path`: clean or source image path;
- `output_path`: distorted, native challenge, control, or transferred image
  path;
- `label`: object class;
- `family`: clean, simulated, native CURE-OR, control, or real transfer family;
- `recipe`: distortion/challenge/pipeline identifier;
- `severity`: clean, control, high, or native level;
- `params_json`: recipe-specific metadata;
- `source_metadata_json`: clean/source metadata where available.

Real-transfer rows additionally preserve capture metadata when available:

- `capture_device`;
- `capture_date`;
- `repeat_id`;
- `pipeline_variant`;
- `source_selection_id`;
- `notes`.

## Intended Uses

Appropriate uses:

- robustness benchmarking for object-recognition and vision-language models;
- comparing model-family failure rankings under controlled visual degradation;
- inspecting per-challenge and per-severity failure modes;
- studying confidence-preserving errors under severe native challenge rows;
- preparing Kaggle/workshop/arXiv-style reproducible benchmark artifacts.

Out-of-scope uses:

- training or certifying production safety-critical systems;
- claiming broad real-world transfer robustness from this small v0.2 validation
  block alone;
- treating the v0.4 controlled probe as an exhaustive Full-CURE-OR evaluation;
- redistributing upstream raw data outside the original dataset terms.

## Known Limitations

- The v0.4 Full-CURE-OR track is sampled and manifest-driven, not exhaustive.
- Real-transfer v0.2 is a small source-matched validation block: 30 sources,
  three pipelines, and two repeats per source/pipeline.
- The object set follows the source CURE-OR labels and is not a general
  open-world recognition dataset.
- Some model rows use zero-shot prompts, while prototype rows use
  leave-clean-condition-out frozen-feature classifiers; these are useful
  contrasts but not identical evaluation settings.
- SigLIP Base P16 224 is kept as a diagnostic prompt-protocol failure, not as a
  main usable baseline.

## Release Notes

Public release should include this dataset card, the evaluation card, the
technical report draft, aggregate tables, figures, paper source, and clear
licensing notes. Raw CURE-OR and mini-CURE-OR images should remain excluded
from the GitHub repository unless their upstream terms explicitly permit
redistribution. Local real-transfer photos and raw hosted-provider response
JSONL files should remain excluded from the public package.
