#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]

CHECKLIST_FIELDNAMES = [
    "done",
    "source_selection_id",
    "label",
    "source_image_id",
    "source_pack_path",
    "source_path",
    "recipe",
    "repeat_id",
    "expected_output_path",
    "capture_device",
    "capture_date",
    "pipeline_variant",
    "notes",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a local collection pack for real-transfer validation.")
    parser.add_argument("--source-selection", default="data/real_transfer/v02/source_selection_v02.csv")
    parser.add_argument("--pairs-template", default="data/real_transfer/v02/pairs_template.csv")
    parser.add_argument("--output-dir", default="data/real_transfer/v02/collection_pack")
    parser.add_argument("--thumb-size", type=int, default=220)
    args = parser.parse_args()

    source_selection_path = resolve_project_path(args.source_selection)
    pairs_template_path = resolve_project_path(args.pairs_template)
    output_dir = resolve_project_path(args.output_dir)

    source_rows = read_csv(source_selection_path)
    pair_rows = read_csv(pairs_template_path)
    source_by_path = {row["image_path"]: row for row in source_rows}

    source_images_dir = output_dir / "source_images"
    source_images_dir.mkdir(parents=True, exist_ok=True)

    copied_sources = copy_sources(source_rows, source_images_dir)
    checklist_rows = build_checklist_rows(pair_rows, source_by_path, copied_sources)

    write_csv(output_dir / "collection_checklist.csv", checklist_rows, CHECKLIST_FIELDNAMES)
    write_html_index(output_dir / "index.html", source_rows, pair_rows, copied_sources)
    write_contact_sheet(output_dir / "source_contact_sheet.jpg", source_rows, copied_sources, args.thumb_size)

    print(f"Sources copied: {len(copied_sources)}")
    print(f"Checklist rows: {len(checklist_rows)}")
    print(f"Wrote {output_dir / 'index.html'}")
    print(f"Wrote {output_dir / 'collection_checklist.csv'}")
    print(f"Wrote {output_dir / 'source_contact_sheet.jpg'}")
    return 0


def copy_sources(rows: list[dict], output_dir: Path) -> dict[str, Path]:
    copied: dict[str, Path] = {}
    for row in rows:
        source_path_text = row["image_path"]
        source_path = resolve_project_path(source_path_text)
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        destination = output_dir / f"{row['selection_id']}__{Path(source_path_text).name}"
        shutil.copy2(source_path, destination)
        copied[source_path_text] = destination
    return copied


def build_checklist_rows(pair_rows: list[dict], source_by_path: dict[str, dict], copied_sources: dict[str, Path]) -> list[dict]:
    output = []
    for row in pair_rows:
        source = source_by_path[row["source_path"]]
        output.append(
            {
                "done": "",
                "source_selection_id": row["source_selection_id"],
                "label": row["label"],
                "source_image_id": source["image_id"],
                "source_pack_path": relative(copied_sources[row["source_path"]]),
                "source_path": row["source_path"],
                "recipe": row["recipe"],
                "repeat_id": row["repeat_id"],
                "expected_output_path": row["output_path"],
                "capture_device": "",
                "capture_date": "",
                "pipeline_variant": "",
                "notes": "",
            }
        )
    return output


def write_html_index(path: Path, source_rows: list[dict], pair_rows: list[dict], copied_sources: dict[str, Path]) -> None:
    pairs_by_source: dict[str, list[dict]] = {}
    for row in pair_rows:
        pairs_by_source.setdefault(row["source_path"], []).append(row)

    cards = []
    for source in source_rows:
        source_path = source["image_path"]
        copied = copied_sources[source_path]
        expected_rows = pairs_by_source[source_path]
        output_items = "\n".join(
            f"<li><code>{html.escape(row['recipe'])}/{html.escape(row['repeat_id'])}</code>: "
            f"<code>{html.escape(row['output_path'])}</code></li>"
            for row in expected_rows
        )
        cards.append(
            f"""
            <section class="card">
              <img src="{html.escape(copied.relative_to(path.parent).as_posix())}" alt="{html.escape(source['selection_id'])}">
              <div>
                <h2>{html.escape(source['selection_id'])}</h2>
                <p><strong>{html.escape(source['label'])}</strong> · image {html.escape(source['image_id'])} · background {html.escape(source['background'])} · perspective {html.escape(source['perspective'])}</p>
                <p>Use source file: <code>{html.escape(copied.relative_to(path.parent).as_posix())}</code></p>
                <ul>{output_items}</ul>
              </div>
            </section>
            """
        )

    document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>CURE-OR++ Real Transfer v0.2 Collection Pack</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 28px; color: #1f2933; }}
    h1 {{ margin-bottom: 4px; }}
    .meta {{ color: #52606d; margin-bottom: 24px; }}
    .card {{ display: grid; grid-template-columns: 180px 1fr; gap: 18px; padding: 16px 0; border-top: 1px solid #d9e2ec; }}
    .card img {{ width: 180px; height: 180px; object-fit: contain; background: #f5f7fa; border: 1px solid #d9e2ec; }}
    h2 {{ margin: 0 0 6px; font-size: 18px; }}
    p {{ margin: 4px 0 8px; }}
    ul {{ margin: 8px 0 0; padding-left: 18px; }}
    code {{ font-size: 12px; }}
  </style>
</head>
<body>
  <h1>CURE-OR++ Real Transfer v0.2 Collection Pack</h1>
  <p class="meta">30 sources · 3 pipelines · 2 repeats · 180 expected outputs</p>
  {''.join(cards)}
</body>
</html>
"""
    path.write_text(document, encoding="utf-8")


def write_contact_sheet(path: Path, source_rows: list[dict], copied_sources: dict[str, Path], thumb_size: int) -> None:
    columns = 5
    label_height = 54
    padding = 18
    rows = (len(source_rows) + columns - 1) // columns
    width = columns * thumb_size + (columns + 1) * padding
    height = rows * (thumb_size + label_height) + (rows + 1) * padding
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, source in enumerate(source_rows):
        row_index = index // columns
        col_index = index % columns
        x = padding + col_index * (thumb_size + padding)
        y = padding + row_index * (thumb_size + label_height + padding)
        image = Image.open(copied_sources[source["image_path"]]).convert("RGB")
        image.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)
        offset_x = x + (thumb_size - image.width) // 2
        offset_y = y + (thumb_size - image.height) // 2
        sheet.paste(image, (offset_x, offset_y))
        draw.rectangle((x, y, x + thumb_size, y + thumb_size), outline="#d9e2ec")
        label = f"{source['selection_id']}\n{source['label']}\n{source['image_id']}"
        draw.multiline_text((x, y + thumb_size + 6), label, fill="#1f2933", font=font, spacing=3)

    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, quality=92)


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
