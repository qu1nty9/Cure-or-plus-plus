#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RECIPES = [
    {
        "recipe": "messenger_upload_download",
        "app_or_pipeline": "Messenger upload/download",
        "capture_notes": "Send the clean image through a messenger, then download the received image.",
    },
    {
        "recipe": "phone_screenshot_resave",
        "app_or_pipeline": "Phone screenshot/resave",
        "capture_notes": "Open the clean image on a phone, take a screenshot, crop only if needed, then resave/export.",
    },
    {
        "recipe": "video_call_frame_capture",
        "app_or_pipeline": "Video-call or screen-share frame capture",
        "capture_notes": "Show the clean image through a call or screen share and save a captured frame.",
    },
]

SOURCE_FIELDNAMES = [
    "selection_id",
    "label",
    "image_path",
    "object_id",
    "image_id",
    "background",
    "perspective",
    "split",
    "challenge_type",
    "challenge_level",
]

PAIR_FIELDNAMES = [
    "source_path",
    "output_path",
    "recipe",
    "severity",
    "app_or_pipeline",
    "label",
    "capture_device",
    "capture_date",
    "repeat_id",
    "pipeline_variant",
    "source_selection_id",
    "notes",
]

RECIPE_FIELDNAMES = [
    "recipe",
    "app_or_pipeline",
    "required_rows",
    "expected_folder",
    "capture_notes",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a balanced real-transfer validation protocol.")
    parser.add_argument("--clean-manifest", default="data/interim/cure_or_clean_test_manifest.csv")
    parser.add_argument("--output-dir", default="data/real_transfer/v02")
    parser.add_argument("--sources-per-label", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=2)
    args = parser.parse_args()

    clean_manifest = resolve_project_path(args.clean_manifest)
    output_dir = resolve_project_path(args.output_dir)
    if args.sources_per_label <= 0:
        raise ValueError("--sources-per-label must be positive")
    if args.repeats <= 0:
        raise ValueError("--repeats must be positive")

    clean_rows = read_csv(clean_manifest)
    selected = select_sources(clean_rows, args.sources_per_label)
    source_rows = build_source_rows(selected)
    pair_rows = build_pair_rows(source_rows, output_dir, args.repeats)
    recipe_rows = build_recipe_rows(output_dir, len(source_rows), args.repeats)

    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "source_selection_v02.csv", source_rows, SOURCE_FIELDNAMES)
    write_csv(output_dir / "pairs_template.csv", pair_rows, PAIR_FIELDNAMES)
    write_csv(output_dir / "recipe_plan_v02.csv", recipe_rows, RECIPE_FIELDNAMES)
    write_gitkeep_files(output_dir, args.repeats)

    print(f"Sources: {len(source_rows)}")
    print(f"Recipes: {len(RECIPES)}")
    print(f"Repeats: {args.repeats}")
    print(f"Planned transfer rows: {len(pair_rows)}")
    print(f"Wrote {output_dir / 'source_selection_v02.csv'}")
    print(f"Wrote {output_dir / 'pairs_template.csv'}")
    print(f"Wrote {output_dir / 'recipe_plan_v02.csv'}")
    return 0


def read_csv(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def select_sources(rows: list[dict], per_label: int) -> list[dict]:
    by_label: dict[str, list[dict]] = {}
    for row in rows:
        by_label.setdefault(row["label"], []).append(row)

    selected: list[dict] = []
    for label in sorted(by_label):
        candidates = sorted(by_label[label], key=lambda row: int(row["image_id"]))
        chosen: list[dict] = []
        used_backgrounds: set[str] = set()
        used_perspectives: set[str] = set()

        while len(chosen) < per_label and candidates:
            best = max(
                candidates,
                key=lambda row: (
                    row["perspective"] not in used_perspectives,
                    row["background"] not in used_backgrounds,
                    -int(row["image_id"]),
                ),
            )
            chosen.append(best)
            candidates.remove(best)
            used_backgrounds.add(best["background"])
            used_perspectives.add(best["perspective"])

        if len(chosen) < per_label:
            raise ValueError(f"Label {label!r} has only {len(chosen)} available clean test rows")
        selected.extend(sorted(chosen, key=lambda row: int(row["image_id"])))
    return selected


def build_source_rows(rows: list[dict]) -> list[dict]:
    output = []
    rank_by_label: dict[str, int] = {}
    for row in rows:
        label = row["label"]
        rank_by_label[label] = rank_by_label.get(label, 0) + 1
        output.append(
            {
                "selection_id": f"rtv02_{label}_{rank_by_label[label]:02d}",
                "label": label,
                "image_path": row["image_path"],
                "object_id": row["object_id"],
                "image_id": row["image_id"],
                "background": row["background"],
                "perspective": row["perspective"],
                "split": row["split"],
                "challenge_type": row["challenge_type"],
                "challenge_level": row["challenge_level"],
            }
        )
    return output


def build_pair_rows(source_rows: list[dict], output_dir: Path, repeats: int) -> list[dict]:
    output = []
    output_dir_text = relative_to_root(output_dir)
    for source in source_rows:
        source_stem = Path(source["image_path"]).stem
        for recipe in RECIPES:
            for repeat in range(1, repeats + 1):
                repeat_id = f"rep_{repeat:02d}"
                output_path = output_dir_text / "images" / recipe["recipe"] / repeat_id / f"{source_stem}.jpg"
                output.append(
                    {
                        "source_path": source["image_path"],
                        "output_path": str(output_path),
                        "recipe": recipe["recipe"],
                        "severity": "real",
                        "app_or_pipeline": recipe["app_or_pipeline"],
                        "label": source["label"],
                        "capture_device": "",
                        "capture_date": "",
                        "repeat_id": repeat_id,
                        "pipeline_variant": "",
                        "source_selection_id": source["selection_id"],
                        "notes": "",
                    }
                )
    return output


def build_recipe_rows(output_dir: Path, source_count: int, repeats: int) -> list[dict]:
    output_dir_text = relative_to_root(output_dir)
    rows = []
    for recipe in RECIPES:
        rows.append(
            {
                "recipe": recipe["recipe"],
                "app_or_pipeline": recipe["app_or_pipeline"],
                "required_rows": source_count * repeats,
                "expected_folder": str(output_dir_text / "images" / recipe["recipe"]),
                "capture_notes": recipe["capture_notes"],
            }
        )
    return rows


def write_gitkeep_files(output_dir: Path, repeats: int) -> None:
    for recipe in RECIPES:
        for repeat in range(1, repeats + 1):
            folder = output_dir / "images" / recipe["recipe"] / f"rep_{repeat:02d}"
            folder.mkdir(parents=True, exist_ok=True)
            (folder / ".gitkeep").write_text("", encoding="utf-8")


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def relative_to_root(path: Path) -> Path:
    try:
        return path.resolve().relative_to(ROOT)
    except ValueError:
        return path


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
