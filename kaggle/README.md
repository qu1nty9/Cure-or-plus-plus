# Kaggle Publishing Notes

## Public aggregate package: v0.4.1

Canonical public Kaggle links:

- Dataset:
  <https://www.kaggle.com/datasets/yaroslavkholmirzayev/cure-or-plus-plus-v041-public-flat>
- Notebook/writeup:
  <https://www.kaggle.com/code/yaroslavkholmirzayev/cure-or-v0-4-1-public-benchmark-writeup>

Do not cite the earlier `yaroslavkholmirzayev/cure-or-plus-plus-v041-public`
Kaggle slug. It is an incomplete upload caused by skipped nested folders. Use
the flat `...v041-public-flat` dataset as the public Kaggle artifact.

Use `kaggle/profile_writeup_v041.md` for Kaggle's profile-level **New writeup**
editor. It is a separate Project writeup draft, not the dataset README and not
the executable notebook.

Prepared writeup images:

- Media gallery:
  - `results/kaggle_writeup_media_v041_01_mean_accuracy.png`
  - `results/kaggle_writeup_media_v041_02_level5_ranking.png`
  - `results/kaggle_writeup_media_v041_03_real_transfer_drops.png`
  - `results/kaggle_writeup_media_v041_04_real_transfer_heatmap.png`
  - `results/kaggle_writeup_media_v041_05_grayscale_control.png`
  - `results/kaggle_writeup_media_v041_06_level5_overconfidence.png`
  - all are `640 x 360`.
- Card and thumbnail: `results/kaggle_writeup_card_thumbnail_v041.png`
  (`560 x 280`).

Build the current public aggregate package:

```bash
.venv/bin/python scripts/build_kaggle_publication_package.py \
  --output-dir kaggle/cure-or-plus-plus-v041-public \
  --kaggle-id yaroslavkholmirzayev/cure-or-plus-plus-v041-public \
  --layout nested \
  --clean

.venv/bin/python scripts/build_kaggle_publication_package.py \
  --output-dir kaggle/cure-or-plus-plus-v041-public-flat \
  --kaggle-id yaroslavkholmirzayev/cure-or-plus-plus-v041-public-flat \
  --layout flat \
  --clean
```

Build the reader-facing notebook/writeup:

```bash
.venv/bin/python scripts/write_kaggle_publication_notebook.py
```

Validate the notebook locally against the package:

```bash
MPLCONFIGDIR=/private/tmp/cure_or_pp_mpl \
XDG_CACHE_HOME=/private/tmp/cure_or_pp_cache \
MPLBACKEND=Agg \
  .venv/bin/python scripts/validate_notebook.py \
  notebooks/cure_or_pp_kaggle_v041_public.ipynb
```

Upload after final manual review:

```bash
kaggle datasets create -p kaggle/cure-or-plus-plus-v041-public-flat
kaggle kernels push -p kaggle/public_kernel_v041
```

If the dataset already exists:

```bash
kaggle datasets version -p kaggle/cure-or-plus-plus-v041-public-flat \
  -m "CURE-OR++ v0.4.1 public aggregate release"
```

Use `kaggle/cure-or-plus-plus-v041-public-flat` for Kaggle API uploads if the
CLI/server skips nested folders. The notebook supports both nested and flat
layouts.

Use `kaggle/writeup_v041.md` as the Kaggle description/writeup copy.

## Legacy mini-CURE package: v0.1

Build the local dataset folder:

```bash
python3 scripts/build_kaggle_package.py \
  --output-dir kaggle/cure-or-plus-plus-v01 \
  --kaggle-id YOUR_KAGGLE_USERNAME/cure-or-plus-plus-v01
```

The generated folder contains `dataset-metadata.json`, metadata CSVs, selected
clean source images, generated distorted images, baseline results, figures, and
citation notes.

Upload with the Kaggle API after setting your real dataset id:

```bash
kaggle datasets create -p kaggle/cure-or-plus-plus-v01
```

The Kaggle API expects `dataset-metadata.json` in the upload folder. Kaggle's
dataset metadata docs list `CC-BY-4.0` as a supported license id.
