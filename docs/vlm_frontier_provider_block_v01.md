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
| 1 | Google | `gemini-3.5-flash` | `scripts/run_gemini_vlm.py` | Usually the best first cost/latency probe. |
| 2 | OpenAI | `gpt-5.4-mini` | `scripts/run_openai_compatible_vlm.py` | OpenAI low-cost/latency contrast. |
| 3 | xAI | `grok-4.3` | `scripts/run_openai_compatible_vlm.py` | Grok provider contrast through an OpenAI-compatible Responses endpoint. |
| 4 | Anthropic | `claude-sonnet-4-6` | `scripts/run_anthropic_vlm.py` | Practical Claude frontier row. |
| 5 | OpenAI | `gpt-5.5` | `scripts/run_openai_compatible_vlm.py` | Strong flagship OpenAI row. |
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

## Privacy Boundary

Running this block sends prompt-pack images to an external provider. Do not run
full rows unless the user explicitly approves the specific provider/model and
understands that usage may be billed.

Rules:

- use smoke mode first: five mixed clean/real-transfer rows;
- use `temperature=0`;
- use `max_tokens=8`;
- use `store=false` on Responses-compatible providers when supported;
- keep raw provider payloads and cache files outside Git;
- track only sanitized `responses.jsonl`, aggregate CSVs, `audit.csv`, and
  summary text after reviewing that no key or private path is present.

## Smoke Commands

OpenAI:

```bash
.venv/bin/python scripts/run_openai_compatible_vlm.py \
  --env-file .secrets/openai.env \
  --provider openai \
  --model gpt-5.5 \
  --endpoint responses \
  --response-store false \
  --output reports/vlm_api_track_v01_responses_openai_gpt_5_5_smoke.jsonl \
  --limit 5
```

Gemini:

```bash
.venv/bin/python scripts/run_gemini_vlm.py \
  --env-file .secrets/gemini.env \
  --provider google_gemini \
  --model gemini-3.5-flash \
  --output reports/vlm_api_track_v01_responses_gemini_3_5_flash_smoke.jsonl \
  --limit 5
```

Anthropic:

```bash
.venv/bin/python scripts/run_anthropic_vlm.py \
  --env-file .secrets/anthropic.env \
  --provider anthropic \
  --model claude-sonnet-4-6 \
  --output reports/vlm_api_track_v01_responses_anthropic_claude_sonnet_4_6_smoke.jsonl \
  --limit 5
```

xAI:

```bash
.venv/bin/python scripts/run_openai_compatible_vlm.py \
  --env-file .secrets/xai.env \
  --api-key-env XAI_API_KEY \
  --provider xai \
  --model grok-4.3 \
  --base-url https://api.x.ai/v1 \
  --endpoint responses \
  --response-store false \
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
full rows:

- one OpenAI row;
- one Gemini row;
- one Claude or Grok row.

The ideal provider block is five or six full rows: OpenAI flagship, OpenAI
mini, Gemini, Claude Sonnet, Claude strongest-accessible, and Grok.
