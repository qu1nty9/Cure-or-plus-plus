# Related Work Notes v0.1

CURE-OR++ should be positioned narrowly. It is not trying to replace broad VLM
robustness suites; it is a compact, object-centric benchmark for digital
transfer chains with reproducible image generation and easy per-class failure
inspection.

## Nearby Benchmarks

| Benchmark | Scope | Why CURE-OR++ is different |
| --- | --- | --- |
| R-Bench | Real-world robustness for large multimodal models, including a capture-to-reception corruption sequence, 33 corruption dimensions, 2,970 QA pairs, and 20 benchmarked LMMs. | CURE-OR++ is smaller and classification-focused, but easier to regenerate and inspect at the object/recipe/class level. |
| MLLM-IC | ICCV 2025 benchmark for MLLMs under image corruptions, with 40 corruption types and 34 low-level multimodal capabilities. | CURE-OR++ targets object recognition and digital transfer recipes rather than broad MLLM capability taxonomy. |
| VLM-RobustBench | Robustness benchmark for VLMs across 49 augmentation types and 133 corrupted settings on MMBench/MMMU-Pro. | CURE-OR++ keeps the recipe set small and transfer-chain-oriented so ranking shifts are easy to read and reproduce. |
| MMD-Bench / CLEAR | Degraded-image understanding benchmark across three severity levels and six standard multimodal benchmarks. | CURE-OR++ is not a model-training method; it is a lightweight measurement artifact for object-centric transfer degradation. |

## Positioning Claim

The safest claim for the first public release:

> CURE-OR++ complements broad VLM robustness benchmarks by measuring how compact
> object-recognition baselines react to realistic digital transfer chains. Its
> value is not scale; its value is transparent generation, paired clean/distorted
> metadata, and model ranking shifts that can be inspected by recipe and class.

## Sources

- R-Bench: https://arxiv.org/abs/2410.05474
- MLLM-IC: https://openaccess.thecvf.com/content/ICCV2025/html/Qiu_Benchmarking_Multimodal_Large_Language_Models_Against_Image_Corruptions_ICCV_2025_paper.html
- VLM-RobustBench: https://arxiv.org/abs/2603.06148
- CLEAR / MMD-Bench: https://arxiv.org/abs/2604.04780
