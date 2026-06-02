#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZENODO_RECORD_API = "https://zenodo.org/api/records/4299330"


def main() -> int:
    parser = argparse.ArgumentParser(description="Download files from the mini-CURE-OR Zenodo record.")
    parser.add_argument("--output-dir", default="data/raw/mini_cure_or")
    parser.add_argument(
        "--files",
        nargs="+",
        default=["train.csv", "test.csv"],
        help="Files to download. Use train.zip/test.zip when ready for the image archives.",
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    output_dir = resolve_project_path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    record = fetch_json(ZENODO_RECORD_API)
    files = {item["key"]: item for item in record.get("files", [])}
    missing = [name for name in args.files if name not in files]
    if missing:
        print(f"Missing files in Zenodo record: {', '.join(missing)}")
        return 1

    for name in args.files:
        target_path = output_dir / name
        if target_path.exists() and not args.overwrite:
            print(f"Already exists: {display_path(target_path)}")
            continue

        file_info = files[name]
        size_mb = file_info.get("size", 0) / (1024 * 1024)
        url = file_info["links"]["self"]
        print(f"Downloading {name} ({size_mb:.1f} MB) -> {display_path(target_path)}")
        download_file(url, target_path)

    return 0


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))


def download_file(url: str, target_path: Path) -> None:
    with urllib.request.urlopen(url) as response, target_path.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)


def resolve_project_path(path: str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())

