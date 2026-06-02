# mini-CURE-OR Notes

Source repositories:

- https://github.com/olivesgatech/CURE-OR
- https://github.com/olivesgatech/mini-CURE-OR
- https://zenodo.org/record/4299330

Zenodo files:

- `train.csv`: 9,900 rows
- `test.csv`: 6,600 rows
- `train.zip`: about 1.88 GB
- `test.zip`: about 1.53 GB

Clean source subset:

- Filter: `challengeType == 1` and `challengeLevel == 0`
- Total clean images: 250
- Split: 150 train, 100 test
- Classes: 10
- Clean images per class: 25

With the current v0 config:

- Recipes: 9
- Severity levels per recipe: 3
- Distorted outputs: 250 x 9 x 3 = 6,750

This is a good first benchmark size: small enough to run quickly, large enough
to produce stable per-class/per-distortion summaries.

