#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "exports" / "arxiv_source_v0.4_preprint"

VERSION = "v0.4-preprint"

PAPER_SOURCE = ROOT / "paper" / "main.tex"
BIB_SOURCE = ROOT / "paper" / "references.bib"

REPORT_TEX_FILES = [
    ROOT / "reports" / "full_cure_or_paper_tables_v04.tex",
    ROOT / "reports" / "vlm_open_weight_full_v03_paper_table.tex",
    ROOT / "reports" / "vlm_provider_full_v03_comparison.tex",
    ROOT / "reports" / "vlm_provider_full_v01_comparison.tex",
]

FIGURE_FILES = [
    ROOT / "results" / "real_transfer_v02_source_matched_drops.png",
    ROOT / "results" / "real_transfer_v02_accuracy_heatmap.png",
]

FORBIDDEN_PARTS = {
    ".git",
    ".secrets",
    "secrets",
    "data",
    "cache",
    "raw",
    "processed",
    "interim",
    "vlm_api_cache",
}
FORBIDDEN_FILENAMES = {
    ".DS_Store",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build a clean CURE-OR++ arXiv/workshop source package."
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory to create. Defaults to exports/arxiv_source_v0.4_preprint.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the output directory first if it already exists.",
    )
    parser.add_argument(
        "--make-zip",
        action="store_true",
        help="Create a sibling .zip archive after building the source directory.",
    )
    parser.add_argument(
        "--version",
        default=VERSION,
        help=f"Release/version label to store in MANIFEST.json. Defaults to {VERSION}.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    ensure_inputs_exist()
    prepare_output_dir(output_dir, clean=args.clean)

    copied_files: list[Path] = []
    copied_files.append(write_staged_main(output_dir))
    copied_files.append(copy_file(BIB_SOURCE, output_dir / "references.bib"))

    for source in REPORT_TEX_FILES:
        copied_files.append(copy_file(source, output_dir / "reports" / source.name))
    for source in FIGURE_FILES:
        copied_files.append(copy_file(source, output_dir / "results" / source.name))

    copied_files.append(write_readme(output_dir, version=args.version))
    manifest_path = write_manifest(output_dir, copied_files, version=args.version)
    copied_files.append(manifest_path)

    remove_macos_sidecars(output_dir)
    validate_package(output_dir, copied_files)

    zip_path = None
    if args.make_zip:
        zip_path = make_zip(output_dir)

    print(f"Built arXiv source package: {output_dir}")
    print(f"Files: {len(copied_files)}")
    print(f"Manifest: {manifest_path}")
    if zip_path:
        print(f"Zip: {zip_path}")
    return 0


def ensure_inputs_exist() -> None:
    required = [PAPER_SOURCE, BIB_SOURCE, *REPORT_TEX_FILES, *FIGURE_FILES]
    missing = [path for path in required if not path.exists()]
    if missing:
        formatted = "\n".join(f"- {path}" for path in missing)
        raise SystemExit(f"Missing package inputs:\n{formatted}")


def prepare_output_dir(output_dir: Path, *, clean: bool) -> None:
    if output_dir.exists():
        if not clean:
            raise SystemExit(f"Output directory already exists: {output_dir}. Use --clean to replace it.")
        if output_dir == ROOT or ROOT in output_dir.parents and output_dir.name in {"paper", "reports", "results"}:
            raise SystemExit(f"Refusing to clean protected repository directory: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "reports").mkdir()
    (output_dir / "results").mkdir()


def write_staged_main(output_dir: Path) -> Path:
    text = PAPER_SOURCE.read_text(encoding="utf-8")
    text = text.replace("../reports/", "reports/")
    text = text.replace("../results/", "results/")

    if "../reports/" in text or "../results/" in text:
        raise SystemExit("Staged main.tex still contains repository-relative report/result paths.")

    target = output_dir / "main.tex"
    target.write_text(text, encoding="utf-8")
    return target


def copy_file(source: Path, target: Path) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target


def write_readme(output_dir: Path, *, version: str) -> Path:
    target = output_dir / "README.md"
    text = f"""# CURE-OR++ arXiv Source Package

Version: `{version}`

This directory is a staged LaTeX source package for the CURE-OR++ preprint. It
contains only paper source, bibliography, generated LaTeX tables, and generated
figures needed to compile `main.tex`.

It intentionally excludes raw CURE-OR images, mini-CURE-OR images,
real-transfer image payloads, provider API caches, raw hosted-provider response
JSONL files, credentials, source dataset archives, and repository metadata.

Build entrypoint:

```bash
tectonic -p main.tex
```

or with a traditional TeX toolchain:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Public contact: `yaric.kholm@gmail.com`.
"""
    target.write_text(text, encoding="utf-8")
    return target


def write_manifest(output_dir: Path, copied_files: list[Path], *, version: str) -> Path:
    target = output_dir / "MANIFEST.json"
    manifest = {
        "package": "CURE-OR++ arXiv source package",
        "version": version,
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_repository_commit": current_git_commit(),
        "source_root": str(ROOT),
        "policy": {
            "includes": [
                "paper source",
                "bibliography",
                "generated LaTeX tables",
                "generated figures",
                "package README",
            ],
            "excludes": [
                "raw CURE-OR images",
                "mini-CURE-OR images",
                "real-transfer image payloads",
                "provider API caches",
                "raw hosted-provider JSONL responses",
                "credentials",
                "source dataset archives",
                "repository metadata",
            ],
        },
        "files": [
            {
                "path": relative_to_package(path, output_dir),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in sorted(copied_files, key=lambda item: relative_to_package(item, output_dir))
        ],
    }
    target.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def validate_package(output_dir: Path, copied_files: list[Path]) -> None:
    sidecars = find_sidecars(output_dir)
    if sidecars:
        formatted = "\n".join(f"- {relative_to_package(path, output_dir)}" for path in sidecars)
        raise SystemExit(f"macOS sidecar files detected in source package:\n{formatted}")

    relative_paths = [Path(relative_to_package(path, output_dir)) for path in copied_files]
    forbidden = []
    for rel_path in relative_paths:
        lower_parts = {part.lower() for part in rel_path.parts}
        if lower_parts & FORBIDDEN_PARTS:
            forbidden.append(str(rel_path))
        if rel_path.name in FORBIDDEN_FILENAMES or rel_path.name.startswith("._"):
            forbidden.append(str(rel_path))
        if rel_path.suffix.lower() in {".env", ".jsonl", ".heic"}:
            forbidden.append(str(rel_path))

    if forbidden:
        formatted = "\n".join(f"- {item}" for item in sorted(set(forbidden)))
        raise SystemExit(f"Forbidden files detected in source package:\n{formatted}")

    main_text = (output_dir / "main.tex").read_text(encoding="utf-8")
    expected_refs = [
        output_dir / "reports" / source.name for source in REPORT_TEX_FILES
    ] + [
        output_dir / "results" / source.name for source in FIGURE_FILES
    ] + [
        output_dir / "references.bib",
    ]
    missing = [path for path in expected_refs if not path.exists()]
    if missing:
        formatted = "\n".join(f"- {path}" for path in missing)
        raise SystemExit(f"Staged package is missing expected references:\n{formatted}")

    if "../reports/" in main_text or "../results/" in main_text:
        raise SystemExit("main.tex contains repository-relative paths after staging.")


def make_zip(output_dir: Path) -> Path:
    zip_path = output_dir.parent / f"{output_dir.name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output_dir.rglob("*")):
            if path.is_dir():
                continue
            if path.name in FORBIDDEN_FILENAMES or path.name.startswith("._"):
                continue
            archive.write(path, arcname=relative_to_package(path, output_dir))
    return zip_path


def remove_macos_sidecars(output_dir: Path) -> None:
    for path in find_sidecars(output_dir):
        path.unlink()


def find_sidecars(output_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in output_dir.rglob("*")
        if path.is_file() and (path.name in FORBIDDEN_FILENAMES or path.name.startswith("._"))
    )


def current_git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unknown"
    return result.stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_to_package(path: Path, output_dir: Path) -> str:
    return path.resolve().relative_to(output_dir.resolve()).as_posix()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        raise SystemExit(130)
