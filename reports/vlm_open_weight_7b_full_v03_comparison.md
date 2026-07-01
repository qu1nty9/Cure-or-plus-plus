# Open-Weight 7B VLM Full v0.3 Comparison

## Scope

This comparison covers the first two completed 900-row open-weight 7B VLM runs
on the CURE-OR++ v0.3 real-transfer protocol:

- `Qwen/Qwen2.5-VL-7B-Instruct`, Kaggle kernel version 28
- `llava-hf/llava-onevision-qwen2-7b-ov-hf`, Kaggle kernel version 29

Both models were evaluated on the same prompt pack:
`reports/vlm_api_track_v03_prompt_pack.jsonl`, with 100 clean rows and 800
real-transfer rows.

## Model-Level Results

| model | clean acc | real-transfer acc | drop vs clean | real errors |
|---|---:|---:|---:|---:|
| Qwen2.5-VL-7B | 0.9800 | 0.9613 | 0.0188 | 31 |
| LLaVA-OneVision-Qwen2-7B | 0.9800 | 0.9775 | 0.0025 | 18 |

Both models produced fully parseable answers with zero abstentions.

## Pipeline Results

| model | WhatsApp | screenshot/resave | Instagram resave | FaceTime frame |
|---|---:|---:|---:|---:|
| Qwen2.5-VL-7B | 0.9700 | 0.9650 | 0.9800 | 0.9300 |
| LLaVA-OneVision-Qwen2-7B | 0.9900 | 0.9850 | 0.9800 | 0.9550 |

## Interpretation

LLaVA-OneVision-Qwen2-7B is stronger on this v0.3 open-weight 7B comparison,
with 13 fewer real-transfer errors and a smaller real-transfer drop. The
important shared pattern is stable across both models: `video_call_frame_capture`
is the hardest real-transfer pipeline.

This gives the project a defensible first VLM benchmark block: the result is not
just one model succeeding or failing, but two strong 7B VLMs showing the same
ordering of real-transfer difficulty.
