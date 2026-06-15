#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SAMPLES = 5000
BOOTSTRAP_SEED = 20260616

ABSTENTION_PATTERNS = [
    "cannot determine",
    "can't determine",
    "can not determine",
    "unable to determine",
    "not enough information",
    "not sure",
    "unclear",
    "unknown",
    "i don't know",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate sanitized VLM/API responses against a CURE-OR++ prompt pack.")
    parser.add_argument("--prompt-pack", default="reports/vlm_api_track_v01_prompt_pack.jsonl")
    parser.add_argument("--responses", required=True, help="JSONL with sample_id, model_id, and response_text/output_text/answer_text.")
    parser.add_argument("--model-summary", default="reports/vlm_api_track_v01_model_summary.csv")
    parser.add_argument("--recipe-table", default="reports/vlm_api_track_v01_recipe_table.csv")
    parser.add_argument("--label-table", default="reports/vlm_api_track_v01_label_table.csv")
    parser.add_argument("--audit-table", default="reports/vlm_api_track_v01_response_audit.csv")
    args = parser.parse_args()

    prompt_rows = load_jsonl(resolve_project_path(args.prompt_pack))
    response_rows = load_jsonl(resolve_project_path(args.responses))
    prompt_by_id = {row["sample_id"]: row for row in prompt_rows}
    allowed_letters = sorted({option["letter"] for row in prompt_rows for option in row["options"]})

    joined_rows = join_responses(prompt_by_id, response_rows, allowed_letters)
    if not joined_rows:
        raise ValueError("No joined response rows. Check sample_id values in the response JSONL.")

    model_summary = build_model_summary(joined_rows)
    recipe_table = build_recipe_table(joined_rows)
    label_table = build_label_table(joined_rows)
    audit_rows = build_audit_rows(joined_rows)

    write_csv(resolve_project_path(args.model_summary), model_summary, MODEL_SUMMARY_FIELDS)
    write_csv(resolve_project_path(args.recipe_table), recipe_table, RECIPE_TABLE_FIELDS)
    write_csv(resolve_project_path(args.label_table), label_table, LABEL_TABLE_FIELDS)
    write_csv(resolve_project_path(args.audit_table), audit_rows, AUDIT_FIELDS)

    print(f"Prompt rows: {len(prompt_rows)}")
    print(f"Response rows: {len(response_rows)}")
    print(f"Joined rows: {len(joined_rows)}")
    print(f"Models: {len({row['model_id'] for row in joined_rows})}")
    print(f"Model summary: {resolve_project_path(args.model_summary)}")
    print(f"Recipe table: {resolve_project_path(args.recipe_table)}")
    print(f"Label table: {resolve_project_path(args.label_table)}")
    print(f"Audit table: {resolve_project_path(args.audit_table)}")
    return 0


MODEL_SUMMARY_FIELDS = [
    "model_id",
    "provider",
    "model_version",
    "clean_n",
    "clean_accuracy",
    "clean_unparseable_rate",
    "clean_abstention_rate",
    "real_n",
    "real_accuracy",
    "real_unparseable_rate",
    "real_abstention_rate",
    "accuracy_drop_vs_clean",
]

RECIPE_TABLE_FIELDS = [
    "model_id",
    "provider",
    "model_version",
    "recipe",
    "n",
    "accuracy",
    "accuracy_ci_low",
    "accuracy_ci_high",
    "unparseable_rate",
    "abstention_rate",
    "accuracy_drop_vs_clean",
    "accuracy_drop_ci_low",
    "accuracy_drop_ci_high",
]

LABEL_TABLE_FIELDS = [
    "model_id",
    "provider",
    "model_version",
    "label",
    "clean_n",
    "clean_accuracy",
    "real_n",
    "real_accuracy",
    "real_unparseable_rate",
    "accuracy_drop_vs_clean",
]

AUDIT_FIELDS = [
    "model_id",
    "provider",
    "model_version",
    "sample_id",
    "family",
    "recipe",
    "label",
    "answer_letter",
    "parsed_letter",
    "is_correct",
    "is_unparseable",
    "is_abstention",
    "response_text",
]


def join_responses(prompt_by_id: dict[str, dict], response_rows: list[dict], allowed_letters: list[str]) -> list[dict]:
    duplicate_counts = Counter(row.get("sample_id", "") for row in response_rows)
    duplicates = sorted(sample_id for sample_id, count in duplicate_counts.items() if sample_id and count > 1)
    if duplicates:
        raise ValueError(f"Duplicate response sample_id values: {duplicates[:5]}")

    output = []
    missing = []
    for response in response_rows:
        sample_id = response.get("sample_id")
        prompt = prompt_by_id.get(sample_id)
        if not prompt:
            missing.append(sample_id)
            continue
        response_text = read_response_text(response)
        parsed_letter = extract_letter(response_text, allowed_letters)
        is_unparseable = parsed_letter is None
        is_abstention = detect_abstention(response_text)
        output.append(
            {
                **prompt,
                "model_id": response.get("model_id", "unknown_model"),
                "provider": response.get("provider", ""),
                "model_version": response.get("model_version", ""),
                "response_text": response_text,
                "parsed_letter": parsed_letter or "",
                "is_unparseable": is_unparseable,
                "is_abstention": is_abstention,
                "is_correct": (parsed_letter == prompt["answer_letter"]) if parsed_letter else False,
            }
        )

    if missing:
        print(f"Skipped responses with unknown sample_id: {len(missing)}")
    return output


def build_model_summary(rows: list[dict]) -> list[dict]:
    output = []
    for model_key, model_rows in grouped(rows, model_key_fn).items():
        clean_rows = [row for row in model_rows if row["family"] == "clean"]
        real_rows = [row for row in model_rows if row["family"] == "real_transfer"]
        output.append(
            {
                **model_key_to_fields(model_key),
                "clean_n": len(clean_rows),
                "clean_accuracy": accuracy(clean_rows),
                "clean_unparseable_rate": rate(clean_rows, "is_unparseable"),
                "clean_abstention_rate": rate(clean_rows, "is_abstention"),
                "real_n": len(real_rows),
                "real_accuracy": accuracy(real_rows),
                "real_unparseable_rate": rate(real_rows, "is_unparseable"),
                "real_abstention_rate": rate(real_rows, "is_abstention"),
                "accuracy_drop_vs_clean": accuracy(clean_rows) - accuracy(real_rows),
            }
        )
    return sorted(output, key=lambda row: row["model_id"])


def build_recipe_table(rows: list[dict]) -> list[dict]:
    output = []
    for model_key, model_rows in grouped(rows, model_key_fn).items():
        clean_rows = [row for row in model_rows if row["family"] == "clean"]
        clean_accuracy = accuracy(clean_rows)
        for recipe, recipe_rows in grouped([row for row in model_rows if row["family"] == "real_transfer"], lambda row: row["recipe"]).items():
            bootstrap = bootstrap_source_matched(clean_rows, recipe_rows, model_key, recipe)
            output.append(
                {
                    **model_key_to_fields(model_key),
                    "recipe": recipe,
                    "n": len(recipe_rows),
                    "accuracy": accuracy(recipe_rows),
                    "accuracy_ci_low": bootstrap["real_accuracy_ci_low"],
                    "accuracy_ci_high": bootstrap["real_accuracy_ci_high"],
                    "unparseable_rate": rate(recipe_rows, "is_unparseable"),
                    "abstention_rate": rate(recipe_rows, "is_abstention"),
                    "accuracy_drop_vs_clean": clean_accuracy - accuracy(recipe_rows),
                    "accuracy_drop_ci_low": bootstrap["accuracy_drop_ci_low"],
                    "accuracy_drop_ci_high": bootstrap["accuracy_drop_ci_high"],
                }
            )
    return sorted(output, key=lambda row: (row["model_id"], row["recipe"]))


def build_label_table(rows: list[dict]) -> list[dict]:
    output = []
    for model_key, model_rows in grouped(rows, model_key_fn).items():
        labels = sorted({row["label"] for row in model_rows})
        for label in labels:
            clean_rows = [row for row in model_rows if row["family"] == "clean" and row["label"] == label]
            real_rows = [row for row in model_rows if row["family"] == "real_transfer" and row["label"] == label]
            output.append(
                {
                    **model_key_to_fields(model_key),
                    "label": label,
                    "clean_n": len(clean_rows),
                    "clean_accuracy": accuracy(clean_rows),
                    "real_n": len(real_rows),
                    "real_accuracy": accuracy(real_rows),
                    "real_unparseable_rate": rate(real_rows, "is_unparseable"),
                    "accuracy_drop_vs_clean": accuracy(clean_rows) - accuracy(real_rows),
                }
            )
    return sorted(output, key=lambda row: (row["model_id"], float(row["real_accuracy"]), row["label"]))


def build_audit_rows(rows: list[dict]) -> list[dict]:
    fields = set(AUDIT_FIELDS)
    return [
        {key: row[key] for key in AUDIT_FIELDS if key in fields}
        for row in sorted(rows, key=lambda row: (row["model_id"], row["sample_id"]))
    ]


def bootstrap_source_matched(clean_rows: list[dict], real_rows: list[dict], model_key: tuple[str, str, str], recipe: str) -> dict[str, float]:
    source_ids = sorted({row["source_selection_id"] for row in real_rows})
    clean_by_source = defaultdict(list)
    real_by_source = defaultdict(list)
    for row in clean_rows:
        clean_by_source[row["source_selection_id"]].append(row)
    for row in real_rows:
        real_by_source[row["source_selection_id"]].append(row)

    if not source_ids:
        return {
            "real_accuracy_ci_low": 0.0,
            "real_accuracy_ci_high": 0.0,
            "accuracy_drop_ci_low": 0.0,
            "accuracy_drop_ci_high": 0.0,
        }

    rng = random.Random(f"{BOOTSTRAP_SEED}:{model_key}:{recipe}")
    real_values = []
    drop_values = []
    for _ in range(BOOTSTRAP_SAMPLES):
        selected = [rng.choice(source_ids) for _ in source_ids]
        sampled_clean = [row for source_id in selected for row in clean_by_source.get(source_id, [])]
        sampled_real = [row for source_id in selected for row in real_by_source.get(source_id, [])]
        clean_acc = accuracy(sampled_clean)
        real_acc = accuracy(sampled_real)
        real_values.append(real_acc)
        drop_values.append(clean_acc - real_acc)

    return {
        "real_accuracy_ci_low": percentile(real_values, 0.025),
        "real_accuracy_ci_high": percentile(real_values, 0.975),
        "accuracy_drop_ci_low": percentile(drop_values, 0.025),
        "accuracy_drop_ci_high": percentile(drop_values, 0.975),
    }


def read_response_text(row: dict) -> str:
    for key in ["response_text", "output_text", "answer_text", "response", "content"]:
        value = row.get(key)
        if value is not None:
            return str(value).strip()
    return ""


def extract_letter(text: str, allowed_letters: list[str]) -> str | None:
    if not text:
        return None
    allowed = "".join(re.escape(letter) for letter in allowed_letters)
    normalized = text.strip().upper()
    exact = re.fullmatch(rf"[{allowed}]", normalized)
    if exact:
        return normalized
    candidates = re.findall(rf"(?<![A-Z])[{allowed}](?![A-Z])", normalized)
    unique = sorted(set(candidates))
    if len(unique) == 1:
        return unique[0]
    first_token = re.match(rf"^\s*([{allowed}])[\).\s:-]", normalized)
    if first_token:
        return first_token.group(1)
    return None


def detect_abstention(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in ABSTENTION_PATTERNS)


def accuracy(rows: list[dict]) -> float:
    if not rows:
        return 0.0
    return sum(1 for row in rows if row["is_correct"]) / len(rows)


def rate(rows: list[dict], key: str) -> float:
    if not rows:
        return 0.0
    return sum(1 for row in rows if row[key]) / len(rows)


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    index = round((len(values) - 1) * q)
    return values[index]


def model_key_fn(row: dict) -> tuple[str, str, str]:
    return (row["model_id"], row.get("provider", ""), row.get("model_version", ""))


def model_key_to_fields(model_key: tuple[str, str, str]) -> dict[str, str]:
    model_id, provider, model_version = model_key
    return {"model_id": model_id, "provider": provider, "model_version": model_version}


def grouped(rows: list[dict], key_fn) -> dict:
    groups = defaultdict(list)
    for row in rows:
        groups[key_fn(row)].append(row)
    return dict(groups)


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


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: format_value(row.get(key, "")) for key in fieldnames})


def format_value(value) -> str:
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
