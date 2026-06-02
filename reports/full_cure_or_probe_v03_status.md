# Full-CURE-OR Probe v0.3

## What Changed

Probe v0.3 extends the v0.2 six-folder Full-CURE-OR probe with official
`level_5` rows where the staged challenge folders provide them.

Sampling:

- clean rows: 500;
- native challenge rows: 12,000;
- labels: 100 official object-ID-aware labels;
- challenge types: 02, 05, 09, 14, 18;
- type 02 levels: 1-4;
- type 05, 09, 14, 18 levels: 1-5;
- selected acquisition-condition pattern: five spread samples per
  object/challenge/level.

All external-disk reads were limited to
`/Volumes/980PRO/CURE-OR++/archives`. No files were written to the external
disk.

## Completed Results

Both zero-shot baselines completed on the v0.3 manifest.

| Model | Predictions | Clean accuracy | Mean native accuracy | Mean level-4 accuracy | Mean level-5 accuracy | Worst level-5 challenge | Worst level-5 accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| CLIP ViT-B/16 | 12,500 | 0.4440 | 0.1274 | 0.1012 | 0.0135 | type 09, salt and pepper noise; tied with type 18 | 0.0100 |
| OpenCLIP ViT-B/32 LAION2B | 12,500 | 0.4120 | 0.1159 | 0.0932 | 0.0115 | type 18, grayscale salt and pepper noise | 0.0080 |

Level-5 native results:

| Challenge | CLIP ViT-B/16 | OpenCLIP ViT-B/32 LAION2B |
| --- | ---: | ---: |
| type 05, gaussian blur | 0.0200 | 0.0140 |
| type 09, salt and pepper noise | 0.0100 | 0.0140 |
| type 14, grayscale gaussian blur | 0.0140 | 0.0100 |
| type 18, grayscale salt and pepper noise | 0.0100 | 0.0080 |

Level-4 native results remain consistent with v0.2 on the shared subset:

| Challenge | CLIP ViT-B/16 | OpenCLIP ViT-B/32 LAION2B |
| --- | ---: | ---: |
| type 02, resize | 0.4240 | 0.3940 |
| type 05, gaussian blur | 0.0200 | 0.0220 |
| type 09, salt and pepper noise | 0.0340 | 0.0300 |
| type 14, grayscale gaussian blur | 0.0120 | 0.0100 |
| type 18, grayscale salt and pepper noise | 0.0160 | 0.0100 |

## Interpretation

The v0.3 result strengthens the core signal. Resize still behaves like a mild
control condition, while severe blur/noise and grayscale combinations almost
collapse both CLIP-family models. At `level_5`, both models fall to roughly
chance-level performance on the four severe native challenge types.

The level-5 ranking is not identical across models:

- CLIP ViT-B/16 is worst on type 09, tied with type 18 at 0.0100 accuracy.
- OpenCLIP ViT-B/32 LAION2B is worst on type 18 at 0.0080 accuracy.

That gives us a useful paper-level angle: the collapse is shared, but the
ordering of the most damaging acquisition/channel corruptions is model-family
dependent.

## Artifacts

- `data/interim/full_cure_or_clean_probe_v03_manifest.csv`
- `data/interim/full_cure_or_native_probe_v03_manifest.csv`
- `configs/openclip_vit_b32_laion2b_full_cure_or_probe_v03.json`
- `configs/clip_vit_b16_full_cure_or_probe_v03.json`
- `configs/full_cure_or_probe_summaries_v03.json`
- `results/openclip_vit_b32_laion2b_full_cure_or_probe_v03_predictions.csv`
- `results/openclip_vit_b32_laion2b_full_cure_or_probe_v03_summary.csv`
- `results/clip_vit_b16_full_cure_or_probe_v03_predictions.csv`
- `results/clip_vit_b16_full_cure_or_probe_v03_summary.csv`
- `results/full_cure_or_probe_v03_comparison.csv`
- `results/full_cure_or_probe_v03_level5_ranking.csv`
- `results/full_cure_or_probe_v03_level5_ranking.png`
- `results/full_cure_or_probe_v03_severity_curves.png`

## Next Step

The first option from this v0.3 checkpoint was completed in
`reports/full_cure_or_probe_v04_status.md`: the remaining official challenge
folders were staged and evaluated in an all-challenge probe. The next active
research step is now to add stronger model families and confidence analysis on
the v0.4 manifest.
