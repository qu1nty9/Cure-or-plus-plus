# VLM/API Track Plan v0.1

## Goal

Add a separate visual-language-model track for modern multimodal assistants and
open VLMs without mixing their open-ended response behavior into the CLIP,
OpenCLIP, and prototype-classifier leaderboard.

The track should answer:

> Do instruction-following VLMs preserve object-recognition decisions under the
> same clean, native CURE-OR, and real-transfer conditions that stress the
> current classifier-style baselines?

## Evaluation Unit

Use multiple-choice visual QA:

```text
Question: Which object category is shown in the image?
Answer with exactly one letter from the options.
```

The answer set should be fixed within a track. For real-transfer v0.2, use the
10 labels already present in the source-matched validation block. For a future
Full-CURE-OR VLM slice, use a budgeted subset of labels and rows so API cost and
latency stay controlled.

## Candidate Model Slots

Use model slots, not hard-coded claims about model availability:

- `openai_frontier_vlm`;
- `anthropic_frontier_vlm`;
- `google_frontier_vlm`;
- `xai_frontier_vlm`;
- `open_weight_vlm_large`;
- `open_weight_vlm_small`.

At run time, record the exact provider, model id, model version/date, endpoint,
temperature, max tokens, image preprocessing, and retry policy.

## Required Metrics

- clean source accuracy;
- transferred/native accuracy;
- source-matched accuracy drop;
- unparseable response rate;
- abstention rate;
- exact-answer extraction accuracy;
- source-level bootstrap confidence intervals for real-transfer rows;
- per-label failure table;
- raw response audit sample.

## Sanitized Response Schema

The evaluator expects a JSONL file with one row per prompt-pack sample:

```json
{"sample_id":"clean__clean__clean__10183","provider":"openai","model_id":"example_model","model_version":"2026-06-16","response_text":"A"}
```

Required fields:

- `sample_id`;
- `model_id`;
- one of `response_text`, `output_text`, `answer_text`, `response`, or
  `content`.

Recommended fields:

- `provider`;
- `model_version`;
- request date;
- temperature;
- image preprocessing note.

Raw provider payloads should stay outside Git unless explicitly sanitized.
The tracked evaluator reads only sanitized text responses.

## OpenAI-Compatible Runner

The repository includes a provider-agnostic runner for APIs that follow the
OpenAI Chat Completions or Responses image-input shape:

```bash
OPENAI_API_KEY=... .venv/bin/python scripts/run_openai_compatible_vlm.py \
  --provider openai \
  --model MODEL_ID_FROM_PROVIDER \
  --model-version YYYY-MM-DD_OR_PROVIDER_VERSION \
  --output reports/vlm_api_track_v01_responses_MODEL_ID.jsonl
```

Useful smoke-test commands:

```bash
.venv/bin/python scripts/run_openai_compatible_vlm.py \
  --provider smoke \
  --model oracle_smoke \
  --output /private/tmp/cure_or_pp_vlm_runner_smoke.jsonl \
  --limit 5 \
  --mock-oracle

.venv/bin/python scripts/evaluate_vlm_response_pack.py \
  --responses /private/tmp/cure_or_pp_vlm_runner_smoke.jsonl \
  --model-summary /private/tmp/cure_or_pp_vlm_runner_smoke_model_summary.csv \
  --recipe-table /private/tmp/cure_or_pp_vlm_runner_smoke_recipe_table.csv \
  --label-table /private/tmp/cure_or_pp_vlm_runner_smoke_label_table.csv \
  --audit-table /private/tmp/cure_or_pp_vlm_runner_smoke_audit.csv
```

For non-OpenAI providers that expose an OpenAI-compatible endpoint, set
`OPENAI_BASE_URL` and use the provider's API-key environment variable:

```bash
PROVIDER_API_KEY=... OPENAI_BASE_URL=https://provider.example/v1 \
  .venv/bin/python scripts/run_openai_compatible_vlm.py \
  --api-key-env PROVIDER_API_KEY \
  --provider provider_name \
  --model MODEL_ID_FROM_PROVIDER \
  --output reports/vlm_api_track_v01_responses_PROVIDER_MODEL.jsonl
```

If a provider still requires `max_tokens` instead of `max_completion_tokens`,
add:

```bash
--chat-token-parameter max_tokens
```

## Guardrails

- Keep raw provider responses and request metadata outside Git unless explicitly
  sanitized.
- Do not mix VLM/API rows into CLIP/OpenCLIP/prototype tables.
- Report model ids and dates exactly; do not use marketing names without
  version identifiers.
- Use zero temperature unless the provider does not allow it.
- Keep prompt text fixed across models.
- Cache responses by image hash, prompt hash, and model id.
- Keep local cache files under `data/vlm_api_cache/`; this path is ignored by
  Git.

## Minimum Useful Pilot

The first pilot should use real-transfer v0.2 only:

- 30 clean source images;
- 180 transferred outputs;
- 10 object labels;
- 210 total image-question rows per model.

This is small enough for API cost control and directly comparable to the
source-matched real-transfer report.

## Success Criterion

The VLM/API track is useful if it shows one of:

- a different robustness ordering from CLIP/OpenCLIP;
- lower real-transfer sensitivity despite stronger language priors;
- higher unparseable/abstention behavior under degraded images;
- label-specific failure modes that classifier-style baselines miss.

## Reproducibility Scripts

- `scripts/build_vlm_prompt_pack.py` builds the 210-row real-transfer v0.2
  prompt pack.
- `scripts/run_openai_compatible_vlm.py` runs cached OpenAI-compatible
  multimodal API calls and writes sanitized response JSONL files.
- `scripts/evaluate_vlm_response_pack.py` evaluates sanitized response JSONL
  files and writes model, recipe, label, and audit tables.
