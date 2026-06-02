#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUBSETS = {
    "all": None,
    "first_probe": {
        "01_no_challenge.tar.gz",
        "02_resize.tar.gz",
        "05_blur.tar.gz",
        "09_saltpepper.tar.gz",
        "14_grayscale_blur.tar.gz",
        "18_grayscale_saltpepper.tar.gz",
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify locally downloaded CURE-OR IEEE DataPort archives.")
    parser.add_argument("--archives-dir", default="/Volumes/980PRO/CURE-OR++/archives")
    parser.add_argument("--config", default="configs/cure_or_dataport_archives_v01.json")
    parser.add_argument("--output", default="reports/cure_or_archive_verification_v01.json")
    parser.add_argument("--subset", choices=sorted(SUBSETS), default="all")
    args = parser.parse_args()

    archives_dir = Path(args.archives_dir)
    config_path = resolve_project_path(args.config)
    output_path = resolve_project_path(args.output)
    config = json.loads(config_path.read_text(encoding="utf-8"))

    required_filenames = SUBSETS[args.subset]
    archives = config["archives"]
    if required_filenames is not None:
        archives = [archive for archive in archives if archive["filename"] in required_filenames]

    rows = []
    total_expected_gb = 0.0
    total_present_bytes = 0
    for archive in archives:
        expected_gb = float(archive["size_gb"])
        total_expected_gb += expected_gb
        path = archives_dir / archive["filename"]
        exists = path.exists()
        size_bytes = path.stat().st_size if exists else 0
        total_present_bytes += size_bytes
        rows.append(
            {
                "challenge_type": archive["challenge_type"],
                "challenge_name": archive["challenge_name"],
                "filename": archive["filename"],
                "expected_size_gb": expected_gb,
                "path": str(path),
                "exists": exists,
                "size_bytes": size_bytes,
                "size_gib": round(size_bytes / (1024**3), 4),
            }
        )

    present = [row for row in rows if row["exists"]]
    missing = [row for row in rows if not row["exists"]]
    summary = {
        "archives_dir": str(archives_dir),
        "source": config["source"],
        "subset": args.subset,
        "expected_archives": len(rows),
        "present_archives": len(present),
        "missing_archives": len(missing),
        "expected_total_gb_decimal": round(total_expected_gb, 2),
        "present_total_gib": round(total_present_bytes / (1024**3), 4),
        "missing_filenames": [row["filename"] for row in missing],
        "archives": rows,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(f"Archives dir: {archives_dir}")
    print(f"Subset: {args.subset}")
    print(f"Present: {len(present)} / {len(rows)}")
    print(f"Expected total: {total_expected_gb:.2f} GB")
    print(f"Present total: {summary['present_total_gib']:.4f} GiB")
    if missing:
        print("Missing:")
        for filename in summary["missing_filenames"]:
            print(f"  {filename}")
    print(f"Wrote {output_path}")
    return 0 if not missing else 1


def resolve_project_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


if __name__ == "__main__":
    raise SystemExit(main())
