# Full-CURE-OR v0.4 Paper Tables

These tables are generated from tracked aggregate result CSVs, not from per-image prediction dumps.

## Model Leaderboard

| Model | Clean | Native mean | Level 1 | Level 5 | L5 drop | Worst L5 |
| --- | --- | --- | --- | --- | --- | --- |
| DINOv2 ViT-S/14 Prototype | 0.752 | 0.439 | 0.588 | 0.277 | 0.475 | Grayscale salt & pepper noise (0.008) |
| ConvNeXt-Tiny Prototype | 0.616 | 0.344 | 0.448 | 0.224 | 0.392 | Grayscale salt & pepper noise (0.008) |
| OpenCLIP ViT-B/16 DataComp XL | 0.546 | 0.256 | 0.362 | 0.145 | 0.401 | Salt & pepper noise (0.008) |
| HGNetV2-B0 Prototype | 0.624 | 0.255 | 0.379 | 0.122 | 0.502 | Gaussian blur (0.010) |
| CLIP ViT-B/16 | 0.444 | 0.193 | 0.277 | 0.099 | 0.345 | Salt & pepper noise (0.010) |
| MobileNetV3-Small Prototype | 0.556 | 0.194 | 0.286 | 0.096 | 0.460 | Gaussian blur (0.010) |
| OpenCLIP ViT-B/32 LAION2B | 0.412 | 0.170 | 0.247 | 0.089 | 0.323 | Grayscale salt & pepper noise (0.008) |
| CLIP ViT-B/32 | 0.350 | 0.153 | 0.222 | 0.074 | 0.276 | Salt & pepper noise (0.006) |

## Consensus Level-5 Failures

| Rank | Type | Challenge | Mean acc. | Median acc. | Floor | Top-3 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 18 | Grayscale salt & pepper noise | 0.009 | 0.010 | 8/8 | 8/8 |
| 2 | 09 | Salt & pepper noise | 0.010 | 0.010 | 8/8 | 6/8 |
| 3 | 14 | Grayscale gaussian blur | 0.011 | 0.010 | 8/8 | 8/8 |
| 4 | 05 | Gaussian blur | 0.015 | 0.014 | 7/8 | 3/8 |
| 5 | 16 | Grayscale dirty lens 1 | 0.026 | 0.018 | 5/8 | 1/8 |
| 6 | 07 | Dirty lens 1 | 0.089 | 0.075 | 0/8 | 0/8 |

## Grayscale Control Guardrail

| Model | Clean | Gray control | Native L5 | Control - L5 | Control drop |
| --- | --- | --- | --- | --- | --- |
| DINOv2 ViT-S/14 Prototype | 0.752 | 0.741 | 0.277 | 0.465 | 0.011 |
| ConvNeXt-Tiny Prototype | 0.616 | 0.491 | 0.224 | 0.267 | 0.125 |
| OpenCLIP ViT-B/16 DataComp XL | 0.546 | 0.391 | 0.145 | 0.246 | 0.155 |
| HGNetV2-B0 Prototype | 0.624 | 0.443 | 0.122 | 0.321 | 0.181 |
| CLIP ViT-B/16 | 0.444 | 0.317 | 0.099 | 0.217 | 0.127 |
| MobileNetV3-Small Prototype | 0.556 | 0.285 | 0.096 | 0.189 | 0.271 |
| OpenCLIP ViT-B/32 LAION2B | 0.412 | 0.246 | 0.089 | 0.157 | 0.166 |
| CLIP ViT-B/32 | 0.350 | 0.224 | 0.074 | 0.150 | 0.126 |

## Notes

- The model leaderboard excludes the SigLIP diagnostic failure row.
- Native means are weighted by row count `n`.
- The grayscale control is type 10/no-challenge grayscale, so it is a guardrail rather than a native challenge.
