# Full-CURE-OR Transition Plan

## Current Status

The project is no longer only a CURE-OR++ simulated-transfer benchmark. We now
have both a small native mini-CURE-OR pilot and an expanded native test-grid
evaluation that use original challenge images from the local mini-CURE-OR
files.

Local scope:

- 16,500 local mini-CURE-OR metadata rows;
- 250 clean rows;
- 16,250 native challenge rows;
- 132 split/type/level scope rows in `reports/mini_cure_or_scope_v01.csv`.
- official challenge type mapping in `docs/native_challenge_mapping_v01.md`.
- official 100-object label mapping in `configs/cure_or_objects_v01.json`.
- mini-CURE-OR probe summary in `reports/mini_cure_or_probe_v01.json`.
- Full-CURE-OR ingestion checklist in
  `docs/full_cure_or_ingestion_checklist.md`.
- all 18 official Full-CURE-OR folders staged under
  `/Volumes/980PRO/CURE-OR++/archives`;
- all-challenge Full-CURE-OR v0.4 probe summary in
  `reports/full_cure_or_probe_v04_status.md`.

Expanded native test-grid scope:

- test split only;
- 100 clean images;
- challenge types 2-9 and 11-18;
- challenge levels 1 through 4;
- 6,400 native challenge images;
- 64 challenge type/level cells, with 100 images per cell.

## Expanded Native Test Result

| Model | Clean accuracy | Mean level-4 accuracy | Worst level-4 native challenge | Worst accuracy | Drop vs clean |
| --- | ---: | ---: | --- | ---: | ---: |
| CLIP ViT-B/16 | 0.9000 | 0.5163 | type 14, grayscale gaussian blur | 0.1000 | 0.8000 |
| OpenCLIP ViT-B/32 LAION2B | 0.8500 | 0.4325 | type 14, grayscale gaussian blur | 0.1000 | 0.7500 |

Interpretation:

- resize stays close to clean accuracy;
- gaussian blur, salt and pepper noise, grayscale gaussian blur, grayscale dirty
  lens 1, and grayscale salt and pepper noise are consistently damaging at
  level 4;
- grayscale gaussian blur collapses both models at level 4;
- OpenCLIP reaches 0.1000 accuracy on both grayscale gaussian blur and
  grayscale salt and pepper noise at level 4, while retaining high mean
  confidence on grayscale salt and pepper noise.

## Next Step Toward Full-CURE-OR

Completed:

- native manifest builder for local mini-CURE-OR challenge images;
- official challenge type mapping;
- official Full-CURE-OR object label mapping;
- 3-type smoke pilot;
- all available local native challenge types on the test split;
- CLIP ViT-B/16 and OpenCLIP ViT-B/32 LAION2B native test-grid results;
- comparison CSV and level-4 ranking figure.
- reusable CURE-OR dataset probe script;
- Full-CURE-OR ingestion checklist.
- Full-CURE-OR zero-shot probe configs with 100 object-ID-aware labels.
- all 18 official extracted folders staged outside git;
- all-challenge v0.4 probe across challenge types 02-09 and 11-18;
- CLIP ViT-B/16 and OpenCLIP ViT-B/32 LAION2B v0.4 results.
- expanded v0.4 pass with CLIP ViT-B/32 and SigLIP diagnostic;
- confidence-collapse and calibration analysis for the current usable v0.4
  zero-shot baselines.
- type-10 grayscale no-challenge control for the current usable v0.4 zero-shot
  baselines.

Next:

1. Add at least two more usable model families or stronger pretrained variants
   on the v0.4 manifest.
2. Extend confidence-collapse and calibration analysis to each new usable
   model.
3. Integrate the evaluated v0.2 real transfer validation block into the final
   report/paper narrative.

## Why The Staged Probe Still Matters

The local mini-CURE-OR grid is 16,500 images and 6.4 GB raw, while the full
original CURE-OR release is much larger. The staged probe reduces risk:

- same evaluator interface;
- same zero-shot prompts;
- measurable runtime on local CPU;
- clear evidence that native CURE-OR stresses models differently from
  CURE-OR++ transfer chains.
- a reusable preflight probe that can catch layout and missing-file problems
  before evaluation.
