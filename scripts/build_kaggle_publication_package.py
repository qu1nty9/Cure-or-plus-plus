#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VERSION = "v0.4.1"
VERSION_DOI = "10.5281/zenodo.21239828"
CONCEPT_DOI = "10.5281/zenodo.21239827"

PUBLIC_FILES = [
    ("README.md", "repository/README.md"),
    ("CITATION.cff", "repository/CITATION.cff"),
    ("LICENSE", "repository/LICENSE"),
    ("docs/dataset_card_cure_or_pp_v04.md", "docs/dataset_card_cure_or_pp_v04.md"),
    ("docs/evaluation_card_full_cure_or_v04.md", "docs/evaluation_card_full_cure_or_v04.md"),
    ("docs/publication_and_archival_plan_v01.md", "docs/publication_and_archival_plan_v01.md"),
    ("reports/full_cure_or_paper_model_table_v04.csv", "reports/full_cure_or_paper_model_table_v04.csv"),
    ("reports/full_cure_or_paper_failure_table_v04.csv", "reports/full_cure_or_paper_failure_table_v04.csv"),
    ("reports/full_cure_or_paper_control_table_v04.csv", "reports/full_cure_or_paper_control_table_v04.csv"),
    ("reports/full_cure_or_paper_tables_v04.md", "reports/full_cure_or_paper_tables_v04.md"),
    ("reports/real_transfer_v02_results.md", "reports/real_transfer_v02_results.md"),
    ("reports/real_transfer_v02_model_pipeline_table.csv", "reports/real_transfer_v02_model_pipeline_table.csv"),
    ("reports/real_transfer_v02_pipeline_consensus_table.csv", "reports/real_transfer_v02_pipeline_consensus_table.csv"),
    ("reports/real_transfer_v02_label_failure_table.csv", "reports/real_transfer_v02_label_failure_table.csv"),
    ("reports/vlm_open_weight_full_v03_paper_table.csv", "reports/vlm_open_weight_full_v03_paper_table.csv"),
    ("reports/vlm_open_weight_full_v03_paper_table.md", "reports/vlm_open_weight_full_v03_paper_table.md"),
    ("reports/vlm_open_weight_full_v03_comparison.csv", "reports/vlm_open_weight_full_v03_comparison.csv"),
    ("reports/vlm_open_weight_full_v03_comparison.md", "reports/vlm_open_weight_full_v03_comparison.md"),
    ("reports/vlm_provider_full_v03_comparison.csv", "reports/vlm_provider_full_v03_comparison.csv"),
    ("reports/vlm_provider_full_v03_comparison.md", "reports/vlm_provider_full_v03_comparison.md"),
    ("reports/vlm_provider_full_v01_comparison.csv", "reports/vlm_provider_full_v01_comparison.csv"),
    ("reports/vlm_provider_full_v01_comparison.md", "reports/vlm_provider_full_v01_comparison.md"),
    ("reports/arxiv_readiness_matrix_v04.md", "reports/arxiv_readiness_matrix_v04.md"),
    ("reports/release_check_v04.json", "reports/release_check_v04.json"),
    ("results/full_cure_or_probe_v04_with_prototypes_level5_ranking.png", "figures/full_cure_or_probe_v04_with_prototypes_level5_ranking.png"),
    ("results/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png", "figures/full_cure_or_probe_v04_with_prototypes_mean_accuracy_by_level.png"),
    ("results/full_cure_or_probe_v04_level5_overconfidence.png", "figures/full_cure_or_probe_v04_level5_overconfidence.png"),
    ("results/full_cure_or_grayscale_control_v04_with_prototypes_comparison.png", "figures/full_cure_or_grayscale_control_v04_with_prototypes_comparison.png"),
    ("results/real_transfer_v02_source_matched_drops.png", "figures/real_transfer_v02_source_matched_drops.png"),
    ("results/real_transfer_v02_accuracy_heatmap.png", "figures/real_transfer_v02_accuracy_heatmap.png"),
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the public Kaggle aggregate package for CURE-OR++ v0.4.1."
    )
    parser.add_argument("--output-dir", default="kaggle/cure-or-plus-plus-v041-public")
    parser.add_argument("--kaggle-id", default="yaroslavkholmirzayev/cure-or-plus-plus-v041-public")
    parser.add_argument("--license-name", default="MIT")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    output_dir = resolve_project_path(args.output_dir)
    if args.clean and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for source_rel, target_rel in PUBLIC_FILES:
        source = ROOT / source_rel
        target = output_dir / target_rel
        copy_file(source, target)
        copied.append(record_file(source_rel, target_rel, target))

    write_dataset_metadata(output_dir / "dataset-metadata.json", args.kaggle_id, args.license_name)
    write_readme(output_dir / "README.md")
    write_citation(output_dir / "CITATION.md")
    write_reproducibility_note(output_dir / "docs/reproducibility_note.md")
    copied.append(record_file("<generated>", "docs/reproducibility_note.md", output_dir / "docs/reproducibility_note.md"))
    write_public_boundary(output_dir / "docs/public_boundary.md")
    copied.append(record_file("<generated>", "docs/public_boundary.md", output_dir / "docs/public_boundary.md"))
    write_manifest(output_dir / "MANIFEST.json", copied, args.kaggle_id, args.license_name)

    print(f"Kaggle public aggregate package: {output_dir}")
    print(f"Files copied: {len(copied)}")
    print(f"Version DOI: https://doi.org/{VERSION_DOI}")
    return 0


def copy_file(source: Path, target: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def record_file(source_rel: str, target_rel: str, target: Path) -> dict:
    return {
        "source": source_rel,
        "path": target_rel,
        "size_bytes": target.stat().st_size,
        "sha256": sha256_file(target),
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_dataset_metadata(path: Path, kaggle_id: str, license_name: str) -> None:
    metadata = {
        "title": "CURE-OR++ v0.4.1 Public Benchmark Aggregates",
        "id": kaggle_id,
        "licenses": [{"name": license_name}],
    }
    path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")


def write_manifest(path: Path, files: list[dict], kaggle_id: str, license_name: str) -> None:
    manifest = {
        "package": "CURE-OR++ public Kaggle aggregate package",
        "version": VERSION,
        "kaggle_id": kaggle_id,
        "license": license_name,
        "version_doi": f"https://doi.org/{VERSION_DOI}",
        "concept_doi": f"https://doi.org/{CONCEPT_DOI}",
        "source_repository": "https://github.com/qu1nty9/Cure-or-plus-plus",
        "source_release": "https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1",
        "public_boundary": {
            "includes": [
                "aggregate CSV and Markdown reports",
                "generated figures",
                "dataset and evaluation documentation",
                "release and reproducibility metadata",
            ],
            "excludes": [
                "raw CURE-OR images",
                "mini-CURE-OR images",
                "local real-transfer photos",
                "provider raw JSONL response dumps",
                "provider API caches",
                "credentials",
                "source dataset archives",
            ],
        },
        "files": files,
    }
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_readme(path: Path) -> None:
    path.write_text(
        f"""# CURE-OR++ {VERSION} Public Benchmark Aggregates

This Kaggle package is the public aggregate companion for CURE-OR++ {VERSION}.
It is designed for reading, plotting, and auditing the benchmark claims without
redistributing raw CURE-OR images, private real-transfer photos, hosted-provider
raw JSONL responses, provider caches, or credentials.

Version DOI: https://doi.org/{VERSION_DOI}

Concept DOI: https://doi.org/{CONCEPT_DOI}

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
""",
        encoding="utf-8",
    )


def write_citation(path: Path) -> None:
    path.write_text(
        f"""# Citation

If you use this public aggregate package, cite the archived release:

```bibtex
@misc{{kholmirzayev2026cureorpp,
  title = {{CURE-OR++: Object Recognition Robustness Under Native CURE-OR Challenges and Digital Transfer Pipelines}},
  author = {{Kholmirzayev, Yaroslav}},
  year = {{2026}},
  note = {{Archival metadata release {VERSION}; scientific preprint baseline v0.4-preprint}},
  doi = {{{VERSION_DOI}}},
  url = {{https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1}}
}}
```

Original upstream dataset:

- CURE-OR: https://github.com/olivesgatech/CURE-OR
""",
        encoding="utf-8",
    )


def write_reproducibility_note(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""# Reproducibility Note

This Kaggle package is a public aggregate package for CURE-OR++ {VERSION}.
It is intended for notebook-level inspection, plotting, and citation of the
stable benchmark evidence.

To reproduce the full image-level benchmark, use the GitHub source release:

- https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1

The public source release documents the scripts used to regenerate paper
tables, figures, release checks, and the arXiv/workshop source package. Full
image-level reproduction requires authorized access to the upstream CURE-OR
dataset and, for hosted-provider rows, rerunning provider APIs under the same
prompt protocol while accepting provider-side model drift.

The version DOI for this package is:

- https://doi.org/{VERSION_DOI}
""",
        encoding="utf-8",
    )


def write_public_boundary(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """# Public Boundary

This package intentionally contains only public aggregate artifacts:

- aggregate CSV and Markdown reports;
- generated figures;
- dataset and evaluation cards;
- release, citation, and reproducibility metadata.

This package intentionally excludes:

- upstream raw image payloads;
- local real-transfer photos and collection packs;
- source dataset archives;
- hosted-provider raw request/response dumps;
- provider caches;
- credential or account-authentication material.

This boundary is part of the benchmark design. It keeps the Kaggle package
auditable while avoiding redistribution of upstream raw data, private local
collection payloads, or provider-specific raw responses.
""",
        encoding="utf-8",
    )


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
