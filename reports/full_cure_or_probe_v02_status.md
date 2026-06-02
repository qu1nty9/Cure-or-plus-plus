# Full-CURE-OR Probe v0.2

## What Changed

Probe v0.2 expands the first Full-CURE-OR probe from one image per
object/challenge/level to five paired acquisition-condition samples per
object/challenge/level.

Sampling:

- clean rows: 500;
- native challenge rows: 10,000;
- labels: 100 official object-ID-aware labels;
- challenge types: 02, 05, 09, 14, 18;
- levels: 1-4;
- selected acquisition-condition pattern: spread across background/device/
  orientation rather than taking the first sorted files.

The manifest builder now supports:

- `--sampling-strategy spread`;
- `--verify-selected-images`;
- `--require-clean-source`.

This caught and avoided one truncated clean JPEG in the staged external-disk
folder without modifying the external disk.

## Completed Results

Both zero-shot baselines completed on the v0.2 manifest.

| Model | Predictions | Clean accuracy | Mean level-4 native accuracy | Worst level-4 challenge | Worst level-4 accuracy |
| --- | ---: | ---: | ---: | --- | ---: |
| CLIP ViT-B/16 | 10,500 | 0.4440 | 0.1012 | type 14, grayscale gaussian blur | 0.0120 |
| OpenCLIP ViT-B/32 LAION2B | 10,500 | 0.4120 | 0.0932 | type 14, grayscale gaussian blur | 0.0100 |

Level-4 native results:

| Challenge | CLIP ViT-B/16 | OpenCLIP ViT-B/32 LAION2B |
| --- | ---: | ---: |
| type 02, resize | 0.4240 | 0.3940 |
| type 05, gaussian blur | 0.0200 | 0.0220 |
| type 09, salt and pepper noise | 0.0340 | 0.0300 |
| type 14, grayscale gaussian blur | 0.0120 | 0.0100 |
| type 18, grayscale salt and pepper noise | 0.0160 | 0.0100 |

The broader sample raises clean accuracy relative to v0.1, but the severe
native blur/noise failures remain. Resize is still a useful low-damage control:
both models stay near their clean accuracy on type 02 even at level 4.

## Previous Blocker

On the first v0.2 attempt, CLIP ViT-B/16 did not complete because the external
disk disappeared during the run:

```text
df: /Volumes/980PRO/CURE-OR++: No such file or directory
OSError: [Errno 6] Device not configured
```

The invalid zero-byte CLIP v0.2 output files were removed so they cannot be
mistaken for valid results. After the disk was remounted, CLIP ViT-B/16 was
rerun successfully.

## Artifacts

- `scripts/build_full_cure_or_probe_manifests.py`
- `data/interim/full_cure_or_clean_probe_v02_manifest.csv`
- `data/interim/full_cure_or_native_probe_v02_manifest.csv`
- `configs/openclip_vit_b32_laion2b_full_cure_or_probe_v02.json`
- `configs/clip_vit_b16_full_cure_or_probe_v02.json`
- `configs/full_cure_or_probe_summaries_v02.json`
- `results/clip_vit_b16_full_cure_or_probe_v02_predictions.csv`
- `results/clip_vit_b16_full_cure_or_probe_v02_summary.csv`
- `results/openclip_vit_b32_laion2b_full_cure_or_probe_v02_predictions.csv`
- `results/openclip_vit_b32_laion2b_full_cure_or_probe_v02_summary.csv`
- `results/full_cure_or_probe_v02_comparison.csv`
- `results/full_cure_or_probe_v02_level4_ranking.csv`
- `results/full_cure_or_probe_v02_level4_ranking.png`
- `results/full_cure_or_probe_v02_severity_curves.png`
- `results/full_cure_or_probe_v02_openclip_only_comparison.csv`
- `results/full_cure_or_probe_v02_openclip_only_level4_ranking.csv`
- `results/full_cure_or_probe_v02_openclip_only_level4_ranking.png`
- `results/full_cure_or_probe_v02_openclip_only_severity_curves.png`

## Next Step

The next research step is not another tiny probe. It is to choose whether to:

1. add more challenge folders from the official release; or
2. expand this six-folder subset from 5 to 10-25 paired samples per
   object/challenge/level; or
3. add a stronger model family to test whether the collapse is specific to
   CLIP-style contrastive models.
