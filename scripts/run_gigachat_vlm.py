#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
import random
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
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
    parser = argparse.ArgumentParser(description="Run a cached GigaChat VLM over a CURE-OR++ prompt pack.")
    parser.add_argument("--prompt-pack", default="reports/vlm_api_track_v01_prompt_pack.jsonl")
    parser.add_argument("--output", help="Sanitized response JSONL output path.")
    parser.add_argument("--cache-dir", default="data/vlm_api_cache/gigachat")
    parser.add_argument("--provider", default="gigachat")
    parser.add_argument("--model", default="GigaChat-2-Max")
    parser.add_argument("--model-version", default="", help="Exact provider model version/date if known.")
    parser.add_argument("--base-url", default=os.environ.get("GIGACHAT_BASE_URL", "https://gigachat.devices.sberbank.ru/api/v1"))
    parser.add_argument("--oauth-url", default=os.environ.get("GIGACHAT_OAUTH_URL", "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"))
    parser.add_argument("--auth-key-env", default="GIGACHAT_AUTH_KEY")
    parser.add_argument("--client-id-env", default="GIGACHAT_CLIENT_ID")
    parser.add_argument("--client-secret-env", default="GIGACHAT_CLIENT_SECRET")
    parser.add_argument("--access-token-env", default="GIGACHAT_ACCESS_TOKEN")
    parser.add_argument("--scope-env", default="GIGACHAT_SCOPE")
    parser.add_argument("--scope", default="GIGACHAT_API_PERS")
    parser.add_argument("--env-file", help="Optional local KEY=VALUE env file, for example secrets/gigachat.env.")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--omit-temperature", action="store_true")
    parser.add_argument("--max-tokens", type=int, default=16)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-sleep", type=float, default=2.0)
    parser.add_argument("--request-sleep", type=float, default=0.0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--family", choices=["clean", "real_transfer"])
    parser.add_argument("--recipe", action="append", help="Restrict to one or more recipes.")
    parser.add_argument("--sample-id", action="append", help="Restrict to one or more sample IDs.")
    parser.add_argument("--system-prompt", default=DEFAULT_SYSTEM_PROMPT)
    parser.add_argument("--delete-uploaded-files", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--cafile", help="Optional CA bundle path for GigaChat TLS verification.")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification for GigaChat endpoints.")
    parser.add_argument("--delete-file-id", action="append", help="Delete one or more previously uploaded GigaChat file IDs, then exit.")
    parser.add_argument("--force", action="store_true", help="Overwrite output and ignore existing output rows.")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and print planned work without API calls.")
    parser.add_argument(
        "--mock-oracle",
        action="store_true",
        help="Write ground-truth letters as responses. For runner/evaluator smoke tests only.",
    )
    args = parser.parse_args()

    if args.delete_file_id:
        if args.env_file:
            load_env_file(resolve_project_path(args.env_file))
        context = build_ssl_context(args)
        token = get_access_token(args, context)
        for file_id in args.delete_file_id:
            try_delete_file(args, token, file_id, context)
        print(f"Delete attempts completed: {len(args.delete_file_id)}")
        return 0

    if not args.output:
        parser.error("--output is required unless --delete-file-id is used.")

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
    print("Endpoint: chat/completions with file attachments")
    print(f"Provider/model: {args.provider}/{args.model}")
    print(f"Output: {output_path}")
    print(f"Cache dir: {cache_dir}")

    if args.dry_run:
        return 0

    if args.force and output_path.exists():
        output_path.unlink()

    if args.env_file:
        load_env_file(resolve_project_path(args.env_file))

    context = build_ssl_context(args)
    token = "" if args.mock_oracle else get_access_token(args, context)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    with output_path.open("a", encoding="utf-8") as output_handle:
        for index, row in enumerate(pending_rows, start=1):
            result = run_row(row, args, token, cache_dir, context)
            output_handle.write(json.dumps(result, sort_keys=True) + "\n")
            output_handle.flush()
            written += 1
            if index % 10 == 0 or index == len(pending_rows):
                print(f"Processed {index}/{len(pending_rows)} pending rows")
            if args.request_sleep > 0 and index < len(pending_rows):
                time.sleep(args.request_sleep)

    print(f"Wrote rows: {written}")
    return 0


def run_row(row: dict, args: argparse.Namespace, access_token: str, cache_dir: Path, context: ssl.SSLContext | None) -> dict:
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
        file_id = ""
    else:
        file_id = upload_file(args, access_token, image_path, context)
        try:
            payload = build_chat_payload(row, args, file_id)
            response_json, status_code = post_json(
                f"{normalized_base(args.base_url)}/chat/completions",
                payload,
                headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
                timeout=args.timeout,
                retries=args.retries,
                retry_sleep=args.retry_sleep,
                context=context,
            )
            response_text = extract_response_text(response_json)
            usage = response_json.get("usage", {})
        finally:
            if args.delete_uploaded_files and file_id:
                try_delete_file(args, access_token, file_id, context)

    cached = {
        "cached_at_utc": datetime.now(UTC).isoformat(),
        "provider": args.provider,
        "model_id": args.model,
        "model_version": args.model_version,
        "endpoint": "chat/completions",
        "status_code": status_code,
        "response_text": response_text,
        "usage": usage,
        "uploaded_file_id": file_id,
        "request_fingerprint": request_fingerprint,
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cached, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return build_output_row(row, args, cached, cache_key, image_hash, prompt_hash, from_cache=False)


def build_ssl_context(args: argparse.Namespace) -> ssl.SSLContext | None:
    if args.insecure:
        return ssl._create_unverified_context()
    if args.cafile:
        return ssl.create_default_context(cafile=str(resolve_project_path(args.cafile)))
    return None


def get_access_token(args: argparse.Namespace, context: ssl.SSLContext | None) -> str:
    existing = os.environ.get(args.access_token_env, "")
    if existing:
        return existing

    auth_key = os.environ.get(args.auth_key_env, "")
    if not auth_key:
        client_id = os.environ.get(args.client_id_env, "")
        client_secret = os.environ.get(args.client_secret_env, "")
        if client_id and client_secret:
            auth_key = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
    if not auth_key:
        raise RuntimeError(
            f"Missing GigaChat authorization credentials: set {args.auth_key_env} "
            f"or both {args.client_id_env} and {args.client_secret_env}"
        )
    authorization = auth_key if auth_key.lower().startswith("basic ") else f"Basic {auth_key}"
    scope = os.environ.get(args.scope_env, args.scope)
    body = urllib.parse.urlencode({"scope": scope}).encode("utf-8")
    headers = {
        "Accept": "application/json",
        "Authorization": authorization,
        "Content-Type": "application/x-www-form-urlencoded",
        "RqUID": str(uuid.uuid4()),
    }
    response_json, _ = post_bytes(
        args.oauth_url,
        body,
        headers=headers,
        timeout=args.timeout,
        retries=args.retries,
        retry_sleep=args.retry_sleep,
        context=context,
    )
    token = response_json.get("access_token", "")
    if not token:
        raise RuntimeError(f"GigaChat OAuth response did not include access_token: {response_json}")
    return token


def upload_file(args: argparse.Namespace, access_token: str, image_path: Path, context: ssl.SSLContext | None) -> str:
    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/jpeg"
    body, content_type = multipart_body(
        fields={"purpose": "general"},
        files={"file": (image_path.name, image_path.read_bytes(), mime_type)},
    )
    response_json, _ = post_bytes(
        f"{normalized_base(args.base_url)}/files",
        body,
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": content_type},
        timeout=args.timeout,
        retries=args.retries,
        retry_sleep=args.retry_sleep,
        context=context,
    )
    file_id = response_json.get("id", "")
    if not file_id:
        raise RuntimeError(f"GigaChat file upload response did not include id: {response_json}")
    return file_id


def try_delete_file(args: argparse.Namespace, access_token: str, file_id: str, context: ssl.SSLContext | None) -> None:
    quoted_file_id = urllib.parse.quote(file_id)
    headers = {"Authorization": f"Bearer {access_token}"}
    delete_attempts = [
        ("POST", f"{normalized_base(args.base_url)}/files/{quoted_file_id}/delete"),
        ("DELETE", f"{normalized_base(args.base_url)}/files/{quoted_file_id}"),
    ]
    last_error: Exception | None = None
    for method, url in delete_attempts:
        request = urllib.request.Request(url, data=b"" if method == "POST" else None, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=args.timeout, context=context) as response:
                response.read()
                return
        except Exception as error:  # noqa: BLE001
            last_error = error
    print(f"Warning: could not delete uploaded GigaChat file {file_id}: {last_error}", file=sys.stderr)


def build_chat_payload(row: dict, args: argparse.Namespace, file_id: str) -> dict:
    messages = []
    if args.system_prompt:
        messages.append({"role": "system", "content": args.system_prompt})
    messages.append({"role": "user", "content": row["prompt"], "attachments": [file_id]})
    payload = {
        "model": args.model,
        "messages": messages,
        "max_tokens": args.max_tokens,
    }
    if not args.omit_temperature:
        payload["temperature"] = args.temperature
    return payload


def post_json(
    url: str,
    payload: dict,
    *,
    headers: dict[str, str],
    timeout: float,
    retries: int,
    retry_sleep: float,
    context: ssl.SSLContext | None,
) -> tuple[dict, int]:
    return post_bytes(
        url,
        json.dumps(payload).encode("utf-8"),
        headers=headers,
        timeout=timeout,
        retries=retries,
        retry_sleep=retry_sleep,
        context=context,
    )


def post_bytes(
    url: str,
    body: bytes,
    *,
    headers: dict[str, str],
    timeout: float,
    retries: int,
    retry_sleep: float,
    context: ssl.SSLContext | None,
) -> tuple[dict, int]:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        request = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                response_body = response.read().decode("utf-8")
                return json.loads(response_body), response.status
        except urllib.error.HTTPError as error:
            response_body = error.read().decode("utf-8", errors="replace")
            last_error = RuntimeError(f"HTTP {error.code}: {response_body[:2000]}")
            if error.code not in RETRYABLE_STATUS_CODES or attempt >= retries:
                raise last_error
        except (TimeoutError, urllib.error.URLError, OSError) as error:
            last_error = error
            if attempt >= retries:
                raise
        sleep_for = retry_sleep * (2**attempt) + random.uniform(0, retry_sleep)
        time.sleep(sleep_for)
    if last_error:
        raise last_error
    raise RuntimeError("post_bytes failed without an error")


def multipart_body(fields: dict[str, str], files: dict[str, tuple[str, bytes, str]]) -> tuple[bytes, str]:
    boundary = f"----cure-or-pp-{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for name, value in fields.items():
        chunks.extend([
            f"--{boundary}\r\n".encode("ascii"),
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("ascii"),
            value.encode("utf-8"),
            b"\r\n",
        ])
    for name, (filename, content, mime_type) in files.items():
        chunks.extend([
            f"--{boundary}\r\n".encode("ascii"),
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode("utf-8"),
            f"Content-Type: {mime_type}\r\n\r\n".encode("ascii"),
            content,
            b"\r\n",
        ])
    chunks.append(f"--{boundary}--\r\n".encode("ascii"))
    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def extract_response_text(response_json: dict) -> str:
    choices = response_json.get("choices", [])
    if not choices:
        return ""
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts).strip()
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
        "endpoint": "chat/completions",
        "response_text": cached.get("response_text", ""),
        "cache_key": cache_key,
        "from_cache": from_cache,
        "image_sha256": image_hash,
        "prompt_sha256": prompt_hash,
        "request_date_utc": cached.get("cached_at_utc", ""),
        "temperature": "" if args.omit_temperature else args.temperature,
        "max_tokens": args.max_tokens,
    }


def build_request_fingerprint(row: dict, args: argparse.Namespace, image_hash: str, prompt_hash: str) -> dict:
    return {
        "provider": args.provider,
        "model_id": args.model,
        "model_version": args.model_version,
        "endpoint": "chat/completions",
        "base_url_origin": url_origin(args.base_url),
        "sample_id": row["sample_id"],
        "image_sha256": image_hash,
        "prompt_sha256": prompt_hash,
        "system_prompt_sha256": sha256_text(args.system_prompt or ""),
        "temperature": "" if args.omit_temperature else args.temperature,
        "max_tokens": args.max_tokens,
    }


def select_rows(rows: list[dict], args: argparse.Namespace) -> list[dict]:
    selected = rows
    if args.family:
        selected = [row for row in selected if row.get("family") == args.family]
    if args.recipe:
        recipes = set(args.recipe)
        selected = [row for row in selected if row.get("recipe") in recipes]
    if args.sample_id:
        sample_ids = set(args.sample_id)
        selected = [row for row in selected if row.get("sample_id") in sample_ids]
    return selected


def load_completed_sample_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    return {row.get("sample_id", "") for row in load_jsonl(path) if row.get("sample_id")}


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def load_env_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ[key.strip()] = value.strip().strip('"').strip("'")


def resolve_project_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def safe_slug(text: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in text)


def normalized_base(base_url: str) -> str:
    return base_url.rstrip("/")


def url_origin(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url
    return f"{parsed.scheme}://{parsed.netloc}"


if __name__ == "__main__":
    raise SystemExit(main())
