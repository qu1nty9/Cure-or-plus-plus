# CURE-OR++ Paper Scaffold

This folder contains the working LaTeX scaffold for the serious CURE-OR++
technical report. It is intentionally not final-publication ready yet: the
current draft now includes Full-CURE-OR v0.4, real-transfer v0.2, and the first
open-weight VLM prompt-pack row, but still needs final citation/license checks,
venue formatting, and optional broader VLM/model coverage.

Validate paper sources and referenced assets without requiring a local TeX
runtime:

```bash
python3 scripts/check_paper_build.py
```

Compile locally after installing TeX Live/MacTeX command-line tools
(`latexmk`, `pdflatex`, and `kpsewhich`):

```bash
python3 scripts/check_paper_build.py --compile --require-tex --output-dir paper/build
```

Main source:

- `paper/main.tex`
- `paper/references.bib`

Inserted generated tables:

- `reports/full_cure_or_paper_tables_v04.tex`

Inserted generated figures:

- `results/real_transfer_v02_source_matched_drops.png`
- `results/real_transfer_v02_accuracy_heatmap.png`

Before public submission:

- verify bibliography metadata;
- decide final venue format;
- decide public release boundary for raw CURE-OR and real-transfer payloads;
- optionally add stronger/frontier VLM rows;
- replace placeholder related-work prose with final citations;
- update limitations after any added VLM/model rows.
