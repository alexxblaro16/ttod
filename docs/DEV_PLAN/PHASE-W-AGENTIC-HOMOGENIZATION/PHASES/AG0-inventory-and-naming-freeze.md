# AG0 — Inventory confirmation and naming freeze

**Status:** DONE (2026-09-18; decision frozen at `DECISIONS/W0-2026-09-18-AGENTIC-HOME.md`,
cold-reviewed PASS at `../PHASE-AG0-COLD-REVIEW.md`, report at `../PHASE-AG0-REPORT.md`)
**Depends on:** Phase W INDEX + FINDINGS-2026-09-18  
**Does not authorize:** branch creation, file moves, or commits

## Goal

Freeze *where* canonical agent bodies live for TTOD, and how that relates to the
studio `~/src/.agents/` home already started 2026-09-11. Close FINDINGS F1 and F3
with a written decision — not with improvisation in AG2.

## Deliverables

1. `docs/DEV_PLAN/DECISIONS/W0-YYYY-MM-DD-AGENTIC-HOME.md` (date stamped on freeze day).
2. Updated inventory table in the decision (or a one-page annex) listing every TTOD
   agent-facing file and its post-freeze home vs landing.
3. Explicit in/out list: which studio skills TTOD may *cite* but must not *absorb*.

## Scope

| In | Out |
| --- | --- |
| Naming map: `agentic/` · `.cursor/` · `.claude/` · `~/src/.agents/` | Moving any file |
| Confirm CI path to `agentic/report-steward/...` stays | Renaming studio `.agents` |
| Product-owner sign-off recorded | Branch creation |

## Prompt (paste when executing)

```text
Execute AG0 only per
docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/PHASES/AG0-inventory-and-naming-freeze.md.

Re-run the FINDINGS inventory commands; amend FINDINGS if the tree drifted.
Draft DECISIONS/W0-…-AGENTIC-HOME.md with the recommended freeze from RATIONALE.md
(agentic/ = TTOD canonical bodies; .cursor/.claude = landings; studio .agents =
studio-shared, mapped explicitly). Do not create a branch. Do not move files.
Stop at VERIFYING with the decision draft ready for product-owner sign-off.
Do not mark DONE; hand off for cold review of the decision clarity.
```

## Acceptance

- [ ] Decision file exists under `docs/DEV_PLAN/DECISIONS/` with status FROZEN or
      DRAFT-AWAITING-SIGN-OFF clearly labeled.
- [ ] F1 and F3 each have a row: closed / deferred-with-id.
- [ ] Inventory lists at least: `ttod-editing`, `public-docs-i18n`, `report-steward/*`,
      `cascade-phase-executor`, `cascade-cold-reviewer`, `AGENTS.md`, `CLAUDE.md`.
- [ ] Decision states whether `.claude` stubs keep pointing at `~/src/.agents/` or
      remapped to `ttod/agentic/agents/` (pick one; no “both silently”).
- [ ] Decision freezes the **discovery map**: `AGENTS.md` ↔ `agentic/` (bidirectional
      link required in AG4); product MCP stays at `services/mcp/` (Astro/Oracle
      consumer path named); **explicit non-goal:** do not relocate MCP under `agentic/`.
- [ ] Decision freezes IDE vs app MCP: project `.cursor/mcp.json` for Astro+Svelte
      (AG6); Docker `services/mcp` is application-only; React MCP portable-or-defer.
- [ ] Decision records validator readiness per [`AGENTIC-HARNESS.md`](../AGENTIC-HARNESS.md)
      §2–§3 (no false claim of a full Ollama validator fleet).
- [ ] No git branch created in this phase (`git branch` shows no new `agentic/homogenize-*`).

## Risks

- Freezing “both homes equally” recreates the duplication Phase W exists to end.
- Absorbing studio `ttod-bridge` into `ttod/agentic/` without a studio plan breaks
  sibling repos that import the skill from `~/src/.cursor/skills/`.
