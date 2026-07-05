# OpenAI GPT-5.4-mini Full Provider Run v0.1

## Run

- Provider: OpenAI
- Model: `gpt-5.4-mini`
- Endpoint: Responses API
- Storage flag: `store=false`
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean and 180 real-transfer
- Temperature: `0.0`
- Output cap: `max_tokens=16`
- Sanitized response file: `reports/vlm_api_track_v01_responses_openai_gpt_5_4_mini_full.jsonl` (local, ignored by Git)

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.9667 | 0.0000 | 0.0000 |
| real-transfer | 180 | 0.9611 | 0.0000 | 0.0000 |

Overall real-transfer drop vs clean: `0.0056`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `messenger_upload_download` | 60 | 0.9667 | 0.0000 |
| `phone_screenshot_resave` | 60 | 0.9833 | -0.0167 |
| `video_call_frame_capture` | 60 | 0.9333 | 0.0333 |

## Failure Concentration

The model made 7 real-transfer errors and 1 clean error. The dominant weak
label is `calcium_bottle`, with clean accuracy `0.6667` and real-transfer
accuracy `0.7222`. The hardest transfer pipeline is `video_call_frame_capture`.

No rows were unparseable, and there were no abstentions or refusals.

## Usage

The local cache records:

- input tokens: `334942`
- output tokens: `1050`
- total tokens: `335992`

## Interpretation

This is the first completed hosted-provider VLM row in CURE-OR++. It confirms
that the provider runner, image transfer path, single-letter extraction, and
audit flow work end to end on the 210-row prompt pack. The row should be
reported separately from the open-weight VLM table because hosted models have
externally managed versioning, pricing, and data-handling policies.

## Artifacts

- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `audit.csv`: joined prompt/response correctness audit.
