# CURE-OR++ v0.4.1 Public Benchmark Aggregates

This Kaggle package is the public aggregate companion for CURE-OR++ v0.4.1.
It is designed for reading, plotting, and auditing the benchmark claims without
redistributing raw CURE-OR images, private real-transfer photos, hosted-provider
raw JSONL responses, provider caches, or credentials.

Version DOI: https://doi.org/10.5281/zenodo.21239828

Concept DOI: https://doi.org/10.5281/zenodo.21239827

GitHub release: https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1

## Contents

- `reports/full_cure_or_paper_*`: Full-CURE-OR v0.4 paper tables.
- `reports/real_transfer_v02_*`: source-matched real-transfer validation.
- `reports/vlm_open_weight_full_v03_*`: 900-row open-weight VLM comparison.
- `reports/vlm_provider_full_v03_*`: 900-row hosted-provider VLM row.
- `reports/vlm_provider_full_v01_*`: 210-row hosted-provider comparison.
- `figures/`: generated paper/readout figures.
- `docs/`: dataset, evaluation, public-boundary, and reproducibility notes.
- `repository/`: README, citation metadata, and license from the GitHub repo.
- `MANIFEST.json`: file hashes and release boundary metadata.

## Public Data Boundary

This package contains aggregate and generated artifacts only. Users who need
to reproduce the full image-level evaluation should obtain upstream CURE-OR
under its own terms and rerun the documented pipeline from the GitHub repo.
