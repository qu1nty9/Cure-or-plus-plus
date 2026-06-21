#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SYSTEM_PROMPT = (
    "You are evaluating object recognition robustness. "
    "Answer with exactly one option letter and no explanation."
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a cached local Hugging Face VLM over a CURE-OR++ prompt pack.")
    parser.add_argument("--prompt-pack", default="reports/vlm_api_track_v01_prompt_pack.jsonl")
    parser.add_argument("--output", required=True, help="Sanitized response JSONL output path.")
    parser.add_argument("--cache-dir", default="data/vlm_api_cache/huggingface")
    parser.add_argument("--provider", default="huggingface")
    parser.add_argument("--model", default="HuggingFaceTB/SmolVLM2-500M-Video-Instruct")
    parser.add_argument("--model-version", default="", help="Revision, commit, or exact local model version if known.")
    parser.add_argument("--revision", default=None)
    parser.add_argument("--processor-kwargs-json", default="{}", help="JSON object passed to AutoProcessor.from_pretrained.")
    parser.add_argument("--model-kwargs-json", default="{}", help="JSON object merged into model from_pretrained kwargs.")
    parser.add_argument("--device-map", default="", help="Optional Transformers device_map value, for example 'auto'.")
    parser.add_argument(
        "--model-class",
        choices=[
            "AutoModelForImageTextToText",
            "AutoModelForVision2Seq",
            "LlavaOnevisionForConditionalGeneration",
            "Qwen2_5_VLForConditionalGeneration",
        ],
        default="AutoModelForImageTextToText",
    )
    parser.add_argument(
        "--generation-backend",
        choices=["chat_template", "qwen_vl_utils"],
        default="chat_template",
        help="How to turn chat messages into model inputs.",
    )
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--device", choices=["auto", "cpu", "cuda", "mps"], default="auto")
    parser.add_argument("--dtype", choices=["auto", "float32", "float16", "bfloat16"], default="auto")
    parser.add_argument(
        "--image-content-key",
        choices=["path", "url", "url_path", "image", "image_path"],
        default="path",
        help="How to reference local images inside the Transformers chat template.",
    )
    parser.add_argument("--max-tokens", type=int, default=8)
    parser.add_argument("--request-sleep", type=float, default=0.0)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--family", choices=["clean", "real_transfer"])
    parser.add_argument("--recipe", action="append", help="Restrict to one or more recipes.")
    parser.add_argument("--sample-id", action="append", help="Restrict to one or more sample IDs.")
    parser.add_argument("--system-prompt", default=DEFAULT_SYSTEM_PROMPT)
    parser.add_argument("--force", action="store_true", help="Overwrite output and ignore existing output rows.")
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and print planned work without loading a model.")
    parser.add_argument(
        "--mock-oracle",
        action="store_true",
        help="Write ground-truth letters as responses. For runner/evaluator smoke tests only.",
    )
    args = parser.parse_args()
    args.processor_kwargs = parse_json_object(args.processor_kwargs_json, "--processor-kwargs-json")
    args.model_kwargs = parse_json_object(args.model_kwargs_json, "--model-kwargs-json")

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
    print(f"Backend: transformers")
    print(f"Provider/model: {args.provider}/{args.model}")
    print(f"Model class: {args.model_class}")
    print(f"Output: {output_path}")
    print(f"Cache dir: {cache_dir}")

    if args.dry_run:
        return 0

    if args.force and output_path.exists():
        output_path.unlink()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cache_dir.mkdir(parents=True, exist_ok=True)

    runtime = None if args.mock_oracle else load_runtime(args)

    written = 0
    with output_path.open("a", encoding="utf-8") as output_handle:
        for index, row in enumerate(pending_rows, start=1):
            result = run_row(row, args, cache_dir, runtime)
            output_handle.write(json.dumps(result, sort_keys=True) + "\n")
            output_handle.flush()
            written += 1
            if index % 10 == 0 or index == len(pending_rows):
                print(f"Processed {index}/{len(pending_rows)} pending rows")
            if args.request_sleep > 0 and index < len(pending_rows):
                time.sleep(args.request_sleep)

    print(f"Wrote rows: {written}")
    return 0


def load_runtime(args: argparse.Namespace) -> dict:
    try:
        import torch
        import transformers
    except ImportError as exc:
        raise RuntimeError("Missing local VLM dependencies. Install torch, transformers, and pillow.") from exc

    model_class = getattr(transformers, args.model_class)
    processor = transformers.AutoProcessor.from_pretrained(
        args.model,
        revision=args.revision,
        trust_remote_code=args.trust_remote_code,
        **args.processor_kwargs,
    )
    device = choose_device(args.device, torch)
    dtype = choose_dtype(args.dtype, device, torch)

    load_kwargs = {
        "revision": args.revision,
        "trust_remote_code": args.trust_remote_code,
    }
    load_kwargs.update(args.model_kwargs)
    if dtype is not None:
        load_kwargs["torch_dtype"] = dtype
    if args.device_map:
        load_kwargs["device_map"] = args.device_map
    try:
        model = model_class.from_pretrained(args.model, **load_kwargs)
    except TypeError:
        if "torch_dtype" in load_kwargs:
            load_kwargs["dtype"] = load_kwargs.pop("torch_dtype")
        model = model_class.from_pretrained(args.model, **load_kwargs)

    if not args.device_map:
        model = model.to(device)
    model.eval()
    print(f"Loaded model on device={device} dtype={dtype} device_map={args.device_map or 'none'}")
    return {
        "torch": torch,
        "processor": processor,
        "model": model,
        "device": device,
        "dtype": dtype,
    }


def run_row(row: dict, args: argparse.Namespace, cache_dir: Path, runtime: dict | None) -> dict:
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
    else:
        if runtime is None:
            raise RuntimeError("Runtime is required unless --mock-oracle is set.")
        response_text = generate_response(row, args, image_path, runtime)

    cached = {
        "cached_at_utc": datetime.now(UTC).isoformat(),
        "provider": args.provider,
        "model_id": args.model,
        "model_version": args.model_version,
        "endpoint": "local_transformers",
        "response_text": response_text,
        "request_fingerprint": request_fingerprint,
    }
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(cached, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return build_output_row(row, args, cached, cache_key, image_hash, prompt_hash, from_cache=False)


def generate_response(row: dict, args: argparse.Namespace, image_path: Path, runtime: dict) -> str:
    torch = runtime["torch"]
    processor = runtime["processor"]
    model = runtime["model"]
    device = runtime["device"]
    dtype = runtime["dtype"]

    messages = build_messages(row, args, image_path)
    if args.generation_backend == "qwen_vl_utils":
        try:
            from qwen_vl_utils import process_vision_info
        except ImportError as exc:
            raise RuntimeError("Missing qwen-vl-utils. Install qwen-vl-utils for Qwen2.5-VL runs.") from exc
        prompt_text = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=False,
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[prompt_text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
    else:
        inputs = processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )
    inputs = move_inputs(inputs, device=device, dtype=dtype, torch=torch)
    input_length = inputs["input_ids"].shape[-1]
    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=args.max_tokens,
        )
    new_tokens = generated_ids[:, input_length:]
    decoded = processor.batch_decode(new_tokens, skip_special_tokens=True)
    return decoded[0].strip() if decoded else ""


def build_messages(row: dict, args: argparse.Namespace, image_path: Path) -> list[dict]:
    image_part: dict[str, str]
    if args.image_content_key == "url":
        image_part = {"type": "image", "url": image_path.resolve().as_uri()}
    elif args.image_content_key == "url_path":
        image_part = {"type": "image", "url": str(image_path.resolve())}
    elif args.image_content_key == "image":
        image_part = {"type": "image", "image": image_path.resolve().as_uri()}
    elif args.image_content_key == "image_path":
        image_part = {"type": "image", "image": str(image_path.resolve())}
    else:
        image_part = {"type": "image", "path": str(image_path.resolve())}
    content = [
        image_part,
        {"type": "text", "text": row["prompt"]},
    ]
    messages = [{"role": "user", "content": content}]
    if args.system_prompt:
        messages.insert(0, {"role": "system", "content": [{"type": "text", "text": args.system_prompt}]})
    return messages


def move_inputs(inputs: dict, *, device: str, dtype, torch):
    moved = {}
    for key, value in inputs.items():
        if hasattr(value, "to"):
            if torch.is_floating_point(value) and dtype is not None:
                moved[key] = value.to(device=device, dtype=dtype)
            else:
                moved[key] = value.to(device=device)
        else:
            moved[key] = value
    return moved


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
        "endpoint": "local_transformers",
        "response_text": cached["response_text"],
        "cache_key": cache_key,
        "from_cache": from_cache,
        "image_sha256": image_hash,
        "prompt_sha256": prompt_hash,
        "request_date_utc": cached["cached_at_utc"],
        "temperature": 0.0,
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
        "revision": args.revision or "",
        "endpoint": "local_transformers",
        "model_class": args.model_class,
        "generation_backend": args.generation_backend,
        "image_content_key": args.image_content_key,
        "image_sha256": image_hash,
        "prompt_sha256": prompt_hash,
        "max_tokens": args.max_tokens,
        "system_prompt_sha256": sha256_text(args.system_prompt or ""),
    }


def choose_device(requested: str, torch) -> str:
    if requested != "auto":
        return requested
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def choose_dtype(requested: str, device: str, torch):
    if requested == "float32":
        return torch.float32
    if requested == "float16":
        return torch.float16
    if requested == "bfloat16":
        return torch.bfloat16
    if requested == "auto":
        if device == "cuda":
            if hasattr(torch.cuda, "is_bf16_supported") and torch.cuda.is_bf16_supported():
                return torch.bfloat16
            return torch.float16
        return torch.float32
    return None


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


def parse_json_object(value: str, argument_name: str) -> dict:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{argument_name} must be valid JSON") from exc
    if not isinstance(parsed, dict):
        raise ValueError(f"{argument_name} must be a JSON object")
    return parsed


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


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
