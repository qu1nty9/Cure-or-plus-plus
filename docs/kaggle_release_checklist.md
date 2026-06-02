# Kaggle Release Checklist

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
