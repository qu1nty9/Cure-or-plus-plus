#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from cure_or_pp.labels import load_labels_from_config  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a zero-shot evaluation config without loading a model.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--allow-missing-manifests", action="store_true")
    args = parser.parse_args()

    config_path = resolve_project_path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    labels = load_labels_from_config(config, ROOT)
    check_required(config, ["clean_manifest_path", "distorted_manifest_path", "predictions_path", "summary_path"])

    missing = []
    for key in ["clean_manifest_path", "distorted_manifest_path"]:
        path = resolve_project_path(config[key])
        if not path.exists():
            missing.append((key, path))

    if missing and not args.allow_missing_manifests:
        for key, path in missing:
            print(f"Missing {key}: {path}")
        return 1

    print(f"Config: {config_path}")
    print(f"Labels: {len(labels)}")
    print(f"First labels: {', '.join(list(labels)[:5])}")
    duplicate_display_names = [
        label
        for label, count in Counter(labels.values()).items()
        if count > 1
    ]
    if duplicate_display_names:
        print(f"Duplicate display names: {', '.join(sorted(duplicate_display_names))}")
    for key, path in missing:
        print(f"Allowed missing {key}: {path}")
    print(f"Predictions path: {resolve_project_path(config['predictions_path'])}")
    print(f"Summary path: {resolve_project_path(config['summary_path'])}")
    return 0


def check_required(config: dict, keys: list[str]) -> None:
    missing = [key for key in keys if key not in config]
    if missing:
        raise KeyError(f"Missing config keys: {', '.join(missing)}")


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
