# CURE-OR++ arXiv Source Package Checklist v0.2

Status date: 2026-07-08.

Target tag: `v0.4.1`.

This checklist defines the intended arXiv/workshop source package boundary. It
does not publish raw image data, provider caches, API keys, or raw hosted
provider responses.

## Recommended Package Layout

For arXiv, prefer a staged source directory rather than submitting directly from
the repository layout. The current paper source uses paths such as
`../reports/...` and `../results/...`, which are convenient inside the repo but
awkward for arXiv. The staged package should use:

```text
arxiv_source/
  main.tex
  references.bib
  reports/
    full_cure_or_paper_tables_v04.tex
    vlm_open_weight_full_v03_paper_table.tex
    vlm_provider_full_v03_comparison.tex
    vlm_provider_full_v01_comparison.tex
  results/
    real_transfer_v02_source_matched_drops.png
    real_transfer_v02_accuracy_heatmap.png
```

In the staged `main.tex`, rewrite:

- `../reports/` to `reports/`
- `../results/` to `results/`

Do not rewrite tracked repository source for this staging step; create a copied
package directory.

Use the tracked builder:

```bash
.venv/bin/python scripts/build_arxiv_source_package.py \
  --output-dir exports/arxiv_source_v0.4.1 \
  --clean \
  --make-zip
```

The builder rewrites paper paths only inside the staged copy, writes
`MANIFEST.json`, creates an optional `.zip` archive, and validates that forbidden
raw-data/provider-cache file classes were not included.

## Include

Paper source:

- `paper/main.tex`
- `paper/references.bib`

LaTeX table inputs:

- `reports/full_cure_or_paper_tables_v04.tex`
- `reports/vlm_open_weight_full_v03_paper_table.tex`
- `reports/vlm_provider_full_v03_comparison.tex`
- `reports/vlm_provider_full_v01_comparison.tex`

Figures:

- `results/real_transfer_v02_source_matched_drops.png`
- `results/real_transfer_v02_accuracy_heatmap.png`

Optional README for the source package:

- short build note;
- public release boundary;
- upstream data access note;
- contact email.

## Exclude

Never include:

- `secrets/` or `.secrets/`
- API keys, provider tokens, OAuth files, or `.env` files
- `data/raw/`, `data/interim/`, `data/processed/`
- raw CURE-OR or mini-CURE-OR images
- local real-transfer photos or collection packs
- source dataset archives
- `data/vlm_api_cache/`
- raw hosted-provider JSONL response dumps
- external-disk build/cache directories
- notebook execution caches
- `.git/`

## Build Checks

Before staging:

```bash
.venv/bin/python scripts/run_release_checks.py
.venv/bin/python scripts/check_paper_build.py --compile --output-dir /private/tmp/cure-or-pp-paper-check
.venv/bin/python scripts/build_arxiv_source_package.py --output-dir /private/tmp/cure-or-pp-arxiv-source-test --clean --make-zip
git diff --check
```

Traditional TeX build command used for final staged-package verification:

```bash
cd /private/tmp/cure-or-pp-arxiv-source-test
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Expected final log state:

- no LaTeX errors;
- no undefined citations;
- no undefined references;
- no `Overfull \hbox` warnings in the final log.

## Manual Review

Before upload:

- Confirm author, affiliation, and email in `main.tex`.
- Confirm title matches the GitHub release.
- Confirm abstract does not overclaim real-transfer coverage.
- Confirm limitations mention small real-transfer v0.2 size and provider drift.
- Confirm data availability text states that raw CURE-OR and real-transfer
  photos are not redistributed.
- Confirm bibliography entries render correctly.
- Open the final PDF and inspect all tables and figures.

## Current Local Package

The latest locally verified staged source package and PDF are:

- `/private/tmp/cure-or-pp-arxiv-source-test.zip`
- `/private/tmp/cure-or-pp-arxiv-source-test/main.pdf`

These paths are local-only and should not be referenced as public artifacts.
