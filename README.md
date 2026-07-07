# CURE-OR++

CURE-OR++ is a compact benchmark package for auditing object-recognition
robustness under native CURE-OR challenge conditions and real app/device
transfer pipelines.

The current public release is:

- GitHub release: <https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1>
- Preprint PDF asset: `cure-or-pp-v0.4.1.pdf`
- Staged paper source asset: `arxiv_source_v0.4.1.zip`
- Release tag: `v0.4.1`

## What This Measures

CURE-OR++ asks a narrow question:

> Do object-recognition models share stable failure patterns when clean object
> images move into severe native challenge conditions and app/device transfer
> pipelines?

The project combines three evaluation views:

- Full-CURE-OR v0.4 controlled native-challenge probe.
- Real-transfer v0.2 validation over WhatsApp upload/download,
  phone screenshot/resave, and FaceTime frame-capture pipelines.
- VLM prompt-pack evaluation for open-weight and hosted assistant-style object
  recognition models.

## Current Evidence Package

The `v0.4.1` release includes:

- 500 clean Full-CURE-OR probe rows.
- 38,999 native CURE-OR challenge rows.
- Eight usable CLIP/OpenCLIP/prototype baseline rows.
- Real-transfer v0.2 block with 30 sources, three pipelines, two repeats, and
  180 transferred outputs.
- Seven completed open-weight VLM rows on the 900-row v0.3 prompt pack.
- Nine hosted-provider VLM rows on the 210-row provider prompt pack across
  OpenAI, xAI, Anthropic, and GigaChat.
- One 900-row xAI Grok 4.3 hosted-provider v0.3 row and repeat run.
- Paper source, generated paper tables, figures, dataset/evaluation cards,
  release notes, and reproducibility documentation.

## Key Findings

- Severe native CURE-OR challenges expose a stable failure core across model
  families.
- All eight usable baselines hit the floor on grayscale salt-and-pepper noise,
  salt-and-pepper noise, and grayscale gaussian blur at level 5.
- Stronger features improve aggregate robustness but do not remove severe
  collapse.
- CLIP/OpenCLIP-family rows can remain overconfident under severe native
  failures.
- Real-transfer v0.2 produces moderate, model-dependent source-matched drops;
  video-call frame capture is the largest drop in the current block.
- The VLM track separates recognition accuracy from generation stability; for
  example, Qwen2.5-VL-3B exposes many unparseable transferred-image outputs.

## Repository Map

- `paper/` - LaTeX paper source.
- `reports/` - aggregate reports, paper tables, VLM summaries, and audits.
- `results/` - generated figures and public summary artifacts.
- `docs/` - dataset card, evaluation card, reproducibility, release, and
  publication notes.
- `configs/` - benchmark and VLM matrix configs.
- `scripts/` - evaluation, integration, reporting, release-check, and source
  package builders.

## Reproducibility Route

Run the release checks:

```bash
.venv/bin/python scripts/run_release_checks.py
```

Validate paper inputs:

```bash
.venv/bin/python scripts/check_paper_build.py
```

Build a staged arXiv/workshop source package:

```bash
.venv/bin/python scripts/build_arxiv_source_package.py \
  --output-dir /private/tmp/cure-or-pp-arxiv-source-test \
  --clean \
  --make-zip
```

The current release baseline is:

```text
scripts/run_release_checks.py: 632 checks, 0 failures
```

For the full release boundary and caveats, see:

- `docs/reproducibility_manifest_v01.md`
- `docs/public_release_checklist_v01.md`
- `docs/arxiv_source_package_checklist_v01.md`

## Public Data Boundary

This repository is an auditable benchmark package, not a raw-image
redistribution.

Public:

- project-authored code and configs;
- aggregate reports and paper-ready tables;
- generated figures;
- paper source and staged source-package builder;
- prompt-pack metadata;
- sanitized parsed-response audits and aggregate summaries.

Not public:

- raw CURE-OR or mini-CURE-OR images;
- local real-transfer image payloads;
- source dataset archives;
- API keys, provider tokens, OAuth files, or `.env` files;
- hosted-provider raw JSONL response dumps;
- provider API caches.

Users should obtain upstream CURE-OR data from the upstream source under its
own terms.

## Citation

For now, cite the stable GitHub archival metadata release:

```bibtex
@misc{kholmirzayev2026cureorpp,
  title = {CURE-OR++: Object Recognition Robustness Under Native CURE-OR Challenges and Digital Transfer Pipelines},
  author = {Kholmirzayev, Yaroslav},
  year = {2026},
  note = {Archival metadata release v0.4.1; scientific preprint baseline v0.4-preprint},
  url = {https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1}
}
```

The machine-readable citation metadata is in `CITATION.cff`, and archival
metadata for Zenodo is in `.zenodo.json`. When Zenodo or another archive mints
a DOI, update `CITATION.cff`, `.zenodo.json`, this README, the paper, and the
Kaggle writeup.

## Publication Status

`v0.4.1` is a public archival metadata release for the `v0.4-preprint`
scientific baseline. The next publication steps are:

1. Wait for the archive service to mint a DOI.
2. Publish a Kaggle notebook/writeup from the stable aggregate package.
3. Submit or post the staged source package as an arXiv/workshop-style
   preprint after final venue-specific formatting review.
4. Collect feedback and use it to shape `v0.5`.

See `docs/publication_and_archival_plan_v01.md` for the current publication
route.
