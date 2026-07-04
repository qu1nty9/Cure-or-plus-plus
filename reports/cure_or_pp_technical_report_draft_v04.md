# CURE-OR++ Technical Report Draft v0.4

## Status

This is the current paper-draft layer for the serious benchmark track. It is
ready for internal iteration, but it should not be treated as a final public
paper until the real-transfer and VLM sections are integrated into final paper
prose and citation/license checks are complete.

Current strongest evidence:

- Full-CURE-OR v0.4 all-challenge probe over challenge types 02-09 and 11-18;
- 500 clean probe images and 38,999 native challenge probe images;
- eight usable baseline rows after excluding the SigLIP prompt-protocol failure;
- confidence/calibration analysis for the four usable CLIP/OpenCLIP-family
  zero-shot baselines;
- type-10 grayscale no-challenge control;
- paired color-vs-grayscale challenge-family analysis;
- level-5 consensus failure and rank-stability analysis;
- paper-ready Markdown, CSV, and LaTeX tables in
  `reports/full_cure_or_paper_tables_v04.md`;
- real-transfer v0.2 evaluation over 30 source images and 180 transferred
  outputs collected with iPhone 15 Pro, WhatsApp, and FaceTime pipelines;
- open-weight VLM prompt-pack runs using
  `HuggingFaceTB/SmolVLM2-500M-Video-Instruct`,
  `HuggingFaceTB/SmolVLM2-2.2B-Instruct`,
  `OpenGVLab/InternVL3-1B-hf`, `OpenGVLab/InternVL3-2B-hf`,
  `llava-hf/llava-onevision-qwen2-0.5b-ov-hf`, and
  `Qwen/Qwen2.5-VL-3B-Instruct`, plus
  `Qwen/Qwen2.5-VL-7B-Instruct` and
  `llava-hf/llava-onevision-qwen2-7b-ov-hf` on Kaggle GPU.
- a newer 900-row VLM v0.3 extension with completed Qwen2.5-VL-3B,
  Qwen2.5-VL-7B, InternVL3-1B, LLaVA-OneVision Qwen2 0.5B,
  LLaVA-OneVision Qwen2 7B, and SmolVLM2-2.2B rows plus a generated comparison
  report.

Main blocker:

- final paper integration, public-release boundary decisions, and optional
  broader VLM/provider model coverage.
- promotion of the completed six-row 900-row VLM extension into the main paper
  tables after optional InternVL3-2B or provider rows, if desired.

## Working Title

CURE-OR++: Object Recognition Robustness Under Native CURE-OR Challenges and
Digital Transfer Pipelines

## Draft Abstract

Object-recognition systems are often evaluated on clean or synthetically
corrupted images, but practical image use also includes acquisition artifacts,
digital transfer, recompression, screenshots, and channel changes. CURE-OR++
builds a compact, reproducible benchmark layer around CURE-OR for measuring how
vision models fail under object-centric native challenge conditions and planned
real transfer pipelines. On the Full-CURE-OR v0.4 probe, eight usable baselines
cover CLIP/OpenCLIP zero-shot models and frozen-feature prototype classifiers.
The strongest current level-5 baseline, DINOv2 ViT-S/14 Prototype, reaches only
0.2766 mean level-5 accuracy despite 0.7520 clean accuracy. Across all eight
usable baselines, grayscale salt-and-pepper noise, salt-and-pepper noise, and
grayscale gaussian blur collapse to near-chance accuracy, with all models at
the floor threshold. Confidence analysis shows that stronger zero-shot models
can remain substantially overconfident under severe native challenges: OpenCLIP
ViT-B/16 DataComp XL reaches 0.1451 level-5 accuracy while retaining 0.4997
mean confidence. A type-10 grayscale control confirms that grayscale conversion
alone is damaging but does not explain the full native level-5 collapse. The
real-transfer v0.2 block now adds 180 transferred outputs covering messenger
upload/download, phone screenshot/resave, and video-call frame capture
pipelines. Eight open-weight VLM rows validate the prompt-pack path and
provide an initial assistant-style model-family contrast, including both a
strong same-family SmolVLM scale-up, a two-step InternVL family comparison, a
completed LLaVA-OneVision 0.5B retry, memory-controlled Qwen2.5-VL-7B and
LLaVA-OneVision 7B strong rows, and a separate Qwen2.5-VL-3B
generation-instability case.

## Contributions

1. A reproducible Full-CURE-OR v0.4 probe that stages clean and native challenge
   samples into manifest-based evaluation configs.
2. A multi-family baseline comparison covering CLIP/OpenCLIP zero-shot models,
   a stronger DataComp XL OpenCLIP variant, and four non-CLIP prototype
   classifiers.
3. A level-5 consensus failure analysis showing that the hardest severe native
   challenge ordering is stable across model families.
4. A confidence/calibration analysis showing that some severe challenge failures
   preserve high confidence rather than simply reducing confidence with
   accuracy.
5. A grayscale-control and paired channel-effect analysis separating grayscale
   conversion from native challenge severity.
6. A real-transfer v0.2 validation block testing whether real app/device
   transfer pipelines reproduce related failure behavior.
7. A 210-row VLM prompt-pack/evaluator path with executed open-weight
   SmolVLM2-500M, SmolVLM2-2.2B, InternVL3-1B, InternVL3-2B,
   LLaVA-OneVision 0.5B, Qwen2.5-VL-3B, Qwen2.5-VL-7B, and
   LLaVA-OneVision 7B rows, validating assistant-style vision-language
   evaluation without paid API calls.
8. A 900-row VLM v0.3 extension with completed Qwen2.5-VL-3B,
   Qwen2.5-VL-7B, InternVL3-1B, LLaVA-OneVision Qwen2 0.5B,
   LLaVA-OneVision Qwen2 7B, and SmolVLM2-2.2B rows over four real-transfer
   pipelines.

## Method Summary

CURE-OR++ uses manifest-driven evaluation. Each row links a source image,
output image, object label, challenge family, recipe, and severity. This keeps
the benchmark auditable and lets every aggregate result trace back to
well-defined image groups.

The Full-CURE-OR v0.4 track uses:

- clean probe rows sampled across 100 official object labels;
- native challenge rows for official challenge types 02-09 and 11-18;
- severity levels 1-5 where available;
- separate type-10 grayscale no-challenge control rows;
- aggregate summaries for accuracy and mean confidence.

The real-transfer v0.2 track is now collected and evaluated. It pins 30 clean
mini-CURE-OR source images, three real transfer pipelines, two repeats per
source/pipeline, and 180 real transferred output images. Activation is handled
by `scripts/activate_real_transfer_protocol.py`; the source-matched aggregate
report is `reports/real_transfer_v02_results.md`. Collector-supplied metadata
identifies iPhone 15 Pro as the capture device, WhatsApp as the messenger
pipeline, and FaceTime as the video-call/video-transmission pipeline.

The VLM/API track converts the same 30 clean source images and 180 transferred
outputs into multiple-choice prompt rows. The completed open-weight rows are
`HuggingFaceTB/SmolVLM2-500M-Video-Instruct`,
`HuggingFaceTB/SmolVLM2-2.2B-Instruct`, `OpenGVLab/InternVL3-1B-hf`,
`OpenGVLab/InternVL3-2B-hf`, `llava-hf/llava-onevision-qwen2-0.5b-ov-hf`, and
`Qwen/Qwen2.5-VL-3B-Instruct`, plus `Qwen/Qwen2.5-VL-7B-Instruct` and
`llava-hf/llava-onevision-qwen2-7b-ov-hf`, all run on Kaggle GPU with
Transformers and evaluated by
`scripts/evaluate_vlm_response_pack.py`.

The larger VLM v0.3 prompt pack expands this path to 900 rows per model: 100
clean source rows and 800 real-transfer rows over WhatsApp transfer, phone
screenshot/resave, Instagram resave, and FaceTime frame capture. Completed
v0.3 rows are compared in `reports/vlm_open_weight_full_v03_comparison.md`.

## Current Baselines

The current main table excludes SigLIP Base P16 224 from the main interpretation
because the current zero-shot prompt protocol produced a diagnostic clean
failure. The eight usable rows are:

- DINOv2 ViT-S/14 Prototype;
- ConvNeXt-Tiny Prototype;
- OpenCLIP ViT-B/16 DataComp XL;
- HGNetV2-B0 Prototype;
- CLIP ViT-B/16;
- MobileNetV3-Small Prototype;
- OpenCLIP ViT-B/32 LAION2B;
- CLIP ViT-B/32.

The paper-ready leaderboard is generated in
`reports/full_cure_or_paper_model_table_v04.csv` and rendered in
`reports/full_cure_or_paper_tables_v04.md`.

## Main Results

### Full-CURE-OR Level-5 Robustness

The strongest current level-5 row is DINOv2 ViT-S/14 Prototype:

- clean accuracy: 0.7520;
- native mean accuracy: 0.4393;
- native level-5 mean accuracy: 0.2766;
- level-5 drop versus clean: 0.4754;
- worst level-5 challenge: grayscale salt-and-pepper noise at 0.0080 accuracy.

The strongest zero-shot contrastive row is OpenCLIP ViT-B/16 DataComp XL:

- clean accuracy: 0.5460;
- native mean accuracy: 0.2561;
- native level-5 mean accuracy: 0.1451;
- worst level-5 challenge: salt-and-pepper noise at 0.0080 accuracy.

Interpretation: stronger pretraining and non-CLIP prototype features improve
the leaderboard, but they do not remove the severe native challenge collapse.

### Consensus Failure Ordering

The top consensus level-5 failures are:

1. grayscale salt-and-pepper noise: mean accuracy 0.0092, floor 8/8;
2. salt-and-pepper noise: mean accuracy 0.0103, floor 8/8;
3. grayscale gaussian blur: mean accuracy 0.0115, floor 8/8;
4. gaussian blur: mean accuracy 0.0150, floor 7/8.

Pairwise level-5 rank correlations range from 0.892 to 0.988. This means the
benchmark is not only producing isolated per-model worst cases. It has a stable
hardness core, with secondary model-family differences.

### Confidence and Calibration

The confidence pass covers the four usable CLIP/OpenCLIP-family zero-shot
baselines. The strongest zero-shot row, OpenCLIP ViT-B/16 DataComp XL, reaches:

- level-5 accuracy: 0.1451;
- level-5 mean confidence: 0.4997;
- level-5 calibration gap: 0.3545;
- level-5 high-confidence wrong rate: 0.3240.

Its worst level-5 overconfidence case is type 18, grayscale salt-and-pepper
noise:

- accuracy: 0.0100;
- mean confidence: 0.7393;
- calibration gap: 0.7293;
- high-confidence wrong rate: 0.9760.

Interpretation: some severe native challenges do not merely reduce accuracy.
They produce low-accuracy, high-confidence failures.

### Real-Transfer and Open-Weight VLM Guardrail

The source-matched real-transfer report covers 30 source images, three
pipelines, and two repeats per source/pipeline. Across the four CLIP/OpenCLIP
zero-shot rows, real-transfer drops are moderate rather than catastrophic. This
supports using the real-transfer block as an external-validity guardrail rather
than as the main native-challenge collapse claim.

The open-weight VLM rows produced:

| Model | Clean source | Real-transfer | Drop | Unparseable |
| --- | ---: | ---: | ---: | ---: |
| SmolVLM2-500M-Video-Instruct | 0.6000 | 0.5556 | 0.0444 | 0.0000 |
| SmolVLM2-2.2B-Instruct | 0.9333 | 0.9333 | 0.0000 | 0.0000 |
| InternVL3-1B-hf | 0.9333 | 0.9333 | 0.0000 | 0.0000 |
| InternVL3-2B-hf | 0.9333 | 0.9278 | 0.0056 | 0.0000 |
| llava-onevision-qwen2-0.5b-ov-hf | 0.9667 | 0.9333 | 0.0333 | 0.0000 |
| Qwen2.5-VL-3B-Instruct | 0.9000 | 0.6389 | 0.2611 | 0.3278 |
| Qwen2.5-VL-7B-Instruct | 0.9667 | 0.9333 | 0.0333 | 0.0000 |
| llava-onevision-qwen2-7b-ov-hf | 0.9667 | 0.9778 | -0.0111 | 0.0000 |

By pipeline, SmolVLM2-500M real-transfer accuracies were:

- messenger upload/download: 0.6333;
- phone screenshot/resave: 0.5000;
- video-call frame capture: 0.5333.

SmolVLM2-2.2B reached 0.9333 for messenger upload/download, 0.9167 for phone
screenshot/resave, and 0.9500 for video-call frame capture. InternVL3-1B
reached 0.9333 accuracy for all three real-transfer pipelines. InternVL3-2B
reached 0.9667 for messenger upload/download, 0.9000 for phone
screenshot/resave, and 0.9167 for video-call frame capture. LLaVA-OneVision
0.5B reached 0.9667 for messenger upload/download, 0.9333 for phone
screenshot/resave, and 0.9000 for video-call frame capture.
Qwen2.5-VL-3B reached 0.9000 clean accuracy, but on real-transfer rows it
often generated the literal string `!!!!!!!!`, producing a 0.3278 unparseable
rate and a 0.2611 accuracy drop.
Qwen2.5-VL-7B reached 0.9667 clean accuracy and 0.9333 real-transfer accuracy
with zero unparseables after a memory-controlled Kaggle path that reduced the
visual-token budget and resized inputs to `max_side=512`.
LLaVA-OneVision Qwen2 7B reached 0.9667 clean accuracy and 0.9778
real-transfer accuracy with zero unparseables after a memory-controlled Kaggle
path that disabled generation cache, used `device_map=auto`, resized inputs to
`max_side=384`, and limited generation to two new tokens. Its real-transfer
recipe accuracies were 1.0000 for messenger upload/download, 1.0000 for phone
screenshot/resave, and 0.9333 for video-call frame capture.

The 900-row VLM v0.3 extension strengthens this block with a larger clean and
real-transfer sample, plus the Instagram `social_app_resave` pipeline:

| Model | Clean | Real-transfer | Drop | Real unparseable |
| --- | ---: | ---: | ---: | ---: |
| LLaVA-OneVision-Qwen2-7B | 0.9800 | 0.9775 | 0.0025 | 0.0000 |
| Qwen2.5-VL-7B | 0.9800 | 0.9613 | 0.0188 | 0.0000 |
| SmolVLM2-2.2B | 0.9600 | 0.9575 | 0.0025 | 0.0000 |
| InternVL3-1B | 0.9500 | 0.9563 | -0.0063 | 0.0000 |
| LLaVA-OneVision-Qwen2-0.5B | 0.9300 | 0.9213 | 0.0088 | 0.0000 |
| Qwen2.5-VL-3B | 0.8800 | 0.7650 | 0.1150 | 0.2088 |

InternVL3-1B adds a strong small-family contrast in the larger setting: it
reaches 0.9500 clean accuracy, 0.9563 real-transfer accuracy, and zero
unparseables, with only a small FaceTime frame weakness at 0.9450 accuracy.
LLaVA-OneVision Qwen2 0.5B adds the small-model LLaVA scale contrast in this
larger setting: it remains fully parseable and reaches 0.9213 real-transfer
accuracy, but its hardest label is `dymo_label_maker` at 0.3500 accuracy and
its hardest pipeline is video-call frame capture at 0.8950 accuracy.

Interpretation: SmolVLM2-500M is weaker than the best CLIP/OpenCLIP
real-transfer rows, but it proves the VLM prompt-pack and response-audit path
is executable on open-weight models without paid APIs. SmolVLM2-2.2B then
shows a strong within-family scaling effect: unlike the 500M row, it preserves
0.9333 accuracy on both clean and real-transfer. InternVL3-1B matches that
strong result in the 210-row block, then stays strong in the larger 900-row
block with 0.9563 real-transfer accuracy. InternVL3-2B stays
fully parseable and very strong, but its small 0.0056 drop shows that scaling
within the InternVL family is not monotonic on the current prompt pack.
LLaVA-OneVision 0.5B adds a different contrast: after a memory-safe input
resize path, it reaches a strong 0.9333 real-transfer accuracy in the 210-row
block and remains fully parseable at 0.9213 in the larger 900-row block, but it
still shows a concentrated `dymo_label_maker` weakness and a larger drop on
video-call frame capture.
Qwen2.5-VL-3B adds a separate generation-stability failure mode under transfer
pipelines. Qwen2.5-VL-7B shows that the stronger Qwen family member is
executable on Kaggle P100 under explicit memory controls and can match the
best completed open-weight headline result while staying fully parseable across
all 210 examples. LLaVA-OneVision Qwen2 7B closes the large LLaVA-family
follow-up and raises the open-weight real-transfer headline result to 0.9778;
the negative clean-to-real drop should be read as small-sample variation, not
as evidence that transfer improves recognition.

### Grayscale Control and Channel Effects

The type-10 grayscale no-challenge control is damaging, but it does not explain
the full level-5 collapse. For OpenCLIP ViT-B/16 DataComp XL:

- clean accuracy: 0.5460;
- grayscale control accuracy: 0.3908;
- native level-5 mean accuracy: 0.1451;
- grayscale control minus native level-5: 0.2456.

The paired challenge-family analysis also shows that every usable model is
worse on grayscale level-5 native challenges than on paired color level-5
native challenges. This supports a channel-interaction claim while preserving
the separate conclusion that severe blur/noise/dirty-lens/exposure distortions
add failure beyond grayscale conversion alone.

## Related Work Positioning

CURE-OR++ should be positioned as a compact, object-centric robustness artifact,
not as a replacement for broad VLM robustness suites. The closest neighboring
benchmarks include R-Bench, MLLM-IC, VLM-RobustBench, and MMD-Bench/CLEAR. The
main differentiator is not scale. It is the combination of transparent
generation, paired metadata, small object-recognition scope, and failure tables
that remain easy to inspect by object class, challenge recipe, severity, and
model family.

## Current Limitations

- Real-transfer v0.2 is small: 30 source images, three pipelines, and two
  repeats per source/pipeline. It is an external-validity guardrail, not a
  comprehensive real-world transfer benchmark.
- The current VLM evidence contains eight 210-row open-weight assistant-style
  rows and six 900-row open-weight extension rows, not a broad
  frontier/provider VLM comparison.
- Full-CURE-OR v0.4 is a controlled probe, not an exhaustive evaluation of all
  images in the original dataset.
- SigLIP is currently a diagnostic prompt-protocol failure rather than a usable
  robustness baseline.
- Prototype classifiers are useful model-family contrasts, but they are not
  the same evaluation setting as zero-shot contrastive models.
- Confidence/calibration analysis currently covers the four usable
  CLIP/OpenCLIP-family zero-shot rows, not every prototype row.
- The current technical report does not yet include human study, deployment
  study, or cross-dataset transfer.

## Reproducibility Pointers

Important tracked artifacts:

- `reports/full_cure_or_paper_tables_v04.md`
- `reports/full_cure_or_paper_tables_v04.tex`
- `reports/full_cure_or_confidence_v04.md`
- `reports/full_cure_or_challenge_family_v04.md`
- `reports/full_cure_or_consensus_v04.md`
- `reports/full_cure_or_grayscale_control_v04.md`
- `reports/real_transfer_v02_readiness.md`
- `reports/real_transfer_v02_results.md`
- `reports/vlm_open_weight_smolvlm2_kaggle_v01/summary.md`
- `reports/vlm_open_weight_full_v03_comparison.md`
- `reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/summary.md`
- `reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/summary.md`

Important scripts:

- `scripts/build_paper_tables.py`
- `scripts/analyze_full_cure_or_confidence.py`
- `scripts/analyze_full_cure_or_challenge_families.py`
- `scripts/analyze_full_cure_or_consensus.py`
- `scripts/activate_real_transfer_protocol.py`
- `scripts/run_hf_vlm.py`
- `scripts/evaluate_vlm_response_pack.py`

## Claim Discipline For Public Release

Safe current claims:

- CURE-OR++ exposes severe native CURE-OR challenge failures across several
  model families.
- The hardest level-5 failures have a stable consensus core across eight usable
  baselines.
- Stronger pretraining and prototype features improve absolute level-5 accuracy
  but do not eliminate near-chance collapse on salt-and-pepper and blur variants.
- Grayscale conversion is a meaningful factor but does not explain the full
  native level-5 collapse.
- Some severe challenge failures are overconfident, especially for stronger
  OpenCLIP zero-shot rows.

Claims to avoid until the final paper is complete:

- CURE-OR++ fully models real messaging/video-call pipelines;
- the benchmark is ready as a final arXiv paper rather than a strong
  pre-paper benchmark artifact.
- the current open-weight VLM row represents frontier VLM behavior.
