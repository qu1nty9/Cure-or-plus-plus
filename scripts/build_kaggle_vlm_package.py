#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_SCRIPT_FILES = [
    "scripts/run_hf_vlm.py",
    "scripts/evaluate_vlm_response_pack.py",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a private Kaggle dataset folder for the VLM real-transfer pilot.")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--kaggle-id", default="YOUR_KAGGLE_USERNAME/cure-or-pp-vlm-real-transfer-v02-private")
    parser.add_argument("--title", default="CURE-OR++ VLM Real-Transfer v0.2 Private Pack")
    parser.add_argument("--api-config", default="configs/vlm_api_track_v01.json")
    parser.add_argument("--model-matrix", default="configs/vlm_open_weight_model_matrix_v01.json")
    parser.add_argument("--prompt-pack", default="")
    parser.add_argument("--no-images", action="store_true", help="Only copy metadata/scripts; skip image payloads.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    api_config_path = resolve_project_path(args.api_config)
    api_config = json.loads(api_config_path.read_text(encoding="utf-8"))
    prompt_pack_text = args.prompt_pack or api_config["prompt_pack_path"]
    prompt_pack_path = resolve_project_path(args.prompt_pack)
    if not args.prompt_pack:
        prompt_pack_path = resolve_project_path(prompt_pack_text)
    prompt_rows = load_jsonl(prompt_pack_path)
    image_paths = sorted({row["image_path"] for row in prompt_rows})

    copied_files = []
    include_files = [
        args.api_config,
        args.model_matrix,
        prompt_pack_text,
        api_config["summary_path"],
        *DEFAULT_SCRIPT_FILES,
    ]
    for path_text in include_files:
        copied_files.append(copy_project_file(path_text, output_dir))

    copied_images = []
    missing_images = []
    if not args.no_images:
        for image_path_text in image_paths:
            source_path = resolve_project_path(image_path_text)
            if not source_path.exists():
                missing_images.append(image_path_text)
                continue
            copied_images.append(copy_project_file(image_path_text, output_dir))

    if missing_images:
        raise FileNotFoundError(f"Missing images: {missing_images[:10]} total={len(missing_images)}")

    write_dataset_metadata(output_dir, args.kaggle_id, args.title)
    write_readme(output_dir, args.title, prompt_rows, copied_images)
    removed_artifacts = remove_macos_artifacts(output_dir)

    print(f"Output dir: {output_dir}")
    print(f"Prompt rows: {len(prompt_rows)}")
    print(f"Unique images: {len(image_paths)}")
    print(f"Copied files: {len(copied_files)}")
    print(f"Copied images: {len(copied_images)}")
    print(f"Removed macOS artifacts: {removed_artifacts}")
    print(f"dataset-metadata.json: {output_dir / 'dataset-metadata.json'}")
    return 0


def copy_project_file(path_text: str, output_dir: Path) -> Path:
    source_path = resolve_project_path(path_text)
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    destination_path = output_dir / path_text
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination_path)
    return destination_path


def write_dataset_metadata(output_dir: Path, kaggle_id: str, title: str) -> None:
    metadata = {
        "title": title,
        "id": kaggle_id,
        "licenses": [{"name": "unknown"}],
    }
    (output_dir / "dataset-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_readme(output_dir: Path, title: str, prompt_rows: list[dict], copied_images: list[Path]) -> None:
    text = f"""# {title}

This private Kaggle dataset folder contains the prompt pack, local scripts, and
image payloads needed to run the CURE-OR++ VLM real-transfer pilot on Kaggle GPU.

Rows: {len(prompt_rows)}
Copied images: {len(copied_images)}

This package is intended for private evaluation only. Do not publish raw CURE-OR
or local real-transfer image payloads unless their upstream terms permit it.
"""
    (output_dir / "README.md").write_text(text, encoding="utf-8")


def remove_macos_artifacts(output_dir: Path) -> int:
    removed = 0
    for path in output_dir.rglob("*"):
        if path.name == ".DS_Store" or path.name.startswith("._"):
            if path.is_file():
                path.unlink()
                removed += 1
    return removed


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


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
