# Open-Weight VLM Full v0.3 Comparison

## Scope

This table is generated from completed 900-row open-weight VLM runs on the CURE-OR++ v0.3 real-transfer protocol.
Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`.
Launch-only or incomplete result directories are intentionally excluded.

## Model-Level Results

| model | clean acc | real-transfer acc | drop | real errors | hardest pipeline | hardest label |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| LLaVA-OneVision-Qwen2-7B | 0.9800 | 0.9775 | 0.0025 | 18 | `video_call_frame_capture` | `canon_camera` |
| Qwen2.5-VL-7B | 0.9800 | 0.9613 | 0.0188 | 31 | `video_call_frame_capture` | `canon_camera` |
| SmolVLM2-2.2B | 0.9600 | 0.9575 | 0.0025 | 34 | `social_app_resave` | `lg_cell_phone` |
| LLaVA-OneVision-Qwen2-0.5B | 0.9300 | 0.9213 | 0.0088 | 63 | `video_call_frame_capture` | `dymo_label_maker` |
| Qwen2.5-VL-3B | 0.8800 | 0.7650 | 0.1150 | 188 | `video_call_frame_capture` | `calcium_bottle` |

## Pipeline Results

| model | WhatsApp | screenshot/resave | Instagram resave | FaceTime frame |
| --- | ---: | ---: | ---: | ---: |
| LLaVA-OneVision-Qwen2-7B | 0.9900 | 0.9850 | 0.9800 | 0.9550 |
| Qwen2.5-VL-7B | 0.9700 | 0.9650 | 0.9800 | 0.9300 |
| SmolVLM2-2.2B | 0.9600 | 0.9650 | 0.9500 | 0.9550 |
| LLaVA-OneVision-Qwen2-0.5B | 0.9400 | 0.9200 | 0.9300 | 0.8950 |
| Qwen2.5-VL-3B | 0.8650 | 0.6650 | 0.8900 | 0.6400 |

## Interpretation

The current leader is `LLaVA-OneVision-Qwen2-7B` with real-transfer accuracy `0.9775`.
The consensus hardest pipeline across completed models is `video_call_frame_capture`.
This generated table is the current main open-weight VLM benchmark block; optional additional full v0.3 runs extend it without changing the audit path.
