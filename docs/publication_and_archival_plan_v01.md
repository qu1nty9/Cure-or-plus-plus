# CURE-OR++ Publication and Archival Plan v0.1

Status date: 2026-07-07.

This document defines the route from the current `v0.4-preprint` GitHub release
to the first public writeups and preprint submissions.

## Current Stable Public Anchor

- Repository: `https://github.com/qu1nty9/Cure-or-plus-plus`
- Release: `https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4-preprint`
- Tag: `v0.4-preprint`
- Release commit: `c1d404e`
- Attached source package: `arxiv_source_v0.4_preprint.zip`
- Attached PDF: `cure-or-pp-v0.4-preprint.pdf`

## Already Done

- GitHub release/tag exists and is marked as a pre-release.
- PDF is built from the staged source package.
- Staged source zip is attached to the GitHub release.
- `scripts/run_release_checks.py` passes 632 checks with 0 failures.
- Public release boundary is documented.
- Raw CURE-OR, mini-CURE-OR, real-transfer photos, provider raw JSONL, API
  caches, and secrets are excluded from the public package.
- `CITATION.cff` exists for GitHub citation metadata.
- `.zenodo.json` exists for Zenodo/GitHub archival metadata.

## Remaining Before First Broad Public Push

1. Archival DOI.
   - Connect the GitHub repository to Zenodo or archive the release through
     OSF/another stable archival service.
   - Because `.zenodo.json` was added after `v0.4-preprint`, prefer publishing
     a small follow-up release such as `v0.4.1` after Zenodo integration is
     enabled, so the archived record includes the metadata file.
   - Record the DOI in `CITATION.cff`, `.zenodo.json`, `README.md`,
     `paper/main.tex`, `docs/github_release_notes_v0.4_preprint.md`, and the
     Kaggle writeup.

2. Kaggle notebook/writeup.
   - Use only public aggregate artifacts and figures.
   - Link to the GitHub release, PDF, source zip, and DOI if available.
   - Explain the benchmark in reader-facing terms rather than as an internal
     development log.

3. arXiv/workshop-style preprint.
   - Submit the staged source package after final venue-specific formatting
     review.
   - Keep data availability and limitations aligned with the public release
     boundary.

4. Public feedback loop.
   - Announce the release with links to GitHub, PDF, Kaggle, and DOI.
   - Invite issues for reproduction problems, unclear claims, and model-row
     extension proposals.

## Recommended Publication Order

1. GitHub release/tag: done.
2. Zenodo/OSF integration and DOI minting.
3. DOI metadata patch release if required, for example `v0.4.1`.
4. Kaggle notebook/writeup.
5. arXiv/workshop-style preprint.
6. Public posts and feedback collection.
7. `v0.5` cleanup release based on feedback.

## Zenodo Workflow

Recommended path:

1. Log in to Zenodo.
2. Connect GitHub to Zenodo.
3. Enable archival for `qu1nty9/Cure-or-plus-plus`.
4. Create a new GitHub release after integration is enabled, preferably
   `v0.4.1` if no scientific content changes are needed.
5. Wait for Zenodo to archive the release and mint a DOI.
6. Add the DOI back to the repository metadata and publish a final DOI metadata
   patch if needed.

Do not upload raw datasets, provider caches, or credentials manually to Zenodo.
The intended archive boundary is the public GitHub release source archive plus
the attached PDF/source package artifacts.

## Do Not Publish

- Raw CURE-OR images or source archives.
- Mini-CURE-OR image payloads.
- Local real-transfer photos or collection packs.
- Provider raw response JSONL files.
- Provider API caches.
- API keys, OAuth material, `.env` files, or other credentials.

## Success Criteria

The first publication wave is considered complete when:

- the GitHub release is stable;
- a DOI or archive landing page exists;
- the Kaggle notebook/writeup is public;
- the preprint source/PDF has been submitted or posted;
- README, citation metadata, paper, and Kaggle all point to the same stable
  public version.
