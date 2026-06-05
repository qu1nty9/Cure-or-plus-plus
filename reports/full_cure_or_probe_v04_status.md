# Full-CURE-OR Probe v0.4

## What Changed

Probe v0.4 is the first all-challenge extracted-folder Full-CURE-OR probe.
It uses all staged official folders under `/Volumes/980PRO/CURE-OR++/archives`,
while keeping the evaluation manifest scoped to object-recognition challenge
types rather than grayscale/no-challenge controls.

Sampling:

- clean rows: 500;
- native challenge rows: 38,999;
- labels: 100 official object-ID-aware labels;
- challenge types: 02-09 and 11-18;
- challenge levels: 1-5 where available;
- type 02 and type 11 levels: 1-4 only;
- selected acquisition-condition pattern: five spread samples per
  object/challenge/level.

The only underfilled cell is `native_challenge_type_12`, `level_1`,
`object_007_rival_clothing_iron`, where the strict paired-clean-source filter
found 4 usable samples instead of 5. All selected distorted rows have a paired
clean source path.

All external-disk reads were limited to
`/Volumes/980PRO/CURE-OR++/archives`. No files were written to the external
disk.

## Completed Results

The two core zero-shot baselines completed on the v0.4 manifest.

| Model | Predictions | Clean accuracy | Mean native accuracy | Mean level-4 accuracy | Mean level-5 accuracy | Worst level-5 challenge | Worst level-5 accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| CLIP ViT-B/16 | 39,499 | 0.4440 | 0.1929 | 0.1596 | 0.0994 | type 09, salt & pepper noise; tied with type 18 | 0.0100 |
| OpenCLIP ViT-B/32 LAION2B | 39,499 | 0.4120 | 0.1705 | 0.1400 | 0.0890 | type 18, grayscale salt & pepper noise | 0.0080 |

An expanded local-cache pass then added CLIP ViT-B/32 and SigLIP Base P16 224
on the same manifest. CLIP ViT-B/32 is a usable additional CLIP-family
baseline. SigLIP completed technically, but clean accuracy is only 0.0120, so
it is retained as a diagnostic protocol failure rather than a strong robustness
baseline.

| Model | Clean accuracy | Mean native accuracy | Mean level-4 accuracy | Mean level-5 accuracy | Worst level-5 challenge | Worst level-5 accuracy |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| CLIP ViT-B/16 | 0.4440 | 0.1929 | 0.1596 | 0.0994 | type 09, salt & pepper noise; tied with type 18 | 0.0100 |
| OpenCLIP ViT-B/32 LAION2B | 0.4120 | 0.1705 | 0.1400 | 0.0890 | type 18, grayscale salt & pepper noise | 0.0080 |
| CLIP ViT-B/32 | 0.3500 | 0.1532 | 0.1249 | 0.0741 | type 09, salt & pepper noise | 0.0060 |
| SigLIP Base P16 224 | 0.0120 | 0.0103 | 0.0096 | 0.0084 | type 03, underexposure | 0.0060 |

The level-5 mean is computed over 14 challenge types because resize
(`type_02`) and grayscale resize (`type_11`) do not provide level-5 rows in the
official CURE-OR mapping.

Weighted mean native accuracy by level:

| Model | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP ViT-B/16 | 0.2772 | 0.2245 | 0.1921 | 0.1596 | 0.0994 |
| OpenCLIP ViT-B/32 LAION2B | 0.2473 | 0.2000 | 0.1659 | 0.1400 | 0.0890 |

Level-5 native results:

| Challenge | CLIP ViT-B/16 | OpenCLIP ViT-B/32 LAION2B |
| --- | ---: | ---: |
| type 18, grayscale salt & pepper noise | 0.0100 | 0.0080 |
| type 09, salt & pepper noise | 0.0100 | 0.0140 |
| type 14, grayscale gaussian blur | 0.0140 | 0.0100 |
| type 05, gaussian blur | 0.0200 | 0.0140 |
| type 16, grayscale dirty lens 1 | 0.0240 | 0.0120 |
| type 17, grayscale dirty lens 2 | 0.0720 | 0.0540 |
| type 13, grayscale overexposure | 0.0740 | 0.0660 |
| type 07, dirty lens 1 | 0.0800 | 0.0480 |
| type 12, grayscale underexposure | 0.1320 | 0.1320 |
| type 15, grayscale contrast | 0.1520 | 0.1220 |
| type 04, overexposure | 0.1580 | 0.1460 |
| type 08, dirty lens 2 | 0.1880 | 0.1240 |
| type 03, underexposure | 0.1900 | 0.2240 |
| type 06, contrast | 0.2680 | 0.2720 |

## Interpretation

The v0.4 result is a material step beyond the six-folder probe. The collapse
pattern is still present after adding the remaining official challenge folders:
both models retain some signal on contrast/exposure challenges, but severe
blur, salt-and-pepper noise, dirty-lens variants, and grayscale combinations
push accuracy close to chance.

The ordering is model-dependent. CLIP ViT-B/16 is worst on salt-and-pepper noise
and ties with grayscale salt-and-pepper noise. OpenCLIP is worst on grayscale
salt-and-pepper noise, with grayscale gaussian blur and grayscale dirty lens 1
also near chance. This supports a stronger research claim than a single
"accuracy drops under corruption" result: native acquisition/channel failures
produce challenge-specific and model-specific robustness rankings.

This is still a probe, not the final arXiv-scale benchmark. The main remaining
gaps are more usable pretrained model families outside nearby CLIP/OpenCLIP
variants and a real transfer validation sample. The v0.4 block now has eight
usable baseline rows across four CLIP/OpenCLIP-family zero-shot models and four
frozen-feature prototype classifiers, plus one SigLIP diagnostic failure under
the current prompt protocol.

The confidence/calibration pass for the four usable CLIP/OpenCLIP-family
zero-shot baselines is now complete. DataComp XL improves mean level-5 accuracy
to 0.1451 but still retains 0.4997 mean confidence, with a 0.3545 calibration
gap and a 0.3240 high-confidence wrong rate. Its worst level-5 overconfidence
case is type 18, grayscale salt-and-pepper noise: 0.0100 accuracy with 0.7393
mean confidence. Details are in `reports/full_cure_or_confidence_v04.md`.

The type-10 grayscale no-challenge control is also complete for the four usable
CLIP/OpenCLIP-family zero-shot baselines. It uses 499 paired control rows and
shows that grayscale alone is damaging but cannot explain the native level-5
collapse. CLIP ViT-B/16 accuracy is 0.3166 on grayscale control versus 0.0994
on native level 5. DataComp XL accuracy is 0.3908 on grayscale control versus
0.1451 on native level 5. Details are in
`reports/full_cure_or_grayscale_control_v04.md`.

The non-CLIP prototype pass is also complete. It adds HGNetV2-B0,
MobileNetV3-Small, ConvNeXt-Tiny, and DINOv2 ViT-S/14 frozen-feature
nearest-centroid baselines with a leave-clean-condition-out protocol.
HGNetV2-B0 reaches 0.6240 clean accuracy and 0.1219 mean native level-5
accuracy. MobileNetV3-Small reaches 0.5560 clean accuracy and 0.0960 mean
native level-5 accuracy. ConvNeXt-Tiny reaches 0.6160 clean accuracy, 0.4910
grayscale-control accuracy, 0.3436 mean native accuracy, and 0.2239 mean native
level-5 accuracy. DINOv2 ViT-S/14 reaches 0.7520 clean accuracy, 0.7415
grayscale-control accuracy, 0.4393 mean native accuracy, and 0.2766 mean native
level-5 accuracy, making it the strongest current v0.4 baseline under the
native challenge metrics. The prototype models also show
model-family-dependent worst-case rankings: HGNetV2 and MobileNet collapse
first on gaussian blur ties, while ConvNeXt-Tiny and DINOv2 are worst on
grayscale salt-and-pepper noise. Details are in
`reports/full_cure_or_prototype_v04.md`.

The stronger OpenCLIP ViT-B/16 DataComp XL pass is now complete. It reaches
0.5460 clean accuracy, 0.2561 mean native accuracy, and 0.1451 mean native
level-5 accuracy, ranking third by mean native accuracy behind DINOv2 and
ConvNeXt-Tiny. Its worst level-5 challenge is type 09, salt-and-pepper noise,
at 0.0080, so the stronger pretrained variant improves the baseline set but
does not remove the severe level-5 collapse.

The challenge-family/channel-effect pass is also complete for the same eight
usable v0.4 baselines. It shows that every model has lower mean level-5 accuracy
on paired grayscale native challenges than on the corresponding color native
challenges. DINOv2 remains strongest in absolute accuracy, but still drops from
0.3071 color level-5 mean accuracy to 0.2460 grayscale level-5 mean accuracy.
Details are in `reports/full_cure_or_challenge_family_v04.md`.

The consensus failure pass is complete as well. The top four level-5 challenges
by mean damaging rank are grayscale salt-and-pepper noise, salt-and-pepper
noise, grayscale gaussian blur, and gaussian blur; all eight usable baselines
are at the floor threshold on the top three, and gaussian blur is near-floor for
all eight. Pairwise level-5 rank correlations range from 0.892 to 0.988, so the
hard-challenge ordering is broadly stable while still leaving room for
model-family differences. Details are in
`reports/full_cure_or_consensus_v04.md`.

## Artifacts

- `data/interim/full_cure_or_clean_probe_v04_manifest.csv`
- `data/interim/full_cure_or_native_probe_v04_manifest.csv`
- `configs/openclip_vit_b32_laion2b_full_cure_or_probe_v04.json`
- `configs/clip_vit_b16_full_cure_or_probe_v04.json`
- `configs/clip_vit_b32_full_cure_or_probe_v04.json`
- `configs/siglip_base_p16_224_full_cure_or_probe_v04.json`
- `configs/full_cure_or_probe_summaries_v04.json`
- `configs/full_cure_or_probe_summaries_v04_expanded.json`
- `results/openclip_vit_b32_laion2b_full_cure_or_probe_v04_predictions.csv`
- `results/openclip_vit_b32_laion2b_full_cure_or_probe_v04_summary.csv`
- `results/clip_vit_b16_full_cure_or_probe_v04_predictions.csv`
- `results/clip_vit_b16_full_cure_or_probe_v04_summary.csv`
- `results/clip_vit_b32_full_cure_or_probe_v04_predictions.csv`
- `results/clip_vit_b32_full_cure_or_probe_v04_summary.csv`
- `results/siglip_base_p16_224_full_cure_or_probe_v04_predictions.csv`
- `results/siglip_base_p16_224_full_cure_or_probe_v04_summary.csv`
- `results/full_cure_or_probe_v04_comparison.csv`
- `results/full_cure_or_probe_v04_level5_ranking.csv`
- `results/full_cure_or_probe_v04_level5_ranking.png`
- `results/full_cure_or_probe_v04_severity_curves.png`
- `results/full_cure_or_probe_v04_mean_accuracy_by_level.png`
- `results/full_cure_or_probe_v04_expanded_comparison.csv`
- `results/full_cure_or_probe_v04_expanded_level5_ranking.csv`
- `results/full_cure_or_probe_v04_expanded_level5_ranking.png`
- `results/full_cure_or_probe_v04_expanded_mean_accuracy_by_level.png`
- `reports/full_cure_or_probe_v04_expanded_models.md`
- `configs/full_cure_or_probe_confidence_v04.json`
- `results/full_cure_or_probe_v04_confidence_shift.csv`
- `results/full_cure_or_probe_v04_confidence_by_level.csv`
- `results/full_cure_or_probe_v04_overconfidence_ranking.csv`
- `results/full_cure_or_probe_v04_confidence_by_level.png`
- `results/full_cure_or_probe_v04_level5_overconfidence.png`
- `reports/full_cure_or_confidence_v04.md`
- `data/interim/full_cure_or_grayscale_control_v04_manifest.csv`
- `results/full_cure_or_grayscale_control_v04_comparison.csv`
- `results/full_cure_or_grayscale_control_v04_comparison.png`
- `reports/full_cure_or_grayscale_control_v04.md`
- `configs/hgnetv2_b0_full_cure_or_prototype_v04.json`
- `configs/mobilenet_v3_small_full_cure_or_prototype_v04.json`
- `configs/convnext_tiny_fb_in1k_full_cure_or_prototype_v04.json`
- `configs/dinov2_vit_small_patch14_full_cure_or_prototype_v04.json`
- `configs/openclip_vit_b16_datacomp_xl_full_cure_or_probe_v04.json`
- `configs/full_cure_or_probe_summaries_v04_with_prototypes.json`
- `configs/full_cure_or_grayscale_control_summaries_v04_with_prototypes.json`
- `results/hgnetv2_b0_full_cure_or_prototype_v04_predictions.csv`
- `results/hgnetv2_b0_full_cure_or_prototype_v04_summary.csv`
- `results/mobilenet_v3_small_full_cure_or_prototype_v04_predictions.csv`
- `results/mobilenet_v3_small_full_cure_or_prototype_v04_summary.csv`
- `results/convnext_tiny_fb_in1k_full_cure_or_prototype_v04_predictions.csv`
- `results/convnext_tiny_fb_in1k_full_cure_or_prototype_v04_summary.csv`
- `results/dinov2_vit_small_patch14_full_cure_or_prototype_v04_predictions.csv`
- `results/dinov2_vit_small_patch14_full_cure_or_prototype_v04_summary.csv`
- `results/openclip_vit_b16_datacomp_xl_full_cure_or_probe_v04_summary.csv`
- `results/full_cure_or_probe_v04_with_prototypes_comparison.csv`
- `results/full_cure_or_probe_v04_with_prototypes_level5_ranking.csv`
- `results/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png`
- `results/full_cure_or_probe_v04_with_prototypes_level5_ranking.png`
- `results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.csv`
- `results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.png`
- `reports/full_cure_or_prototype_v04.md`
- `scripts/analyze_full_cure_or_challenge_families.py`
- `results/full_cure_or_probe_v04_with_prototypes_channel_effects.csv`
- `results/full_cure_or_probe_v04_with_prototypes_paired_channel_gaps.csv`
- `reports/full_cure_or_challenge_family_v04.md`
- `scripts/analyze_full_cure_or_consensus.py`
- `results/full_cure_or_probe_v04_with_prototypes_level5_consensus.csv`
- `results/full_cure_or_probe_v04_with_prototypes_level5_rank_correlations.csv`
- `reports/full_cure_or_consensus_v04.md`

## Next Step

The next research step should be the v0.2 real transfer validation block or
another strong pretrained model family on the same v0.4 manifest before
expanding row count. Candidate directions:

1. add at least one non-CLIP/OpenCLIP VLM family with usable clean accuracy;
2. extend confidence-collapse and calibration tables to any further usable
   zero-shot/VLM model;
3. collect the 180-output v0.2 real transfer validation sample and compare its
   ranking against native CURE-OR severity rankings.
