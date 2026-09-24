#!/usr/bin/env python3
"""AG6 deliverable 9a — the "am I actually wired" check.

verify-ide-mcp.py checks config shape and the allowlist; it does not prove a server
speaks MCP. This script sends a REAL MCP `initialize` JSON-RPC request to every
server in the committed .cursor/mcp.json (stdio servers over their own stdin/stdout,
the HTTP server as a POST) and asserts a well-formed response comes back.

This is a LIVE check: it needs network access and, for stdio servers, an `npx`
fetch (fast once npm's cache is warm, slower on a genuinely first run — allow the
default timeout, don't assume something is broken from one slow run). Never folded
into the offline CI gate verify-ide-mcp.py owns.

Usage:
  agentic/ide-mcp/scripts/simulate-student-check.py
  agentic/ide-mcp/scripts/simulate-student-check.py --timeout 90   # slower network
"""
from __future__ import annotations

import argparse
import json
import os
import select
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CURSOR_MCP = REPO_ROOT / ".cursor" / "mcp.json"

INITIALIZE_REQUEST = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "ttod-student-simulation", "version": "0.1.0"},
    },
}


def check_stdio(name: str, command: str, args: list[str], timeout: int) -> tuple[bool, str]:
    """Spawn the exact committed stdio command, send a real initialize request,
    and wait for a well-formed JSON-RPC response with the matching id."""
    try:
        proc = subprocess.Popen(
            [command, *args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            start_new_session=True,  # own process group, so timeout cleanup can't orphan a child
        )
    except FileNotFoundError as e:
        return False, f"could not spawn '{command}': {e}"

    try:
        proc.stdin.write(json.dumps(INITIALIZE_REQUEST) + "\n")
        proc.stdin.flush()

        deadline = time.time() + timeout
        while time.time() < deadline:
            ready, _, _ = select.select([proc.stdout], [], [], 1)
            if proc.stdout in ready:
                line = proc.stdout.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except ValueError:
                    continue
                if msg.get("id") == 1:
                    if "result" in msg:
                        info = msg["result"].get("serverInfo", msg["result"])
                        return True, f"responded: {json.dumps(info)}"
                    return False, f"server returned a JSON-RPC error: {msg.get('error')}"
            if proc.poll() is not None:
                return False, f"process exited early (code {proc.returncode}) before responding"
        return False, f"no valid initialize response within {timeout}s"
    finally:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass


def check_http(name: str, url: str, timeout: int) -> tuple[bool, str]:
    body = json.dumps(INITIALIZE_REQUEST).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            # Cloudflare (fronting mcp.docs.astro.build) blocks urllib's default
            # "Python-urllib/x.y" User-Agent as a bot signature — confirmed by testing
            # the identical request with curl (succeeds) vs bare urllib (403). Any
            # ordinary browser-shaped UA clears it; this is not credential/auth-related.
            "User-Agent": "Mozilla/5.0 (compatible; ttod-student-simulation/0.1)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode()
    except (urllib.error.URLError, TimeoutError) as e:
        return False, f"HTTP request failed: {e}"

    # Streamable HTTP MCP responses may arrive as SSE ("event: message\ndata: {...}")
    # or as a bare JSON body, depending on the server. Handle both.
    payload = raw
    for line in raw.splitlines():
        if line.startswith("data:"):
            payload = line[len("data:"):].strip()
            break
    try:
        msg = json.loads(payload)
    except ValueError:
        return False, f"response was not valid JSON (or SSE data:) — got: {raw[:200]!r}"
    if msg.get("id") == 1 and "result" in msg:
        info = msg["result"].get("serverInfo", msg["result"])
        return True, f"responded: {json.dumps(info)}"
    return False, f"unexpected response shape: {raw[:200]!r}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=60,
                         help="seconds to wait per server (default 60; raise on slow "
                              "networks or a genuinely first-ever npx fetch)")
    args = parser.parse_args()

    try:
        cfg = json.loads(CURSOR_MCP.read_text())
    except FileNotFoundError:
        print(f"FAIL: {CURSOR_MCP} does not exist — run verify-ide-mcp.py first.")
        return 1
    except json.JSONDecodeError as e:
        print(f"FAIL: {CURSOR_MCP} does not parse as JSON: {e}")
        return 1

    servers = cfg.get("mcpServers", {})
    if not servers:
        print("FAIL: no mcpServers entries to check.")
        return 1

    results: dict[str, bool] = {}
    for name, spec in servers.items():
        print(f"=== {name} ===")
        if "url" in spec:
            ok, detail = check_http(name, spec["url"], args.timeout)
        else:
            ok, detail = check_stdio(name, spec.get("command", ""), spec.get("args", []), args.timeout)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name} — {detail}")
        print()
        results[name] = ok

    failed = [n for n, ok in results.items() if not ok]
    print(f"{len(results) - len(failed)}/{len(results)} servers passed a real MCP initialize handshake.")
    if failed:
        print(f"Failed: {failed}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
