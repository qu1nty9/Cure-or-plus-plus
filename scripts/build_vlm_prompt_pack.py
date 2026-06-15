#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a multiple-choice VLM/API prompt pack from real-transfer v0.2.")
    parser.add_argument("--config", default="configs/vlm_api_track_v01.json")
    args = parser.parse_args()

    config_path = resolve_project_path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8"))
    manifest_path = resolve_project_path(config["real_transfer_manifest_path"])
    prompt_pack_path = resolve_project_path(config["prompt_pack_path"])
    summary_path = resolve_project_path(config["summary_path"])

    manifest_rows = load_csv(manifest_path)
    if not manifest_rows:
        raise ValueError(f"No real-transfer manifest rows found: {manifest_path}")

    labels = config["labels"]
    label_order = list(labels.keys())
    options = [
        {"letter": LETTERS[index], "label": label, "display": labels[label]}
        for index, label in enumerate(label_order)
    ]

    prompt_rows = []
    prompt_rows.extend(build_clean_rows(manifest_rows, config, options, label_order))
    prompt_rows.extend(build_transfer_rows(manifest_rows, config, options, label_order))

    write_jsonl(prompt_pack_path, prompt_rows)
    write_summary(summary_path, config, prompt_rows, options)

    print(f"Prompt rows: {len(prompt_rows)}")
    print(f"Prompt pack: {prompt_pack_path}")
    print(f"Summary: {summary_path}")
    return 0


def build_clean_rows(
    manifest_rows: list[dict[str, str]],
    config: dict,
    options: list[dict[str, str]],
    label_order: list[str],
) -> list[dict]:
    by_source = {}
    for row in manifest_rows:
        by_source.setdefault(row["source_path"], row)

    output = []
    for source_path, row in sorted(by_source.items(), key=lambda item: item[0]):
        output.append(build_prompt_row(
            image_path=source_path,
            source_path=source_path,
            label=row["label"],
            family="clean",
            recipe="clean",
            repeat_id="clean",
            source_selection_id=row["source_selection_id"],
            question=config["question"],
            options=options,
            label_order=label_order,
        ))
    return output


def build_transfer_rows(
    manifest_rows: list[dict[str, str]],
    config: dict,
    options: list[dict[str, str]],
    label_order: list[str],
) -> list[dict]:
    output = []
    for row in manifest_rows:
        output.append(build_prompt_row(
            image_path=row["output_path"],
            source_path=row["source_path"],
            label=row["label"],
            family=row["family"],
            recipe=row["recipe"],
            repeat_id=row["repeat_id"],
            source_selection_id=row["source_selection_id"],
            question=config["question"],
            options=options,
            label_order=label_order,
        ))
    return output


def build_prompt_row(
    *,
    image_path: str,
    source_path: str,
    label: str,
    family: str,
    recipe: str,
    repeat_id: str,
    source_selection_id: str,
    question: str,
    options: list[dict[str, str]],
    label_order: list[str],
) -> dict:
    if label not in label_order:
        raise ValueError(f"Label {label!r} is not present in configured label order.")
    answer_index = label_order.index(label)
    answer_letter = LETTERS[answer_index]
    option_text = "\n".join(f"{option['letter']}. {option['display']}" for option in options)
    prompt = f"{question}\n\nOptions:\n{option_text}"
    sample_id = "__".join([family, recipe, repeat_id, Path(image_path).stem])
    return {
        "sample_id": sample_id,
        "image_path": image_path,
        "source_path": source_path,
        "family": family,
        "recipe": recipe,
        "repeat_id": repeat_id,
        "source_selection_id": source_selection_id,
        "label": label,
        "answer_letter": answer_letter,
        "answer_display": options[answer_index]["display"],
        "question": question,
        "options": options,
        "prompt": prompt,
        "expected_response_format": "single_letter",
    }


def write_summary(path: Path, config: dict, rows: list[dict], options: list[dict[str, str]]) -> None:
    family_counts = Counter(row["family"] for row in rows)
    recipe_counts = Counter(row["recipe"] for row in rows)
    label_counts = Counter(row["label"] for row in rows)
    summary = {
        "track_id": config["track_id"],
        "row_count": len(rows),
        "family_counts": dict(sorted(family_counts.items())),
        "recipe_counts": dict(sorted(recipe_counts.items())),
        "label_counts": dict(sorted(label_counts.items())),
        "option_count": len(options),
        "provider_model_slots": config.get("provider_model_slots", []),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
