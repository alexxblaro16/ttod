# PHASE-AG0-COLD-REVIEW.md

**Reviewer:** `cascade-cold-reviewer` (fresh subagent session, zero prior context on this
implementation) · 2026-09-18
**Reviewed deliverable:** `docs/DEV_PLAN/DECISIONS/W0-2026-09-18-AGENTIC-HOME.md`
**Verdict:** **PASS** on all AG0 Acceptance bullets. No factual mismatch found between the
decision doc and the live filesystem. Safe to promote to DONE — no amendment required.

## Acceptance audit

| # | Acceptance bullet | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Decision file exists with clear status | PASS | File present, header line 3: "Status: FROZEN by product-owner direction, 2026-09-18" |
| 2 | F1 and F3 each closed/deferred-with-id | PASS | Doc's "Findings closure" table: F1 "Closed by this record", F3 "Closed by this record"; matches `FINDINGS-2026-09-18.md` lines 51, 53 (both P0-for-AG0) |
| 3 | Inventory lists required items | PASS | Inventory table covers `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/ttod-editing.mdc`, `.cursor/skills/public-docs-i18n/SKILL.md`, `agentic/report-steward/**`, both `cascade-*.md` stubs |
| 4 | `.claude` stubs pick one home, not both | PASS | Decision §2: stubs stay pointing at `~/src/.agents/agents/`. Verified live: both stub files end with `Canonical: \`~/src/.agents/agents/...\`` — matches claim exactly, and both target files exist under `~/src/.agents/agents/` (2984/3306 bytes) |
| 5 | Discovery map freeze (bidirectional link required in AG4; MCP stays at `services/mcp/`; non-goal against relocating) | PASS | Doc states this explicitly, correctly scoped as AG4 work, not claimed done now |
| 6 | IDE vs app MCP freeze | PASS | Table present: `.cursor/mcp.json` for AG6, Docker `services/mcp` application-only, React MCP portable-or-defer |
| 7 | Validator readiness per `AGENTIC-HARNESS.md` §2–3, no overclaim | PASS | Doc's "Ready today" / "Not wired" lists match `AGENTIC-HARNESS.md` in substance; correctly disclaims an Ollama validator fleet |
| 8 | No git branch created | PASS | `git branch -a` shows no `agentic/homogenize-*`; only pre-existing branches |

## Independent filesystem checks (not trusting the decision doc's own claims)

- `.cursor/rules/ttod-editing.mdc` — 153 lines, full body present, not yet a stub. Matches doc's "Today: Full body".
- `.cursor/skills/public-docs-i18n/SKILL.md` — 65 lines, full body present, not yet a stub. Matches.
- `agentic/report-steward/` — contains `agent/`, `PACK.md`, `rules/`, `scripts/`, `skills/` — matches claimed "existing pack shape unchanged".
- `agentic/ide-mcp/` — confirmed absent, matches doc's "Does not exist" / AG6-only claim.
- `ls agentic/` shows only `report-steward` — confirms nothing was created under `ttod/agentic/agents/`.

## Informational note (not a defect)

Two files were modified and pre-date this deliverable: `PHASE-W-AGENTIC-HOMOGENIZATION-CASCADE.md`
and `PHASES/AG5-verify-and-merge-gate.md`. Disposition (confirmed against session history, not
speculation): both edits — fixing a broken relative link to the cascade subagent stubs, and
adding the explicit `gh pr create` / `gh pr merge` command blocks to AG5 — were made earlier in
the same working session, before AG0 was executed, at the product owner's explicit request. They
are not AG0 scope creep and do not touch AG0's own deliverable. Still on `main`, no new branch —
not a hard-constraint violation.

## Result

No P0/P1 findings. AG0 promotes to DONE.
