# GigaChat 2 Max Full Provider Run v0.1

## Run

- Provider: GigaChat
- Model: `GigaChat-2-Max`
- Endpoint: Chat Completions API with uploaded file attachments
- Prompt pack: `reports/vlm_api_track_v01_prompt_pack.jsonl`
- Rows: 210 total, 30 clean and 180 real-transfer
- Temperature: `0.0`
- Output cap: `max_tokens=16`
- TLS: `certs/russian_trusted_root_ca.pem`
- Response file: `reports/vlm_api_track_v01_responses_gigachat_2_max_full.jsonl` (local, ignored by Git)

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 30 | 0.9000 | 0.0000 | 0.0000 |
| real-transfer | 180 | 0.8778 | 0.0000 | 0.0000 |

Overall real-transfer drop vs clean: `0.0222`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `messenger_upload_download` | 60 | 0.8667 | 0.0333 |
| `phone_screenshot_resave` | 60 | 0.9167 | -0.0167 |
| `video_call_frame_capture` | 60 | 0.8500 | 0.0500 |

## Failure Concentration

The model made 25 total errors: 3 clean errors and 22 real-transfer errors.
The dominant weak labels are `canon_camera`, `dymo_label_maker`,
`hair_brush`, and `calcium_bottle`. There were no unparseable responses,
abstentions, or refusals.

## Usage

The local cache records:

- prompt tokens: `420350`
- completion tokens: `420`
- total tokens: `420770`
- precached prompt tokens: `6386`
- HTTP 200 responses: `210`
- rows served from smoke cache: `5`

## Interpretation

GigaChat 2 Max is a useful regional-provider contrast row. It is substantially
weaker than the OpenAI, xAI, and Anthropic provider rows on this 210-row
protocol, but it has stable one-letter formatting with zero unparseable
responses. Its weakness is object recognition under specific labels rather
than response-format compliance.

## Artifacts

- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `audit.csv`: joined prompt/response correctness audit.
