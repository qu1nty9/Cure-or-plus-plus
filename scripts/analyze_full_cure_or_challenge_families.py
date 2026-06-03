#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPE_RE = re.compile(r"native_challenge_type_(\d{2})$")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Full-CURE-OR native challenge families.")
    parser.add_argument(
        "--comparison",
        default="results/full_cure_or_probe_v04_with_prototypes_comparison.csv",
        help="Native comparison CSV produced by compare_native_pilot.py.",
    )
    parser.add_argument(
        "--challenge-types",
        default="configs/cure_or_challenge_types_v01.json",
        help="Official CURE-OR challenge type mapping.",
    )
    parser.add_argument(
        "--channel-effects-output",
        default="results/full_cure_or_probe_v04_with_prototypes_channel_effects.csv",
    )
    parser.add_argument(
        "--paired-output",
        default="results/full_cure_or_probe_v04_with_prototypes_paired_channel_gaps.csv",
    )
    args = parser.parse_args()

    comparison_path = resolve_project_path(args.comparison)
    challenge_types_path = resolve_project_path(args.challenge_types)
    channel_effects_output = resolve_project_path(args.channel_effects_output)
    paired_output = resolve_project_path(args.paired_output)

    challenge_types = load_challenge_types(challenge_types_path)
    rows = load_native_rows(comparison_path, challenge_types)
    channel_effects = build_channel_effects(rows)
    paired_gaps = build_paired_gaps(rows)

    write_csv(channel_effects_output, channel_effects)
    write_csv(paired_output, paired_gaps)
    print(f"Channel effect rows: {len(channel_effects)}")
    print(f"Paired channel gap rows: {len(paired_gaps)}")
    print_headline(channel_effects, paired_gaps)
    return 0


def load_challenge_types(path: Path) -> dict[int, dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))["challenge_types"]
    output: dict[int, dict] = {}
    for key, value in raw.items():
        challenge_type = int(key)
        if 2 <= challenge_type <= 9:
            base_type = challenge_type
            channel = "color"
        elif 11 <= challenge_type <= 18:
            base_type = challenge_type - 9
            channel = "grayscale"
        else:
            continue

        base = raw[f"{base_type:02d}"]
        output[challenge_type] = {
            "challenge_type": f"{challenge_type:02d}",
            "display_name": value["display_name"],
            "base_type": f"{base_type:02d}",
            "base_name": base["name"],
            "base_display_name": base["display_name"],
            "channel": channel,
        }
    return output


def load_native_rows(path: Path, challenge_types: dict[int, dict]) -> list[dict]:
    rows = []
    with path.open("r", newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["family"] != "native_cure_or":
                continue
            match = TYPE_RE.match(row["recipe"])
            if not match:
                continue
            challenge_type = int(match.group(1))
            if challenge_type not in challenge_types:
                continue
            meta = challenge_types[challenge_type]
            rows.append(
                {
                    "model_name": row["model_name"],
                    "model_slug": row["model_slug"],
                    "severity": row["severity"],
                    "n": int(row["n"]),
                    "accuracy": float(row["accuracy"]),
                    "mean_confidence": float(row["mean_confidence"]),
                    **meta,
                }
            )
    return rows


def build_channel_effects(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str, str], list[dict]] = {}
    for row in rows:
        key = (row["model_name"], row["model_slug"], row["severity"], row["channel"])
        grouped.setdefault(key, []).append(row)

    output = []
    for (model_name, model_slug, severity, channel), group in sorted(grouped.items()):
        total_n = sum(row["n"] for row in group)
        output.append(
            {
                "model_name": model_name,
                "model_slug": model_slug,
                "severity": severity,
                "channel": channel,
                "n": total_n,
                "weighted_accuracy": weighted_mean(group, "accuracy"),
                "weighted_mean_confidence": weighted_mean(group, "mean_confidence"),
                "challenge_count": len(group),
            }
        )
    return output


def build_paired_gaps(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str, str], dict[str, dict]] = {}
    for row in rows:
        key = (row["model_name"], row["model_slug"], row["severity"], row["base_name"])
        grouped.setdefault(key, {})[row["channel"]] = row

    output = []
    for (model_name, model_slug, severity, base_name), pair in sorted(grouped.items()):
        color = pair.get("color")
        grayscale = pair.get("grayscale")
        if color is None or grayscale is None:
            continue
        output.append(
            {
                "model_name": model_name,
                "model_slug": model_slug,
                "severity": severity,
                "base_type": color["base_type"],
                "base_name": base_name,
                "base_display_name": color["base_display_name"],
                "color_accuracy": color["accuracy"],
                "grayscale_accuracy": grayscale["accuracy"],
                "grayscale_minus_color_accuracy": grayscale["accuracy"] - color["accuracy"],
                "color_mean_confidence": color["mean_confidence"],
                "grayscale_mean_confidence": grayscale["mean_confidence"],
                "grayscale_minus_color_confidence": grayscale["mean_confidence"] - color["mean_confidence"],
            }
        )
    return output


def weighted_mean(rows: list[dict], field: str) -> float:
    total_n = sum(row["n"] for row in rows)
    if total_n == 0:
        return 0.0
    return sum(row[field] * row["n"] for row in rows) / total_n


def print_headline(channel_effects: list[dict], paired_gaps: list[dict]) -> None:
    level5_effects = [row for row in channel_effects if row["severity"] == "level_5"]
    for row in level5_effects:
        if row["channel"] != "grayscale":
            continue
        color = next(
            (
                other
                for other in level5_effects
                if other["model_slug"] == row["model_slug"] and other["channel"] == "color"
            ),
            None,
        )
        if color is None:
            continue
        gap = float(row["weighted_accuracy"]) - float(color["weighted_accuracy"])
        print(
            f"{row['model_name']} level_5 grayscale-minus-color: "
            f"{gap:.4f} ({float(row['weighted_accuracy']):.4f} vs {float(color['weighted_accuracy']):.4f})"
        )

    worst_level5 = sorted(
        [row for row in paired_gaps if row["severity"] == "level_5"],
        key=lambda row: float(row["grayscale_accuracy"]),
    )[:5]
    print("Worst grayscale level_5 paired rows:")
    for row in worst_level5:
        print(
            f"  {row['model_name']} / {row['base_display_name']}: "
            f"gray={float(row['grayscale_accuracy']):.4f}, color={float(row['color_accuracy']):.4f}"
        )


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
