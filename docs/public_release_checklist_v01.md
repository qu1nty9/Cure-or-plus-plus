# CURE-OR++ Public Release Checklist v0.1

This checklist defines the public-release boundary for the current CURE-OR++
benchmark draft. It is intentionally stricter than the internal workspace:
public artifacts should be reproducible and inspectable without redistributing
upstream raw datasets, local transfer payloads, API secrets, or raw provider
responses.

Current status date: 2026-07-06.

## Project Metadata

- Author: Yaroslav Kholmirzayev.
- Affiliation: Independent Researcher.
- Public contact email: `yaric.kholm@gmail.com`.
- Code/config/report license: MIT for project-authored code, configs, reports,
  generated aggregate artifacts, figures, documentation, and paper source.
- Raw-data policy: do not publish raw CURE-OR images, mini-CURE-OR images,
  local real-transfer photos, local collection packs, raw hosted-provider JSONL
  responses, API caches, or credentials.
- Recommended publication route: GitHub repository plus arXiv/workshop-style
  preprint first; Kaggle notebook/writeup after the paper text and aggregate
  package are stable.
- Stable archival release DOI:
  `https://doi.org/10.5281/zenodo.21239828`.
- Zenodo concept DOI for the release series:
  `https://doi.org/10.5281/zenodo.21239827`.

## Release Targets

| Target | Status | Intended contents | Exclusions |
|---|---|---|---|
| GitHub repository | Ready after final review | Code, configs, aggregate reports, generated paper tables, generated figures, dataset/evaluation cards, paper source | raw CURE-OR images, mini-CURE-OR images, real-transfer images, source archives, API keys, provider caches, raw provider JSONL |
| arXiv/workshop paper | Draft-ready | `paper/main.tex`, references, generated tables, figures, clear limitations and data availability text | raw data payloads, private provider responses |
| Kaggle notebook/writeup | Ready after packaging pass | explanatory notebook, public aggregate tables/figures, setup commands, dataset access instructions | raw CURE-OR unless license/access terms explicitly allow redistribution |
| Hugging Face/Kaggle dataset card | Optional | public metadata, configs, reports, small derived artifacts if license-safe | upstream raw images and private real-transfer payloads |

## Publicly Safe To Track

- Source code under `scripts/`, `configs/`, and notebooks that do not contain
  credentials or private raw payloads.
- Aggregate CSV/Markdown/LaTeX reports under `reports/`.
- Generated figures under `results/`.
- Paper source under `paper/`.
- Dataset/evaluation/release documentation under `docs/`.
- VLM prompt-pack metadata JSONL files, as long as they reference repository
  paths and not private credentials.
- Parsed-response audits and aggregate summaries in canonical result
  directories such as `reports/vlm_provider_*` and
  `reports/vlm_open_weight_*`.

## Must Stay Local

- `secrets/` and `.secrets/`.
- API keys, provider tokens, OAuth material, and local environment files.
- `data/raw/`, `data/interim/`, `data/processed/`, and source dataset archives.
- Raw CURE-OR or mini-CURE-OR images unless upstream terms explicitly allow
  redistribution through the selected release channel.
- Local real-transfer image payloads and collection packs.
- `data/vlm_api_cache/`.
- Raw hosted-provider response JSONL files under
  `reports/vlm_api_track_*_responses*.jsonl`.
- Raw provider request/response dumps from OpenAI, xAI, Anthropic, GigaChat,
  Gemini, or future hosted providers unless explicitly sanitized.
- Root-level evaluator scratch CSV files under
  `reports/vlm_api_track_*_smoke_*.csv` and
  `reports/vlm_api_track_*_full_*.csv`; canonical copies live in
  `reports/vlm_provider_*`.

## Current Evidence Package

The current serious benchmark evidence consists of:

- Public entrypoint and citation metadata:
  `README.md`, `CITATION.cff`, and `.zenodo.json`.
- Full-CURE-OR v0.4 controlled probe:
  `reports/full_cure_or_paper_tables_v04.*`.
- Real-transfer v0.2 validation:
  `reports/real_transfer_v02_results.md` and figures under `results/`.
- Open-weight VLM v0.3 table:
  `reports/vlm_open_weight_full_v03_paper_table.*`.
- Hosted-provider VLM v0.1 table:
  `reports/vlm_provider_full_v01_comparison.*`.
- Hosted-provider VLM v0.3 xAI row and repeat:
  `reports/vlm_provider_full_v03_comparison.*`.
- arXiv readiness matrix:
  `reports/arxiv_readiness_matrix_v04.md`.
- Reproducibility manifest:
  `docs/reproducibility_manifest_v01.md`.
- arXiv source package checklist:
  `docs/arxiv_source_package_checklist_v01.md`.
- Draft GitHub release notes:
  `docs/github_release_notes_v0.4_preprint.md`.
- Publication and archival plan:
  `docs/publication_and_archival_plan_v01.md`.
- Paper scaffold:
  `paper/main.tex`.

## Required Preflight Commands

Run these before any public push, paper package, or notebook release:

```bash
.venv/bin/python -m py_compile \
  scripts/run_release_checks.py \
  scripts/build_arxiv_source_package.py \
  scripts/build_paper_tables.py \
  scripts/build_vlm_provider_comparison.py \
  scripts/build_vlm_provider_v03_comparison.py \
  scripts/run_gigachat_vlm.py \
  scripts/run_anthropic_vlm.py

.venv/bin/python scripts/run_release_checks.py
.venv/bin/python scripts/check_paper_build.py
.venv/bin/python scripts/build_arxiv_source_package.py --output-dir /private/tmp/cure-or-pp-arxiv-source-test --clean
git diff --check
git status --short
```

For final paper packaging, also run TeX compilation on a machine with
`latexmk`, `pdflatex`, and `kpsewhich` installed:

```bash
.venv/bin/python scripts/check_paper_build.py --compile --require-tex --output-dir paper/build
```

## Manual Review Gates

- Confirm that no key-like strings are staged:
  `sk-`, `sk-proj-`, `KGAT_`, `OPENAI_API_KEY=`, `ANTHROPIC_API_KEY=`,
  `XAI_API_KEY=`, `GIGACHAT_AUTH_KEY=`, `GEMINI_API_KEY=`.
- Confirm that no raw CURE-OR archives or image payloads are staged.
- Confirm that raw provider JSONL files are not staged.
- Confirm that provider summaries do not expose account identifiers,
  credentials, or private absolute image paths.
- Confirm that paper text distinguishes:
  open-weight rows, hosted-provider rows, raw data access, and aggregate
  artifacts.
- Confirm that limitations explicitly mention small real-transfer v0.2 size,
  provider versioning, and incomplete frontier-provider coverage.
- Confirm that dataset and evaluation cards match the actual public package.

## Publication Blocking Items

These should be resolved before a final arXiv or workshop submission:

- Final citation verification for related work and CURE-OR source references.
- Local TeX compile with required tools installed.
- Final license review if any public dataset/package goes beyond code,
  documentation, figures, aggregate reports, and sanitized parsed audits.

## Non-Blocking Future Extensions

These are useful but not required for the current serious draft:

- Gemini or Mistral hosted-provider row.
- Additional provider repeatability runs beyond xAI Grok 4.3 v0.3 repeat.
- Larger real-transfer v0.3/v0.4 collection.
- Broader confidence/calibration coverage for non-CLIP rows.
- Public interactive notebook with lightweight visual examples.

## Current Recommendation

Proceed toward a polished GitHub release plus arXiv/workshop-style draft using
the current evidence package. Do not expand the model matrix further unless the
paper narrative specifically needs another provider family. The highest-return
work is now paper clarity, release boundary discipline, final citations,
reproducible packaging, and a later Kaggle writeup built from the stable
aggregate package.
