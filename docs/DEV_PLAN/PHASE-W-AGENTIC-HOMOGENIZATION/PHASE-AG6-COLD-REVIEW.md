# PHASE-AG6-COLD-REVIEW.md

**Reviewer:** `cascade-cold-reviewer` (fresh subagent session, zero prior context on this
implementation) · 2026-09-19
**Reviewed deliverable:** `docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/PHASE-AG6-REPORT.md`
**Verdict:** Clean, honest pass. Zero discrepancies between the report's claims and
independently reproduced evidence. Safe to promote to DONE-with-one-open-item.

## Acceptance audit

| # | Bullet | Result | Evidence |
| --- | --- | --- | --- |
| 1 | `.cursor/mcp.json` lists `astro-docs`, `svelte`, `playwright` (+ `filesystem`) | PASS | Read directly |
| 2 | Astro HTTP + documented stdio fallback | PASS | `type: http`; `mcp-remote` fallback documented, HTTP default |
| 3 | Svelte = `npx -y @sveltejs/mcp` | PASS | Exact match |
| 4 | Playwright = `npx @playwright/mcp@latest` | PASS | Exact match |
| 5 | Allowlist documented + enforced | PASS | `verify-ide-mcp.py` run; negative test reproduced |
| 6 | `llms/` Svelte index + file-vs-MCP guidance | PASS | Present, digest-checked |
| 7 | `verify-ide-mcp` offline exits 0 | PASS | Reproduced, all PASS |
| 8 | `AGENTS.md` discovery map + Docker MCP ≠ IDE MCP | PASS | Confirmed both |
| 9 | React: no key, correct reason stated | PASS | Confirmed |
| 10 | GitHub MCP opt-in only, correct official image | PASS | `ghcr.io/github/github-mcp-server`, absent from default |
| 11 | `git grep` frontend package.json | PASS | Exit 1, no match |
| 12 | Full suite green | PASS | 219 tests OK, reproduced verbatim |
| 13 | Negative: missing config fails | PASS | Reproduced, restored clean |
| 14 | Negative: unlisted key fails | PASS | Reproduced (both allowlist + byte-equality checks fail), restored clean |
| 15 | `simulate-student-check` real handshake | PASS | **Independently re-run live**: 4/4 pass, output byte-for-byte matches the report's quoted evidence |
| 16 | README walkthrough actually run | Honestly unchecked | See judgment call below |

## Other independently reproduced checks

- Config byte-identity, no `react`/`github` key — PASS.
- `.env.example` line 1 unchanged; GitHub PAT addition clearly optional — PASS.
- No trace of the mistaken `@modelcontextprotocol/server-github` package anywhere in
  committed config/code (only in the report's own prose describing the caught mistake,
  which is expected) — PASS.
- `git diff --stat main...agentic/ag6-student-ide-harness -- ttod.yml` empty — PASS.
- Root `README.md` correctly excluded from this branch's commit — PASS.
- `cli.py validate --strict --json` → `is_valid: true` — PASS.

## Deliverable 9b judgment call

Independently assessed whether a feasible CLI substitute existed. This machine has
`Cursor.app` and a `cursor` CLI shim, but that shim only opens a folder in the GUI — there is
no headless way to drive Cursor's chat, read its MCP panel state, or judge answer fluency
without a human present. The runbook's own text is explicit that 9b is about Cursor's UI
specifically, not a protocol check (9a already owns that). Agree with the implementer: leaving
the box unchecked and naming the gap explicitly is correct; no feasible substitute was
overlooked.

## Result

Every command, every negative test, and the live 4-server MCP handshake reproduced exactly as
claimed, including the Cloudflare User-Agent fix behaving as described. Safe to promote to
DONE-with-one-open-item — a named human should still run 9b and record results, but nothing
here blocks that promotion. No P0/P1 findings.
