# CURE-OR++ arXiv Source Package Checklist v0.1

Status date: 2026-07-06.

Target tag: `v0.4-preprint`.

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
.venv/bin/python scripts/check_paper_build.py
git diff --check
```

Local Tectonic build command used for verification:

```bash
cd /Users/yaroslav/Documents/CURE-OR++/paper
env \
  XDG_CACHE_HOME=/Volumes/980PRO/CURE-OR++/cache \
  TECTONIC_CACHE_DIR=/Volumes/980PRO/CURE-OR++/cache/tectonic \
  tectonic -p --keep-logs \
    --outdir /Volumes/980PRO/CURE-OR++/builds/paper_tectonic \
    main.tex
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

## Current Local PDF

The latest locally verified PDF is:

- `/Volumes/980PRO/CURE-OR++/builds/paper_tectonic/main.pdf`

This path is local-only and should not be referenced as a public artifact.
