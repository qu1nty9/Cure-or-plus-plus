# Anthropic Claude Fable 5 Full Provider Run v0.1

## Run

- Provider: Anthropic
- Model: `claude-fable-5`
- Endpoint: Messages API
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean and 180 real-transfer
- Temperature: omitted
- Initial output cap: `max_tokens=64`
- Targeted retry: four rows retried with `max_tokens=128`
- Merged response file: `reports/vlm_api_track_v01_responses_anthropic_claude_fable_5_merged_full.jsonl` (local, ignored by Git)

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.9667 | 0.0333 | 0.0000 |
| real-transfer | 180 | 0.9611 | 0.0056 | 0.0000 |

Overall real-transfer drop vs clean: `0.0056`.

## Pipeline Results

| pipeline | n | accuracy | unparseable | drop vs clean |
|---|---:|---:|---:|---:|
| `messenger_upload_download` | 60 | 0.9667 | 0.0167 | 0.0000 |
| `phone_screenshot_resave` | 60 | 0.9667 | 0.0000 | 0.0000 |
| `video_call_frame_capture` | 60 | 0.9500 | 0.0000 | 0.0167 |

## Failure Concentration

The model made 8 total errors after the targeted retry: 1 clean error and 7
real-transfer errors. Two rows remained unparseable after retry, both tied to
the `calcium_bottle` source `12815`. The dominant weak label is
`calcium_bottle`, with real-transfer accuracy `0.6667`.

## Usage

The local cache records:

- input tokens: `373059`
- output tokens: `1253`
- hidden thinking tokens: `629`
- max-token stops in merged output: `2`
- end-turn stops in merged output: `208`

## Interpretation

Claude Fable 5 matches GPT-5.4-mini, Claude Sonnet 5, and Haiku 4.5 on
aggregate real-transfer accuracy in this 210-row slice, but it retains two
unparseable rows after retry. This is useful evidence that larger hosted
assistant models can still exhibit format/output-budget failure modes on a
strict one-letter recognition protocol.

## Artifacts

- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `audit.csv`: joined prompt/response correctness audit.
