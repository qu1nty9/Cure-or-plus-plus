# Full-CURE-OR Probe v0.1

## Scope

This is the first controlled Full-CURE-OR probe using the extracted IEEE
DataPort folders staged under:

```text
/Volumes/980PRO/CURE-OR++/archives
```

The local external-disk subset currently contains 312,500 image files across
six official challenge folders:

- type 01: no challenge;
- type 02: resize;
- type 05: gaussian blur;
- type 09: salt and pepper noise;
- type 14: grayscale gaussian blur;
- type 18: grayscale salt and pepper noise.

The evaluated probe is intentionally balanced and small:

| Split | Rows | Sampling |
| --- | ---: | --- |
| Clean | 100 | 1 image per official object ID |
| Native challenge | 2,000 | 5 challenge types x 4 levels x 100 objects |

The manifests use the official 100-object map from
`configs/cure_or_objects_v01.json`. Duplicate display names are represented by
object-ID-aware label keys, for example `object_034_calculator` and
`object_066_calculator`.

## Models

| Model | Role |
| --- | --- |
| CLIP ViT-B/16 | stronger OpenAI CLIP zero-shot baseline |
| OpenCLIP ViT-B/32 LAION2B | open contrastive zero-shot baseline |

## Main Results

| Model | Clean accuracy | Mean level-4 native accuracy | Worst level-4 challenge | Worst level-4 accuracy |
| --- | ---: | ---: | --- | ---: |
| CLIP ViT-B/16 | 0.3900 | 0.0780 | type 09, salt and pepper noise | 0.0000 |
| OpenCLIP ViT-B/32 LAION2B | 0.3100 | 0.0620 | type 05, gaussian blur | 0.0100 |

CLIP ViT-B/16 also reaches 0.0000 on type 18, grayscale salt and pepper noise.
OpenCLIP ties at 0.0100 across type 05, type 09, type 14, and type 18.

Level-4 accuracy by challenge:

| Model | Resize | Gaussian blur | Salt and pepper | Grayscale blur | Grayscale salt and pepper |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP ViT-B/16 | 0.3600 | 0.0200 | 0.0000 | 0.0100 | 0.0000 |
| OpenCLIP ViT-B/32 LAION2B | 0.2700 | 0.0100 | 0.0100 | 0.0100 | 0.0100 |

## Interpretation

The move from mini-CURE-OR to the official 100-object Full-CURE-OR label space
changes the difficulty sharply. Clean zero-shot accuracy falls to 0.3900 for
CLIP ViT-B/16 and 0.3100 for OpenCLIP, so these numbers should be treated as
full-probe results rather than direct replacements for the mini-CURE-OR
headlines.

The robustness signal is strong anyway:

- resize behaves like a low-damage control;
- blur, salt and pepper noise, and grayscale combinations almost collapse both
  zero-shot models at level 4;
- the failure pattern from the native mini-CURE-OR grid survives in the full
  release subset.

This is not yet a paper-scale result. It is a validated ingestion and
evaluation bridge: official Full-CURE-OR images are being read from the
external disk, object-ID-aware labels work, both model configs run, predictions
are written, and the comparison scripts produce publication-oriented tables and
figures.

## Artifacts

- `scripts/build_full_cure_or_probe_manifests.py`
- `data/interim/full_cure_or_clean_probe_v01_manifest.csv`
- `data/interim/full_cure_or_native_probe_v01_manifest.csv`
- `results/clip_vit_b16_full_cure_or_probe_v01_summary.csv`
- `results/openclip_vit_b32_laion2b_full_cure_or_probe_v01_summary.csv`
- `results/full_cure_or_probe_v01_comparison.csv`
- `results/full_cure_or_probe_v01_level4_ranking.csv`
- `results/full_cure_or_probe_v01_level4_ranking.png`
- `results/full_cure_or_probe_v01_severity_curves.png`

## Next Gate

The next serious step is to scale the probe without losing control:

1. increase sampling to multiple backgrounds/devices/orientations per object;
2. add the remaining downloaded and available challenge types;
3. add stronger model families only after the full-probe sampling protocol is
   fixed;
4. add paired clean-vs-distorted analysis so the writeup can separate label
   difficulty from transfer degradation.
