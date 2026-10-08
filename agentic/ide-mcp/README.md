# Student IDE MCP harness

Project-level Model Context Protocol (MCP) client config for the coding agent inside
your editor (Cursor, Claude Code, …) — separate from the product's own Docker MCP
(`services/mcp`, read-only corpus retrieval for the Oracle/Astro app). See
[`AGENTS.md`](../../AGENTS.md)'s discovery map and
[`../../docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/AGENTIC-HARNESS.md`](../../docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/AGENTIC-HARNESS.md)
for the full rationale behind every decision below — this file is the short,
student-facing version.

## What's committed, and why

| Server | Type | Command | Why it's here |
| --- | --- | --- | --- |
| `astro-docs` | HTTP | `https://mcp.docs.astro.build/mcp` | Astro's own official docs MCP |
| `svelte` | stdio | `npx -y @sveltejs/mcp` | Svelte's own official MCP (docs, autofixer) |
| `playwright` | stdio | `npx @playwright/mcp@latest` | Microsoft's own official browser-automation MCP — the closest thing to a "React-shaped" testing capability available, since React itself has none (below) |
| `filesystem` | stdio | `npx -y @modelcontextprotocol/server-filesystem .` | `modelcontextprotocol`-org reference server, sandboxed to the repo root (the trailing `.` — never your home directory) |

**Official-only policy (hard rule, not a preference):** a server ships in the
committed default only if it is published and maintained by the framework/tool
vendor itself, or by the `modelcontextprotocol` reference-server org itself.
Third-party/community/marketplace listings are never cohort-default, no matter how
convenient the install looks — they're an unaudited attack surface running on every
student's machine, not a taste preference. `agentic/ide-mcp/scripts/verify-ide-mcp.py`
enforces this mechanically: an unlisted server key in `.cursor/mcp.json` fails CI.

**React gets no entry — settled, not deferred.** Meta does not publish an official
React MCP server. This is not a "revisit later" TODO and not an invitation to
substitute a third-party one; re-check only whether a vendor-official server has
shipped before ever reconsidering. React context stays file/docs-based for now
(existing course materials, copy-paste from react.dev).

**GitHub MCP is opt-in only, never in the committed default** — not just because it
needs a credential, but because a `github` entry would show disconnected/red for
every student who hasn't set one up, failing the "fresh clone just works, nothing
red by default" bar. See [`examples/github.json`](examples/github.json) and the
"Optional: GitHub MCP" section below if you want it.

`git` and `fetch` (`modelcontextprotocol`-org reference servers) are on the official
allowlist but not committed by default, to keep the Day-0 surface minimal. Add them
yourself by copying their block into `.cursor/mcp.json` from
[`AGENTIC-HARNESS.md` §5](../../docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/AGENTIC-HARNESS.md).

## HTTP vs stdio

- **`astro-docs` prefers HTTP** (`type: http`) — if your client doesn't support
  streamable HTTP MCP, fall back to stdio: `npx -y mcp-remote https://mcp.docs.astro.build/mcp`.
- **Everything else is stdio**, launched fresh by your IDE via `npx` each time —
  nothing to install ahead of time beyond Node/npm, which this project already
  requires for `services/frontend`.

## Single-folder Cursor warning

Cursor can fail to load a project's `.cursor/mcp.json` from a **multi-root**
`.code-workspace`. Open the **`ttod` folder itself** (or the student skeleton
folder) as a single root — this is the one setup detail that silently breaks
everything else in this file if skipped.

## First time in the IDE: servers start disabled — that's expected

Opening this folder loads the config; it does not connect the servers. Cursor (and MCP
clients generally) treat project-committed MCP config as untrusted by default — every
server here shows **disabled**, not connected, until you flip it on once in Cursor's own
MCP settings panel (Settings → MCP, or the panel's own enable/toggle control — exact
wording varies by Cursor version). This is a one-time, per-server trust step, the same
category as a "do you trust this workspace" prompt, not a sign that this config is broken
or that setup failed. Zero-install (nothing to run beforehand) is still true; zero-click
is not — plan for one click per server on Day 0.

If a server still fails to connect *after* you enable it, that's a real problem worth
reporting — `scripts/simulate-student-check.py` (below) is the tool to confirm whether the
server itself is reachable, independent of Cursor's UI state.

## Verifying it's actually wired

Two scripts, two different questions:

1. **`scripts/verify-ide-mcp.py`** — does the config exist, parse, list the right
   servers, and stay on the official allowlist? Offline, CI-safe:
   ```bash
   python3 agentic/ide-mcp/scripts/verify-ide-mcp.py
   ```
2. **`scripts/simulate-student-check.py`** — does each server actually *speak MCP*?
   Sends a real `initialize` handshake to every committed server (network + a
   first-time `npx` fetch required — a slow first run is normal, not a failure):
   ```bash
   python3 agentic/ide-mcp/scripts/simulate-student-check.py
   ```
   A passing run prints each server's real `serverInfo` response, e.g.
   `{"name": "Astro Docs server", "version": "1.0.0"}` — not a guess, an actual
   round-trip.

Neither script can see inside Cursor's own UI (whether its MCP panel shows
"connected"). For that, do the walkthrough below.

## Confirm it like a new co-developer would

Don't trust "it works on my machine" — your own editor may have global MCP config,
a warm `npx` cache, or an already-authenticated tool that a genuinely fresh student
clone would not have. Run this from a **throwaway checkout**, not your regular one:

1. `git worktree add --detach /tmp/ttod-student-sim <branch-under-test>` — detached, not a
   second checkout of the branch by name, since your primary clone may already have that
   branch checked out (worktrees can't share a branch across two working directories).
   Sanity-check before opening the IDE: `ls /tmp/ttod-student-sim/.cursor/mcp.json` and
   `ls /tmp/ttod-student-sim/agentic/ide-mcp/` should both list real files — if the harness
   only exists on a feature branch (not yet merged to `main`), simulating against `main`
   proves nothing; point `<branch-under-test>` at the branch that actually has it.
2. Open **that folder** as a fresh Cursor window (single root — see warning above).
3. Enable each server in Cursor's MCP panel (the one-time trust step from "First time
   in the IDE" above — expected, not a bug), then confirm each shows connected/green.
   Nothing to install first; the one click per server is the only manual step.
4. Ask the agent one *real*, checkable question per server — one only a working
   tool call, not model memory, could answer correctly:
   - Svelte: "use the Svelte MCP to fetch the current `$state` rune docs and quote
     one exact sentence."
   - Playwright: "use the Playwright MCP to take an accessibility snapshot of
     `http://localhost:4321`" (with `make up` running).
   - Astro: ask for a specific, current config option from Astro's own docs.

   A fluent-sounding but unverifiable answer is a **fail** — model memory can fake a
   docs summary; only a real MCP round-trip returns something you can check against
   the live source.
5. `git worktree remove /tmp/ttod-student-sim` when done — a one-off simulation, not
   a standing worktree to maintain.

## Optional: GitHub MCP

GitHub's own official `github-mcp-server` needs a Personal Access Token (or OAuth) —
**not** your SSH key (SSH authenticates git's transport; this server calls GitHub's
REST/GraphQL API, a different credential surface entirely, and does not read an
existing `gh auth login` session).

To opt in:

1. Copy the repo root's `.env.example` to `.env` (already gitignored) and fill in
   `GITHUB_PERSONAL_ACCESS_TOKEN=<your token>`.
2. Merge the `github` block from [`examples/github.json`](examples/github.json) into
   your own `.cursor/mcp.json`.

Never paste a token directly into `.cursor/mcp.json` or any other file the repo
tracks — the `${env:GITHUB_PERSONAL_ACCESS_TOKEN}` interpolation keeps the secret
out of git entirely.

## `llms/` — vendored docs index

See [`llms/README.md`](llms/README.md) — a vendored Svelte prompts index for when
the MCP connection itself is unreachable.
