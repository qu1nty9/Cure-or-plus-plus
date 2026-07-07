# GitHub Release Notes: v0.4.1

Tag: `v0.4.1`

Status: archival metadata patch release.

## Summary

This release is a metadata-only archival patch for the `v0.4-preprint`
scientific baseline. It adds Zenodo/GitHub archival metadata, a public README
route, citation metadata, and an explicit publication/archival plan. The
benchmark results, paper claims, public data boundary, and core evaluation
artifacts are unchanged from `v0.4-preprint`.

## Changes Since v0.4-preprint

- Added `.zenodo.json` for Zenodo archival metadata.
- Added `CITATION.cff` for GitHub citation metadata.
- Reworked `README.md` into a public entrypoint for release/PDF/source,
  reproducibility, data boundary, and citation.
- Added `docs/publication_and_archival_plan_v01.md`.
- Strengthened `scripts/run_release_checks.py` so README, LICENSE,
  `CITATION.cff`, `.zenodo.json`, and archival docs are required and scanned.
- Release checks now pass with 632 checks and 0 failures.

## Attached Release Artifacts

```text
arxiv_source_v0.4.1.zip
cure-or-pp-v0.4.1.pdf
```

The source zip is generated from the staged paper package. The PDF is built
from that staged source package.

## Not Included

- Raw CURE-OR or mini-CURE-OR images.
- Local real-transfer photos or collection packs.
- Source dataset archives.
- API keys, provider tokens, OAuth material, `.env` files, or secrets.
- Hosted-provider raw JSONL response dumps.
- Provider API caches.

## Next Step

Wait for Zenodo or the selected archival service to mint a DOI for this release.
After the DOI exists, update `CITATION.cff`, `.zenodo.json`, `README.md`,
`paper/main.tex`, release notes, and the future Kaggle writeup.
