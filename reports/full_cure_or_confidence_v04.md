# Full-CURE-OR v0.4 Confidence and Calibration

## Scope

This analysis uses the unchanged Full-CURE-OR v0.4 probe predictions for the
three usable zero-shot baselines:

- CLIP ViT-B/16;
- OpenCLIP ViT-B/32 LAION2B;
- CLIP ViT-B/32.

SigLIP Base P16 224 is excluded from the main confidence interpretation because
its v0.4 clean accuracy is 0.0120 under the current prompt protocol.

No images were read for this pass. The script reads local prediction CSV files
under `results/`.

## Metrics

For each model/challenge/level group, the analysis reports:

- accuracy;
- mean max-class confidence;
- accuracy drop versus clean;
- confidence drop versus clean;
- calibration gap: `mean_confidence - accuracy`;
- expected calibration error with 10 bins;
- top-1 Brier score: mean `(confidence - correct)^2`;
- high-confidence wrong rate: fraction of all rows with an incorrect
  prediction and confidence >= 0.5.

## Level-5 Summary

| Model | Level-5 accuracy | Level-5 confidence | Calibration gap | ECE | High-conf wrong rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP ViT-B/16 | 0.0994 | 0.2610 | 0.1616 | 0.1616 | 0.0439 |
| OpenCLIP ViT-B/32 LAION2B | 0.0890 | 0.4781 | 0.3891 | 0.3891 | 0.3141 |
| CLIP ViT-B/32 | 0.0741 | 0.2716 | 0.1974 | 0.1974 | 0.0700 |

The most important result is that confidence does not collapse at the same rate
as accuracy. OpenCLIP is the clearest case: at level 5, mean accuracy is 0.0890
while mean confidence is still 0.4781. That creates a calibration gap of 0.3891
and a high-confidence wrong rate of 0.3141.

## Worst Level-5 Overconfidence Cases

| Model | Challenge | Accuracy | Mean confidence | Calibration gap | High-conf wrong rate |
| --- | --- | ---: | ---: | ---: | ---: |
| CLIP ViT-B/16 | type 18, grayscale salt and pepper noise | 0.0100 | 0.2613 | 0.2513 | 0.0000 |
| CLIP ViT-B/32 | type 18, grayscale salt and pepper noise | 0.0100 | 0.4188 | 0.4088 | 0.2680 |
| OpenCLIP ViT-B/32 LAION2B | type 07, dirty lens 1 | 0.0480 | 0.5972 | 0.5492 | 0.6240 |

This gives the writeup a stronger claim than "accuracy drops under native
distortions." Some native distortions produce low-accuracy, high-confidence
failure modes, and the pattern differs by model.

## Clean Calibration Context

| Model | Clean accuracy | Clean confidence | Clean calibration gap | Clean ECE | Clean high-conf wrong rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| CLIP ViT-B/16 | 0.4440 | 0.5248 | 0.0808 | 0.0808 | 0.1340 |
| OpenCLIP ViT-B/32 LAION2B | 0.4120 | 0.6648 | 0.2528 | 0.2528 | 0.3320 |
| CLIP ViT-B/32 | 0.3500 | 0.4644 | 0.1144 | 0.1171 | 0.1220 |

OpenCLIP is already overconfident on clean Full-CURE-OR images, but the gap
widens under native challenge severity. This matters for any deployment framing:
the model does not merely fail more often; it can fail while preserving
substantial confidence.

## Artifacts

- `configs/full_cure_or_probe_confidence_v04.json`
- `scripts/analyze_full_cure_or_confidence.py`
- `scripts/plot_full_cure_or_confidence_by_level.py`
- `scripts/plot_full_cure_or_overconfidence.py`
- `results/full_cure_or_probe_v04_confidence_shift.csv`
- `results/full_cure_or_probe_v04_confidence_by_level.csv`
- `results/full_cure_or_probe_v04_overconfidence_ranking.csv`
- `results/full_cure_or_probe_v04_confidence_by_level.png`
- `results/full_cure_or_probe_v04_level5_overconfidence.png`

## Reproduction

```bash
.venv/bin/python scripts/analyze_full_cure_or_confidence.py \
  --config configs/full_cure_or_probe_confidence_v04.json

MPLCONFIGDIR=/private/tmp/cure_or_pp_mpl MPLBACKEND=Agg \
  .venv/bin/python scripts/plot_full_cure_or_confidence_by_level.py \
  --input results/full_cure_or_probe_v04_confidence_by_level.csv \
  --output results/full_cure_or_probe_v04_confidence_by_level.png

MPLCONFIGDIR=/private/tmp/cure_or_pp_mpl MPLBACKEND=Agg \
  .venv/bin/python scripts/plot_full_cure_or_overconfidence.py \
  --input results/full_cure_or_probe_v04_overconfidence_ranking.csv \
  --output results/full_cure_or_probe_v04_level5_overconfidence.png \
  --severity level_5 \
  --top-k 8
```

## Next Step

Add the same confidence/calibration tables to any new usable model family before
expanding the v0.4 row count. Otherwise, model additions will improve the
leaderboard but not the paper-level failure analysis.
