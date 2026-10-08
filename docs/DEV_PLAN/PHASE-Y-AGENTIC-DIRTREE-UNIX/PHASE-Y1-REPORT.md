# PHASE-Y1-REPORT.md

**Status:** DONE (2026-09-20) — cold review (two passes; first said amend, reversal applied, second PASS). See [`PHASE-Y1-COLD-REVIEW.md`](PHASE-Y1-COLD-REVIEW.md)
**Runbook:** [`PHASES/Y1-layout-decision.md`](PHASES/Y1-layout-decision.md)
**Decision:** [`DECISIONS/Y1-2026-09-20-AGENTIC-LAYOUT.md`](../DECISIONS/Y1-2026-09-20-AGENTIC-LAYOUT.md)

## Checklist result

- [x] Flat siblings — recommended default adopted
- [x] `public-docs-i18n` → **stays a leaf skill**, script dependency declared — recommended default adopted
- [x] Collection `dear_tree` — recommended default adopted
- [x] `report-steward/` frozen

The product owner delegated the full Y cycle on 2026-09-20; every row is the plan's recommended
default, adopted on that delegation rather than chosen row-by-row. Any may be overturned.

## What the cold review changed

The first draft **promoted** `public-docs-i18n` to a pack. The review (asked to argue the opposite
case in earnest) found the rationale oversold: no new evidence since Y0 had called the skill
borderline; the coupling is one-way; promotion needs a code edit and empties `agentic/skills/`; and
the option "pack that only indexes the script" had not been weighed. The row was **reversed**.
Amendments applied: rejected alternatives recorded; the runbook's "one surface" count and the first draft's
reversal of it acknowledged in the decision file's Amendment section; `agents/` described as *inaccurate* (the directory
does not exist), not "ambiguous"; the weakest control claim softened; both legibility transcripts
saved with an honest caveat (one small-model sample each); pack criterion tightened.

## Reconsidered upcoming phases

- **Y2 is again a documented no-op for moves** — one real content edit remains: the README's
  `public-docs-i18n` row names the script it calls, and the criterion text is tightened. Then verify
  landings resolve and re-run the legibility test on the final tree.
- The hazards the review listed for a promotion (script root constant, `ttod_core` import path,
  landing retarget) are moot under the leaf decision; they are kept in the review record.
- Y3/Y4 unchanged.
