# CURE-OR++ Technical Report Draft v0.4

## Status

This is the current paper-draft layer for the serious benchmark track. It is
ready for internal iteration, but it should not be treated as a final public
paper until the v0.2 real-transfer validation block is collected and evaluated.

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
  `reports/full_cure_or_paper_tables_v04.md`.

Main blocker:

- real-transfer v0.2 still needs 180 real transferred output images before its
  evaluation section can be written.

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
remaining validation step is a 180-output real-transfer block covering
messenger upload/download, phone screenshot/resave, and video-call frame
capture pipelines.

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
6. A prepared real-transfer v0.2 validation protocol that will test whether
   real app/device transfer pipelines reproduce related failure behavior.

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

## Real-Transfer Section Placeholder

This section should be written after:

```bash
.venv/bin/python scripts/activate_real_transfer_protocol.py --require-ready
```

returns `ready_for_eval: true` and writes
`data/real_transfer/v02/manifest.csv`.

Planned evaluation rows:

- CLIP ViT-B/16;
- CLIP ViT-B/32;
- OpenCLIP ViT-B/32 LAION2B;
- OpenCLIP ViT-B/16 DataComp XL.

The key question is whether messenger upload/download, phone screenshot/resave,
and video-call frame capture reproduce related ranking shifts,
confidence-preserving failures, or model-family sensitivity seen in the native
and simulated probes.

## Reproducibility Pointers

Important tracked artifacts:

- `reports/full_cure_or_paper_tables_v04.md`
- `reports/full_cure_or_paper_tables_v04.tex`
- `reports/full_cure_or_confidence_v04.md`
- `reports/full_cure_or_challenge_family_v04.md`
- `reports/full_cure_or_consensus_v04.md`
- `reports/full_cure_or_grayscale_control_v04.md`
- `reports/real_transfer_v02_readiness.md`

Important scripts:

- `scripts/build_paper_tables.py`
- `scripts/analyze_full_cure_or_confidence.py`
- `scripts/analyze_full_cure_or_challenge_families.py`
- `scripts/analyze_full_cure_or_consensus.py`
- `scripts/activate_real_transfer_protocol.py`

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

Claims to avoid until real-transfer v0.2 is evaluated:

- real app-transfer failures are already proven;
- CURE-OR++ fully models real messaging/video-call pipelines;
- the benchmark is ready as a final arXiv paper rather than a strong
  pre-paper benchmark artifact.
