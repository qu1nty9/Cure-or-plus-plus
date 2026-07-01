# CURE-OR++

CURE-OR++ is a research benchmark project for measuring how modern vision and
vision-language models degrade under realistic visual transfer distortions.

The core hypothesis is narrow on purpose:

> Modern digital transfer pipelines, such as messenger recompression, social
> media resizing, screenshots, video-call artifacts, and AI restoration artifacts,
> create failure modes that are not fully captured by classic corruption
> benchmarks such as ImageNet-C.

## Why This Exists

Many robustness benchmarks test clean images against isolated corruptions:
noise, blur, JPEG compression, weather, or geometric transforms. Real images
often pass through chains instead:

- phone capture in weak lighting;
- crop or screenshot;
- app resize;
- messenger recompression;
- platform preview generation;
- user-side restoration, denoising, or upscaling.

CURE-OR++ aims to evaluate models against these practical chains and compare
them with classic single-step corruptions.

## First Target

The first milestone is a small, reproducible benchmark rather than a large
platform:

- a curated CURE-OR subset or compatible open object-recognition subset;
- 6-10 distortion recipes;
- 5-8 baseline models;
- accuracy, confidence degradation, stability, and ranking-shift metrics;
- degradation curves and robustness heatmaps;
- a public dataset card and a short technical write-up.

## Expected Artifacts

- Reproducible evaluation code.
- Distorted image generation scripts.
- Benchmark configuration files.
- Baseline result tables.
- Kaggle or Hugging Face dataset release.
- arXiv/workshop-ready technical report if the empirical signal is strong.

## Current v0.1 Status

The first Kaggle-ready artifact is built locally:

- 250 mini-CURE-OR clean source images.
- 6,750 generated distorted images.
- 7,000 CLIP ViT-B/32 zero-shot predictions.
- 7,000 OpenCLIP ViT-B/32 LAION2B zero-shot predictions.
- Clean accuracy: 0.8280.
- Largest high-severity drop: `low_light_upload`, 0.1720 below clean accuracy.

Local Kaggle package:

- `kaggle/cure-or-plus-plus-v01`
- `notebooks/cure_or_pp_kaggle_v01.ipynb`

Serious-level work has started:

- CLIP ViT-B/32 zero-shot baseline.
- CLIP ViT-B/16 zero-shot baseline.
- OpenCLIP ViT-B/32 LAION2B zero-shot baseline.
- SigLIP Base P16 224 zero-shot diagnostic baseline.
- HGNetV2-B0 clean-train prototype baseline.
- MobileNetV3-Small clean-train prototype baseline.
- ConvNeXt-Tiny clean-train prototype baseline.
- DINOv2 ViT-S/14 self-supervised prototype baseline.
- Cross-model comparison and per-class failure tables.
- Combined high-severity comparison figure.
- Confidence shift table and high-severity confidence figure.
- Related-work positioning notes.
- Real transfer validation protocol and manifest builder.
- Native mini-CURE-OR challenge pilot toward Full-CURE-OR.
- Expanded native mini-CURE-OR test-grid evaluation.
- Official native CURE-OR challenge type mapping.
- Official Full-CURE-OR 100-object label mapping.
- Full-CURE-OR ingestion checklist and dataset probe script.
- Full-CURE-OR zero-shot probe configs for OpenCLIP and CLIP ViT-B/16.
- First extracted-folder Full-CURE-OR probe with CLIP ViT-B/16 and OpenCLIP.
- All-challenge Full-CURE-OR probe v0.4 across challenge types 02-09 and
  11-18.
- Expanded Full-CURE-OR v0.4 model pass with CLIP ViT-B/32 and a SigLIP
  diagnostic run.
- Full-CURE-OR v0.4 type-10 grayscale no-challenge control.
- Full-CURE-OR v0.4 leave-clean-condition-out prototype baselines with
  HGNetV2-B0, MobileNetV3-Small, ConvNeXt-Tiny, and DINOv2 ViT-S/14.
- Full-CURE-OR v0.4 OpenCLIP ViT-B/16 DataComp XL stronger-baseline run.
- Full-CURE-OR v0.4 challenge-family/channel-effect analysis across eight
  usable baselines.
- Full-CURE-OR v0.4 consensus failure analysis across eight usable baselines.
- Full-CURE-OR v0.4 paper-table pack with Markdown, CSV, and LaTeX outputs.
- Full-CURE-OR v0.4 technical report draft with claims, limitations, and a
  real-transfer placeholder.
- Dataset card, evaluation card, and arXiv readiness matrix for the current
  v0.4 benchmark state.
- LaTeX paper scaffold under `paper/` with generated table input.
- Real-transfer validation v0.2 protocol: 30 sources, 3 real pipelines, 2
  repeats, 180 planned outputs, and four zero-shot evaluation configs.
- Real-transfer VLM/API prompt pack v0.1: 30 clean source rows and 180
  transferred rows per model, designed for separate multiple-choice VLM
  evaluation rather than direct mixing into the classifier leaderboard.

Corrected test-split headline:

| Model | Clean accuracy | Worst high-severity recipe | Worst accuracy |
| --- | ---: | --- | ---: |
| CLIP ViT-B/16 | 0.9000 | low_light_upload | 0.7800 |
| OpenCLIP ViT-B/32 LAION2B | 0.8500 | low_light_upload | 0.6300 |
| HGNetV2-B0 Prototype | 0.8400 | low_light_upload | 0.6400 |
| CLIP ViT-B/32 | 0.7900 | low_light_upload | 0.6400 |
| MobileNetV3-Small Prototype | 0.5600 | video_call_frame | 0.4600 |
| SigLIP Base P16 224 | 0.1900 | video_call_frame | 0.1500 |

OpenCLIP now provides a usable non-OpenAI contrastive baseline. SigLIP is still
included as a diagnostic run, but its clean accuracy is too low under the
current prompt protocol for strong robustness claims.

Expanded native mini-CURE-OR test grid:

- 100 clean test images.
- 6,400 native challenge images.
- 16 available native challenge types: 2-9 and 11-18.
- 4 challenge levels per type.

| Model | Worst native level-4 challenge | Worst accuracy | Drop vs clean |
| --- | --- | ---: | ---: |
| CLIP ViT-B/16 | type 14, grayscale gaussian blur | 0.1000 | 0.8000 |
| OpenCLIP ViT-B/32 LAION2B | type 14, grayscale gaussian blur | 0.1000 | 0.7500 |

Mean level-4 native accuracy is 0.5163 for CLIP ViT-B/16 and 0.4325 for
OpenCLIP ViT-B/32 LAION2B. OpenCLIP also reaches 0.1000 accuracy on type 18,
grayscale salt and pepper noise, with 0.9730 mean confidence. This native grid
is not packaged into the first Kaggle dataset yet. It is the bridge toward a
broader Full-CURE-OR evaluation.

Full-CURE-OR staged probe:

- all 18 official extracted folders staged on the external disk.
- v0.1: 100 clean probe images and 2,000 native challenge images.
- v0.2: 500 clean probe images and 10,000 native challenge images, with five
  paired acquisition-condition samples per object/challenge/level.
- v0.3: 500 clean probe images and 12,000 native challenge images, adding
  official level-5 rows for challenge types 05, 09, 14, and 18.
- v0.4: 500 clean probe images and 38,999 native challenge images across
  challenge types 02-09 and 11-18.

| Model | Clean accuracy | Mean native accuracy | Mean level-4 native accuracy | Mean level-5 native accuracy | Worst level-5 challenge | Worst level-5 accuracy |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| DINOv2 ViT-S/14 Prototype | 0.7520 | 0.4393 | 0.3819 | 0.2766 | type 18, grayscale salt and pepper noise | 0.0080 |
| ConvNeXt-Tiny Prototype | 0.6160 | 0.3436 | 0.2965 | 0.2239 | type 18, grayscale salt and pepper noise | 0.0080 |
| OpenCLIP ViT-B/16 DataComp XL | 0.5460 | 0.2561 | 0.2153 | 0.1451 | type 09, salt and pepper noise | 0.0080 |
| HGNetV2-B0 Prototype | 0.6240 | 0.2547 | 0.2045 | 0.1219 | type 05, gaussian blur; tied with types 09, 14, and 18 | 0.0100 |
| MobileNetV3-Small Prototype | 0.5560 | 0.1936 | 0.1631 | 0.0960 | type 05, gaussian blur; tied with types 09, 14, and 18 | 0.0100 |
| CLIP ViT-B/16 | 0.4440 | 0.1929 | 0.1596 | 0.0994 | type 09, salt and pepper noise; tied with type 18 | 0.0100 |
| OpenCLIP ViT-B/32 LAION2B | 0.4120 | 0.1705 | 0.1400 | 0.0890 | type 18, grayscale salt and pepper noise | 0.0080 |
| CLIP ViT-B/32 | 0.3500 | 0.1532 | 0.1249 | 0.0741 | type 09, salt and pepper noise | 0.0060 |
| SigLIP Base P16 224 | 0.0120 | 0.0103 | 0.0096 | 0.0084 | type 03, underexposure | 0.0060 |

The latest full-probe status is in `reports/full_cure_or_probe_v04_status.md`,
with expanded-model details in
`reports/full_cure_or_probe_v04_expanded_models.md`, prototype-baseline details
in `reports/full_cure_or_prototype_v04.md`, and confidence/calibration details
in `reports/full_cure_or_confidence_v04.md`. The type-10 grayscale control is
in `reports/full_cure_or_grayscale_control_v04.md`. This is now our
strongest evidence that the native CURE-OR failure pattern survives outside
mini-CURE-OR and across the full challenge-type grid. The confidence pass adds a
second paper-level finding: the stronger DataComp XL row reaches 0.1451 mean
level-5 accuracy but still retains 0.4997 mean confidence, while OpenCLIP
ViT-B/32 LAION2B reaches 0.0890 accuracy with 0.4781 confidence. The grayscale
control adds a third
guardrail: grayscale alone hurts, but it does not explain level-5 collapse.
DataComp XL reaches 0.3908 on grayscale no-challenge control while falling to
0.1451 on native level 5.
The prototype pass adds a fourth finding: non-CLIP frozen-feature classifiers
produce different level-5 robustness rankings. HGNetV2-B0 and
MobileNetV3-Small make gaussian blur a top collapse case, while ConvNeXt-Tiny
and DINOv2 substantially improve mean native and level-5 accuracy but still
fail near chance on grayscale salt-and-pepper noise. DINOv2 is the strongest
current v0.4 row. The DataComp XL run adds a stronger OpenCLIP pretrained
variant and lands third by mean native accuracy, but it also collapses near
chance on salt-and-pepper and grayscale salt-and-pepper noise. This is still a
controlled probe rather than a full paper-scale evaluation; the remaining gaps
are broader frontier/provider VLM coverage, final paper polish, and
release-boundary decisions.
The challenge-family analysis in
`reports/full_cure_or_challenge_family_v04.md` adds a fifth finding: every
usable model is worse on paired grayscale level-5 challenges than on the
corresponding color level-5 challenges, while some blur/noise pairs are already
near chance on both sides.
The consensus analysis in `reports/full_cure_or_consensus_v04.md` adds a sixth
finding: the top three level-5 failure types are at floor accuracy for all eight
usable baselines, and pairwise level-5 rank correlations stay high.
The paper-table pack in `reports/full_cure_or_paper_tables_v04.md` collects the
main leaderboard, consensus failure table, and grayscale-control guardrail into
Markdown plus CSV and LaTeX artifacts for the technical writeup.
The current technical report draft is in
`reports/cure_or_pp_technical_report_draft_v04.md`; it is suitable for internal
iteration and now has real-transfer v0.2 results available for integration.
Release-quality documentation is now split into
`docs/dataset_card_cure_or_pp_v04.md`,
`docs/evaluation_card_full_cure_or_v04.md`, and
`reports/arxiv_readiness_matrix_v04.md`.
The LaTeX paper scaffold is in `paper/main.tex`; source references are checked
by `scripts/check_paper_build.py`, and full PDF compilation requires
TeX Live/MacTeX command-line tools.
The real-transfer validation block is collected and evaluated. The activation
status is in `reports/real_transfer_v02_activation_status.json`, and the
source-matched results with bootstrap intervals and figures are in
`reports/real_transfer_v02_results.md`.
The VLM/API extension now has eight executed open-weight rows on the 210-row
prompt pack: `HuggingFaceTB/SmolVLM2-500M-Video-Instruct`,
`HuggingFaceTB/SmolVLM2-2.2B-Instruct`, `OpenGVLab/InternVL3-1B-hf`,
`OpenGVLab/InternVL3-2B-hf`, `llava-hf/llava-onevision-qwen2-0.5b-ov-hf`, and
`Qwen/Qwen2.5-VL-3B-Instruct`, plus `Qwen/Qwen2.5-VL-7B-Instruct` and
`llava-hf/llava-onevision-qwen2-7b-ov-hf`. Their
summaries are in
`reports/vlm_open_weight_smolvlm2_kaggle_v01/summary.md`,
`reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/summary.md`,
`reports/vlm_open_weight_internvl3_1b_kaggle_v01/summary.md`, and
`reports/vlm_open_weight_internvl3_2b_kaggle_v01/summary.md`,
`reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/summary.md`,
plus
`reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/summary.md` and
`reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/summary.md`, plus
`reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/summary.md`. The
open-weight expansion queue is tracked in
`configs/vlm_open_weight_model_matrix_v01.json` and documented in
`docs/vlm_open_weight_model_matrix_v01.md`; the open-weight queue is now clear
for the current matrix, and the next priority rows are selected
frontier/provider VLMs if that comparison is needed. Kaggle
kernel version 9 passed the smoke gate for all four tier-1 candidates; kernel
version 12 completed the InternVL3-1B full run; kernel version 13 completed
the Qwen2.5-VL-3B full run; kernel version 14 completed the SmolVLM2-2.2B
full run; kernel version 16 completed the InternVL3-2B full run; and kernel
version 20 completed the LLaVA-OneVision 0.5B full run after a memory-safe
input-resize retry. Kernel version 23 then completed the Qwen2.5-VL-7B full
run after a version 21 CUDA-OOM smoke failure and a memory-controlled version
22 retry. Kernel version 26 completed the LLaVA-OneVision Qwen2 7B full run
after a version 24 CUDA-OOM smoke failure and a memory-controlled version 25
retry, setting the strongest completed open-weight real-transfer split at
0.9778 with zero unparseables. The smoke artifact is in
`reports/vlm_open_weight_matrix_smoke_kaggle_v01/summary.md`. The prompt pack
summary is in `reports/vlm_api_track_v01_prompt_pack_summary.json`, and the
protocol is in `docs/vlm_api_track_plan_v01.md`. Sanitized model responses can
be collected with `scripts/run_openai_compatible_vlm.py` or
`scripts/run_gemini_vlm.py`; open-weight local VLMs can be collected with
`scripts/run_hf_vlm.py`. All VLM rows can be evaluated with
`scripts/evaluate_vlm_response_pack.py`. A Kaggle GPU path for open-weight VLM
runs is documented in `docs/kaggle_vlm_gpu_plan.md`.
SigLIP is listed as a diagnostic failure under the current zero-shot prompt
protocol, not as a strong robustness baseline.

## License

Code, configs, reports, and generated aggregate result artifacts in this
repository are released under the MIT License. Raw CURE-OR and mini-CURE-OR
data are not included in this repository and are not relicensed here; use those
datasets only under the terms provided by their original sources.
