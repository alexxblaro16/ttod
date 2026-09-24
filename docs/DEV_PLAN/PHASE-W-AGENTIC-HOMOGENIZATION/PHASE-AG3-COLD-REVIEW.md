# PHASE-AG3-COLD-REVIEW.md

**Reviewer:** `cascade-cold-reviewer` (fresh subagent session, zero prior context on this
implementation) · 2026-09-18
**Reviewed deliverable:** `docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/PHASE-AG3-REPORT.md`
**Verdict:** **PASS**. No findings. Safe to promote to DONE.

## Acceptance audit

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Each landing body ≤ ~15 lines, explicit canonical path | PASS | Both stubs read in full: 3-line bodies, correct canonical paths named |
| 2 | `test -f` for every redirect target exits 0 | PASS | Both `agentic/` canonical files exist, hold complete AG2-migrated content, untouched by AG3 |
| 3 | Cursor rule/skill frontmatter intact; Claude agent frontmatter intact | PASS | Byte-for-byte match against AG2 canonical copies for `.cursor`; `.claude/agents/cascade-*.md` frontmatter (`name`/`description`/`tools`/`model`) confirmed untouched |
| 4 | Full suite green | PASS | 219 tests OK; `validate --strict` → `is_valid: true` |
| 5 | Negative check (`Never delete quotes` moved) | PASS | No match under `.cursor/rules/`; matches `agentic/rules/ttod-editing.md:18` |

## `.claude` untouched — legitimate, not a dodge

Independently confirmed against `DECISIONS/W0-2026-09-18-AGENTIC-HOME.md`'s own inventory
table: both cascade subagent stubs are listed with target "Unchanged (studio-canonical per
Decision §2)" and action "Stub stays as-is" — a pre-existing, frozen table entry, not the AG3
report's own interpretive spin. Remapping them to `ttod/agentic/agents/` (which W0 explicitly
keeps empty) would contradict W0 rather than fulfill AG3's deliverable wording.

## Other checks

- `git status --porcelain` matches the report exactly: only the two `.cursor` files modified,
  no `.claude` diff, no `ttod.yml` diff.
- `.cursor` and `.claude` directories both still exist — not deleted.
- No factual discrepancy found between the report and the live tree.
