#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
DEFAULT_SCOPES = ("GIGACHAT_API_PERS", "GIGACHAT_API_B2B", "GIGACHAT_API_CORP")
NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "docrel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


@dataclass(frozen=True)
class Candidate:
    value: str
    sheet: str
    row: int
    col: str


def main() -> int:
    parser = argparse.ArgumentParser(description="Find a working GigaChat auth key in an XLSX without printing secrets.")
    parser.add_argument("--xlsx", required=True, help="Path to the XLSX file with candidate keys.")
    parser.add_argument("--env-file", default="secrets/gigachat.env", help="Env file to update after a successful OAuth check.")
    parser.add_argument("--oauth-url", default=os.environ.get("GIGACHAT_OAUTH_URL", DEFAULT_OAUTH_URL))
    parser.add_argument("--scope", action="append", help="OAuth scope to try. Defaults to PERS, B2B, CORP.")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--request-sleep", type=float, default=0.4)
    parser.add_argument("--limit", type=int, help="Max number of unique keys to test.")
    parser.add_argument("--cafile", help="Optional CA bundle path for TLS verification.")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification.")
    parser.add_argument("--dry-run", action="store_true", help="Extract and validate candidates only; do not call OAuth.")
    args = parser.parse_args()

    xlsx_path = Path(args.xlsx).expanduser()
    if not xlsx_path.exists():
        raise FileNotFoundError(xlsx_path)

    candidates = extract_candidates(xlsx_path)
    if args.limit is not None:
        candidates = candidates[: args.limit]

    print(f"Candidates extracted: {len(candidates)}")
    for index, candidate in enumerate(candidates, start=1):
        print(f"{index:03d}: sheet={candidate.sheet!r} cell={candidate.col}{candidate.row} {describe_key(candidate.value)}")

    if args.dry_run:
        return 0

    scopes = tuple(args.scope or DEFAULT_SCOPES)
    context = build_ssl_context(args)

    for index, candidate in enumerate(candidates, start=1):
        print(f"Testing candidate {index:03d}/{len(candidates)} from {candidate.sheet!r} {candidate.col}{candidate.row}")
        for scope in scopes:
            ok, status, message = test_oauth(
                auth_key=candidate.value,
                scope=scope,
                oauth_url=args.oauth_url,
                timeout=args.timeout,
                context=context,
            )
            print(f"  scope={scope}: status={status} result={message}")
            if ok:
                write_env_file(resolve_project_path(args.env_file), candidate.value, scope)
                print(f"Working key saved to {resolve_project_path(args.env_file)} with scope={scope}")
                return 0
            if args.request_sleep > 0:
                time.sleep(args.request_sleep)

    print("No working GigaChat key found.")
    return 1


def extract_candidates(path: Path) -> list[Candidate]:
    workbook, rels, shared_strings = read_workbook_parts(path)
    candidates: list[Candidate] = []
    seen: set[str] = set()

    with zipfile.ZipFile(path) as archive:
        for sheet_name, target in workbook:
            sheet_path = resolve_sheet_path(rels[target])
            root = ElementTree.fromstring(archive.read(sheet_path))
            for cell in root.findall(".//main:sheetData/main:row/main:c", NS):
                ref = cell.attrib.get("r", "")
                col, row = split_cell_ref(ref)
                value = read_cell_text(cell, shared_strings)
                for token in possible_tokens(value):
                    normalized = normalize_candidate(token)
                    if not normalized or normalized in seen:
                        continue
                    seen.add(normalized)
                    candidates.append(Candidate(value=normalized, sheet=sheet_name, row=row, col=col))

    return candidates


def read_workbook_parts(path: Path) -> tuple[list[tuple[str, str]], dict[str, str], list[str]]:
    with zipfile.ZipFile(path) as archive:
        workbook_root = ElementTree.fromstring(archive.read("xl/workbook.xml"))
        rels_root = ElementTree.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        rels = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rels_root.findall("rel:Relationship", NS)
            if "Id" in rel.attrib and "Target" in rel.attrib
        }
        sheets = [
            (sheet.attrib.get("name", ""), sheet.attrib.get(f"{{{NS['docrel']}}}id", ""))
            for sheet in workbook_root.findall("main:sheets/main:sheet", NS)
        ]
        shared_strings = read_shared_strings(archive)
    return sheets, rels, shared_strings


def read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
    strings: list[str] = []
    for item in root.findall("main:si", NS):
        parts = [node.text or "" for node in item.findall(".//main:t", NS)]
        strings.append("".join(parts))
    return strings


def resolve_sheet_path(target: str) -> str:
    target = target.lstrip("/")
    if target.startswith("xl/"):
        return target
    return f"xl/{target}"


def read_cell_text(cell: ElementTree.Element, shared_strings: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    value_node = cell.find("main:v", NS)
    if cell_type == "s" and value_node is not None:
        try:
            return shared_strings[int(value_node.text or "0")]
        except (ValueError, IndexError):
            return ""
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(".//main:t", NS))
    return "" if value_node is None else (value_node.text or "")


def possible_tokens(value: str) -> list[str]:
    if not value:
        return []
    return re.findall(r"(?:Basic\s+)?[A-Za-z0-9+/=_-]{40,}", value)


def normalize_candidate(value: str) -> str:
    value = value.strip().strip('"').strip("'")
    if value.lower().startswith("basic "):
        value = value.split(None, 1)[1].strip()
    value = value.replace("\n", "").replace("\r", "").replace(" ", "")
    if len(value) < 40:
        return ""
    try:
        decoded = base64.b64decode(pad_base64(value), validate=False)
    except Exception:
        return ""
    if b":" not in decoded:
        return ""
    return value


def pad_base64(value: str) -> str:
    return value + ("=" * ((4 - len(value) % 4) % 4))


def split_cell_ref(ref: str) -> tuple[str, int]:
    match = re.match(r"([A-Z]+)([0-9]+)", ref)
    if not match:
        return "", 0
    return match.group(1), int(match.group(2))


def describe_key(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
    return f"len={len(value)} fingerprint={digest}"


def test_oauth(
    *,
    auth_key: str,
    scope: str,
    oauth_url: str,
    timeout: float,
    context: ssl.SSLContext | None,
) -> tuple[bool, int, str]:
    body = urllib.parse.urlencode({"scope": scope}).encode("utf-8")
    request = urllib.request.Request(
        oauth_url,
        data=body,
        headers={
            "Accept": "application/json",
            "Authorization": f"Basic {auth_key}",
            "Content-Type": "application/x-www-form-urlencoded",
            "RqUID": str(uuid.uuid4()),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            response_body = response.read().decode("utf-8", errors="replace")
            data = json.loads(response_body) if response_body else {}
            if data.get("access_token"):
                return True, response.status, "access_token_received"
            return False, response.status, "missing_access_token"
    except urllib.error.HTTPError as error:
        body_text = error.read().decode("utf-8", errors="replace")
        return False, error.code, compact_error(body_text)
    except Exception as error:  # noqa: BLE001
        return False, 0, type(error).__name__


def build_ssl_context(args: argparse.Namespace) -> ssl.SSLContext | None:
    if args.insecure:
        return ssl._create_unverified_context()
    if args.cafile:
        return ssl.create_default_context(cafile=str(resolve_project_path(args.cafile)))
    return None


def compact_error(body: str) -> str:
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return body[:120].replace("\n", " ")
    message = data.get("message") or data.get("error_description") or data.get("error") or data.get("code")
    return str(message)[:120].replace("\n", " ")


def write_env_file(path: Path, auth_key: str, scope: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "GIGACHAT_AUTH_KEY=" + auth_key,
                "GIGACHAT_SCOPE=" + scope,
                "",
            ]
        ),
        encoding="utf-8",
    )
    path.chmod(0o600)


def resolve_project_path(path_text: str) -> Path:
    path = Path(path_text).expanduser()
    if path.is_absolute():
        return path
    return ROOT / path


if __name__ == "__main__":
    raise SystemExit(main())
