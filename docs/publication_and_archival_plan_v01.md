# CURE-OR++ Publication and Archival Plan v0.1

Status date: 2026-07-07.

This document defines the route from the current `v0.4.1` archival metadata
release to the first public writeups and preprint submissions.

## Current Stable Public Anchor

- Repository: `https://github.com/qu1nty9/Cure-or-plus-plus`
- Release: `https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1`
- Tag: `v0.4.1`
- Release commit: see the GitHub release tag.
- Attached source package: `arxiv_source_v0.4.1.zip`
- Attached PDF: `cure-or-pp-v0.4.1.pdf`
- Version DOI: `https://doi.org/10.5281/zenodo.21239828`
- Concept DOI: `https://doi.org/10.5281/zenodo.21239827`
- Kaggle public aggregate dataset:
  `https://www.kaggle.com/datasets/yaroslavkholmirzayev/cure-or-plus-plus-v041-public-flat`
- Kaggle public notebook/writeup:
  `https://www.kaggle.com/code/yaroslavkholmirzayev/cure-or-v0-4-1-public-benchmark-writeup`

## Already Done

- GitHub `v0.4-preprint` release/tag exists and is marked as a pre-release.
- PDF is built from the staged source package.
- Staged source zip is attached to the GitHub release.
- `scripts/run_release_checks.py` passes 670 checks with 0 failures.
- Public release boundary is documented.
- Raw CURE-OR, mini-CURE-OR, real-transfer photos, provider raw JSONL, API
  caches, and secrets are excluded from the public package.
- `CITATION.cff` exists for GitHub citation metadata.
- `.zenodo.json` exists for Zenodo/GitHub archival metadata.
- Zenodo DOI metadata exists for the `v0.4.1` release.
- Kaggle public aggregate package and reader-facing notebook/writeup are
  published and validated against the public release boundary.
- Kaggle profile-level writeup draft exists at
  `kaggle/profile_writeup_v041.md`; this is a separate manual Kaggle UI
  publication from the dataset description and executable notebook.

## Remaining Before First Broad Public Push

1. Kaggle profile-level writeup publication.
   - Paste `kaggle/profile_writeup_v041.md` into Kaggle's New writeup editor.
   - Use Project type, the v0.4.1 title, public links, and generated figures.
   - Do not upload raw CURE-OR, mini-CURE-OR, local real-transfer photos,
     provider raw JSONL, caches, or credentials.

2. arXiv/workshop-style preprint.
   - Submit the staged source package after final venue-specific formatting
     review.
   - Keep data availability and limitations aligned with the public release
     boundary.

3. Public feedback loop.
   - Announce the release with links to GitHub, PDF, Kaggle, and DOI.
   - Invite issues for reproduction problems, unclear claims, and model-row
     extension proposals.

## Recommended Publication Order

1. GitHub `v0.4-preprint` release/tag: done.
2. Zenodo/OSF integration: user-enabled.
3. GitHub `v0.4.1` archival metadata release: done.
4. DOI minting and DOI metadata update: done.
5. Kaggle public aggregate dataset and notebook/writeup: done.
6. Kaggle profile-level project writeup.
7. arXiv/workshop-style preprint.
8. Public posts and feedback collection.
9. `v0.5` cleanup release based on feedback.

## Zenodo Workflow

Recommended path:

1. Log in to Zenodo.
2. Connect GitHub to Zenodo.
3. Enable archival for `qu1nty9/Cure-or-plus-plus`.
4. Create a new GitHub release after integration is enabled: `v0.4.1` if no
   scientific content changes are needed.
5. Confirm that Zenodo archived the release and minted a DOI.
6. Add the DOI back to the repository metadata. Avoid creating another release
   solely for this metadata update unless a venue explicitly requires it,
   because each new GitHub release can mint a new Zenodo version DOI.

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
- a DOI exists;
- the Kaggle notebook/writeup is public;
- README, citation metadata, paper, and Kaggle all point to the same stable
  public version.
- the preprint source/PDF has been submitted or posted.
