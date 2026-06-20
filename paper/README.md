# CURE-OR++ Paper Scaffold

This folder contains the working LaTeX scaffold for the serious CURE-OR++
technical report. It is intentionally not final-publication ready yet: the
current draft now includes Full-CURE-OR v0.4, real-transfer v0.2, and the first
open-weight VLM prompt-pack row, but still needs final citation/license checks,
venue formatting, and optional broader VLM/model coverage.

Compile locally with:

```bash
python3 /Users/yaroslav/.codex/plugins/cache/openai-bundled/latex/0.2.2/scripts/compile_latex.py \
  /Users/yaroslav/Documents/CURE-OR++/paper/main.tex \
  --output-directory /private/tmp/cure_or_pp_paper_build
```

Main source:

- `paper/main.tex`
- `paper/references.bib`

Inserted generated tables:

- `reports/full_cure_or_paper_tables_v04.tex`

Before public submission:

- verify bibliography metadata;
- decide final venue format;
- decide public release boundary for raw CURE-OR and real-transfer payloads;
- optionally add stronger/frontier VLM rows;
- replace placeholder related-work prose with final citations;
- update limitations after any added VLM/model rows.
