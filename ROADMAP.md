# CURE-OR++ Roadmap

## Current Stage

We now have a local v0.1 benchmark artifact: generated mini-CURE-OR++
distortions, reproducible evaluation scripts, six baseline result sets, a
Kaggle notebook/package draft, and an expanded native mini-CURE-OR test-grid
evaluation. The Full-CURE-OR ingestion path now has a reusable probe and a
checklist. The immediate goal is to turn this into a serious public v0.2 with
real-transfer validation, related-work framing, and a clean limitations section.

Current positioning notes live in `docs/related_work_v01.md`. The first
real-transfer pilot protocol lives in `docs/real_transfer_validation_protocol.md`.
The Full-CURE transition is tracked in `docs/full_cure_or_transition_plan.md`.

## Research Positioning

Working title:

**CURE-OR++: Evaluating Vision and Vision-Language Robustness Under Modern
Digital Transfer Distortions**

Main claim to test:

Classic corruption benchmarks do not fully explain model degradation under
realistic image transfer chains used in messengers, social media, video calls,
and AI restoration workflows.

## Milestone 0: Scope Lock

Deliverable:

- fixed v0 contribution;
- small list of related benchmarks to compare against;
- exact data/model/metric choices.

Success criterion:

- the project can be explained in 2-3 sentences without sounding like a generic
  ImageNet-C clone.

## Milestone 1: Dataset v0

Deliverable:

- clean base image subset;
- generated distorted variants;
- metadata table with image id, label, distortion family, recipe, severity, and
  source image path.

Recommended v0 distortion families:

- classic JPEG compression;
- resize down/up;
- screenshot-like resampling;
- messenger-style recompression;
- low-light plus denoise;
- low-light plus recompression;
- dirty-lens overlay;
- AI-upscale or restoration artifact simulation.

V0 dataset decision:

- use mini-CURE-OR from Zenodo record `4299330`;
- start from the clean subset only: `challengeType = 1`, `challengeLevel = 0`;
- this gives 250 clean source images across 10 classes;
- current v0 config expands it to 6,750 distorted images.

Success criterion:

- 250 clean source images;
- 3 severity levels per recipe;
- deterministic regeneration from scripts and config;
- preserve CURE-OR metadata in the generated manifest.

## Milestone 2: Baseline Evaluation

Deliverable:

- evaluation runner;
- result CSV/Parquet files;
- model cards for evaluated baselines.

Recommended v0 model set:

- ResNet or ConvNeXt;
- EfficientNet;
- ViT;
- DINOv2 or another self-supervised vision encoder;
- CLIP or SigLIP zero-shot;
- one open VLM if local or cloud compute allows.

Success criterion:

- at least 5 model families evaluated on the same distorted subset;
- clean-vs-distorted degradation table exists;
- results are reproducible from a single command.

## Milestone 3: Analysis

Deliverable:

- degradation curves;
- robustness heatmaps;
- model ranking shift under each distortion;
- confidence collapse analysis where logits/probabilities are available.

Success criterion:

- at least one non-obvious finding, such as a model that ranks high on classic
  corruptions but drops sharply under transfer-chain distortions.

## Milestone 4: Public Artifact

Deliverable:

- GitHub repository;
- dataset card;
- Kaggle or Hugging Face dataset;
- Kaggle notebook or reproducible demo notebook.

Success criterion:

- an external reader can run a small version and understand the result without
  private files.

## Milestone 5: Paper Track

Deliverable:

- 4-8 page technical report;
- related work table;
- methodology section;
- experiment tables and figures;
- limitations section.

Possible destinations:

- Kaggle write-up plus dataset: realistic after Milestone 4.
- arXiv preprint: realistic after Milestone 5 if the contribution is empirical,
  reproducible, and not just a survey/position piece.
- Workshop paper: realistic if the findings are strong and framed against
  ImageNet-C, RobustBench, R-Bench, MLLM-IC, VLM-RobustBench, and MMD-Bench.

## Rough Timeline

Fast portfolio version:

- 1 week: dataset generator, simple metrics, 2-3 models;
- 2 weeks: 5-8 models, figures, public write-up;
- 3 weeks: polished repo plus Kaggle/Hugging Face release.

Research version:

- 4-6 weeks: serious benchmark artifact and technical report;
- 6-10 weeks: arXiv-quality draft;
- 8-14 weeks: workshop-submission quality, depending on compute and result
  strength.
