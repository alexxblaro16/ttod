# Y1 — Layout decision (no moves)

## Rule

Decide **after** Y0's legibility test, on its evidence. If the test passed with the flat layout,
"change nothing structural" is the boring, correct answer (Unix: worse is better) and Y2 becomes
a documented no-op. If the test failed, the failure text says what to move.

## Decision checklist (product owner — pre-filled with the recommended defaults; owner may overturn)

- [x] Keep packs as **flat siblings** under `agentic/` (recommended) · or nest under `agentic/packs/`
- [x] `public-docs-i18n`: keep as **leaf skill** · or promote to **pack** with `PACK.md`
      (decided: leaf; it calls a standalone repo-level CLI, one-way coupling — see decision)
- [x] Collection id: `dear_tree` (recommended) · `dirtree_wisdom` · other: ________
- [x] Confirm `report-steward/` path **frozen** (CI)

## Deliverable

`DECISIONS/Y1-2026-09-20-AGENTIC-LAYOUT.md` + `PHASE-Y1-REPORT.md`. Record which checklist rows
were adopted from the recommended defaults and which the owner explicitly chose.

No filesystem moves in this phase.
