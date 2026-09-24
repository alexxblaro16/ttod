# PHASE-AG4-REPORT.md

**Status:** DONE (2026-09-18) — cold-reviewed PASS, zero findings. See
[`PHASE-AG4-COLD-REVIEW.md`](PHASE-AG4-COLD-REVIEW.md).
**Runbook:** [`PHASES/AG4-rewrite-references.md`](PHASES/AG4-rewrite-references.md)
**Branch:** `agentic/homogenize-landings`
**Depends on:** AG3 DONE — satisfied

## What was done (all in `AGENTS.md`; no historical report rewritten)

1. **Path table** — added `agentic/` as edit-home (with an explicit pointer to
   `agentic/README.md`), and reworded the `.cursor/rules/ttod-editing.mdc` row to say
   "Load-path landing (Cursor) → `agentic/rules/ttod-editing.md`" instead of implying it's
   the source of truth.
2. **"Edit existing quotes" step 1** — was `Read \`.cursor/rules/ttod-editing.mdc\`.`; now
   `Read \`agentic/rules/ttod-editing.md\` — Cursor loads the same content via the
   \`.cursor/rules/ttod-editing.mdc\` landing.` This closes AG4's own negative-check bullet.
3. **Discovery map** — new subsection under Integration, using the exact wording W0 froze
   (from `RATIONALE.md` § Discovery map): the ASCII tree plus the "Agent harness / Product
   MCP / Studio MCP ingest" paragraph. States plainly that `services/mcp/` is never
   relocated under `agentic/`.
4. **Integration table** — added `services/mcp/` and the Astro/Astro-backend client rows so
   the product MCP path is discoverable from the same table as Web Atelier / DevIAC / etc.,
   without claiming Astro or `agentic/` contains the server.
5. **Related docs table** — added `agentic/README.md` and `agentic/rules/ttod-editing.md`
   rows; annotated the studio `ttod-bridge` row as "cited, not absorbed" with a pointer to
   `DECISIONS/W0-2026-09-18-AGENTIC-HOME.md`.

## Generator check (deliverable #2) — verified non-issue, not modified

`scripts/generate-ts5-teaching-baseline.sh` copies `.cursor/rules/ttod-editing.mdc` from its
source branch `skeleton/ts5-hello-world`. Checked directly: `git show
skeleton/ts5-hello-world:.cursor/rules/ttod-editing.mdc` is **153 lines — the full body, not
a stub** — because that branch forked before the `agentic/` pack existed (the script's own
comment says as much for a different file, at line 91). The generator is not currently
broken by AG2/AG3's work on this branch, and this branch has not merged to `main`, so nothing
downstream of it has changed yet either. **Deliberately not edited**: speculatively patching
a carefully-tuned, already-tested generator for a scenario that hasn't happened yet
(`skeleton/ts5-hello-world` rebased onto post-AG5-merge `main`) risks breaking something that
works, for no present benefit — exactly the over-engineering AG4's own risk list warns
against ("updating generators to omit `agentic/` leaves students without …"). Flagging this
here as the record AG5/whoever eventually regenerates that baseline should re-check: at that
future point, `.cursor/rules/ttod-editing.mdc` **will** be a stub, and the generator will need
an added `copy agentic/rules/ttod-editing.md` line (guarded, since today that path doesn't
exist on the source branch) to keep giving students the actual checklist.

`scripts/generate-cohort-starter.sh` does not reference `.cursor` or `agentic` at all —
unaffected, not touched.

## Verification

- `git grep -n 'Read \`.cursor/rules/ttod-editing' AGENTS.md` → no match (exit 1). Closes the
  negative-check bullet.
- `agentic/report-steward/scripts/check_public_privacy.py` still referenced at that exact path
  in `.github/workflows/public-docs-pages.yml` (2 occurrences, unchanged).
- `test -d services/mcp && test ! -d agentic/mcp` → both true; product MCP was not moved.
- `agentic/README.md` already links back to `../AGENTS.md` and one-lines the `services/mcp/`
  pointer (written in AG2; re-verified here, no change needed).
- `python -m unittest discover -s tests -p 'test_*.py'` → 219 tests, OK.
- `python cli.py validate --strict --json` → `is_valid: true`, exit 0.
- `git diff --stat -- ttod.yml` → empty.
- `git status --porcelain` → only `AGENTS.md` newly modified for this phase, plus the
  pre-existing AG0–AG3 doc/agentic artifacts from earlier in this session.

## Acceptance

- [x] `AGENTS.md` states `agentic/` as edit-home for TTOD rules/skills and names
      `.cursor`/`.claude` as landings.
- [x] `AGENTS.md` contains a discovery map linking `agentic/` harness, `services/mcp/`
      product FastMCP, and Astro/Oracle as MCP client — without claiming Astro or `agentic/`
      contains the server.
- [x] `agentic/README.md` links back to `../AGENTS.md` and one-lines the product MCP
      pointer (already true from AG2; unchanged here).
- [x] `git grep -n 'Read \`.cursor/rules/ttod-editing'` AGENTS.md` returns 0.
- [x] Privacy watcher still invoked at the same CI path.
- [x] Generator check performed and documented; no edit made because none was needed today
      (see § Generator check above — this is a documented decision, not a skipped bullet).
- [x] Full suite green.
- [x] Negative: `services/mcp` not moved under `agentic/`.

Cold review found zero discrepancies, independently re-ran every check (including the
`skeleton/ts5-hello-world` line count and the full suite), and reached its own independent
verdict agreeing with the generator-script judgment call rather than deferring to this
report's framing. Promoted to DONE.
