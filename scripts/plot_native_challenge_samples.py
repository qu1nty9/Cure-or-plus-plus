#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import pandas as pd
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a contact sheet of native mini-CURE-OR challenge samples.")
    parser.add_argument("--manifest", default="data/interim/mini_cure_or_native_test_v01_manifest.csv")
    parser.add_argument("--output", default="results/native_challenge_level4_samples.png")
    parser.add_argument("--challenge-map", default="configs/cure_or_challenge_types_v01.json")
    parser.add_argument("--severity", default="level_4")
    parser.add_argument("--label", default=None, help="Optional object label to keep comparable samples.")
    parser.add_argument("--thumb-size", type=int, default=160)
    parser.add_argument("--columns", type=int, default=4)
    args = parser.parse_args()

    manifest_path = resolve_project_path(args.manifest)
    output_path = resolve_project_path(args.output)
    challenge_names = load_challenge_names(resolve_project_path(args.challenge_map))
    df = pd.read_csv(manifest_path)
    df = df[df["severity"] == args.severity].copy()
    if args.label:
        df = df[df["label"] == args.label].copy()
    if df.empty:
        raise ValueError("No rows left after applying severity/label filters.")

    rows = []
    for recipe, group in df.sort_values(["recipe", "label", "output_path"]).groupby("recipe"):
        row = group.iloc[0].to_dict()
        row["recipe"] = recipe
        rows.append(row)

    images = [load_thumb(resolve_project_path(row["output_path"]), args.thumb_size) for row in rows]
    sheet = build_sheet(images, rows, challenge_names, args.thumb_size, args.columns)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)
    print(f"Wrote {output_path}")
    print(f"Rows: {len(rows)}")
    return 0


def load_thumb(path: Path, size: int) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image = ImageOps.contain(image, (size, size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), "white")
    x = (size - image.width) // 2
    y = (size - image.height) // 2
    canvas.paste(image, (x, y))
    return canvas


def load_challenge_names(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {
        key: value["display_name"]
        for key, value in raw.get("challenge_types", {}).items()
        if isinstance(value, dict) and "display_name" in value
    }


def build_sheet(
    images: list[Image.Image],
    rows: list[dict],
    challenge_names: dict[str, str],
    thumb_size: int,
    columns: int,
) -> Image.Image:
    from PIL import ImageDraw, ImageFont

    label_height = 54
    gap = 14
    rows_count = math.ceil(len(images) / columns)
    width = columns * thumb_size + (columns + 1) * gap
    height = rows_count * (thumb_size + label_height) + (rows_count + 1) * gap
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for idx, (image, row) in enumerate(zip(images, rows)):
        col = idx % columns
        grid_row = idx // columns
        x = gap + col * (thumb_size + gap)
        y = gap + grid_row * (thumb_size + label_height + gap)
        sheet.paste(image, (x, y))
        challenge_type = row["recipe"].replace("native_challenge_type_", "")
        title = f"type {challenge_type}"
        subtitle = challenge_names.get(challenge_type, row["label"])
        draw.text((x, y + thumb_size + 6), title, fill="black", font=font)
        draw.text((x, y + thumb_size + 20), subtitle, fill="#444444", font=font)
        draw.text((x, y + thumb_size + 34), row["label"], fill="#666666", font=font)

    return sheet


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
