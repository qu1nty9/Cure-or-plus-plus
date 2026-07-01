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
    parser = argparse.ArgumentParser(description="Run a cached Anthropic Claude VLM over a CURE-OR++ prompt pack.")
    parser.add_argument("--prompt-pack", default="reports/vlm_api_track_v01_prompt_pack.jsonl")
    parser.add_argument("--output", required=True, help="Sanitized response JSONL output path.")
    parser.add_argument("--cache-dir", default="data/vlm_api_cache/anthropic")
    parser.add_argument("--provider", default="anthropic")
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-version", default="", help="Exact provider model version/date if known.")
    parser.add_argument("--base-url", default=os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com/v1"))
    parser.add_argument("--api-key-env", default="ANTHROPIC_API_KEY")
    parser.add_argument("--anthropic-version", default="2023-06-01")
    parser.add_argument("--env-file", help="Optional local KEY=VALUE env file, for example .secrets/anthropic.env.")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=8)
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
    print("Endpoint: messages")
    print(f"Provider/model: {args.provider}/{args.model}")
    print(f"Output: {output_path}")
    print(f"Cache dir: {cache_dir}")

    if args.dry_run:
        return 0

    if args.force and output_path.exists():
        output_path.unlink()

    if args.env_file:
        load_env_file(resolve_project_path(args.env_file))

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
        stop_reason = ""
    else:
        payload = build_payload(row, args, image_path)
        response_json, status_code = post_json(
            endpoint_url(args.base_url),
            payload,
            api_key=api_key,
            anthropic_version=args.anthropic_version,
            timeout=args.timeout,
            retries=args.retries,
            retry_sleep=args.retry_sleep,
        )
        response_text = extract_response_text(response_json)
        usage = response_json.get("usage", {})
        stop_reason = str(response_json.get("stop_reason", ""))

    cached = {
        "cached_at_utc": datetime.now(UTC).isoformat(),
        "provider": args.provider,
        "model_id": args.model,
        "model_version": args.model_version,
        "endpoint": "messages",
        "status_code": status_code,
        "stop_reason": stop_reason,
        "response_text": response_text,
        "usage": usage,
        "request_fingerprint": request_fingerprint,
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cached, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return build_output_row(row, args, cached, cache_key, image_hash, prompt_hash, from_cache=False)


def build_payload(row: dict, args: argparse.Namespace, image_path: Path) -> dict:
    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/jpeg"
    image_data = base64.b64encode(image_path.read_bytes()).decode("ascii")
    payload = {
        "model": args.model,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": row["prompt"]},
                ],
            }
        ],
    }
    if args.system_prompt:
        payload["system"] = args.system_prompt
    return payload


def post_json(
    url: str,
    payload: dict,
    *,
    api_key: str,
    anthropic_version: str,
    timeout: float,
    retries: int,
    retry_sleep: float,
) -> tuple[dict, int]:
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": anthropic_version,
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


def extract_response_text(response_json: dict) -> str:
    texts = []
    for item in response_json.get("content", []):
        if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str):
            texts.append(item["text"])
    return "\n".join(texts).strip()


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
        "endpoint": "messages",
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
        "endpoint": "messages",
        "base_url_origin": base_url_origin(args.base_url),
        "anthropic_version": args.anthropic_version,
        "image_sha256": image_hash,
        "prompt_sha256": prompt_hash,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "system_prompt_sha256": sha256_text(args.system_prompt or ""),
    }


def endpoint_url(base_url: str) -> str:
    return f"{base_url.rstrip('/')}/messages"


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


def load_env_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Env file not found: {path}")
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            raise ValueError(f"Invalid env line {path}:{line_number}; expected KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if not key:
            raise ValueError(f"Invalid empty env key at {path}:{line_number}")
        os.environ.setdefault(key, value)


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def safe_slug(text: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in text)


def base_url_origin(url: str) -> str:
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
