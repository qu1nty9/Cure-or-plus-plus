#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Execute notebook code cells in order for a lightweight validation.")
    parser.add_argument("notebook")
    args = parser.parse_args()

    namespace = {"__name__": "__notebook_validation__"}
    notebook_path = Path(args.notebook)
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    code_cell_count = 0
    for index, cell in enumerate(notebook["cells"], start=1):
        if cell.get("cell_type") != "code":
            continue
        code = "".join(cell.get("source", []))
        code_cell_count += 1
        print(f"Executing code cell {index}...")
        exec(compile(code, f"{notebook_path}:cell-{index}", "exec"), namespace)

    print(f"Executed {code_cell_count} code cells.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

