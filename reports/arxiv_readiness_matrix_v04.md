# arXiv Readiness Matrix v0.4

## Summary

CURE-OR++ is currently a strong pre-paper benchmark artifact, not a final
arXiv-ready paper. The Full-CURE-OR v0.4 controlled benchmark evidence is
substantial, and the real-transfer v0.2 external-validity guardrail has now
been collected and evaluated. The open-weight VLM/API path now has eight full
rows, including a strong SmolVLM2-2.2B same-family scale-up, two strong
InternVL family rows with a slight non-monotonic 2B follow-up, a completed
LLaVA-OneVision 0.5B row after memory-safe retry, a memory-controlled
Qwen2.5-VL-7B strong row, a completed memory-controlled LLaVA-OneVision 7B
row, and a Qwen2.5-VL generation-instability row at 3B.
The v0.3 900-row VLM real-transfer extension now has seven completed
open-weight rows: Qwen2.5-VL-7B, LLaVA-OneVision Qwen2 7B,
LLaVA-OneVision Qwen2 0.5B, InternVL3-1B, InternVL3-2B, SmolVLM2-2.2B, and
Qwen2.5-VL-3B.
The hosted-provider path has seven completed rows on the 210-row prompt pack:
xAI Grok 4.3 reaches 0.9833 real-transfer accuracy, GPT-5.4-mini reaches
0.9611, Claude Sonnet 5 reaches 0.9611 after one targeted max-token retry,
Claude Fable 5 reaches 0.9611 with two remaining unparseable rows, GPT-5.4
reaches 0.9556, and GPT-5.5 and Claude Haiku 4.5 reach 0.9500. It also now has a 900-row v0.3 xAI
Grok 4.3 row, reaching 0.9788 real-transfer accuracy with zero unparseable
responses, plus a repeat run that preserves 0.9788 real-transfer accuracy.
The remaining work is paper polish, metadata cleanup, optional frontier/provider
VLM coverage, and final release-boundary decisions.

## Readiness Matrix

| Area | Status | Evidence | Remaining work |
| --- | --- | --- | --- |
| Repository hygiene | Ready | code, configs, reports, aggregate tables tracked; raw payloads ignored | keep raw CURE-OR and prediction dumps out of Git |
| Full-CURE-OR native probe | Ready for draft | 500 clean rows, 38,999 native challenge rows, all v0.4 reports | make clear this is a controlled probe |
| Model coverage | Strong for draft | 8 usable rows across CLIP/OpenCLIP and prototype families, eight completed open-weight VLM prompt-pack rows, nine hosted-provider v0.1 rows across OpenAI, xAI, Anthropic, and GigaChat, and one hosted xAI v0.3 row with repeat evidence | optional Gemini provider row |
| Confidence analysis | Strong partial | CLIP/OpenCLIP-family confidence/calibration complete | extend if new VLM rows are added |
| Grayscale control | Ready | type-10 control and paired channel-effect analysis complete | keep as guardrail, not main causal proof |
| Consensus analysis | Ready | top three level-5 failures floor 8/8; rank correlations 0.892-0.988 | none before draft |
| Paper tables | Ready | Markdown, CSV, and LaTeX paper-table pack generated | final formatting in paper source |
| Technical report draft | Draft-ready | `reports/cure_or_pp_technical_report_draft_v04.md` | convert to final paper structure |
| LaTeX paper source | Draft-ready | `paper/main.tex`, `paper/references.bib` | final citation verification and venue formatting |
| Dataset card | Draft-ready | `docs/dataset_card_cure_or_pp_v04.md` | update if public release packaging changes |
| Evaluation card | Draft-ready | `docs/evaluation_card_full_cure_or_v04.md` | update after any added frontier/provider VLM rows |
| Related work | Draft-ready | `docs/related_work_v01.md`, expanded LaTeX related-work paragraph | verify final citations before public submission |
| Real-transfer validation | Ready for draft | 180 outputs, activation status, source-matched report, bootstrap intervals, figures, collector-supplied iPhone/WhatsApp/FaceTime metadata | integrate into final paper; optionally extract per-file dates from EXIF |
| VLM/API track | Eight v0.2 open-weight rows executed; seven-row v0.3 900-row extension complete; nine hosted-provider v0.1 rows complete; one hosted-provider v0.3 row and repeat run complete | `reports/vlm_open_weight_smolvlm2_kaggle_v01/`, `reports/vlm_open_weight_smolvlm2_2b_kaggle_v01/`, `reports/vlm_open_weight_internvl3_1b_kaggle_v01/`, `reports/vlm_open_weight_internvl3_2b_kaggle_v01/`, `reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_v01/`, `reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_v01/`, `reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_v01/`, `reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_v01/`, `reports/vlm_open_weight_full_v03_comparison.md`, `reports/vlm_provider_openai_gpt_5_4_mini_full_v01/`, `reports/vlm_provider_openai_gpt_5_4_full_v01/`, `reports/vlm_provider_openai_gpt_5_5_full_v01/`, `reports/vlm_provider_anthropic_claude_sonnet_5_full_v01/`, `reports/vlm_provider_anthropic_claude_fable_5_full_v01/`, `reports/vlm_provider_anthropic_claude_haiku_4_5_full_v01/`, `reports/vlm_provider_gigachat_2_pro_full_v01/`, `reports/vlm_provider_gigachat_2_max_full_v01/`, `reports/vlm_provider_xai_grok_4_3_full_v01/`, `reports/vlm_provider_xai_grok_4_3_full_v03/`, `reports/vlm_provider_xai_grok_4_3_full_v03_repeat_01/`, `reports/vlm_provider_full_v01_comparison.md`, `reports/vlm_provider_full_v03_comparison.md`, `reports/vlm_open_weight_qwen2_5_vl_3b_kaggle_full_v03/`, `reports/vlm_open_weight_qwen2_5_vl_7b_kaggle_full_v03/`, `reports/vlm_open_weight_internvl3_1b_kaggle_full_v03/`, `reports/vlm_open_weight_internvl3_2b_kaggle_full_v03/`, `reports/vlm_open_weight_llava_onevision_qwen2_0_5b_kaggle_full_v03/`, `reports/vlm_open_weight_llava_onevision_qwen2_7b_kaggle_full_v03/`, `reports/vlm_open_weight_smolvlm2_2b_kaggle_full_v03/`, `scripts/run_hf_vlm.py`, `scripts/evaluate_vlm_response_pack.py`, `scripts/integrate_kaggle_vlm_output.py`, `scripts/build_vlm_provider_comparison.py`, `scripts/build_vlm_provider_v03_comparison.py`, `scripts/merge_vlm_response_retries.py`; SmolVLM2-500M, SmolVLM2-2.2B, InternVL3-1B, InternVL3-2B, LLaVA-OneVision 0.5B, Qwen2.5-VL-3B, Qwen2.5-VL-7B, and LLaVA-OneVision 7B full v0.2 Kaggle GPU runs complete; Qwen2.5-VL-3B, Qwen2.5-VL-7B, InternVL3-1B, InternVL3-2B, LLaVA-OneVision 0.5B, LLaVA-OneVision 7B, and SmolVLM2-2.2B full v0.3 runs complete; OpenAI GPT-5.4-mini, GPT-5.4, GPT-5.5, xAI Grok 4.3, Anthropic Claude Sonnet 5, Claude Fable 5, Claude Haiku 4.5, GigaChat 2 Pro, and GigaChat 2 Max full v0.1 provider rows complete; xAI Grok 4.3 full v0.3 provider row and repeat run complete | optionally add Gemini row and final raw-response audit rules |
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

- execution of the VLM/API prompt pack on selected frontier VLMs beyond the completed OpenAI, xAI, Anthropic, and GigaChat provider rows;
- completion of the v0.3 900-row open-weight VLM scale/family extension beyond the current seven rows;
- repeatability reruns for the strongest open-weight rows if needed for final release confidence;
- confidence/calibration for any added zero-shot/VLM row;
- final related-work table;
- final dataset card and evaluation card;
- arXiv-style paper source with stable tables and limitations.

## Current Publication Recommendation

Do not submit as a final arXiv paper yet. The work is strong enough for an
internal technical report and close to a workshop-style benchmark draft. The
critical external-validity gap is now reduced by real-transfer v0.2, and the
open-weight VLM path has a real model-family contrast. The hosted OpenAI and
xAI and Claude rows now prove the provider path across three hosted-provider
families. The next bar is final paper polish, capture metadata, and optionally
adding a Gemini provider row.
