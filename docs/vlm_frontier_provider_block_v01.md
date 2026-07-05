# Frontier/Provider VLM Block v0.1

## Goal

Add a provider-facing VLM comparison to the existing CURE-OR++ 210-row
real-transfer prompt pack without mixing hosted assistant results into the
CLIP/OpenCLIP/prototype leaderboard.

This block should answer:

- how current provider VLMs compare with the eight completed open-weight rows;
- whether provider models preserve object-recognition decisions across the same
  clean and real-transfer splits;
- whether failures are recognition errors, parser failures, abstentions, or
  provider-specific refusal/formatting behavior.

## Current Provider Matrix

The executable matrix is in `configs/vlm_frontier_provider_matrix_v01.json`.

Recommended first full rows after smoke:

| priority | provider | model | runner | reason |
| ---: | --- | --- | --- | --- |
| done | OpenAI | `gpt-5.4-mini` | `scripts/run_openai_compatible_vlm.py` | Completed first hosted-provider row. |
| done | OpenAI | `gpt-5.4` | `scripts/run_openai_compatible_vlm.py` | Completed middle OpenAI tier row. |
| done | OpenAI | `gpt-5.5` | `scripts/run_openai_compatible_vlm.py` | Completed flagship OpenAI row with targeted retry/merge. |
| 1 | Google | `gemini-3.5-flash` | `scripts/run_gemini_vlm.py` | Usually the best next cost/latency probe. |
| 3 | xAI | `grok-4.3` | `scripts/run_openai_compatible_vlm.py` | Grok provider contrast through an OpenAI-compatible Responses endpoint. |
| 4 | Anthropic | `claude-sonnet-4-6` | `scripts/run_anthropic_vlm.py` | Practical Claude frontier row. |
| 6 | Anthropic | `claude-fable-5` | `scripts/run_anthropic_vlm.py` | Strongest Claude row if the account has access. |

Model names are intentionally kept in config rather than prose-only notes. If a
provider changes access or aliases, update the matrix before running.

## Source Notes

- OpenAI docs list `gpt-5.5`, `gpt-5.4`, and `gpt-5.4-mini`, and state that
  latest OpenAI models support text and image input via the Responses API.
- OpenAI image-input docs show `input_image` examples for `gpt-5.5` and describe
  image detail behavior.
- Anthropic docs list current Claude model IDs, including `claude-fable-5`,
  `claude-opus-4-8`, `claude-sonnet-4-6`, and `claude-haiku-4-5`, and state that
  current Claude models support image input and vision.
- Anthropic vision docs document base64 image blocks for the Messages API.
- Google Gemini docs list current Gemini 3 models and give `gemini-3.5-flash`
  as a stable model-string example.
- xAI docs list `grok-4.3`, document OpenAI SDK usage with
  `base_url=https://api.x.ai/v1`, and document image-input constraints for
  image-input models.

## Completed Rows

| provider | model | prompt pack | clean | real-transfer | unparseable | notes |
| --- | --- | --- | ---: | ---: | ---: | --- |
| OpenAI | `gpt-5.4-mini` | `reports/vlm_api_track_v01_prompt_pack.jsonl` | 0.9667 | 0.9611 | 0.0000 | First completed hosted-provider row; hardest pipeline is FaceTime frame capture. |
| OpenAI | `gpt-5.4` | `reports/vlm_api_track_v01_prompt_pack.jsonl` | 0.9667 | 0.9556 | 0.0000 | Middle OpenAI tier row; no parser failures or abstentions. |
| OpenAI | `gpt-5.5` | `reports/vlm_api_track_v01_prompt_pack.jsonl` | 0.9667 | 0.9500 | 0.0000 | Flagship OpenAI row; targeted retries were needed because hidden reasoning consumed smaller output caps. |

## Privacy Boundary

Running this block sends prompt-pack images to an external provider. Do not run
full rows unless the user explicitly approves the specific provider/model and
understands that usage may be billed.

Rules:

- use smoke mode first via
  `reports/vlm_api_track_v01_mixed_smoke_prompt_pack.jsonl` with two clean rows
  and one row from each v0.2 real-transfer pipeline;
- use `temperature=0`;
- omit `temperature` for hosted models that reject the parameter, including
  the current GPT-5.4 and GPT-5.5 Responses API paths;
- use `reasoning.effort=low` for GPT-5.5 and allocate enough visible-output
  budget; a 16-token cap can be consumed entirely by hidden reasoning tokens;
- use the shortest accepted output cap (`max_tokens=16` for OpenAI-compatible
  Responses providers; `8` remains acceptable where provider APIs allow it);
- use `store=false` on Responses-compatible providers when supported;
- keep raw provider payloads and cache files outside Git;
- track only sanitized `responses.jsonl`, aggregate CSVs, `audit.csv`, and
  summary text after reviewing that no key or private path is present.

## Smoke Commands

OpenAI:

```bash
.venv/bin/python scripts/run_openai_compatible_vlm.py \
  --prompt-pack reports/vlm_api_track_v01_mixed_smoke_prompt_pack.jsonl \
  --env-file .secrets/openai.env \
  --provider openai \
  --model gpt-5.5 \
  --endpoint responses \
  --response-store false \
  --omit-temperature \
  --reasoning-effort low \
  --max-tokens 64 \
  --output reports/vlm_api_track_v01_responses_openai_gpt_5_5_smoke.jsonl \
  --limit 5
```

Gemini:

```bash
.venv/bin/python scripts/run_gemini_vlm.py \
  --prompt-pack reports/vlm_api_track_v01_mixed_smoke_prompt_pack.jsonl \
  --env-file .secrets/gemini.env \
  --provider google_gemini \
  --model gemini-3.5-flash \
  --output reports/vlm_api_track_v01_responses_gemini_3_5_flash_smoke.jsonl \
  --limit 5
```

Anthropic:

```bash
.venv/bin/python scripts/run_anthropic_vlm.py \
  --prompt-pack reports/vlm_api_track_v01_mixed_smoke_prompt_pack.jsonl \
  --env-file .secrets/anthropic.env \
  --provider anthropic \
  --model claude-sonnet-4-6 \
  --output reports/vlm_api_track_v01_responses_anthropic_claude_sonnet_4_6_smoke.jsonl \
  --limit 5
```

xAI:

```bash
.venv/bin/python scripts/run_openai_compatible_vlm.py \
  --prompt-pack reports/vlm_api_track_v01_mixed_smoke_prompt_pack.jsonl \
  --env-file .secrets/xai.env \
  --api-key-env XAI_API_KEY \
  --provider xai \
  --model grok-4.3 \
  --base-url https://api.x.ai/v1 \
  --endpoint responses \
  --response-store false \
  --max-tokens 16 \
  --output reports/vlm_api_track_v01_responses_xai_grok_4_3_smoke.jsonl \
  --limit 5
```

Evaluate any smoke output:

```bash
.venv/bin/python scripts/evaluate_vlm_response_pack.py \
  --responses reports/vlm_api_track_v01_responses_PROVIDER_MODEL_smoke.jsonl \
  --model-summary reports/vlm_api_track_v01_PROVIDER_MODEL_smoke_model_summary.csv \
  --recipe-table reports/vlm_api_track_v01_PROVIDER_MODEL_smoke_recipe_table.csv \
  --label-table reports/vlm_api_track_v01_PROVIDER_MODEL_smoke_label_table.csv \
  --audit-table reports/vlm_api_track_v01_PROVIDER_MODEL_smoke_audit.csv
```

## Full-Run Promotion Rule

Promote a provider/model to the 210-row full run only when:

- smoke completes 5/5 rows;
- `unparseable_rate` is 0 or the failure is scientifically interesting;
- no provider-side safety/refusal behavior blocks benign object-recognition
  prompts;
- the user approves cost and data transfer for that provider/model.

For the first serious public paper, the minimum useful provider block is three
full rows. Two OpenAI rows are now complete, so the remaining minimum is:

- one Gemini row;
- one Claude or Grok row.

The ideal provider block is five or six full rows: OpenAI flagship, OpenAI
mini, Gemini, Claude Sonnet, Claude strongest-accessible, and Grok.
