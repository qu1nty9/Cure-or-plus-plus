# OpenAI GPT-5.4 Full Provider Run v0.1

## Run

- Provider: OpenAI
- Model: `gpt-5.4`
- Endpoint: Responses API
- Storage flag: `store=false`
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean and 180 real-transfer
- Temperature: omitted
- Output cap: `max_tokens=16`
- Sanitized response file: `reports/vlm_api_track_v01_responses_openai_gpt_5_4_full.jsonl` (local, ignored by Git)

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.9667 | 0.0000 | 0.0000 |
| real-transfer | 180 | 0.9556 | 0.0000 | 0.0000 |

Overall real-transfer drop vs clean: `0.0111`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `messenger_upload_download` | 60 | 0.9667 | 0.0000 |
| `phone_screenshot_resave` | 60 | 0.9500 | 0.0167 |
| `video_call_frame_capture` | 60 | 0.9500 | 0.0167 |

## Failure Concentration

The model made 8 real-transfer errors and 1 clean error. The dominant weak
label is `calcium_bottle`, with clean accuracy `0.6667` and real-transfer
accuracy `0.6667`. The hardest transfer pipelines are
`phone_screenshot_resave` and `video_call_frame_capture`.

No rows were unparseable, and there were no abstentions or refusals.

## Usage

The local cache records:

- input tokens: `334942`
- output tokens: `1050`
- total tokens: `335992`
- hidden reasoning tokens: `0`

## Interpretation

This row fills the middle OpenAI provider tier between GPT-5.4-mini and GPT-5.5
on the same 210-row CURE-OR++ provider prompt pack. It provides a clean
cost/quality comparison point: GPT-5.4 is slightly below GPT-5.4-mini on this
small slice but above GPT-5.5 in aggregate real-transfer accuracy, with zero
parser failures.

## Artifacts

- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `audit.csv`: joined prompt/response correctness audit.
