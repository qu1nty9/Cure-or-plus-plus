# Full-CURE-OR Readiness v0.4

## Current State

We have completed a controlled all-challenge Full-CURE-OR ingestion and
evaluation probe, but we are not ready for a final paper-scale evaluation yet.

Completed locally:

- official challenge type mapping;
- local native mini-CURE-OR test-grid evaluation;
- reusable native manifest builder;
- reusable dataset probe script;
- official 100-object label map for Full-CURE-OR;
- Full-CURE-OR OpenCLIP and CLIP probe configs;
- config validator with duplicate-display-name warning;
- mini-CURE-OR probe report with image existence checks;
- extracted Full-CURE-OR first-probe folders on the external disk;
- balanced Full-CURE-OR clean and native probe manifests;
- all 18 official extracted folders staged on the external disk;
- Full-CURE-OR CLIP ViT-B/16 and OpenCLIP ViT-B/32 zero-shot probe results;
- all-challenge Full-CURE-OR v0.4 probe across challenge types 02-09 and
  11-18.
- expanded v0.4 local-cache model pass with CLIP ViT-B/32 and a SigLIP
  diagnostic result.
- v0.4 confidence-collapse and calibration analysis for the four usable
  CLIP/OpenCLIP-family zero-shot baselines.
- v0.4 type-10 grayscale no-challenge control for the first three usable
  zero-shot baselines.
- v0.4 leave-clean-condition-out prototype baselines with HGNetV2-B0,
  MobileNetV3-Small, ConvNeXt-Tiny, and DINOv2 ViT-S/14.
- v0.4 OpenCLIP ViT-B/16 DataComp XL stronger-baseline run.
- v0.4 challenge-family/channel-effect analysis for eight usable baselines.
- v0.4 consensus failure analysis for eight usable baselines.
- real-transfer validation v0.2 source selection, validator, and four
  zero-shot evaluation configs prepared.

## Mini Probe Result

`scripts/probe_cure_or_dataset.py` was run on `data/raw/mini_cure_or`.

| Check | Result |
| --- | ---: |
| CSV rows | 16,500 |
| Clean rows | 250 |
| Native challenge rows | 16,250 |
| Image files | 16,500 |
| Image bytes | 3,455,399,222 |
| Image GiB | 3.2181 |
| Missing image rows | 0 |
| Scope rows | 132 |

Artifacts:

- `reports/mini_cure_or_probe_v01.json`
- `reports/mini_cure_or_scope_v01.csv`
- `configs/cure_or_objects_v01.json`
- `configs/openclip_vit_b32_laion2b_full_cure_or_probe_v01.json`
- `configs/clip_vit_b16_full_cure_or_probe_v01.json`
- `scripts/validate_eval_config.py`

## Full-CURE-OR Probe Result

The Full-CURE-OR probes use extracted official folders under
`/Volumes/980PRO/CURE-OR++/archives`.

Local extracted folders:

- all 18 official folders are staged;
- type 01 and type 10 are no-challenge controls;
- type 02 and type 11 provide levels 1-4;
- types 03-09 and 12-18 provide levels 1-5.

Evaluated v0.1 probe:

- 100 clean images, one per official object ID;
- 2,000 native challenge images;
- challenge types: 02, 05, 09, 14, 18;
- challenge levels: 1-4;
- models: CLIP ViT-B/16, OpenCLIP ViT-B/32 LAION2B, CLIP ViT-B/32, and
  SigLIP Base P16 224 diagnostic.

Evaluated v0.2 probe:

- 500 clean images;
- 10,000 native challenge images;
- 5 paired acquisition-condition samples per object/challenge/level;
- challenge types: 02, 05, 09, 14, 18;
- challenge levels: 1-4;
- models: CLIP ViT-B/16, OpenCLIP ViT-B/32 LAION2B, CLIP ViT-B/32, and
  SigLIP Base P16 224 diagnostic.

Headline v0.2 results:

| Model | Clean accuracy | Mean level-4 native accuracy | Worst level-4 accuracy |
| --- | ---: | ---: | ---: |
| CLIP ViT-B/16 | 0.4440 | 0.1012 | 0.0120 |
| OpenCLIP ViT-B/32 LAION2B | 0.4120 | 0.0932 | 0.0100 |

v0.3 extends the same six-folder probe to official level 5 for challenge types
05, 09, 14, and 18:

| Model | Clean accuracy | Mean level-5 native accuracy | Worst level-5 accuracy |
| --- | ---: | ---: | ---: |
| CLIP ViT-B/16 | 0.4440 | 0.0135 | 0.0100 |
| OpenCLIP ViT-B/32 LAION2B | 0.4120 | 0.0115 | 0.0080 |

This subset directly tests whether the strongest mini-CURE-OR native failures
survive on the full release. They do: resize remains comparatively mild, while
blur, salt and pepper noise, and grayscale combinations nearly collapse both
zero-shot models at level 4.

Evaluated v0.4 probe:

- 500 clean images;
- 38,999 native challenge images;
- 5 paired acquisition-condition samples per object/challenge/level, except one
  strict paired-source group with 4 usable samples;
- challenge types: 02-09 and 11-18;
- challenge levels: 1-5 where available;
- type 02 and type 11 have levels 1-4 only;
- main comparison models: CLIP ViT-B/16, OpenCLIP ViT-B/32 LAION2B,
  CLIP ViT-B/32, HGNetV2-B0 Prototype, MobileNetV3-Small Prototype,
  ConvNeXt-Tiny Prototype, and DINOv2 ViT-S/14 Prototype.

Headline v0.4 results:

| Model | Clean accuracy | Mean native accuracy | Mean level-4 native accuracy | Mean level-5 native accuracy | Worst level-5 accuracy |
| --- | ---: | ---: | ---: | ---: | ---: |
| DINOv2 ViT-S/14 Prototype | 0.7520 | 0.4393 | 0.3819 | 0.2766 | 0.0080 |
| ConvNeXt-Tiny Prototype | 0.6160 | 0.3436 | 0.2965 | 0.2239 | 0.0080 |
| CLIP ViT-B/16 | 0.4440 | 0.1929 | 0.1596 | 0.0994 | 0.0100 |
| HGNetV2-B0 Prototype | 0.6240 | 0.2547 | 0.2045 | 0.1219 | 0.0100 |
| MobileNetV3-Small Prototype | 0.5560 | 0.1936 | 0.1631 | 0.0960 | 0.0100 |
| OpenCLIP ViT-B/32 LAION2B | 0.4120 | 0.1705 | 0.1400 | 0.0890 | 0.0080 |
| CLIP ViT-B/32 | 0.3500 | 0.1532 | 0.1249 | 0.0741 | 0.0060 |
| SigLIP Base P16 224 | 0.0120 | 0.0103 | 0.0096 | 0.0084 | 0.0060 |

This is now the strongest local evidence for the project: the native CURE-OR
failure pattern survives after moving from mini-CURE-OR to the official
100-object Full-CURE-OR label space and after adding the remaining official
challenge folders.

DINOv2 ViT-S/14 raises the current benchmark ceiling: it is strongest on clean
accuracy, grayscale control, mean native accuracy, and level-5 native accuracy.
The key failure claim still holds because its worst level-5 challenge remains
near chance at 0.0080 accuracy.

SigLIP should not be counted as a strong robustness baseline yet. Its clean
accuracy is 0.0120 under the current prompt protocol, so the run is useful as a
documented diagnostic failure, not as evidence about SigLIP robustness.

Confidence/calibration result:

| Model | Level-5 accuracy | Level-5 confidence | Calibration gap | High-conf wrong rate |
| --- | ---: | ---: | ---: | ---: |
| CLIP ViT-B/16 | 0.0994 | 0.2610 | 0.1616 | 0.0439 |
| OpenCLIP ViT-B/32 LAION2B | 0.0890 | 0.4781 | 0.3891 | 0.3141 |
| OpenCLIP ViT-B/16 DataComp XL | 0.1451 | 0.4997 | 0.3545 | 0.3240 |
| CLIP ViT-B/32 | 0.0741 | 0.2716 | 0.1974 | 0.0700 |

This adds an arXiv-relevant failure mode: native distortions can produce
low-accuracy, high-confidence predictions, including in the stronger DataComp
XL row.

Grayscale control result:

| Model | Clean | Grayscale control | Drop vs clean | Native level 5 |
| --- | ---: | ---: | ---: | ---: |
| CLIP ViT-B/16 | 0.4440 | 0.3166 | 0.1274 | 0.0994 |
| OpenCLIP ViT-B/32 LAION2B | 0.4120 | 0.2465 | 0.1655 | 0.0890 |
| CLIP ViT-B/32 | 0.3500 | 0.2244 | 0.1256 | 0.0741 |
| HGNetV2-B0 Prototype | 0.6240 | 0.4429 | 0.1811 | 0.1219 |
| MobileNetV3-Small Prototype | 0.5560 | 0.2846 | 0.2714 | 0.0960 |
| ConvNeXt-Tiny Prototype | 0.6160 | 0.4910 | 0.1250 | 0.2239 |
| DINOv2 ViT-S/14 Prototype | 0.7520 | 0.7415 | 0.0105 | 0.2766 |

This separates grayscale/channel loss from full native severity: grayscale
alone hurts, but it does not explain level-5 collapse.

Challenge-family result:

| Model | Color level 5 | Grayscale level 5 | Grayscale minus color |
| --- | ---: | ---: | ---: |
| DINOv2 ViT-S/14 Prototype | 0.3071 | 0.2460 | -0.0611 |
| ConvNeXt-Tiny Prototype | 0.2743 | 0.1734 | -0.1009 |
| CLIP ViT-B/16 | 0.1306 | 0.0683 | -0.0623 |
| OpenCLIP ViT-B/32 LAION2B | 0.1203 | 0.0577 | -0.0626 |

Every usable model is worse on paired grayscale level-5 native challenges than
on the corresponding color level-5 challenges. The largest paired penalties
often appear in dirty-lens, contrast, and exposure distortions; blur/noise pairs
can show small gaps because both color and grayscale variants are already near
chance.

Consensus failure result:

| Consensus rank | Challenge | Mean accuracy | Floor models |
| ---: | --- | ---: | ---: |
| 1 | Grayscale salt & pepper noise | 0.0092 | 8 / 8 |
| 2 | Salt & pepper noise | 0.0103 | 8 / 8 |
| 3 | Grayscale gaussian blur | 0.0115 | 8 / 8 |
| 4 | Gaussian blur | 0.0150 | 7 / 8 |

Pairwise level-5 rank correlations across the eight usable baselines range from
0.892 to 0.988. This makes the current v0.4 evidence stronger: the worst
challenge ordering has a stable consensus core, not only isolated per-model
worst cases.

Config validation status:

- OpenCLIP Full-CURE v0.4 probe config loads 100 label keys.
- CLIP ViT-B/16 Full-CURE v0.4 probe config loads 100 label keys.
- CLIP ViT-B/32 Full-CURE v0.4 probe config loads 100 label keys.
- OpenCLIP ViT-B/16 DataComp XL Full-CURE v0.4 probe config loads 100 label
  keys.
- SigLIP Base P16 224 Full-CURE v0.4 probe config loads 100 label keys.
- All configs warn that `Calculator` is a duplicate display name in the
  official object list.

Artifacts:

- `reports/full_cure_or_probe_v01.md`
- `reports/full_cure_or_probe_v02_status.md`
- `reports/full_cure_or_probe_v03_status.md`
- `reports/full_cure_or_probe_v04_status.md`
- `data/interim/full_cure_or_clean_probe_v01_manifest.csv`
- `data/interim/full_cure_or_native_probe_v01_manifest.csv`
- `data/interim/full_cure_or_clean_probe_v02_manifest.csv`
- `data/interim/full_cure_or_native_probe_v02_manifest.csv`
- `data/interim/full_cure_or_clean_probe_v03_manifest.csv`
- `data/interim/full_cure_or_native_probe_v03_manifest.csv`
- `data/interim/full_cure_or_clean_probe_v04_manifest.csv`
- `data/interim/full_cure_or_native_probe_v04_manifest.csv`
- `results/full_cure_or_probe_v01_comparison.csv`
- `results/full_cure_or_probe_v01_level4_ranking.csv`
- `results/full_cure_or_probe_v01_level4_ranking.png`
- `results/full_cure_or_probe_v01_severity_curves.png`
- `results/full_cure_or_probe_v02_comparison.csv`
- `results/full_cure_or_probe_v02_level4_ranking.csv`
- `results/full_cure_or_probe_v02_level4_ranking.png`
- `results/full_cure_or_probe_v02_severity_curves.png`
- `results/full_cure_or_probe_v03_comparison.csv`
- `results/full_cure_or_probe_v03_level5_ranking.csv`
- `results/full_cure_or_probe_v03_level5_ranking.png`
- `results/full_cure_or_probe_v03_severity_curves.png`
- `results/full_cure_or_probe_v04_comparison.csv`
- `results/full_cure_or_probe_v04_level5_ranking.csv`
- `results/full_cure_or_probe_v04_level5_ranking.png`
- `results/full_cure_or_probe_v04_severity_curves.png`
- `results/full_cure_or_probe_v04_mean_accuracy_by_level.png`
- `reports/full_cure_or_probe_v04_expanded_models.md`
- `results/full_cure_or_probe_v04_expanded_comparison.csv`
- `results/full_cure_or_probe_v04_expanded_level5_ranking.csv`
- `results/full_cure_or_probe_v04_expanded_level5_ranking.png`
- `results/full_cure_or_probe_v04_expanded_mean_accuracy_by_level.png`
- `reports/full_cure_or_confidence_v04.md`
- `results/full_cure_or_probe_v04_confidence_shift.csv`
- `results/full_cure_or_probe_v04_confidence_by_level.csv`
- `results/full_cure_or_probe_v04_overconfidence_ranking.csv`
- `results/full_cure_or_probe_v04_confidence_by_level.png`
- `results/full_cure_or_probe_v04_level5_overconfidence.png`
- `reports/full_cure_or_grayscale_control_v04.md`
- `data/interim/full_cure_or_grayscale_control_v04_manifest.csv`
- `results/full_cure_or_grayscale_control_v04_comparison.csv`
- `results/full_cure_or_grayscale_control_v04_comparison.png`
- `reports/full_cure_or_prototype_v04.md`
- `configs/convnext_tiny_fb_in1k_full_cure_or_prototype_v04.json`
- `configs/dinov2_vit_small_patch14_full_cure_or_prototype_v04.json`
- `results/convnext_tiny_fb_in1k_full_cure_or_prototype_v04_summary.csv`
- `results/dinov2_vit_small_patch14_full_cure_or_prototype_v04_summary.csv`
- `configs/openclip_vit_b16_datacomp_xl_full_cure_or_probe_v04.json`
- `results/openclip_vit_b16_datacomp_xl_full_cure_or_probe_v04_summary.csv`
- `results/full_cure_or_probe_v04_with_prototypes_comparison.csv`
- `results/full_cure_or_probe_v04_with_prototypes_level5_ranking.csv`
- `results/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png`
- `results/full_cure_or_probe_v04_with_prototypes_level5_ranking.png`
- `results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.csv`
- `results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.png`
- `scripts/analyze_full_cure_or_challenge_families.py`
- `results/full_cure_or_probe_v04_with_prototypes_channel_effects.csv`
- `results/full_cure_or_probe_v04_with_prototypes_paired_channel_gaps.csv`
- `reports/full_cure_or_challenge_family_v04.md`
- `scripts/analyze_full_cure_or_consensus.py`
- `results/full_cure_or_probe_v04_with_prototypes_level5_consensus.csv`
- `results/full_cure_or_probe_v04_with_prototypes_level5_rank_correlations.csv`
- `reports/full_cure_or_consensus_v04.md`
- `data/real_transfer/v02/source_selection_v02.csv`
- `data/real_transfer/v02/recipe_plan_v02.csv`
- `data/real_transfer/v02/pairs_template.csv`
- `scripts/validate_real_transfer_pairs.py`
- `configs/clip_vit_b16_real_transfer_v02.json`
- `configs/clip_vit_b32_real_transfer_v02.json`
- `configs/openclip_vit_b32_laion2b_real_transfer_v02.json`
- `configs/openclip_vit_b16_datacomp_xl_real_transfer_v02.json`
- `reports/real_transfer_v02_readiness.md`

## Remaining Limitation

The complete 18-folder release is now staged and probed, so the remaining
limitation is no longer folder availability. The v0.4 probe now has four usable
CLIP/OpenCLIP-family zero-shot baselines including DataComp XL, four usable
frozen-feature prototype baselines including self-supervised DINOv2, and one
SigLIP diagnostic failure. It still needs
non-CLIP/OpenCLIP pretrained VLM family diversity, uses five paired samples per
object/challenge group, and does not yet include a real transfer validation
result. The v0.2 real-transfer scaffold is ready, but actual transferred images
have not been collected yet.

The next step is to collect the v0.2 real transfer validation sample or add a
usable pretrained VLM family outside nearby CLIP/OpenCLIP variants before
scaling beyond five paired samples per group.
