#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PAPER = ROOT / "paper" / "main.tex"

INPUT_RE = re.compile(r"\\input\{([^{}]+)\}")
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^{}]+)\}")
BIBLIOGRAPHY_RE = re.compile(r"\\bibliography\{([^{}]+)\}")

REQUIRED_TEX_TOOLS = ("latexmk", "pdflatex", "kpsewhich")
RECOMMENDED_TEX_TOOLS = ("biber", "xelatex", "lualatex")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate CURE-OR++ paper assets and optionally compile the LaTeX PDF."
    )
    parser.add_argument("--paper", default=str(DEFAULT_PAPER), help="Path to the LaTeX entrypoint.")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="PDF output directory for --compile. Defaults to a temporary directory.",
    )
    parser.add_argument("--compile", action="store_true", help="Run latexmk after preflight checks.")
    parser.add_argument(
        "--require-tex",
        action="store_true",
        help="Fail when TeX Live/MacTeX command-line tools are missing.",
    )
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable report.")
    args = parser.parse_args()

    paper_path = resolve_path(args.paper)
    checks: list[dict[str, object]] = []
    checks.append(check("paper_exists", paper_path.exists(), relative_detail(paper_path)))

    if paper_path.exists():
        checks.extend(check_source_references(paper_path))
    else:
        checks.append(check("paper_references", False, "paper entrypoint is missing"))

    tex_report = detect_tex_runtime()
    checks.append(
        check(
            "tex_required_tools",
            tex_report["required_ready"] or not args.require_tex,
            f"missing={tex_report['missing_required']}",
        )
    )

    compile_report: dict[str, object] = {"attempted": False, "passed": False, "reason": "not requested"}
    if args.compile:
        if not tex_report["required_ready"]:
            compile_report = {
                "attempted": False,
                "passed": False,
                "reason": f"missing required TeX tools: {tex_report['missing_required']}",
            }
            checks.append(check("paper_compile", False, compile_report["reason"]))
        else:
            output_dir = Path(args.output_dir) if args.output_dir else Path(tempfile.mkdtemp(prefix="cure-or-pp-paper-"))
            compile_report = compile_paper(paper_path, resolve_path(output_dir))
            checks.append(check("paper_compile", bool(compile_report["passed"]), str(compile_report["reason"])))

    failed = [item for item in checks if not item["passed"]]
    report = {
        "passed": not failed,
        "paper": relative_detail(paper_path),
        "checks": checks,
        "tex": tex_report,
        "compile": compile_report,
    }

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human_report(report)

    return 1 if failed else 0


def check_source_references(paper_path: Path) -> list[dict[str, object]]:
    text = paper_path.read_text(encoding="utf-8")
    base_dir = paper_path.parent
    checks: list[dict[str, object]] = []

    for raw_path in sorted(set(INPUT_RE.findall(text))):
        target = (base_dir / raw_path).resolve()
        checks.append(check(f"input_exists:{raw_path}", target.exists(), relative_detail(target)))

    for raw_path in sorted(set(GRAPHICS_RE.findall(text))):
        target = (base_dir / raw_path).resolve()
        checks.append(check(f"graphics_exists:{raw_path}", target.exists(), relative_detail(target)))

    bibliography_items = []
    for raw_group in BIBLIOGRAPHY_RE.findall(text):
        bibliography_items.extend(item.strip() for item in raw_group.split(",") if item.strip())
    for item in sorted(set(bibliography_items)):
        target = (base_dir / f"{item}.bib").resolve()
        checks.append(check(f"bibliography_exists:{item}", target.exists(), relative_detail(target)))

    checks.append(
        check(
            "paper_has_bibliography",
            bool(bibliography_items),
            f"bibliography_items={bibliography_items}",
        )
    )
    return checks


def detect_tex_runtime() -> dict[str, object]:
    required = {tool: shutil.which(tool) for tool in REQUIRED_TEX_TOOLS}
    recommended = {tool: shutil.which(tool) for tool in RECOMMENDED_TEX_TOOLS}
    missing_required = [tool for tool, path in required.items() if path is None]
    missing_recommended = [tool for tool, path in recommended.items() if path is None]
    return {
        "required_tools": required,
        "recommended_tools": recommended,
        "required_ready": not missing_required,
        "missing_required": missing_required,
        "missing_recommended": missing_recommended,
    }


def compile_paper(paper_path: Path, output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-outdir=" + str(output_dir),
        paper_path.name,
    ]
    result = subprocess.run(
        cmd,
        cwd=paper_path.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    pdf_path = output_dir / (paper_path.stem + ".pdf")
    pdf_ok = pdf_path.exists() and pdf_path.stat().st_size > 0
    return {
        "attempted": True,
        "passed": result.returncode == 0 and pdf_ok,
        "reason": f"exit_code={result.returncode} pdf_exists={pdf_path.exists()} pdf_size={pdf_path.stat().st_size if pdf_path.exists() else 0}",
        "command": cmd,
        "output_dir": str(output_dir),
        "pdf": str(pdf_path),
        "stdout_tail": tail(result.stdout),
        "stderr_tail": tail(result.stderr),
    }


def print_human_report(report: dict[str, object]) -> None:
    print(f"Paper: {report['paper']}")
    for item in report["checks"]:
        status = "OK" if item["passed"] else "FAIL"
        if item["name"] == "tex_required_tools" and item["passed"] and not report["tex"]["required_ready"]:
            status = "WARN"
        print(f"{status}: {item['name']} ({item['detail']})")

    tex = report["tex"]
    if tex["required_ready"]:
        print("TeX runtime: ready")
    else:
        print(f"TeX runtime: missing required tools {tex['missing_required']}")

    compile_report = report["compile"]
    if compile_report["attempted"]:
        status = "OK" if compile_report["passed"] else "FAIL"
        print(f"{status}: compile ({compile_report['reason']})")
    else:
        print(f"Compile: skipped ({compile_report['reason']})")


def check(name: str, passed: bool, detail: str) -> dict[str, object]:
    return {"name": name, "passed": bool(passed), "detail": detail}


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return (ROOT / candidate).resolve()


def relative_detail(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def tail(text: str, max_chars: int = 4000) -> str:
    return text[-max_chars:] if len(text) > max_chars else text


if __name__ == "__main__":
    raise SystemExit(main())
