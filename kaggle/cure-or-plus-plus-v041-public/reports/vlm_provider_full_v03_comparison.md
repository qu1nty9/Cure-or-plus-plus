# Hosted-Provider VLM Full v0.3 Comparison

## Scope

This table is generated from completed hosted-provider VLM runs on the CURE-OR++ 900-row v0.3 real-transfer prompt pack.
Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`.
Raw provider response JSONL files and caches are local artifacts; tracked tables contain only sanitized aggregates and audits.

## Model-Level Results

| model | provider | clean acc | real-transfer acc | drop | real errors | hardest pipeline | hardest label |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| xAI Grok 4.3 | xai | 0.9900 | 0.9788 | 0.0113 | 17 | `video_call_frame_capture` | `toy` |

## Pipeline Results

| model | WhatsApp | screenshot/resave | Instagram resave | FaceTime frame |
| --- | --- | ---: | ---: | ---: |
| xAI Grok 4.3 | 0.9950 | 0.9800 | 0.9900 | 0.9500 |

## Interpretation

The current hosted-provider v0.3 leader is `xAI Grok 4.3` with real-transfer accuracy `0.9788`.
This table should be interpreted separately from the open-weight v0.3 table because hosted providers have externally managed versioning, pricing, caching, and data-handling policies.
