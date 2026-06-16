#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import random
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SYSTEM_PROMPT = (
    "You are evaluating object recognition robustness. "
    "Answer with exactly one option letter and no explanation."
)
RETRYABLE_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a cached OpenAI-compatible VLM over a CURE-OR++ prompt pack."
    )
    parser.add_argument("--prompt-pack", default="reports/vlm_api_track_v01_prompt_pack.jsonl")
    parser.add_argument("--output", required=True, help="Sanitized response JSONL output path.")
    parser.add_argument("--cache-dir", default="data/vlm_api_cache/openai_compatible")
    parser.add_argument("--provider", default="openai_compatible")
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-version", default="", help="Exact provider model version/date if known.")
    parser.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    parser.add_argument("--api-key-env", default="OPENAI_API_KEY")
    parser.add_argument("--endpoint", choices=["chat_completions", "responses"], default="chat_completions")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=8)
    parser.add_argument(
        "--chat-token-parameter",
        choices=["max_completion_tokens", "max_tokens"],
        default="max_completion_tokens",
        help="Use max_tokens for providers that have not adopted max_completion_tokens.",
    )
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-sleep", type=float, default=2.0)
    parser.add_argument("--request-sleep", type=float, default=0.0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--family", choices=["clean", "real_transfer"])
    parser.add_argument("--recipe", action="append", help="Restrict to one or more recipes.")
    parser.add_argument("--sample-id", action="append", help="Restrict to one or more sample IDs.")
    parser.add_argument("--system-prompt", default=DEFAULT_SYSTEM_PROMPT)
    parser.add_argument("--force", action="store_true", help="Overwrite output and ignore existing output rows.")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and print planned work without API calls.")
    parser.add_argument(
        "--mock-oracle",
        action="store_true",
        help="Write ground-truth letters as responses. For runner/evaluator smoke tests only.",
    )
    args = parser.parse_args()

    prompt_rows = select_rows(load_jsonl(resolve_project_path(args.prompt_pack)), args)
    if args.limit is not None:
        prompt_rows = prompt_rows[: args.limit]

    missing_images = [row["image_path"] for row in prompt_rows if not resolve_project_path(row["image_path"]).exists()]
    if missing_images:
        raise FileNotFoundError(f"Missing image files: {missing_images[:5]} total={len(missing_images)}")

    output_path = resolve_project_path(args.output)
    cache_dir = resolve_project_path(args.cache_dir)
    completed_ids = set() if args.force else load_completed_sample_ids(output_path)
    pending_rows = [row for row in prompt_rows if row["sample_id"] not in completed_ids]

    print(f"Prompt rows selected: {len(prompt_rows)}")
    print(f"Already completed: {len(completed_ids & {row['sample_id'] for row in prompt_rows})}")
    print(f"Pending rows: {len(pending_rows)}")
    print(f"Endpoint: {args.endpoint}")
    print(f"Provider/model: {args.provider}/{args.model}")
    print(f"Output: {output_path}")
    print(f"Cache dir: {cache_dir}")

    if args.dry_run:
        return 0

    if args.force and output_path.exists():
        output_path.unlink()

    api_key = "" if args.mock_oracle else os.environ.get(args.api_key_env, "")
    if not args.mock_oracle and not api_key:
        raise RuntimeError(f"Missing API key environment variable: {args.api_key_env}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    with output_path.open("a", encoding="utf-8") as output_handle:
        for index, row in enumerate(pending_rows, start=1):
            result = run_row(row, args, api_key, cache_dir)
            output_handle.write(json.dumps(result, sort_keys=True) + "\n")
            output_handle.flush()
            written += 1
            if index % 10 == 0 or index == len(pending_rows):
                print(f"Processed {index}/{len(pending_rows)} pending rows")
            if args.request_sleep > 0 and index < len(pending_rows):
                time.sleep(args.request_sleep)

    print(f"Wrote rows: {written}")
    return 0


def run_row(row: dict, args: argparse.Namespace, api_key: str, cache_dir: Path) -> dict:
    image_path = resolve_project_path(row["image_path"])
    image_hash = sha256_file(image_path)
    prompt_hash = sha256_text(row["prompt"])
    request_fingerprint = build_request_fingerprint(
        row=row,
        args=args,
        image_hash=image_hash,
        prompt_hash=prompt_hash,
    )
    cache_key = sha256_text(json.dumps(request_fingerprint, sort_keys=True))
    cache_path = cache_dir / safe_slug(args.provider) / safe_slug(args.model) / f"{cache_key}.json"

    if cache_path.exists():
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        return build_output_row(row, args, cached, cache_key, image_hash, prompt_hash, from_cache=True)

    if args.mock_oracle:
        response_text = row["answer_letter"]
        usage = {}
        status_code = 0
    else:
        payload = build_payload(row, args, image_path)
        response_json, status_code = post_json(
            endpoint_url(args.base_url, args.endpoint),
            payload,
            api_key=api_key,
            timeout=args.timeout,
            retries=args.retries,
            retry_sleep=args.retry_sleep,
        )
        response_text = extract_response_text(response_json, args.endpoint)
        usage = response_json.get("usage", {})

    cached = {
        "cached_at_utc": datetime.now(UTC).isoformat(),
        "provider": args.provider,
        "model_id": args.model,
        "model_version": args.model_version,
        "endpoint": args.endpoint,
        "status_code": status_code,
        "response_text": response_text,
        "usage": usage,
        "request_fingerprint": request_fingerprint,
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cached, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return build_output_row(row, args, cached, cache_key, image_hash, prompt_hash, from_cache=False)


def build_payload(row: dict, args: argparse.Namespace, image_path: Path) -> dict:
    data_url = image_data_url(image_path)
    if args.endpoint == "responses":
        payload = {
            "model": args.model,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": row["prompt"]},
                        {"type": "input_image", "image_url": data_url},
                    ],
                }
            ],
            "temperature": args.temperature,
            "max_output_tokens": args.max_tokens,
        }
        if args.system_prompt:
            payload["instructions"] = args.system_prompt
        return payload

    messages = []
    if args.system_prompt:
        messages.append({"role": "system", "content": args.system_prompt})
    messages.append(
        {
            "role": "user",
            "content": [
                {"type": "text", "text": row["prompt"]},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        }
    )
    return {
        "model": args.model,
        "messages": messages,
        "temperature": args.temperature,
        args.chat_token_parameter: args.max_tokens,
    }


def post_json(
    url: str,
    payload: dict,
    *,
    api_key: str,
    timeout: float,
    retries: int,
    retry_sleep: float,
) -> tuple[dict, int]:
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                response_body = response.read().decode("utf-8")
                return json.loads(response_body), response.status
        except urllib.error.HTTPError as error:
            response_body = error.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"HTTP {error.code}: {response_body[:2000]}")
            if error.code not in RETRYABLE_STATUS_CODES or attempt >= retries:
                raise last_error
        except urllib.error.URLError as error:
            last_error = error
            if attempt >= retries:
                raise RuntimeError(f"Request failed: {error}") from error
        sleep_seconds = retry_sleep * (2 ** attempt) + random.uniform(0, 0.25)
        time.sleep(sleep_seconds)
    raise RuntimeError(f"Request failed after retries: {last_error}")


def extract_response_text(response_json: dict, endpoint: str) -> str:
    if endpoint == "responses":
        output_text = response_json.get("output_text")
        if isinstance(output_text, str):
            return output_text.strip()
        texts = []
        for item in response_json.get("output", []):
            for content in item.get("content", []):
                if isinstance(content, dict):
                    text = content.get("text")
                    if isinstance(text, str):
                        texts.append(text)
        return "\n".join(texts).strip()

    choices = response_json.get("choices", [])
    if not choices:
        return ""
    content = choices[0].get("message", {}).get("content", "")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        texts = [
            item.get("text", "")
            for item in content
            if isinstance(item, dict) and isinstance(item.get("text"), str)
        ]
        return "\n".join(texts).strip()
    return str(content).strip()


def build_output_row(
    row: dict,
    args: argparse.Namespace,
    cached: dict,
    cache_key: str,
    image_hash: str,
    prompt_hash: str,
    *,
    from_cache: bool,
) -> dict:
    return {
        "sample_id": row["sample_id"],
        "provider": args.provider,
        "model_id": args.model,
        "model_version": args.model_version,
        "endpoint": args.endpoint,
        "response_text": cached["response_text"],
        "cache_key": cache_key,
        "from_cache": from_cache,
        "image_sha256": image_hash,
        "prompt_sha256": prompt_hash,
        "request_date_utc": cached["cached_at_utc"],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
    }


def build_request_fingerprint(
    *,
    row: dict,
    args: argparse.Namespace,
    image_hash: str,
    prompt_hash: str,
) -> dict:
    return {
        "sample_id": row["sample_id"],
        "provider": args.provider,
        "model_id": args.model,
        "model_version": args.model_version,
        "endpoint": args.endpoint,
        "base_url_origin": base_url_origin(args.base_url),
        "image_sha256": image_hash,
        "prompt_sha256": prompt_hash,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "system_prompt_sha256": sha256_text(args.system_prompt or ""),
        "chat_token_parameter": args.chat_token_parameter if args.endpoint == "chat_completions" else "",
    }


def endpoint_url(base_url: str, endpoint: str) -> str:
    normalized = base_url.rstrip("/")
    if endpoint == "responses":
        return f"{normalized}/responses"
    return f"{normalized}/chat/completions"


def image_data_url(path: Path) -> str:
    mime_type = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def select_rows(rows: list[dict], args: argparse.Namespace) -> list[dict]:
    selected = rows
    if args.family:
        selected = [row for row in selected if row["family"] == args.family]
    if args.recipe:
        recipes = set(args.recipe)
        selected = [row for row in selected if row["recipe"] in recipes]
    if args.sample_id:
        sample_ids = set(args.sample_id)
        selected = [row for row in selected if row["sample_id"] in sample_ids]
    return selected


def load_completed_sample_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {
        row["sample_id"]
        for row in load_jsonl(path)
        if row.get("sample_id")
    }


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSON on {path}:{line_number}") from exc
    return rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def safe_slug(value: str) -> str:
    return "".join(character if character.isalnum() or character in "-._" else "_" for character in value)[:120]


def base_url_origin(base_url: str) -> str:
    parsed = urlparse(base_url)
    if not parsed.scheme or not parsed.netloc:
        return base_url.rstrip("/")
    return f"{parsed.scheme}://{parsed.netloc}"


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
