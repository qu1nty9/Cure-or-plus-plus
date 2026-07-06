# xAI Grok 4.3 Full Provider Run v0.1

## Run

- Provider: xAI
- Model: `grok-4.3`
- Endpoint: Responses API
- Storage flag: `store=false`
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean and 180 real-transfer
- Temperature: `0.0`
- Reasoning effort: `none`
- Output cap: `max_tokens=16`
- Sanitized response file: `reports/vlm_api_track_v01_responses_xai_grok_4_3_no_reasoning_full.jsonl` (local, ignored by Git)

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.9667 | 0.0000 | 0.0000 |
| real-transfer | 180 | 0.9833 | 0.0000 | 0.0000 |

Overall real-transfer drop vs clean: `-0.0167`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `messenger_upload_download` | 60 | 1.0000 | -0.0333 |
| `phone_screenshot_resave` | 60 | 0.9667 | 0.0000 |
| `video_call_frame_capture` | 60 | 0.9833 | -0.0167 |

## Failure Concentration

The model made 3 real-transfer errors and 1 clean error. The dominant weak
label is `lg_cell_phone`, with clean accuracy `0.6667` and real-transfer
accuracy `0.8889`. The weakest transfer pipeline is
`phone_screenshot_resave`, though its accuracy still matches clean accuracy.

No rows were unparseable, and there were no abstentions or refusals.

## Usage

The local cache records:

- input tokens: `307316`
- cached input tokens: `38656`
- output tokens: `275`
- total tokens: `307591`
- hidden reasoning tokens: `0`
- provider-reported cost: `3442437000` USD ticks, approximately `$0.3442`

## Interpretation

This is the first completed non-OpenAI hosted-provider row in CURE-OR++. With
`reasoning.effort=none`, Grok 4.3 follows the single-letter protocol closely,
keeps output cost low, and currently leads the 210-row hosted-provider table in
real-transfer accuracy. The row is reported separately from open-weight VLMs
because xAI model versioning, pricing, caching, and data-handling behavior are
externally managed.

## Artifacts

- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `audit.csv`: joined prompt/response correctness audit.
