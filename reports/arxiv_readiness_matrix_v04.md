# arXiv Readiness Matrix v0.4

## Summary

CURE-OR++ is currently a strong pre-paper benchmark artifact, not a final
arXiv-ready paper. The Full-CURE-OR v0.4 controlled benchmark evidence is
substantial, and the real-transfer v0.2 external-validity guardrail has now
been collected and evaluated. The open-weight VLM/API path now has two full
rows, including a stronger InternVL3-1B family-contrast row. The remaining work
is paper polish, metadata cleanup, optional frontier/provider VLM coverage, and
final release-boundary decisions.

## Readiness Matrix

| Area | Status | Evidence | Remaining work |
| --- | --- | --- | --- |
| Repository hygiene | Ready | code, configs, reports, aggregate tables tracked; raw payloads ignored | keep raw CURE-OR and prediction dumps out of Git |
| Full-CURE-OR native probe | Ready for draft | 500 clean rows, 38,999 native challenge rows, all v0.4 reports | make clear this is a controlled probe |
| Model coverage | Strong for draft | 8 usable rows across CLIP/OpenCLIP and prototype families, plus two completed open-weight VLM prompt-pack rows | optional frontier/provider VLM rows |
| Confidence analysis | Strong partial | CLIP/OpenCLIP-family confidence/calibration complete | extend if new VLM rows are added |
| Grayscale control | Ready | type-10 control and paired channel-effect analysis complete | keep as guardrail, not main causal proof |
| Consensus analysis | Ready | top three level-5 failures floor 8/8; rank correlations 0.892-0.988 | none before draft |
| Paper tables | Ready | Markdown, CSV, and LaTeX paper-table pack generated | final formatting in paper source |
| Technical report draft | Draft-ready | `reports/cure_or_pp_technical_report_draft_v04.md` | convert to final paper structure |
| LaTeX paper source | Draft-ready | `paper/main.tex`, `paper/references.bib` | final citation verification and venue formatting |
| Dataset card | Draft-ready | `docs/dataset_card_cure_or_pp_v04.md` | update if public release packaging changes |
| Evaluation card | Draft-ready | `docs/evaluation_card_full_cure_or_v04.md` | update after any added frontier/provider VLM rows |
| Related work | Draft-ready | `docs/related_work_v01.md`, expanded LaTeX related-work paragraph | verify final citations before public submission |
| Real-transfer validation | Ready for draft | 180 outputs, activation status, four summaries, source-matched report, bootstrap intervals, figures, collector-supplied iPhone/WhatsApp/FaceTime metadata | integrate into final paper; optionally extract per-file dates from EXIF |
| VLM/API track | Two open-weight rows executed | `reports/vlm_open_weight_smolvlm2_kaggle_v01/`, `reports/vlm_open_weight_internvl3_1b_kaggle_v01/`, `scripts/run_hf_vlm.py`, `scripts/evaluate_vlm_response_pack.py`; SmolVLM2-500M and InternVL3-1B full Kaggle GPU runs complete | optionally add selected frontier/provider VLM rows and report raw-response audit rules |
| Public release | Not final | Kaggle v0.1 package exists locally | decide Kaggle/HF release boundary and license text |

## Minimum Path To A Serious Public Draft

1. Integrate `reports/real_transfer_v02_results.md` into the technical draft
   and LaTeX paper source.
2. Fill capture metadata in the real-transfer checklist if the device/app
   details are available.
3. Convert the technical draft into final paper prose with tables from
   `reports/full_cure_or_paper_tables_v04.tex`.

## Ideal Path

The ideal version adds:

- one additional usable pretrained VLM/model-family row if practical beyond the completed InternVL3-1B row;
- execution of the VLM/API prompt pack on selected frontier VLMs beyond the completed open-weight rows;
- confidence/calibration for any added zero-shot/VLM row;
- final related-work table;
- final dataset card and evaluation card;
- arXiv-style paper source with stable tables and limitations.

## Current Publication Recommendation

Do not submit as a final arXiv paper yet. The work is strong enough for an
internal technical report and close to a workshop-style benchmark draft. The
critical external-validity gap is now reduced by real-transfer v0.2, and the
open-weight VLM path has a real model-family contrast. The next bar is final
paper polish, capture metadata, and optionally adding frontier/provider VLM
rows.
