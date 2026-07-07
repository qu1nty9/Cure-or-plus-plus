# CURE-OR++ Reproducibility Manifest v0.1

Status date: 2026-07-06.

This manifest defines how the current CURE-OR++ preprint package can be audited
from public, tracked artifacts. It complements `docs/public_release_checklist_v01.md`.

## Release Scope

Target release: `v0.4-preprint`.

Author metadata:

- Author: Yaroslav Kholmirzayev.
- Affiliation: Independent Researcher.
- Public email: `yaric.kholm@gmail.com`.

Public package policy:

- Include project-authored code, configs, documentation, paper source,
  generated figures, aggregate reports, LaTeX tables, prompt-pack metadata,
  parsed audits, and non-sensitive summaries.
- Exclude API keys, provider tokens, raw CURE-OR images, mini-CURE-OR images,
  local real-transfer photos, local collection packs, source archives, hosted
  provider raw JSONL responses, and provider API caches.
- Open-weight model response files that are already tracked under canonical
  `reports/vlm_open_weight_*` directories are treated as non-provider generated
  artifacts. Hosted-provider raw request/response dumps remain local/private.

## Paper Build

The paper source is:

- `paper/main.tex`
- `paper/references.bib`

The current local verified build uses Tectonic and writes build/cache artifacts
to the external workspace:

```bash
mkdir -p /Volumes/980PRO/CURE-OR++/builds/paper_tectonic
mkdir -p /Volumes/980PRO/CURE-OR++/cache/tectonic

cd /Users/yaroslav/Documents/CURE-OR++/paper
env \
  XDG_CACHE_HOME=/Volumes/980PRO/CURE-OR++/cache \
  TECTONIC_CACHE_DIR=/Volumes/980PRO/CURE-OR++/cache/tectonic \
  tectonic -p --keep-logs \
    --outdir /Volumes/980PRO/CURE-OR++/builds/paper_tectonic \
    main.tex
```

Verified local PDF:

- `/Volumes/980PRO/CURE-OR++/builds/paper_tectonic/main.pdf`
- `/Volumes/980PRO/CURE-OR++/builds/arxiv_source_v0.4_preprint/main.pdf`

The repository preflight checker also validates that all paper inputs, figures,
and bibliography files exist:

```bash
.venv/bin/python scripts/check_paper_build.py
```

This local machine currently lacks `latexmk`, `pdflatex`, and `kpsewhich`, so
the strict TeX toolchain compile path remains a final packaging gate on a
machine with those tools installed.

The arXiv/workshop source package is generated with:

```bash
.venv/bin/python scripts/build_arxiv_source_package.py \
  --output-dir /Volumes/980PRO/CURE-OR++/exports/arxiv_source_v0.4_preprint \
  --make-zip
```

This creates a staged package with `main.tex`, `references.bib`, required
LaTeX table inputs, required figures, `README.md`, and `MANIFEST.json`. The
staged `main.tex` uses package-local `reports/` and `results/` paths.

Latest verified staged source package:

- `/Volumes/980PRO/CURE-OR++/exports/arxiv_source_v0.4_preprint.zip`

## Aggregate Table Generation

Full-CURE-OR v0.4 paper tables:

```bash
.venv/bin/python scripts/build_paper_tables.py
```

Primary outputs:

- `reports/full_cure_or_paper_model_table_v04.csv`
- `reports/full_cure_or_paper_failure_table_v04.csv`
- `reports/full_cure_or_paper_control_table_v04.csv`
- `reports/full_cure_or_paper_tables_v04.md`
- `reports/full_cure_or_paper_tables_v04.tex`

Hosted-provider VLM v0.1 comparison:

```bash
.venv/bin/python scripts/build_vlm_provider_comparison.py
```

Primary outputs:

- `reports/vlm_provider_full_v01_comparison.csv`
- `reports/vlm_provider_full_v01_comparison.md`
- `reports/vlm_provider_full_v01_comparison.tex`

Hosted-provider VLM v0.3 comparison:

```bash
.venv/bin/python scripts/build_vlm_provider_v03_comparison.py
```

Primary outputs:

- `reports/vlm_provider_full_v03_comparison.csv`
- `reports/vlm_provider_full_v03_comparison.md`
- `reports/vlm_provider_full_v03_comparison.tex`

Open-weight VLM v0.3 paper table:

- `reports/vlm_open_weight_full_v03_paper_table.csv`
- `reports/vlm_open_weight_full_v03_paper_table.md`
- `reports/vlm_open_weight_full_v03_paper_table.tex`

## Main Evidence Artifacts

Full-CURE-OR v0.4:

- `reports/full_cure_or_probe_v04_status.md`
- `reports/full_cure_or_probe_v04_expanded_models.md`
- `reports/full_cure_or_prototype_v04.md`
- `reports/full_cure_or_confidence_v04.md`
- `reports/full_cure_or_grayscale_control_v04.md`
- `reports/full_cure_or_challenge_family_v04.md`
- `reports/full_cure_or_consensus_v04.md`
- `reports/full_cure_or_paper_tables_v04.*`

Real-transfer validation:

- `reports/real_transfer_v02_results.md`
- `reports/real_transfer_v02_model_pipeline_table.csv`
- `reports/real_transfer_v02_pipeline_consensus_table.csv`
- `reports/real_transfer_v02_label_failure_table.csv`
- `results/real_transfer_v02_source_matched_drops.png`
- `results/real_transfer_v02_accuracy_heatmap.png`

VLM prompt packs:

- `reports/vlm_api_track_v01_prompt_pack.jsonl`
- `reports/vlm_api_track_v01_prompt_pack_summary.json`
- `reports/vlm_api_track_v03_prompt_pack.jsonl`
- `reports/vlm_api_track_v03_prompt_pack_summary.json`

Open-weight VLM aggregates:

- `reports/vlm_open_weight_full_v03_comparison.*`
- `reports/vlm_open_weight_full_v03_paper_table.*`
- canonical result directories under `reports/vlm_open_weight_*`.

Hosted-provider VLM aggregates:

- `reports/vlm_provider_full_v01_comparison.*`
- `reports/vlm_provider_full_v03_comparison.*`
- canonical sanitized result directories under `reports/vlm_provider_*`.

Documentation:

- `README.md`
- `CITATION.cff`
- `.zenodo.json`
- `docs/dataset_card_cure_or_pp_v04.md`
- `docs/evaluation_card_full_cure_or_v04.md`
- `docs/public_release_checklist_v01.md`
- `docs/publication_and_archival_plan_v01.md`
- `reports/arxiv_readiness_matrix_v04.md`
- `docs/reproducibility_manifest_v01.md`

## Required Preflight

Run before release, paper package creation, or public notebook publication:

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

Current release-check baseline:

- `scripts/run_release_checks.py`: 632 checks, 0 failures.

## Reproduction Caveats

- Raw CURE-OR and mini-CURE-OR images must be obtained from the upstream source
  under upstream terms.
- Local real-transfer photos are not redistributed; public artifacts expose
  protocol metadata and aggregate results.
- Hosted-provider rows are reproducible at the protocol level but exact answers
  can drift because provider-side model routing, versioning, caching, pricing,
  and data handling are externally controlled.
- Open-weight VLM rows require the referenced model weights and a compatible GPU
  environment; the current Kaggle runners document the tested path.
