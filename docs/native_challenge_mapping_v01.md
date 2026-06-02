# Native CURE-OR Challenge Mapping v0.1

The official challenge type mapping is pinned from the
[`olivesgatech/CURE-OR`](https://github.com/olivesgatech/CURE-OR) README. The
paper abstract also groups the controlled challenging conditions as
underexposure, overexposure, blur, contrast, dirty lens, image noise, resizing,
and loss of color information.

## Challenge Types

| Type | Challenge | Levels |
| --- | --- | --- |
| 01 | No challenge | 0 |
| 02 | Resize | 1-4 |
| 03 | Underexposure | 1-5 |
| 04 | Overexposure | 1-5 |
| 05 | Gaussian blur | 1-5 |
| 06 | Contrast | 1-5 |
| 07 | Dirty lens 1 | 1-5 |
| 08 | Dirty lens 2 | 1-5 |
| 09 | Salt & pepper noise | 1-5 |
| 10 | Grayscale | 0 |
| 11 | Grayscale resize | 1-4 |
| 12 | Grayscale underexposure | 1-5 |
| 13 | Grayscale overexposure | 1-5 |
| 14 | Grayscale gaussian blur | 1-5 |
| 15 | Grayscale contrast | 1-5 |
| 16 | Grayscale dirty lens 1 | 1-5 |
| 17 | Grayscale dirty lens 2 | 1-5 |
| 18 | Grayscale salt & pepper noise | 1-5 |

## Local mini-CURE-OR Test Grid

The local mini-CURE-OR test split currently includes challenge types 2-9 and
11-18 at levels 1-4. It excludes type 1 and type 10 because those are
level-0-only conditions, and it does not include level 5 in the local mini test
grid we evaluated.

The strongest level-4 failures are now interpretable:

- type 14: grayscale gaussian blur;
- type 18: grayscale salt & pepper noise;
- type 05: gaussian blur;
- type 09: salt & pepper noise;
- type 16: grayscale dirty lens 1.

The visual sanity sheet for level-4 canon camera examples is stored at
`results/native_challenge_level4_samples.png`.
