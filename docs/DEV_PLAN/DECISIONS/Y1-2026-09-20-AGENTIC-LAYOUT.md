# Y1 decision — agentic layout: flat packs; `public-docs-i18n` stays a leaf

**Status:** FROZEN 2026-09-20, amended after cold review the same day (see § Amendment).
**Row 2 is superseded by [Y5](Y5-2026-09-21-ONE-AXIS-TREE.md) — accepted by the owner 2026-09-21** (rows 1, 3, 4 stand). Kept unedited below as the record of why the leaf design was tried.
**Owner:** `ruvebal@crea-comm.net` — may overturn any row.
**Implementation authority:** Y2 only; no file moved by this record.

## Decisions

| # | Question | Decision | Basis |
| --- | --- | --- | --- |
| 1 | Packs flat under `agentic/`, or nested under `agentic/packs/`? | **Flat siblings** (recommended default) | Legibility test passed on the flat tree (Y0); nesting adds a level to solve a problem the test does not show. "Worse is better." |
| 2 | `public-docs-i18n`: leaf skill or pack? | **Leaf skill** (recommended default) — with its script dependency now declared | See below |
| 3 | Collection id | **`dear_tree`** (recommended default) | Names an affection for structure; readable aloud |
| 4 | `report-steward/` path | **Frozen** | CI runs `report-steward/scripts/check_public_privacy.py` at that path |

## Row 2 — what was considered

The skill's step 2 calls `scripts/translate_public_docs.py`; that call is the script's only
consumer outside DEV_PLAN history (`git grep`; no Makefile, CI, or test). Three options:

| Option | For | Against |
| --- | --- | --- |
| A. Promote to a pack **and move** the script in | pack is self-contained | code edit (the script computes the repo root as `parents[1]` of its own path); relocates a working repo-level CLI; empties `agentic/skills/`, so the legend loses its only leaf-skill example |
| B. Pack whose `PACK.md` **indexes** the external script | no code change | a "pack" whose parts do not live together contradicts what a pack is |
| C. **Keep leaf**, declare the dependency in the README row | zero risk; script stays a standalone CLI (`--help` works without the skill) | the executable half is outside `agentic/` (mitigated by naming it) |

**Chosen: C.** The coupling is one-way — the skill names a path, and moving the skill breaks
nothing about the script. The pack criterion is about files that live *inside* `agentic/` and must
move together; a skill that merely invokes a standalone repo-level CLI is still one surface. The
criterion text is tightened accordingly (README, INDEX).

## Amendment (why this is not the first draft)

The first draft of this record chose **A** ("promote"), reading the criterion's "skill + script"
example literally. The cold review called that "defensible but borderline… the decision
overclaims", noted no new evidence had arrived (Y0 had already flagged the skill as borderline
with one surface), argued the opposite case, and observed that option B had not even been
weighed. On that evidence the row was reversed to C. The first draft also called the criterion
"decorative" if the skill stayed a leaf; that was rhetoric, not an argument, and is withdrawn.

## Evidence that the legend, not the layout, was the defect

Legibility test with a negative control (transcripts saved in
[`PHASE-Y-LEGIBILITY-TRANSCRIPTS.md`](../PHASE-Y-AGENTIC-DIRTREE-UNIX/PHASE-Y-LEGIBILITY-TRANSCRIPTS.md)).
A naive reader given `main`'s pre-Y0 README plus the same listing found contradictions; the same
reader given the Y0 README found none. Verified against `main`'s README by the reviewer:
`ide-mcp/` is described as "Not yet created" although it is tracked (real); `agents/` is described
as "reserved, currently empty" although no such directory exists (inaccurate, not merely
ambiguous); the "deliberately absent" wording about the cascade subagents is the weakest point
(only misleading if a redirect stub is taken for a fork). Also misfiled: `.cursor/mcp.json`.

What this evidence does **not** show: that flat packs are the *best* layout. Nesting under
`agentic/packs/` was never tested; the decision is only that the flat tree, once legible, gives
the reader no reason to pay for another level.

## Non-authorization

No move, no `ttod.yml` change, no `proposal accept`, no rename of `report-steward/`.
