# xAI Grok 4.3 Full Provider Run v0.3

## Run

- Provider: xAI
- Model: `grok-4.3`
- Endpoint: Responses API
- Storage flag: `store=false`
- Prompt pack: `reports/vlm_api_track_v03_prompt_pack.jsonl`
- Rows: 900 total, 100 clean and 800 real-transfer
- Temperature: `0.0`
- Reasoning effort: `none`
- Output cap: `max_tokens=16`
- Sanitized response file: `reports/vlm_api_track_v03_responses_xai_grok_4_3_no_reasoning_full.jsonl` (local, ignored by Git)

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 100 | 0.9900 | 0.0000 | 0.0000 |
| real-transfer | 800 | 0.9788 | 0.0000 | 0.0000 |

Overall real-transfer drop vs clean: `0.0113`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `messenger_upload_download` | 200 | 0.9950 | -0.0050 |
| `phone_screenshot_resave` | 200 | 0.9800 | 0.0100 |
| `social_app_resave` | 200 | 0.9900 | 0.0000 |
| `video_call_frame_capture` | 200 | 0.9500 | 0.0400 |

## Failure Concentration

The model made 17 real-transfer errors and 1 clean error. The dominant weak
labels are `toy` and `canon_camera`, with real-transfer accuracies `0.9125`
and `0.9375`, respectively. The hardest transfer pipeline is
`video_call_frame_capture`.

No rows were unparseable, and there were no abstentions or refusals.

## Usage

The local cache records:

- input tokens: `1276267`
- cached input tokens: `269312`
- output tokens: `1161`
- total tokens: `1277428`
- hidden reasoning tokens: `0`
- provider-reported cost: `13154586500` USD ticks, approximately `$1.3155`

## Interpretation

This is the first hosted-provider result on the 900-row CURE-OR++ v0.3 VLM
prompt pack. It provides a direct hosted-provider contrast to the open-weight
v0.3 table while preserving the same prompt pack, parser, and audit protocol.
Grok 4.3 slightly exceeds the strongest completed open-weight v0.3 row in
real-transfer accuracy on this slice, but it remains reported separately
because provider models have externally managed versioning, pricing, caching,
and data-handling policies.

## Artifacts

- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `audit.csv`: joined prompt/response correctness audit.
