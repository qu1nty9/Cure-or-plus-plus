# Serious-Level Plan Before Public Release

The current v0.1 artifact is Kaggle-ready, but not yet strong enough to be the
main public version. To make the project feel serious, the next release should
prove that CURE-OR++ is not just another corruption demo.

## Current Evidence

CLIP ViT-B/32 on the full mini-CURE-OR clean subset:

- clean accuracy: 0.8280;
- strongest high-severity degradation: `low_light_upload`;
- `low_light_upload` accuracy: 0.6560;
- drop vs clean: 0.1720.

High-severity damage ranking:

1. `low_light_upload`
2. `blur_classic`
3. `video_call_frame`
4. `restoration_artifact`
5. `resize_roundtrip`
6. `dirty_lens_recompress`
7. `jpeg_classic`
8. `screenshot_chain`
9. `messenger_chain`

Test-split comparison now includes six evaluated baselines:

- CLIP ViT-B/16 zero-shot:
  - clean test accuracy: 0.9000;
  - worst high-severity recipe: `low_light_upload`;
  - worst high-severity accuracy: 0.7800.
- CLIP ViT-B/32 zero-shot:
  - clean test accuracy: 0.7900;
  - worst high-severity recipe: `low_light_upload`;
  - worst high-severity accuracy: 0.6400.
- OpenCLIP ViT-B/32 LAION2B zero-shot:
  - clean test accuracy: 0.8500;
  - worst high-severity recipe: `low_light_upload`;
  - worst high-severity accuracy: 0.6300;
  - role: usable non-OpenAI contrastive baseline.
- SigLIP Base P16 224 zero-shot diagnostic:
  - clean test accuracy: 0.1900;
  - worst high-severity recipe: `video_call_frame`;
  - worst high-severity accuracy: 0.1500;
  - caveat: clean accuracy is too low for strong robustness claims.
- HGNetV2-B0 prototype:
  - clean test accuracy: 0.8400;
  - worst high-severity recipe: `low_light_upload`;
  - worst high-severity accuracy: 0.6400.
- MobileNetV3-Small prototype:
  - clean test accuracy: 0.5600;
  - worst high-severity recipe: `video_call_frame`;
  - worst high-severity accuracy: 0.4600.

## Why This Still Needs One More Pass

Six evaluated baselines, including two zero-shot CLIP variants, a usable
OpenCLIP contrastive baseline, one SigLIP diagnostic run, and two clean-train
prototype classifiers, are enough for a first serious comparison. The remaining
gap is no longer model count. It is external validity, scale, and positioning.

The most important missing pieces:

- per-class failure analysis in the notebook narrative;
- clearer positioning against existing VLM robustness benchmarks, tracked in
  `docs/related_work_v01.md`;
- at least one real transfer pipeline, not only simulated transfer chains;
- a controlled path from the local native mini-CURE-OR grid to Full-CURE-OR,
  now started with the first extracted-folder Full-CURE-OR probe.

## External Benchmark Context

Recent related work already covers a lot of the generic robustness space:

- R-Bench studies real-world robustness of large multimodal models across a
  capture-to-reception corruption sequence.
- MLLM-IC evaluates multimodal large language models under image corruptions.
- VLM-RobustBench evaluates VLMs across many perturbation settings and reports
  that severity is not always predictive of difficulty.

Our strongest differentiator should therefore be narrow:

> CURE-OR++ focuses on small, reproducible, object-centric digital transfer
> chains and makes ranking shifts easy to inspect across models, object classes,
> and distortion recipes.

## Release Gate For v0.2

Do not publish the main Kaggle version until these are done:

- 6 evaluated models, completed:
  - CLIP ViT-B/16;
  - CLIP ViT-B/32;
  - OpenCLIP ViT-B/32 LAION2B;
  - SigLIP Base P16 224 diagnostic;
  - HGNetV2-B0 prototype;
  - MobileNetV3-Small prototype.
- 1 non-OpenAI VLM or contrastive baseline with usable clean accuracy,
  completed:
  - OpenCLIP ViT-B/32 LAION2B.
- 1 cross-model ranking table, completed.
- 1 per-class failure table, completed.
- 1 combined high-severity figure, completed.
- 1 short related-work section in the notebook, completed and validated.
- 1 limitations section that admits simulated transfer chains.
- Expanded local native mini-CURE-OR test grid, completed outside the first
  Kaggle package:
  - 6,400 native challenge images;
  - 16 available challenge types;
  - CLIP ViT-B/16 and OpenCLIP ViT-B/32 LAION2B results;
  - official challenge mapping pinned;
  - official Full-CURE-OR 100-object label mapping pinned;
  - Full-CURE-OR ingestion checklist and mini probe completed;
  - worst level-4 accuracy: 0.1000 for both models on type 14, grayscale
    gaussian blur.
- First extracted-folder Full-CURE-OR probe v0.1, completed:
  - 312,500 staged images across six official challenge folders;
  - 100 clean probe images;
  - 2,000 native challenge probe images;
  - CLIP ViT-B/16 clean accuracy: 0.3900;
  - OpenCLIP ViT-B/32 LAION2B clean accuracy: 0.3100;
  - mean level-4 native accuracy: 0.0780 for CLIP and 0.0620 for OpenCLIP;
  - worst level-4 accuracy: 0.0000 for CLIP and 0.0100 for OpenCLIP.
- Expanded extracted-folder Full-CURE-OR probe v0.2, completed:
  - 500 clean probe images;
  - 10,000 native challenge probe images;
  - 5 paired acquisition-condition samples per object/challenge/level;
  - CLIP ViT-B/16 clean accuracy: 0.4440;
  - OpenCLIP ViT-B/32 LAION2B clean accuracy: 0.4120;
  - mean level-4 native accuracy: 0.1012 for CLIP and 0.0932 for OpenCLIP;
  - worst level-4 challenge: type 14, grayscale gaussian blur.
- Level-5 six-folder Full-CURE-OR probe v0.3, completed:
  - 500 clean probe images;
  - 12,000 native challenge probe images;
  - official level-5 rows for challenge types 05, 09, 14, and 18;
  - mean level-5 native accuracy: 0.0135 for CLIP and 0.0115 for OpenCLIP.
- All-challenge Full-CURE-OR probe v0.4, completed:
  - all 18 official extracted folders staged locally;
  - 500 clean probe images;
  - 38,999 native challenge probe images;
  - challenge types 02-09 and 11-18;
  - CLIP ViT-B/16 clean accuracy: 0.4440;
  - OpenCLIP ViT-B/32 LAION2B clean accuracy: 0.4120;
  - CLIP ViT-B/32 clean accuracy: 0.3500;
  - SigLIP Base P16 224 clean accuracy: 0.0120, diagnostic failure under the
    current prompt protocol;
  - mean native accuracy: 0.1929 for CLIP and 0.1705 for OpenCLIP;
  - mean level-5 native accuracy: 0.0994 for CLIP and 0.0890 for OpenCLIP;
  - worst level-5 accuracy: 0.0100 for CLIP and 0.0080 for OpenCLIP.
- Expanded v0.4 model pass, completed:
  - CLIP ViT-B/32 mean native accuracy: 0.1532;
  - CLIP ViT-B/32 mean level-5 native accuracy: 0.0741;
  - SigLIP Base P16 224 mean native accuracy: 0.0103;
  - conclusion: there are three usable zero-shot CLIP-family baselines and one
    documented SigLIP protocol mismatch before adding the DataComp XL and
    non-CLIP prototype blocks.
- Full-CURE-OR v0.4 confidence/calibration pass, completed:
  - usable models: CLIP ViT-B/16, OpenCLIP ViT-B/32 LAION2B,
    OpenCLIP ViT-B/16 DataComp XL, CLIP ViT-B/32;
  - OpenCLIP level-5 accuracy: 0.0890;
  - OpenCLIP level-5 mean confidence: 0.4781;
  - OpenCLIP level-5 calibration gap: 0.3891;
  - DataComp XL level-5 accuracy: 0.1451;
  - DataComp XL level-5 mean confidence: 0.4997;
  - DataComp XL level-5 calibration gap: 0.3545;
  - strongest DataComp XL level-5 overconfidence case: type 18, grayscale
    salt-and-pepper noise, with 0.0100 accuracy and 0.7393 mean confidence;
  - strongest OpenCLIP level-5 overconfidence case: type 07, dirty lens 1,
    with 0.0480 accuracy and 0.5972 mean confidence.
- Full-CURE-OR v0.4 type-10 grayscale control, completed:
  - paired grayscale control rows: 499;
  - CLIP ViT-B/16 grayscale control accuracy: 0.3166;
  - OpenCLIP grayscale control accuracy: 0.2465;
  - DataComp XL grayscale control accuracy: 0.3908;
  - CLIP ViT-B/32 grayscale control accuracy: 0.2244;
  - conclusion: grayscale alone is damaging but does not explain native
    level-5 collapse.
- Full-CURE-OR v0.4 non-CLIP prototype pass, completed:
  - HGNetV2-B0 Prototype clean accuracy: 0.6240;
  - HGNetV2-B0 Prototype mean native accuracy: 0.2547;
  - HGNetV2-B0 Prototype mean level-5 native accuracy: 0.1219;
  - MobileNetV3-Small Prototype clean accuracy: 0.5560;
  - MobileNetV3-Small Prototype mean native accuracy: 0.1936;
  - MobileNetV3-Small Prototype mean level-5 native accuracy: 0.0960;
  - ConvNeXt-Tiny Prototype clean accuracy: 0.6160;
  - ConvNeXt-Tiny Prototype mean native accuracy: 0.3436;
  - ConvNeXt-Tiny Prototype mean level-5 native accuracy: 0.2239;
  - DINOv2 ViT-S/14 Prototype clean accuracy: 0.7520;
  - DINOv2 ViT-S/14 Prototype mean native accuracy: 0.4393;
  - DINOv2 ViT-S/14 Prototype mean level-5 native accuracy: 0.2766;
  - conclusion: prototype classifiers add useful model-family diversity.
    HGNetV2-B0 and MobileNetV3-Small change the level-5 worst-case ranking to
    type 05, gaussian blur ties, while ConvNeXt-Tiny and DINOv2 become much
    stronger native-severity baselines but still collapse near chance on type
    18, grayscale salt-and-pepper noise.
- Full-CURE-OR v0.4 challenge-family/channel-effect pass, completed:
  - eight usable baselines analyzed;
  - every usable model has lower level-5 mean accuracy on paired grayscale
    native challenges than on corresponding color native challenges;
  - DINOv2 ViT-S/14 color level-5 mean accuracy: 0.3071;
  - DINOv2 ViT-S/14 grayscale level-5 mean accuracy: 0.2460;
  - OpenCLIP ViT-B/16 DataComp XL color level-5 mean accuracy: 0.1791;
  - OpenCLIP ViT-B/16 DataComp XL grayscale level-5 mean accuracy: 0.1111;
  - ConvNeXt-Tiny has the largest level-5 grayscale penalty, from 0.2743 color
    mean accuracy to 0.1734 grayscale mean accuracy;
  - conclusion: grayscale/channel removal acts as an interaction term, while
    blur/noise floor effects can hide paired gaps because both variants are
    already near chance.
- Full-CURE-OR v0.4 consensus failure pass, completed:
  - eight usable baselines analyzed;
  - top four consensus level-5 failures: grayscale salt-and-pepper noise,
    salt-and-pepper noise, grayscale gaussian blur, and gaussian blur;
  - all eight usable baselines are at the floor threshold on the top three;
  - gaussian blur is near-floor for all eight, with seven of eight at the floor
    threshold;
  - pairwise level-5 rank correlations range from 0.892 to 0.988;
  - conclusion: the hardest level-5 failure ordering has a stable consensus
    core, with secondary model-family differences.
- Full-CURE-OR v0.4 paper-table pack, completed:
  - leaderboard, consensus failure, and grayscale-control guardrail tables
    generated from tracked aggregate CSVs;
  - Markdown report: `reports/full_cure_or_paper_tables_v04.md`;
  - LaTeX snippets: `reports/full_cure_or_paper_tables_v04.tex`;
  - strongest current level-5 row: DINOv2 ViT-S/14 Prototype at 0.2766;
  - top consensus failure: grayscale salt-and-pepper noise, mean accuracy
    0.0092 with all eight usable baselines at the floor threshold.
- OpenCLIP ViT-B/16 DataComp XL stronger-baseline pass, completed:
  - config exists at
    `configs/openclip_vit_b16_datacomp_xl_full_cure_or_probe_v04.json`;
  - direct checkpoint download completed after Hugging Face CLI download stalled;
  - clean accuracy: 0.5460;
  - mean native accuracy: 0.2561;
  - mean level-5 native accuracy: 0.1451;
  - conclusion: DataComp XL improves on smaller CLIP/OpenCLIP zero-shot rows
    and is third by mean native accuracy, but still collapses near chance on
    salt-and-pepper and grayscale salt-and-pepper noise.
- Real-transfer validation v0.2 scaffold, prepared but not evaluated:
  - 30 clean mini-CURE-OR test source images pinned in
    `data/real_transfer/v02/source_selection_v02.csv`;
  - 3 real transfer pipelines and 2 repeats per source/pipeline;
  - 180 planned real transferred outputs in
    `data/real_transfer/v02/pairs_template.csv`;
  - preflight validator checks row count, label coverage, recipe coverage, and
    repeat coverage;
  - CLIP ViT-B/16, CLIP ViT-B/32, OpenCLIP ViT-B/32 LAION2B, and DataComp XL
    evaluation configs prepared;
  - remaining blocker: real transferred outputs and filled
    `data/real_transfer/v02/pairs.csv`.

## Stretch Gate For arXiv/Workshop

For arXiv or workshop seriousness, add:

- real app transfer validation:
  - actual messenger recompression samples;
  - actual screenshot/resave chain;
  - actual video-call frame capture or screen recording compression;
- at least 5 usable model families or pretrained variants on the v0.4
  Full-CURE-OR probe, satisfied by eight usable baseline rows but still weak on
  pretrained family diversity because four rows are CLIP/OpenCLIP-family zero-shot
  models and four rows are frozen-feature prototype classifiers;
- confidence calibration or confidence-collapse analysis on the v0.4 probe,
  completed for the current four usable CLIP/OpenCLIP-family zero-shot
  baselines and still required for new models;
- release scripts that regenerate all distortions deterministically;
- model cards and dataset card;
- related-work table with exact benchmark differences.
- challenge-family/channel-effect analysis, completed for current eight usable
  v0.4 baselines.
- consensus failure/rank-stability analysis, completed for current eight usable
  v0.4 baselines.
- paper-ready benchmark table pack, completed for current eight usable v0.4
  baselines.

## Immediate Next Steps

1. Collect the v0.2 real app-transfer validation sample using
   `docs/real_transfer_validation_protocol_v02.md`.
2. Run `scripts/activate_real_transfer_protocol.py --require-ready` to create
   `data/real_transfer/v02/pairs.csv`, validate file completeness, build
   `data/real_transfer/v02/manifest.csv`, and then evaluate it with the four
   prepared zero-shot configs.
3. Add another strong pretrained model family on the v0.4 Full-CURE-OR
   manifest, preferably a non-CLIP/OpenCLIP VLM family rather than another
   nearby CLIP variant or nearest-centroid prototype.
4. Add confidence-collapse and calibration tables for each further usable
   zero-shot/VLM Full-CURE-OR model.
5. Add type 10, grayscale no-challenge, as a separate control condition,
   completed for the current four CLIP/OpenCLIP-family zero-shot baselines.
