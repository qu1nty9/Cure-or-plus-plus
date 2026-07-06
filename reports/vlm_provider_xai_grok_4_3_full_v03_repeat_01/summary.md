# xAI Grok 4.3 Full Provider Repeat Run v0.3

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
- Repeat response file: `reports/vlm_api_track_v03_responses_xai_grok_4_3_no_reasoning_full_repeat_01.jsonl` (local, ignored by Git)

## Result

| split | n | accuracy | unparseable | abstention |
|---|---:|---:|---:|---:|
| clean | 100 | 0.9700 | 0.0000 | 0.0000 |
| real-transfer | 800 | 0.9788 | 0.0000 | 0.0000 |

Overall real-transfer drop vs clean: `-0.0088`.

## Pipeline Results

| pipeline | n | accuracy | drop vs clean |
|---|---:|---:|---:|
| `messenger_upload_download` | 200 | 0.9900 | -0.0200 |
| `phone_screenshot_resave` | 200 | 0.9800 | -0.0100 |
| `social_app_resave` | 200 | 0.9900 | -0.0200 |
| `video_call_frame_capture` | 200 | 0.9550 | 0.0150 |

## Repeatability

Compared with the first xAI Grok 4.3 v0.3 full run:

- real-transfer accuracy is unchanged: `0.9788` vs `0.9788`;
- clean accuracy changed from `0.9900` to `0.9700`;
- total answer disagreements: `8/900` (`0.0089`);
- clean answer disagreements: `2/100` (`0.0200`);
- real-transfer answer disagreements: `6/800` (`0.0075`);
- first-run errors: `18`; repeat-run errors: `20`;
- overlapping errors: `15`;
- real-transfer error overlap: `14/17`.

## Interpretation

This repeat run supports the use of the xAI v0.3 result as a stable hosted
provider measurement for the real-transfer split. The small clean-split drift
should be reported as provider nondeterminism or backend drift, despite
`temperature=0` and `reasoning.effort=none`.

## Artifacts

- `model_summary.csv`: clean vs real-transfer summary.
- `recipe_table.csv`: per-pipeline summary.
- `label_table.csv`: per-label summary.
- `audit.csv`: joined prompt/response correctness audit.
