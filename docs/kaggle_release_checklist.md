# Kaggle Release Checklist

## Current Public Aggregate Package: v0.4.1

Ready locally:

- Public aggregate package:
  `kaggle/cure-or-plus-plus-v041-public`.
- Public notebook/writeup:
  `notebooks/cure_or_pp_kaggle_v041_public.ipynb`.
- Kaggle kernel folder:
  `kaggle/public_kernel_v041`.
- Kaggle writeup copy:
  `kaggle/writeup_v041.md`.
- Version DOI:
  `https://doi.org/10.5281/zenodo.21239828`.
- Release:
  `https://github.com/qu1nty9/Cure-or-plus-plus/releases/tag/v0.4.1`.

Package boundary:

- Includes aggregate reports, generated figures, release documentation,
  citation metadata, and reproducibility notes.
- Excludes raw CURE-OR images, mini-CURE-OR images, local real-transfer photos,
  source archives, provider raw JSONL files, provider caches, and credentials.

Validate before upload:

```bash
.venv/bin/python scripts/build_kaggle_publication_package.py \
  --output-dir kaggle/cure-or-plus-plus-v041-public \
  --kaggle-id yaroslavkholmirzayev/cure-or-plus-plus-v041-public \
  --clean

.venv/bin/python scripts/write_kaggle_publication_notebook.py

MPLCONFIGDIR=/private/tmp/cure_or_pp_mpl \
XDG_CACHE_HOME=/private/tmp/cure_or_pp_cache \
MPLBACKEND=Agg \
  .venv/bin/python scripts/validate_notebook.py \
  notebooks/cure_or_pp_kaggle_v041_public.ipynb
```

Expected notebook validation:

- Full-CURE-OR baseline rows: 8.
- Real-transfer model/pipeline rows: 12.
- Open-weight VLM rows: 7.
- Hosted-provider v0.1 rows: 9.
- Hosted-provider v0.3 rows: 1.

Upload after final manual review:

```bash
kaggle datasets create -p kaggle/cure-or-plus-plus-v041-public
kaggle kernels push -p kaggle/public_kernel_v041
```

If the Kaggle dataset already exists:

```bash
kaggle datasets version -p kaggle/cure-or-plus-plus-v041-public \
  -m "CURE-OR++ v0.4.1 public aggregate release"
```

## Legacy mini-CURE Package: v0.1

## Ready Locally

- Full mini-CURE-OR clean subset: 250 images.
- CURE-OR++ v0.1 distorted images: 6,750 images.
- CLIP ViT-B/32 predictions: 7,000 rows.
- CLIP ViT-B/16 predictions: 7,000 rows.
- OpenCLIP ViT-B/32 LAION2B predictions: 7,000 rows.
- SigLIP Base P16 224 predictions: 7,000 rows.
- CLIP ViT-B/32 test-split predictions: 2,800 rows.
- CLIP ViT-B/16 test-split predictions: 2,800 rows.
- OpenCLIP ViT-B/32 LAION2B test-split predictions: 2,800 rows.
- SigLIP Base P16 224 test-split predictions: 2,800 rows.
- HGNetV2-B0 prototype predictions: 2,800 rows.
- MobileNetV3-Small prototype predictions: 2,800 rows.
- Cross-model comparison, ranking, per-class failure, and confidence shift
  tables.
- Kaggle dataset package: `kaggle/cure-or-plus-plus-v01`.
- Kaggle notebook: `notebooks/cure_or_pp_kaggle_v01.ipynb`.
- Kaggle kernel folder: `kaggle/kernel`.

## Validate Before Upload

```bash
MPLCONFIGDIR=/private/tmp/cure_or_pp_mpl MPLBACKEND=Agg \
  .venv/bin/python scripts/validate_notebook.py notebooks/cure_or_pp_kaggle_v01.ipynb
```

Expected output:

- 250 clean images
- 6,750 distorted images
- 7,000 evaluated images
- clean accuracy 0.8280
- 13 code cells executed

## Update Username

Replace `USERNAME` or `YOUR_KAGGLE_USERNAME` in:

- `kaggle/cure-or-plus-plus-v01/dataset-metadata.json`
- `kaggle/kernel/kernel-metadata.json`

## Upload Dataset

```bash
kaggle datasets create -p kaggle/cure-or-plus-plus-v01
```

If the dataset already exists:

```bash
kaggle datasets version -p kaggle/cure-or-plus-plus-v01 -m "CURE-OR++ v0.1 release"
```

## Upload Notebook

```bash
kaggle kernels push -p kaggle/kernel
```

## Manual Kaggle Copy

Short description:

> CURE-OR++ v0.1 evaluates model robustness on 250 mini-CURE-OR clean images and
> 6,750 generated distortions, then compares two CLIP variants, OpenCLIP, a
> SigLIP diagnostic baseline, and two clean-train prototype image backbones on
> the mini-CURE-OR test split.

Main result:

> On the fair test split, `low_light_upload` is the strongest high-severity
> degradation for both CLIP variants, OpenCLIP, and HGNetV2-B0, while
> MobileNetV3-Small is most affected by `video_call_frame`. OpenCLIP provides a
> usable non-OpenAI contrastive baseline; SigLIP is retained as a diagnostic run
> because its clean accuracy is low under this prompt protocol.
