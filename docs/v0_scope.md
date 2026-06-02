# V0 Scope

## One-Sentence Version

CURE-OR++ measures whether realistic digital transfer chains degrade modern
vision and vision-language models differently from classic one-step corruptions.

## What V0 Is

V0 is a compact, reproducible benchmark with a limited dataset, limited model
set, and strong analysis. It is designed to produce a useful public artifact
quickly.

## What V0 Is Not

V0 is not a full leaderboard, not a new foundation-model suite, and not a broad
survey of robustness. Those can come later if the first results are interesting.

## Minimum Novelty Bar

The project should answer at least one of these:

- Do transfer-chain distortions cause different model rankings than classic
  corruptions?
- Are VLMs more sensitive to screenshot/recompression/resampling chains than
  object classifiers?
- Do confidence scores collapse before accuracy collapses?
- Are large models smoother or more brittle across severity levels?

## V0 Distortion Recipes

Classic baselines:

- JPEG compression;
- Gaussian blur or motion blur;
- resize down/up.

Modern transfer recipes:

- screenshot chain: resize, sharpen, chroma subsampling, JPEG;
- messenger chain: resize cap, JPEG quality drop, metadata removal;
- video-call frame: downscale, block artifacts, mild blur, noise;
- low-light upload: gamma darkening, noise, denoise, recompression;
- restoration chain: blur, upscale, sharpen/denoise artifacts;
- dirty lens plus recompression.

## V0 Metrics

- Clean accuracy.
- Distorted accuracy.
- Relative performance drop.
- Area under degradation curve.
- Stability score across severity.
- Ranking shift between clean/classic/modern conditions.
- Confidence drop when probabilities are available.

## First Decision

Start with image classification and CLIP-style zero-shot evaluation first.
VLM question-answer evaluation should be added only after the base pipeline is
working, because it is slower, more expensive, and harder to score cleanly.

