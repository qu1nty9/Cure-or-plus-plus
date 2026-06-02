from __future__ import annotations

from pathlib import Path
from typing import Iterable


def iter_images(input_dir: Path, extensions: Iterable[str]) -> list[Path]:
    normalized = {ext.lower() for ext in extensions}
    return sorted(
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in normalized
    )


def infer_label(path: Path, input_dir: Path) -> str:
    relative = path.relative_to(input_dir)
    if len(relative.parts) > 1:
        return relative.parts[0]
    return ""


def output_path_for(
    source_path: Path,
    input_dir: Path,
    output_dir: Path,
    recipe_name: str,
    severity: str,
) -> Path:
    relative = source_path.relative_to(input_dir)
    return output_dir / recipe_name / severity / relative.with_suffix(".jpg")

