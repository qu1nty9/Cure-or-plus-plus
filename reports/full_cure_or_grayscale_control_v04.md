# Full-CURE-OR v0.4 Grayscale Control

## Scope

This pass adds CURE-OR challenge type 10, grayscale no-challenge, as a separate
control condition. It is intentionally not part of the native severity grid:
`type_10` has `challenge_level=0` and tests color/channel removal without the
additional severity distortions used in challenge types 11-18.

The control manifest is paired against the existing v0.4 clean manifest:

- clean source rows: 500;
- grayscale control rows: 499;
- objects covered: 100;
- one underfilled object group: `object_057`, with 4 paired control rows
  instead of 5;
- family: `control_cure_or`;
- recipe: `grayscale_no_challenge`;
- severity: `control`.

All external-disk reads stayed under
`/Volumes/980PRO/CURE-OR++/archives`. No files were written to the external
disk.

## Result

| Model | Clean | Grayscale control | Drop vs clean | Native level 1 | Native level 5 | Control minus level 5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| CLIP ViT-B/16 | 0.4440 | 0.3166 | 0.1274 | 0.2772 | 0.0994 | 0.2172 |
| OpenCLIP ViT-B/32 LAION2B | 0.4120 | 0.2465 | 0.1655 | 0.2473 | 0.0890 | 0.1575 |
| CLIP ViT-B/32 | 0.3500 | 0.2244 | 0.1256 | 0.2220 | 0.0741 | 0.1503 |

The prototype-extended control comparison is generated separately in
`results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.csv`
and summarized in `reports/full_cure_or_prototype_v04.md`. That extended table
now includes HGNetV2-B0, MobileNetV3-Small, ConvNeXt-Tiny, and DINOv2 ViT-S/14.

## Interpretation

The grayscale-only control is damaging, but it does not explain the full native
level-5 collapse.

For CLIP ViT-B/16, grayscale no-challenge accuracy is 0.3166, above native
level-1 mean accuracy of 0.2772 and far above native level-5 mean accuracy of
0.0994. For OpenCLIP and CLIP ViT-B/32, grayscale control is almost equal to
native level 1, but still much higher than level 5.

This supports a cleaner paper claim: grayscale/channel removal contributes to
the difficulty of grayscale native challenges, but severe blur, noise, dirty
lens, exposure, and contrast distortions introduce additional failure beyond
grayscale conversion alone.

## Artifacts

- `scripts/build_full_cure_or_control_manifest.py`
- `scripts/compare_full_cure_or_control.py`
- `scripts/plot_full_cure_or_control.py`
- `configs/clip_vit_b16_full_cure_or_grayscale_control_v04.json`
- `configs/clip_vit_b32_full_cure_or_grayscale_control_v04.json`
- `configs/openclip_vit_b32_laion2b_full_cure_or_grayscale_control_v04.json`
- `configs/full_cure_or_grayscale_control_summaries_v04.json`
- `data/interim/full_cure_or_grayscale_control_v04_manifest.csv`
- `results/clip_vit_b16_full_cure_or_grayscale_control_v04_predictions.csv`
- `results/clip_vit_b16_full_cure_or_grayscale_control_v04_summary.csv`
- `results/clip_vit_b32_full_cure_or_grayscale_control_v04_predictions.csv`
- `results/clip_vit_b32_full_cure_or_grayscale_control_v04_summary.csv`
- `results/openclip_vit_b32_laion2b_full_cure_or_grayscale_control_v04_predictions.csv`
- `results/openclip_vit_b32_laion2b_full_cure_or_grayscale_control_v04_summary.csv`
- `results/full_cure_or_grayscale_control_v04_comparison.csv`
- `results/full_cure_or_grayscale_control_v04_comparison.png`

## Reproduction

```bash
.venv/bin/python scripts/build_full_cure_or_control_manifest.py \
  --archives-dir /Volumes/980PRO/CURE-OR++/archives \
  --clean-manifest data/interim/full_cure_or_clean_probe_v04_manifest.csv \
  --output data/interim/full_cure_or_grayscale_control_v04_manifest.csv \
  --control-type 10 \
  --max-per-object 5 \
  --sampling-strategy spread \
  --verify-selected-images

HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  .venv/bin/python scripts/evaluate_clip_zero_shot.py \
  --config configs/clip_vit_b16_full_cure_or_grayscale_control_v04.json \
  --device cpu

HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  .venv/bin/python scripts/evaluate_clip_zero_shot.py \
  --config configs/clip_vit_b32_full_cure_or_grayscale_control_v04.json \
  --device cpu

.venv/bin/python scripts/evaluate_openclip_zero_shot.py \
  --config configs/openclip_vit_b32_laion2b_full_cure_or_grayscale_control_v04.json \
  --device cpu

.venv/bin/python scripts/compare_full_cure_or_control.py \
  --config configs/full_cure_or_grayscale_control_summaries_v04.json \
  --native-comparison results/full_cure_or_probe_v04_expanded_comparison.csv \
  --output results/full_cure_or_grayscale_control_v04_comparison.csv

MPLCONFIGDIR=/private/tmp/cure_or_pp_mpl MPLBACKEND=Agg \
  .venv/bin/python scripts/plot_full_cure_or_control.py \
  --input results/full_cure_or_grayscale_control_v04_comparison.csv \
  --output results/full_cure_or_grayscale_control_v04_comparison.png
```

## Next Step

The remaining paper-level gaps are no longer dataset staging, all-challenge
coverage, confidence analysis, or grayscale control. The next high-value step is
adding more usable model families or a real transfer validation sample.
