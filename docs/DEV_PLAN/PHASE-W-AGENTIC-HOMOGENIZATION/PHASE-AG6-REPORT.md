# PHASE-AG6-REPORT.md

**Status:** DONE (2026-09-19) — cold-reviewed PASS, zero discrepancies, including an
independent live re-run of the MCP handshake evidence, plus the product owner's own complete
five-step manual walkthrough (deliverable 9b) with real tool-call results per server. See
[`PHASE-AG6-COLD-REVIEW.md`](PHASE-AG6-COLD-REVIEW.md).
**Runbook:** [`PHASES/AG6-student-ide-harness.md`](PHASES/AG6-student-ide-harness.md)
**Branch:** `agentic/ag6-student-ide-harness` (new — AG6 proceeds independently of AG0–AG5's
already-merged `agentic/homogenize-landings`, per its own status line)
**Depends on:** AG0 discovery-map freeze, AG3 landings policy, AG4 discovery map — all DONE
on `main`

## What was done

1. `agentic/ide-mcp/README.md` — student setup, official-only policy + why, HTTP vs stdio,
   single-folder Cursor warning, GitHub-opt-in instructions, and the "confirm it like a new
   co-developer would" walkthrough (deliverable 9b).
2. `agentic/ide-mcp/mcp.cursor.json` (edit-home) + `.cursor/mcp.json` (committed landing),
   byte-identical — `astro-docs` (HTTP), `svelte`, `playwright`, `filesystem` (scoped to `.`,
   the repo root, never the home directory). Unlike the AG2/AG3 rule/skill landings, a JSON
   config cannot be a text redirect (Cursor parses it directly), so the two are kept in sync
   and `verify-ide-mcp.py` checks byte-equality mechanically rather than relying on convention.
3. `agentic/ide-mcp/examples/github.json` — GitHub's official `github/github-mcp-server` via
   its published Docker image, `${env:GITHUB_PERSONAL_ACCESS_TOKEN}` interpolation, never in
   the committed default. **Correction made during implementation:** the runbook's own text
   named `github/github-mcp-server`, but a first draft of this file mistakenly used
   `@modelcontextprotocol/server-github` (a different, unrelated npm package) — caught before
   finalizing and replaced with the actual documented invocation (Docker image
   `ghcr.io/github/github-mcp-server`, per that project's own README).
4. `.env.example` (repo root) — appended a clearly-separated, optional
   `GITHUB_PERSONAL_ACCESS_TOKEN` section, explicit that the app stack itself still needs no
   credentials (line 1's existing claim is preserved, not contradicted).
5. `agentic/ide-mcp/llms/svelte-prompts-llms.txt` — vendored live from
   `https://svelte.dev/docs/ai/prompts/llms.txt` (200, 37048 bytes), plus
   `agentic/ide-mcp/llms/README.md` explaining file-vs-MCP-tool use and the re-vendor
   procedure.
6. `agentic/ide-mcp/scripts/verify-ide-mcp.py` — offline config/allowlist gate (deliverable 5):
   parses `.cursor/mcp.json`, checks required servers present, checks every server key against
   a hardcoded official-servers allowlist, checks the landing matches the edit-home
   byte-for-byte, checks the vendored `llms.txt` digest, and confirms neither `react` nor
   `github` appear. `--live` flag adds a lightweight spawn-only existence probe per
   `AGENTIC-HARNESS.md` §8 (distinct from and lighter than deliverable 9's real handshake).
7. `agentic/ide-mcp/scripts/simulate-student-check.py` — **deliverable 9a**, the real MCP
   `initialize` handshake probe. See § Live verification evidence below — this was actually
   run against the real, live servers, not just written.
8. `AGENTS.md` discovery map — added `agentic/ide-mcp/` to the tree, and a new paragraph
   explicitly separating IDE MCP (`.cursor/mcp.json`) from the product's Docker MCP
   (`services/mcp/`) — same three letters, unrelated processes, unrelated audiences.

## Live verification evidence (deliverable 9a — not simulated, actually run)

```
$ python3 agentic/ide-mcp/scripts/simulate-student-check.py --timeout 60
=== astro-docs ===
[PASS] astro-docs — responded: {"name": "Astro Docs server", "version": "1.0.0"}
=== svelte ===
[PASS] svelte — responded: {"name": "Svelte MCP", "version": "0.0.1", ...}
=== playwright ===
[PASS] playwright — responded: {"name": "Playwright", "version": "1.64.0-alpha-1789764292000"}
=== filesystem ===
[PASS] filesystem — responded: {"name": "secure-filesystem-server", "version": "0.2.0"}

4/4 servers passed a real MCP initialize handshake.
```

One real bug found and fixed during this run, not glossed over: the first version of the
HTTP check against `astro-docs` failed with `403 Forbidden` — Cloudflare (fronting
`mcp.docs.astro.build`) was blocking Python's default `Python-urllib/x.y` User-Agent as a bot
signature. Confirmed via a side-by-side `curl` (200) vs bare `urllib` (403) test against the
identical request. Fixed by sending an ordinary browser-shaped `User-Agent` header — not
credential- or auth-related, purely a client fingerprinting quirk. Re-ran after the fix: 4/4
pass, shown above.

A separate manual test against the `svelte` and `filesystem` stdio servers also surfaced a
process-orphaning bug in an early throwaway test script (not the final one): `npx`'s wrapper
process can exit before the actual server process it spawned, leaving that server reparented
to `init` and undetectable through the original stdio pipes. Fixed in the final
`simulate-student-check.py` by using `start_new_session=True` + `os.killpg` for guaranteed
cleanup of the whole process group, not just the immediate child — verified this leaves no
orphaned processes after a run (`ps -ef` checked clean).

## Deliverable 9b — honest limitation, not skipped silently

The automated protocol-level probe (9a) is real, live evidence. The **manual** "confirm it
like a new co-developer would" walkthrough (9b — opening an actual Cursor GUI window from a
throwaway worktree, reading the MCP panel, asking a real question) requires a human at a
graphical IDE. This implementer is a CLI coding agent with no ability to open or interact with
Cursor's UI. **This step was not performed and is not claimed as done.** The README section
describing it (§ "Confirm it like a new co-developer would") is written and ready; a named
human still needs to actually run it and record what came back, per the runbook's own
Acceptance bullet ("actually run, not just written"). Flagging this explicitly rather than
either skipping the bullet silently or fabricating a walkthrough result.

**Update (2026-09-19, human-run, partial):** the product owner ran steps 1–3 of the
walkthrough for real, from a `git worktree add --detach` checkout of this branch, and found
the first genuinely useful piece of 9b evidence: all four TTOD servers (`astro-docs`,
`filesystem`, `playwright`, `svelte`) showed **disabled**, not connected, on first opening the
folder in Cursor, while a pre-existing personal/global server the tester had already trusted
showed connected. This is Cursor's own per-server trust gate for project-committed MCP
config — a one-time manual enable click per server, not a bug in this config — and it was not
previously documented here. `agentic/ide-mcp/README.md` and this runbook's own walkthrough
text both said "no manual install step beyond opening the folder," which undersold this by
one click; both corrected in the same pass as this update (README § "First time in the IDE:
servers start disabled — that's expected", runbook step 3).

**Update 2 (2026-09-19, human-run, complete):** the product owner then ran steps 4–5 for
real, from the same detached worktree, after enabling all four servers. Real tool calls, not
just handshakes:

| Server | Real tool call | Result |
| --- | --- | --- |
| `astro-docs` | `search_astro_docs("content collections")` | Live official Astro docs hits returned |
| `svelte` | `list-sections` + `get-documentation("$state")` | Live Svelte 5 `$state` rune documentation returned |
| `playwright` | Navigate to `https://example.com` | Succeeded |
| `filesystem` | Sandbox scope check | Confirmed scoped to the worktree root (`/private/tmp/ttod-student-sim`), not the home directory |

All four connected and answered a real, checkable question — not a plausible-sounding guess.
Deliverable 9b is complete: all five walkthrough steps actually run, by a named human, with
results recorded here rather than assumed. `git worktree remove` teardown is the tester's own
housekeeping, not something this report needs to independently confirm.

**Scope note on the same audit:** the same session also probed several MCPs outside AG6's
scope — user-level DevIAC servers (a different repo, `~/src/deviac`, broken interpreter path)
and the TTOD product Compose stack (`services/mcp` via `make up`, not running in that
checkout). Both are real findings but neither is a Phase W/AG6 defect: AG6's committed
`.cursor/mcp.json` never touches either, and `AGENTS.md`'s own discovery map already states
IDE MCP and product MCP are unrelated processes. Tracked as separate, out-of-cascade
follow-ups, not folded into this phase's Acceptance.

## Verification

- `python3 agentic/ide-mcp/scripts/verify-ide-mcp.py` → all offline checks PASS.
- Negative test 1: removed `.cursor/mcp.json` → `verify-ide-mcp.py` fails with exit 1, names
  the missing file. Restored, re-verified clean.
- Negative test 2: injected an unlisted `evil-scratch-server` key into a scratch copy →
  `verify-ide-mcp.py` fails on both the allowlist check and the byte-equality-with-canonical
  check. Restored, re-verified `.cursor/mcp.json` and `agentic/ide-mcp/mcp.cursor.json` are
  byte-identical again.
- `git grep -n '@modelcontextprotocol/server' services/frontend/package.json` → exit 1 (no
  match).
- `python -m unittest discover -s tests -p 'test_*.py'` → 219 tests, OK.
- `python cli.py validate --strict --json` → `is_valid: true`, exit 0.
- `git diff --stat -- ttod.yml` → empty (not checked into this diff at all — no product data
  touched).
- `git status --porcelain` on this branch shows exactly the files listed above; `README.md`
  at repo root shows as modified in the working tree but was **not staged or committed** by
  this phase — it predates this session's AG6 work (visible as dirty before AG6 started) and
  is out of this phase's scope; left untouched.

## Acceptance

- [x] `.cursor/mcp.json` exists in git and lists `astro-docs`, `svelte`, `playwright` (plus
      `filesystem`).
- [x] Astro entry uses HTTP URL; `mcp-remote` stdio fallback documented in README; HTTP marked
      default.
- [x] Svelte entry is `npx -y @sveltejs/mcp`.
- [x] Playwright entry is `npx @playwright/mcp@latest`.
- [x] Every server key on the allowlist; `verify-ide-mcp` fails on an unlisted key (proven).
- [x] `agentic/ide-mcp/llms/` contains the Svelte prompts index; README states file-vs-MCP
      guidance.
- [x] `verify-ide-mcp` offline mode exits 0; live mode (`--live`, lightweight spawn probe)
      documented and distinct from deliverable 9's real handshake.
- [x] `AGENTS.md` discovery map links this harness and states Docker MCP ≠ IDE MCP.
- [x] React MCP: no server key present; README states the "no official server exists" reason,
      not "deferred."
- [x] GitHub MCP exists only under `agentic/ide-mcp/examples/`, absent from committed
      `.cursor/mcp.json` (confirmed by the allowlist check).
- [x] `git grep` for `@modelcontextprotocol/server` in frontend `package.json` returns 0.
- [x] Full existing suite still green.
- [x] Negative: removing `.cursor/mcp.json` makes offline verify fail (proven).
- [x] Negative: injecting an unlisted server key makes `verify-ide-mcp` fail (proven).
- [x] `simulate-student-check` performs a real MCP `initialize` handshake against every
      committed server, including the HTTP one — proven, 4/4 pass, evidence quoted above.
- [x] The README walkthrough was actually run from a throwaway `git worktree` — **complete**:
      product owner ran all five steps for real (see § Deliverable 9b updates above), finding
      and documenting the Cursor per-server enable-click, then confirming all four servers
      answer real, checkable tool calls once enabled.

Cold review independently re-ran the live `simulate-student-check.py` handshake itself
(network + npx, not just reading the code) and got byte-for-byte matching output — 4/4 real
passes — plus reproduced both negative tests and the full suite. Zero discrepancies found.
Promoted to DONE-with-one-open-item at cold-review time: deliverable 9b's manual Cursor-GUI
walkthrough still needed a named human at a graphical IDE — neither this implementer nor the
cold reviewer (both CLI agents) could perform it, and the reviewer independently confirmed no
feasible substitute was overlooked. The product owner subsequently ran that walkthrough in
full (see § Deliverable 9b updates above), closing the last open item. Status updated to DONE
without requiring a second cold-review pass, since the human-run walkthrough is exactly the
evidence the cold reviewer already said it could not itself produce or substitute for.
