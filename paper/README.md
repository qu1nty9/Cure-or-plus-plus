# CURE-OR++ Paper Scaffold

This folder contains the working LaTeX source for the CURE-OR++ technical
report. The current draft includes Full-CURE-OR v0.4, real-transfer v0.2, eight
210-row open-weight VLM prompt-pack rows, seven 900-row open-weight VLM v0.3
extension rows, nine 210-row hosted-provider rows across OpenAI, xAI,
Anthropic, and GigaChat, and one 900-row xAI Grok 4.3 provider row with a
repeat run. The current public release boundary and submission checks are
tracked in `docs/public_release_checklist_v01.md`.

Validate paper sources and referenced assets without requiring a local TeX
runtime:

```bash
python3 scripts/check_paper_build.py
```

Compile locally after installing TeX Live/MacTeX/BasicTeX command-line tools
(`pdflatex`, `bibtex`, and `kpsewhich`; `latexmk` is optional):

```bash
python3 scripts/check_paper_build.py --compile --require-tex --output-dir /private/tmp/cure-or-pp-paper-check
```

Main source:

- `paper/main.tex`
- `paper/references.bib`

Inserted generated tables:

- `reports/full_cure_or_paper_tables_v04.tex`
- `reports/vlm_open_weight_full_v03_paper_table.tex`
- `reports/vlm_provider_full_v03_comparison.tex`
- `reports/vlm_provider_full_v01_comparison.tex`

Inserted generated figures:

- `results/real_transfer_v02_source_matched_drops.png`
- `results/real_transfer_v02_accuracy_heatmap.png`

Before public submission:

- pass `docs/public_release_checklist_v01.md`;
- verify bibliography metadata;
- decide final venue format;
- preserve the public release boundary for raw CURE-OR and real-transfer
  payloads;
- treat any additional provider rows as future extensions unless they directly
  improve the paper narrative;
- update limitations after any added VLM/model rows.
