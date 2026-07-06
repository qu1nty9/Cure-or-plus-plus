# Draft GitHub Release Notes: v0.4-preprint

Tag: `v0.4-preprint`

Status: draft release notes, not yet tagged.

## Summary

This preprint release packages the current CURE-OR++ benchmark state for public
inspection. It includes a Full-CURE-OR v0.4 controlled probe, real-transfer v0.2
validation, open-weight VLM prompt-pack runs, hosted-provider VLM comparisons,
paper source, generated paper tables, figures, dataset/evaluation cards, and
release-boundary documentation.

## Highlights

- Full-CURE-OR v0.4 controlled probe over 500 clean rows and 38,999 native
  challenge rows.
- Eight usable baseline rows across CLIP/OpenCLIP and prototype model families.
- Consensus level-5 failure analysis showing stable severe-challenge floor
  failures.
- Confidence/calibration analysis for usable CLIP/OpenCLIP-family zero-shot
  rows.
- Real-transfer v0.2 validation over WhatsApp upload/download, screenshot/resave,
  and FaceTime frame-capture pipelines.
- Open-weight VLM v0.3 900-row prompt-pack comparison across seven completed
  rows.
- Hosted-provider VLM rows across OpenAI, xAI, Anthropic, and GigaChat on the
  210-row provider prompt pack.
- xAI Grok 4.3 hosted-provider v0.3 900-row run and repeatability check.
- Tectonic-verified PDF build with clean final LaTeX log.

## Included Public Artifacts

- Source code under `scripts/`, configs, and public notebooks.
- Aggregate reports and paper-ready tables under `reports/`.
- Figures under `results/`.
- Paper source under `paper/`.
- Dataset, evaluation, reproducibility, and release documentation under `docs/`.
- Prompt-pack metadata JSONL files.
- Sanitized parsed-response audits and aggregate summaries.

## Not Included

- Raw CURE-OR or mini-CURE-OR images.
- Local real-transfer photos or collection packs.
- Source dataset archives.
- API keys, provider tokens, OAuth material, `.env` files, or secrets.
- Hosted-provider raw JSONL response dumps.
- Provider API caches.
- External-disk build/cache directories.

## Verification

Current preflight status:

```text
scripts/run_release_checks.py: 623 checks, 0 failures
scripts/check_paper_build.py: paper inputs, figures, and bibliography present
Tectonic PDF build: successful
Final Tectonic log: no LaTeX errors, no undefined citations, no overfull boxes
```

Current locally verified PDF:

```text
/Volumes/980PRO/CURE-OR++/builds/paper_tectonic/main.pdf
```

The PDF path is local-only. A release PDF can be attached manually after final
review if desired.

## Recommended Citation

```bibtex
@misc{kholmirzayev2026cureorpp,
  title = {CURE-OR++: Object Recognition Robustness Under Native CURE-OR Challenges and Digital Transfer Pipelines},
  author = {Kholmirzayev, Yaroslav},
  year = {2026},
  note = {Preprint release v0.4-preprint}
}
```

## Next Steps

- Build a staged arXiv/workshop source package.
- Perform final source-package review.
- Publish the GitHub release/tag after final approval.
- Prepare a Kaggle notebook/writeup from the stable aggregate package.
