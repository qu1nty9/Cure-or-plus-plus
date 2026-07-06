# Anthropic Claude Sonnet 5 Full Provider Run v0.1

## Run

- Provider: Anthropic
- Model: `claude-sonnet-5`
- Endpoint: Messages API
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean and 180 real-transfer
- Temperature: omitted because this model rejects the parameter on the tested API path
- Initial output cap: `max_tokens=16`
- Targeted retry: one row retried with `max_tokens=64` after a visible empty response caused by `stop_reason=max_tokens`
- Merged response file: `reports/vlm_api_track_v01_responses_anthropic_claude_sonnet_5_merged_full.jsonl` (local, ignored by Git)

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.9333 | 0.0000 | 0.0000 |
| real-transfer | 180 | 0.9611 | 0.0000 | 0.0000 |

Overall real-transfer drop vs clean: `-0.0278`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `messenger_upload_download` | 60 | 0.9500 | -0.0167 |
| `phone_screenshot_resave` | 60 | 0.9833 | -0.0500 |
| `video_call_frame_capture` | 60 | 0.9500 | -0.0167 |

## Failure Concentration

The model made 9 total errors after the targeted retry: 2 clean errors and 7
real-transfer errors. The dominant weak labels are `calcium_bottle` and
`lg_cell_phone`, with real-transfer accuracies `0.7222` and `0.8889`,
respectively.

No rows were unparseable after the targeted retry, and there were no
abstentions or refusals.

## Usage

The local cache records:

- input tokens: `373059`
- output tokens: `691`
- hidden thinking tokens: `62`
- max-token stops in merged output: `1`
- end-turn stops in merged output: `209`

## Interpretation

Claude Sonnet 5 matches GPT-5.4-mini on real-transfer accuracy in the 210-row
provider block while showing a lower clean accuracy on this slice. The row is
useful because it adds an independent non-OpenAI, non-xAI hosted provider under
the same prompt pack, parser, and audit protocol.

## Artifacts

- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `audit.csv`: joined prompt/response correctness audit.
