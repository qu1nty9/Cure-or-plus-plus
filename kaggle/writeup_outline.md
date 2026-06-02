# Kaggle Notebook Write-Up Outline

## Title

CURE-OR++: Measuring Model Robustness Under Modern Transfer Distortions

## Hook

Classic robustness benchmarks usually test isolated corruptions. Real images
often pass through transfer chains: low-light capture, resize, screenshot,
messenger recompression, video-call compression, denoise or upscale.

## Dataset

- Derived from mini-CURE-OR.
- 250 clean source images.
- 10 object classes, 25 images per class.
- 9 distortion recipes.
- 3 severity levels.
- 6,750 generated distorted images.

## Baselines

- CLIP ViT-B/32 zero-shot classification over the 10 mini-CURE-OR classes.
- CLIP ViT-B/16 zero-shot classification over the 10 mini-CURE-OR classes.
- OpenCLIP ViT-B/32 LAION2B zero-shot classification over the 10 mini-CURE-OR
  classes.
- SigLIP Base P16 224 zero-shot diagnostic baseline.
- HGNetV2-B0 clean-train prototype classifier.
- MobileNetV3-Small clean-train prototype classifier.
- CLIP total evaluated images: 7,000 per CLIP variant.
- OpenCLIP total evaluated images: 7,000.
- Fair test-split comparison: 100 clean images plus 2,700 distorted images per
  model.

## Main Result

On the full clean subset, CLIP ViT-B/16 clean accuracy is 0.9160, OpenCLIP
ViT-B/32 LAION2B clean accuracy is 0.8800, and CLIP ViT-B/32 clean accuracy is
0.8280. On the fair test split, `low_light_upload` is the worst high-severity
recipe for both CLIP variants, OpenCLIP, and HGNetV2-B0, while
MobileNetV3-Small is most affected by `video_call_frame`.

OpenCLIP gives the benchmark a usable non-OpenAI contrastive baseline. SigLIP
is included as a diagnostic baseline, but its clean test accuracy is only
0.1900 under the current prompt protocol.

## Interpretation

Modern transfer distortions are not uniformly harder than classic corruptions.
The useful finding is more specific: some realistic transfer chains create a
distinct failure profile, and the ranking changes across model families.
The confidence shift table adds a second axis: some failures come with strong
confidence collapse, while OpenCLIP keeps relatively high confidence on its
largest `low_light_upload` drop.

Position this against R-Bench, MLLM-IC, VLM-RobustBench, and CLEAR/MMD-Bench:
CURE-OR++ is smaller, but it is object-centric, reproducible, and designed for
recipe/class-level inspection.

## Limitations

- SigLIP needs prompt/protocol work before it can support strong robustness
  claims.
- Simulated transfer chains.
- Small object vocabulary.
- Prototype classifiers are lightweight baselines, not fully trained task
  models.

## Next Step

Add at least one real app-transfer validation sample, then run a Full-CURE-OR
pilot after the local mini-CURE-OR story is frozen.

Local native-CURE note:

- A native mini-CURE-OR test-grid evaluation has been run outside the first
  Kaggle package.
- It evaluates 6,400 native challenge images from the test split.
- It covers challenge types 2-9 and 11-18 across levels 1-4.
- Type 14, grayscale gaussian blur, collapses both CLIP ViT-B/16 and OpenCLIP
  to 0.1000 accuracy at level 4.
- OpenCLIP also falls to 0.1000 on type 18, grayscale salt and pepper noise,
  while retaining 0.9730 mean confidence.
- Keep it as v0.2 evidence unless the corresponding native challenge images are
  added to the public dataset package.
