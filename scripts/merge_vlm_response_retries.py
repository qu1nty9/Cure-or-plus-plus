#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge VLM response JSONL files, with later retry files overriding earlier rows.")
    parser.add_argument("--prompt-pack", default="reports/vlm_api_track_v01_prompt_pack.jsonl")
    parser.add_argument("--base", required=True, help="Primary response JSONL.")
    parser.add_argument("--retry", action="append", default=[], help="Retry response JSONL. May be passed multiple times.")
    parser.add_argument("--output", required=True, help="Merged response JSONL output.")
    args = parser.parse_args()

    prompt_rows = load_jsonl(resolve_path(args.prompt_pack))
    prompt_ids = [row["sample_id"] for row in prompt_rows]
    expected_ids = set(prompt_ids)

    merged: dict[str, dict] = {}
    source_counts: dict[str, int] = {}
    for source in [args.base, *args.retry]:
        path = resolve_path(source)
        rows = load_jsonl(path)
        source_counts[relative_text(path)] = len(rows)
        for row in rows:
            sample_id = row.get("sample_id")
            if not sample_id:
                raise ValueError(f"Missing sample_id in {path}")
            if sample_id not in expected_ids:
                raise ValueError(f"Unknown sample_id in {path}: {sample_id}")
            merged[sample_id] = row

    missing = [sample_id for sample_id in prompt_ids if sample_id not in merged]
    if missing:
        raise ValueError(f"Merged output is missing {len(missing)} prompt rows; first missing={missing[:5]}")

    output_rows = [merged[sample_id] for sample_id in prompt_ids]
    output_path = resolve_path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for row in output_rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    empty = sum(not str(row.get("response_text", "")).strip() for row in output_rows)
    print(f"Sources: {source_counts}")
    print(f"Wrote rows: {len(output_rows)}")
    print(f"Empty response_text rows: {empty}")
    print(f"Output: {output_path}")
    return 0


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def resolve_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def relative_text(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
