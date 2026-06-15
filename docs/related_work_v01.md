# Related Work v0.2

CURE-OR++ should be positioned narrowly. It is not trying to replace broad VLM
robustness suites. It is a compact, object-centric benchmark layer for native
CURE-OR challenge rows, digital transfer chains, real app/device transfers, and
easy per-class failure inspection.

## Nearby Benchmarks

| Benchmark | Evidence | Scope | Why CURE-OR++ is different |
| --- | --- | --- |
| R-Bench | arXiv:2410.05474 | Real-world robustness for large multimodal models, including a capture-to-reception corruption sequence, 33 corruption dimensions, 2,970 QA pairs, and 20 benchmarked LMMs. | CURE-OR++ is smaller and classification-focused, but easier to regenerate and inspect at the object/recipe/class level. The real-transfer v0.2 block is a compact counterpart, not a replacement. |
| MLLM-IC | ICCV 2025 | Benchmark for MLLMs under image corruptions, with 40 corruption types and 34 low-level multimodal capabilities. | CURE-OR++ targets object recognition and digital transfer recipes rather than broad MLLM capability taxonomy. |
| VLM-RobustBench | arXiv:2603.06148 | Robustness benchmark for VLMs across 49 augmentation types and 133 corrupted settings on MMBench/MMMU-Pro, evaluating Qwen, InternVL, Molmo, and Gemma families. | CURE-OR++ keeps the recipe set small and transfer-chain-oriented so ranking shifts are easy to read and reproduce. |
| MMD-Bench / CLEAR | arXiv:2604.04780 | Degraded-image understanding benchmark across three degradation severity levels and six standard multimodal benchmarks, paired with a generate-then-answer training framework. | CURE-OR++ is not a model-training method; it is a lightweight measurement artifact for object-centric transfer degradation. |

## Positioning Claim

The safest claim for the first public release:

> CURE-OR++ complements broad VLM robustness benchmarks by measuring how compact
> object-recognition baselines react to native CURE-OR challenge rows and
> realistic transfer pipelines. Its value is not scale; its value is transparent
> metadata, source-matched comparisons, and failure rankings that can be
> inspected by recipe and class.

## VLM/API Track Positioning

The planned VLM/API track should be framed as a separate multiple-choice visual
QA evaluation, not as another CLIP-style classifier row. It should report:

- exact provider/model id and date;
- prompt text and answer-extraction rule;
- clean source accuracy on the same source set;
- transferred/native accuracy;
- abstention/unparseable response rate;
- source-level bootstrap intervals for real-transfer rows;
- raw response logs kept outside Git if they contain provider metadata or
  paid-API traces.

This lets us compare modern multimodal assistants without pretending that their
open-ended text responses are directly equivalent to contrastive logits or
prototype classifier scores.

## Sources

- R-Bench: https://arxiv.org/abs/2410.05474
- MLLM-IC: https://openaccess.thecvf.com/content/ICCV2025/html/Qiu_Benchmarking_Multimodal_Large_Language_Models_Against_Image_Corruptions_ICCV_2025_paper.html
- VLM-RobustBench: https://arxiv.org/abs/2603.06148
- CLEAR / MMD-Bench: https://arxiv.org/abs/2604.04780
