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
    documented SigLIP protocol mismatch, not yet five usable model families.
- Full-CURE-OR v0.4 confidence/calibration pass, completed:
  - usable models: CLIP ViT-B/16, OpenCLIP ViT-B/32 LAION2B, CLIP ViT-B/32;
  - OpenCLIP level-5 accuracy: 0.0890;
  - OpenCLIP level-5 mean confidence: 0.4781;
  - OpenCLIP level-5 calibration gap: 0.3891;
  - strongest OpenCLIP level-5 overconfidence case: type 07, dirty lens 1,
    with 0.0480 accuracy and 0.5972 mean confidence.
- Full-CURE-OR v0.4 type-10 grayscale control, completed:
  - paired grayscale control rows: 499;
  - CLIP ViT-B/16 grayscale control accuracy: 0.3166;
  - OpenCLIP grayscale control accuracy: 0.2465;
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
  - conclusion: prototype classifiers add useful model-family diversity and
    change the level-5 worst-case ranking to type 05, gaussian blur, but they
    do not replace the need for stronger pretrained VLM baselines.

## Stretch Gate For arXiv/Workshop

For arXiv or workshop seriousness, add:

- real app transfer validation:
  - actual messenger recompression samples;
  - actual screenshot/resave chain;
  - actual video-call frame capture or screen recording compression;
- at least 5 usable model families or pretrained variants on the v0.4
  Full-CURE-OR probe, partially satisfied by three zero-shot CLIP-family
  baselines plus two frozen-feature prototype baselines;
- confidence calibration or confidence-collapse analysis on the v0.4 probe,
  completed for current usable zero-shot baselines and still required for new
  models;
- release scripts that regenerate all distortions deterministically;
- model cards and dataset card;
- related-work table with exact benchmark differences.

## Immediate Next Steps

1. Collect one small real app-transfer validation sample using
   `docs/real_transfer_validation_protocol.md`.
2. Evaluate the real-transfer manifest with CLIP ViT-B/16 and OpenCLIP.
3. Add at least one stronger pretrained model family or variant on the v0.4
   Full-CURE-OR manifest.
4. Add confidence-collapse and calibration tables for each new usable
   zero-shot/VLM Full-CURE-OR model.
5. Add type 10, grayscale no-challenge, as a separate control condition,
   completed for current usable zero-shot baselines.
