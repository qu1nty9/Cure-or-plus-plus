# Anthropic Claude Haiku 4.5 Full Provider Run v0.1

## Run

- Provider: Anthropic
- Model: `claude-haiku-4-5-20251001`
- Endpoint: Messages API
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean and 180 real-transfer
- Temperature: omitted
- Output cap: `max_tokens=16`
- Response file: `reports/vlm_api_track_v01_responses_anthropic_claude_haiku_4_5_full.jsonl` (local, ignored by Git)

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.9333 | 0.0000 | 0.0000 |
| real-transfer | 180 | 0.9500 | 0.0000 | 0.0000 |

Overall real-transfer drop vs clean: `-0.0167`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `messenger_upload_download` | 60 | 0.9500 | -0.0167 |
| `phone_screenshot_resave` | 60 | 0.9667 | -0.0333 |
| `video_call_frame_capture` | 60 | 0.9333 | 0.0000 |

## Failure Concentration

The model made 11 total errors: 2 clean errors and 9 real-transfer errors.
The dominant weak labels are `calcium_bottle`, `canon_camera`,
`lg_cell_phone`, and `training_marker_cone`. There were no unparseable
responses, abstentions, or refusals.

## Usage

The local cache records:

- input tokens: `274928`
- output tokens: `840`
- hidden thinking tokens: `0`
- max-token stops: `0`
- end-turn stops: `210`

## Interpretation

Claude Haiku 4.5 is a useful low-cost Anthropic contrast row. It is slightly
weaker than Sonnet/Fable on aggregate real-transfer accuracy, but it has better
format stability than Fable on this protocol, with zero unparseable responses
at a 16-token output cap.

## Artifacts

- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `audit.csv`: joined prompt/response correctness audit.
