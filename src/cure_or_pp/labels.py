from __future__ import annotations

import json
from pathlib import Path


def load_labels_from_config(config: dict, root: Path) -> dict[str, str]:
    if "labels" in config:
        return dict(config["labels"])

    labels_path = config.get("labels_path")
    if not labels_path:
        raise KeyError("Config must define either 'labels' or 'labels_path'.")

    path = resolve_project_path(labels_path, root)
    raw = json.loads(path.read_text(encoding="utf-8"))
    labels_key = config.get("labels_key", "objects")
    values = raw[labels_key]
    if labels_key == "objects":
        return {
            object_label_key(object_id, label): label
            for object_id, label in values.items()
        }
    return {normalize_label(label): label for label in values.values()}


def normalize_label(label: str) -> str:
    normalized = (
        label.strip()
        .lower()
        .replace("&", "and")
        .replace("/", " ")
        .replace("-", " ")
        .replace("_", " ")
    )
    return " ".join(normalized.split())


def object_label_key(object_id: str, label: str) -> str:
    normalized = normalize_label(label).replace(" ", "_")
    return f"object_{object_id.zfill(3)}_{normalized}"


def resolve_project_path(path: str | Path, root: Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return root / candidate
