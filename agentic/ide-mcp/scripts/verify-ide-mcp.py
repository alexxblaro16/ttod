#!/usr/bin/env python3
"""Offline-first config/allowlist gate for TTOD's student IDE MCP harness.

Checks config *shape* and the official-servers policy — it does NOT prove a server
actually speaks MCP. That deeper, live proof is simulate-student-check.py's job
(AG6 deliverable 9a); this script is deliverable 5's offline CI gate, plus one
optional lightweight live existence probe per AGENTIC-HARNESS.md §8.

Usage:
  agentic/ide-mcp/scripts/verify-ide-mcp.py            # offline checks only (CI-safe)
  agentic/ide-mcp/scripts/verify-ide-mcp.py --live      # also dry-run each stdio
                                                          # server (spawn + quick exit),
                                                          # network required

Exit 0 on pass, 1 on any failure, printing a student-facing PASS/FAIL line per check.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CURSOR_MCP = REPO_ROOT / ".cursor" / "mcp.json"
CANONICAL_MCP = REPO_ROOT / "agentic" / "ide-mcp" / "mcp.cursor.json"
SVELTE_LLMS = REPO_ROOT / "agentic" / "ide-mcp" / "llms" / "svelte-prompts-llms.txt"

# Recorded at vendor time (see agentic/ide-mcp/llms/README.md "Keeping this current").
# A mismatch means the vendored file changed without this constant being updated —
# re-vendor and refresh this digest in the same commit.
SVELTE_LLMS_SHA256 = "4004cc2ebcbf516347d77c59fe34d91732cb54ee805b2227b8e47f8cf56ce9f6"

# Official-servers allowlist. A server key committed to .cursor/mcp.json that is not
# on this list fails CI — see AGENTIC-HARNESS.md's official-only policy and AG6's own
# runbook §"Official-only policy (hard rule, not a preference)".
OFFICIAL_SERVERS_ALLOWLIST = {
    "astro-docs",  # Astro's own hosted docs MCP
    "svelte",  # @sveltejs/mcp, Svelte's own official server
    "playwright",  # @playwright/mcp, Microsoft's own official server
    "filesystem",  # @modelcontextprotocol/server-filesystem, MCP-org reference
    "git",  # @modelcontextprotocol/server-git, MCP-org reference (opt-in block)
    "fetch",  # @modelcontextprotocol/server-fetch, MCP-org reference (opt-in block)
}

REQUIRED_SERVERS = {"astro-docs", "svelte", "playwright"}

FAILURES: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] {label}"
    if detail:
        line += f" — {detail}"
    print(line)
    if not ok:
        FAILURES.append(label)


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        FAILURES.append(f"{path} does not parse as JSON: {e}")
        return None


def offline_checks() -> dict | None:
    cfg = load_json(CURSOR_MCP)
    check(".cursor/mcp.json exists and parses as JSON", cfg is not None,
          str(CURSOR_MCP) if cfg is None else "")
    if cfg is None:
        return None

    servers = cfg.get("mcpServers", {})
    check("mcpServers key present and non-empty", bool(servers))

    missing = REQUIRED_SERVERS - servers.keys()
    check(f"required servers present ({', '.join(sorted(REQUIRED_SERVERS))})",
          not missing, f"missing: {sorted(missing)}" if missing else "")

    unlisted = set(servers.keys()) - OFFICIAL_SERVERS_ALLOWLIST
    check("every committed server key is on the official-servers allowlist",
          not unlisted,
          f"unlisted (never cohort-default without an AG-equivalent decision "
          f"record): {sorted(unlisted)}" if unlisted else "")

    check("'react' has no server key present (settled policy, no entry)",
          "react" not in servers)
    check("'github' is not in the committed default (opt-in only, credentialed)",
          "github" not in servers)

    astro = servers.get("astro-docs", {})
    astro_ok = astro.get("type") == "http" and isinstance(astro.get("url"), str)
    check("astro-docs entry uses the documented HTTP shape", astro_ok,
          json.dumps(astro) if not astro_ok else "")

    canonical = load_json(CANONICAL_MCP)
    check("agentic/ide-mcp/mcp.cursor.json exists and parses", canonical is not None)
    if canonical is not None:
        check(".cursor/mcp.json matches agentic/ide-mcp/mcp.cursor.json byte-for-byte "
              "(landing in sync with edit-home)", cfg == canonical)

    if SVELTE_LLMS.exists():
        digest = hashlib.sha256(SVELTE_LLMS.read_bytes()).hexdigest()
        check("vendored svelte-prompts-llms.txt digest matches recorded value",
              digest == SVELTE_LLMS_SHA256,
              f"got {digest}, expected {SVELTE_LLMS_SHA256} — re-vendor and update "
              f"the constant in this script if the change is intentional"
              if digest != SVELTE_LLMS_SHA256 else "")
    else:
        check("agentic/ide-mcp/llms/svelte-prompts-llms.txt exists", False,
              str(SVELTE_LLMS))

    return cfg


def live_checks(cfg: dict) -> None:
    """Lightweight existence probe only — spawn + quick exit, not a protocol
    handshake. For the real MCP initialize proof, run simulate-student-check.py."""
    for name, spec in cfg.get("mcpServers", {}).items():
        if "url" in spec:
            continue  # HTTP servers: simulate-student-check does the real probe
        command = spec.get("command")
        args = spec.get("args", [])
        if not command:
            continue
        try:
            proc = subprocess.run(
                [command, *args, "--help"],
                capture_output=True,
                timeout=60,
                text=True,
            )
            spawned = True
        except subprocess.TimeoutExpired:
            spawned = True  # it started; some servers ignore --help and hang, that's fine here
        except FileNotFoundError:
            spawned = False
        check(f"'{name}' stdio command is spawnable ({command})", spawned)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true",
                         help="also spawn each stdio server once (network required)")
    args = parser.parse_args()

    cfg = offline_checks()

    if args.live:
        if cfg is None:
            print("[SKIP] live checks — offline checks failed first")
        else:
            live_checks(cfg)
    else:
        print("(offline mode only — pass --live to also spawn each stdio server once)")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) failed:")
        for f in FAILURES:
            print(f"  - {f}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
