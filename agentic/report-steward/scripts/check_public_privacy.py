#!/usr/bin/env python3
"""Fail when candidate text exposes local paths, private coordinates, or disallowed identities.

Also fails public/student markup that CI htmlproofer rejects as "'a' tag is missing a
reference" — empty citation anchors and Archify UI shells without href. Shipped 2026-09-08
from docs/public Archify HTML + `<a id="ref-…">` markers.
"""

from __future__ import annotations

import argparse
import ipaddress
import os
from pathlib import Path
import re
import subprocess
import sys


TEXT_SUFFIXES = {
    ".astro", ".css", ".html", ".js", ".json", ".md", ".mdc", ".mjs", ".py",
    ".sh", ".svelte", ".tex", ".toml", ".ts", ".tsx", ".txt", ".yaml", ".yml",
}
HOME_PATH = re.compile(r"/(?:Users|home)/[^\s)`'\"]+|[A-Za-z]:\\Users\\[^\s)`'\"]+", re.I)
# Require a path-like segment after ~/ (avoids LaTeX date blanks ~/~ and guía~/ encargo).
TILDE_PATH = re.compile(r"(?<![\w])~/(?:[A-Za-z0-9._-]+(?:/[^\s)`'\"]*)?)")
MOUNT_PATH = re.compile(r"/(?:Volumes|private/(?:tmp|var))/[^\s)`'\"]+", re.I)
IPV4 = re.compile(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])")
PRIVATE_IPV6 = re.compile(r"(?<![0-9a-f:])(?:f[cd][0-9a-f]{2}|fe[89ab][0-9a-f]):[0-9a-f:%.-]+", re.I)
INTERNAL_HOST = re.compile(r"\b[a-z0-9][a-z0-9.-]*\.(?:loc|local|lan|internal|home)\b", re.I)
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.I)
PUBLIC_PHASE = re.compile(
    r"\b(?:phase\s+(?:[A-Z]+\d*[a-z]?|\d+)|R(?:3b|[0-9]+)|RC[0-9]+|TS[0-9]+|Q[0-9]+)\b",
    re.I,
)
# htmlproofer Links check: "'a' tag is missing a reference"
ANCHOR_MISSING_HREF = re.compile(r"<a\b(?![^>]*\bhref\s*=)[^>]*>", re.I)
MARKUP_SUFFIXES = {".html", ".md", ".astro", ".svelte"}


def tracked_files(root: Path) -> list[Path]:
    raw = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"])
    return [root / item.decode() for item in raw.split(b"\0") if item]


def deny_terms() -> list[str]:
    configured = os.environ.get("TTOD_PRIVATE_TERMS_FILE")
    if not configured:
        return []
    path = Path(configured)
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")]


def private_ip(value: str) -> bool:
    try:
        address = ipaddress.ip_address(value)
    except ValueError:
        return False
    return address.is_private and not address.is_loopback


def is_public_surface(path: Path) -> bool:
    return any(part in {"public", "_site-public"} for part in path.parts)


def is_ethics_institutional(path: Path) -> bool:
    parts = path.parts
    for root in ("ethics", "institutional"):
        if root in parts:
            idx = parts.index(root)
            if idx >= 2 and parts[idx - 2 : idx] == ("docs", "research"):
                return True
    return False


def allowed_email_domain(domain: str, path: Path) -> bool:
    lowered = domain.casefold()
    if lowered == "crea-comm.net":
        return True
    return lowered == "udit.es" and is_ethics_institutional(path)


def findings(path: Path, text: str, terms: list[str]) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    lowered_terms = [(term, term.casefold()) for term in terms]
    public = is_public_surface(path)
    check_markup = public and path.suffix.lower() in MARKUP_SUFFIXES
    for number, line in enumerate(text.splitlines(), 1):
        reasons: set[str] = set()
        if HOME_PATH.search(line):
            reasons.add("local absolute home path")
        if TILDE_PATH.search(line):
            reasons.add("tilde-expanded local path")
        if MOUNT_PATH.search(line):
            reasons.add("local mount or temporary path")
        if INTERNAL_HOST.search(line):
            reasons.add("internal hostname")
        if any(private_ip(match.group()) for match in IPV4.finditer(line)):
            reasons.add("private network address")
        if PRIVATE_IPV6.search(line):
            reasons.add("private IPv6 address")
        if any(
            not allowed_email_domain(match.group(1), path)
            for match in EMAIL.finditer(line)
        ):
            reasons.add("email outside approved studio domain")
        if public and PUBLIC_PHASE.search(line):
            reasons.add("internal development phase identifier in public documentation")
        if check_markup and ANCHOR_MISSING_HREF.search(line):
            reasons.add("anchor tag missing href (htmlproofer)")
        folded = line.casefold()
        for display, term in lowered_terms:
            if term in folded:
                reasons.add(f"private denylist term ({display!r})")
        for reason in sorted(reasons):
            found.append((number, reason))
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", help="candidate files/directories; defaults to tracked files")
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--quiet", action="store_true", help="print only the final result")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    candidates: list[Path] = []
    if args.paths:
        for raw in args.paths:
            target = (root / raw).resolve()
            candidates.extend(p for p in target.rglob("*") if p.is_file()) if target.is_dir() else candidates.append(target)
    else:
        candidates = tracked_files(root)

    terms = deny_terms()
    total = 0
    for path in sorted(set(candidates)):
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"AGENTS.md", "LICENSE-CODE", "LICENSE-CONTENT"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line, reason in findings(path, text, terms):
            total += 1
            if not args.quiet:
                print(f"{path.relative_to(root)}:{line}: {reason}")
    if total:
        print(f"FAIL: {total} public-privacy finding(s)", file=sys.stderr)
        return 1
    print("PASS: no public-privacy findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
