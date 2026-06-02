# Kaggle Publishing Notes

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

