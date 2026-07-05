# Hosted-Provider VLM Full v0.1 Comparison

## Scope

This table is generated from completed hosted-provider VLM runs on the CURE-OR++ 210-row real-transfer prompt pack.
Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`.
Raw provider response JSONL files are local artifacts; tracked tables contain only sanitized aggregates and audits.

## Model-Level Results

| model | provider | clean acc | real-transfer acc | drop | real errors | hardest pipeline | hardest label |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| OpenAI GPT-5.4-mini | openai | 0.9667 | 0.9611 | 0.0056 | 7 | `video_call_frame_capture` | `calcium_bottle` |
| OpenAI GPT-5.4 | openai | 0.9667 | 0.9556 | 0.0111 | 8 | `phone_screenshot_resave` | `calcium_bottle` |
| OpenAI GPT-5.5 | openai | 0.9667 | 0.9500 | 0.0167 | 9 | `video_call_frame_capture` | `calcium_bottle` |

## Pipeline Results

| model | WhatsApp | screenshot/resave | FaceTime frame |
| --- | --- | ---: | ---: |
| OpenAI GPT-5.4-mini | 0.9667 | 0.9833 | 0.9333 |
| OpenAI GPT-5.4 | 0.9667 | 0.9500 | 0.9500 |
| OpenAI GPT-5.5 | 0.9667 | 0.9500 | 0.9333 |

## Interpretation

The current hosted-provider leader is `OpenAI GPT-5.4-mini` with real-transfer accuracy `0.9611`.
This block should be interpreted separately from the open-weight VLM table because provider models have externally managed versioning, pricing, and data-handling policies.
