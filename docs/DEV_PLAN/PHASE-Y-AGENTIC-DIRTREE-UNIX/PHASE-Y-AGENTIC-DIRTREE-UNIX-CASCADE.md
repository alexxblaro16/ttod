# Phase Y — Technical director cascade (Dear Tree tidy)

**Status:** AUTHORIZED 2026-09-20 (plan audited — see INDEX § Plan audit)  
**Index:** [`INDEX.md`](INDEX.md)  
**Branch (only after Y0+Y1 auth):** `agentic/dear-tree-tidy`  
**Hard rule:** no `ttod.yml` mutation in Y0–Y3 and Y5; Y4 only stages proposals (already done once — re-run only if rejected/amended).

---

## Programme

| Step | File | Deliverable | Gate |
| --- | --- | --- | --- |
| Y0 | [`PHASES/Y0-criteria-and-readme.md`](PHASES/Y0-criteria-and-readme.md) | Freeze placement criteria; add `ide-mcp/PACK.md`; rewrite `agentic/README.md` with legend + Cathedral epigraph (cite re-verified live) + live TTOD `arch-001` and `arch-014` | Criteria table matches INDEX; watcher **clean on every tracked file touched** (repo is public); **legibility test** passes |
| Y1 | [`PHASES/Y1-layout-decision.md`](PHASES/Y1-layout-decision.md) | Written decision: promote `public-docs-i18n` to pack **or** keep leaf; keep packs flat **or** nest under `packs/` | Product-owner checkbox in report; no moves yet |
| Y2 | [`PHASES/Y2-execute-moves.md`](PHASES/Y2-execute-moves.md) | Apply Y1 moves (**a documented no-op is a valid outcome**); retarget landings; CI path for report-steward unchanged unless Y1 explicitly renames (default: **no rename**) | `make check` or project equivalent green; landings resolve; legibility test re-run on the final tree |
| Y3 | [`PHASES/Y3-compose-lens-ops.md`](PHASES/Y3-compose-lens-ops.md) | Document how to use `lao-tzu-tao-compose` post-tidy; link Dear Tree collection (meta only until human accept) | Pack README + skill path still valid after Y2 |
| Y4 | [`PHASES/Y4-dear-tree-proposals.md`](PHASES/Y4-dear-tree-proposals.md) | Human review of staged proposals; optional `collections.dear_tree` after accepts | `proposal accept` by named human; `validate --strict` |
| Y5 | [`PHASES/Y5-one-axis-tree.md`](PHASES/Y5-one-axis-tree.md) | One-axis tree: `ttod-editing/` and `public-docs-i18n/` become packs; `agents/` plural; `PACK.md` contract; `tests/test_agentic_tree.py`; README rewritten for a human reader | **Blocked until the owner ticks the Y5 decision.** `unittest` green + tree-test control fails as it should; privacy watcher shows **no new finding vs the recorded baseline**; **owner reads the tree cold and writes the verdict** (model pass is secondary); cold review |

---

## Master paste

```text
You are executing Phase Y of TTOD (Dear Tree / agentic dirtree Unix tidy).
Read first:
  ~/src/ttod/docs/DEV_PLAN/PHASE-Y-AGENTIC-DIRTREE-UNIX/INDEX.md
  ~/src/ttod/docs/DEV_PLAN/PHASE-Y-AGENTIC-DIRTREE-UNIX/PHASE-Y-AGENTIC-DIRTREE-UNIX-CASCADE.md
  docs/DEV_PLAN/DECISIONS/Y5-2026-09-21-ONE-AXIS-TREE.md   (Y5 only; repo-relative)
  ~/src/ttod/AGENTS.md
  ~/src/.cursor/skills/cascade-forge/SKILL.md
Out of scope: mutating ttod.yml except via human proposal accept in Y4;
  creating ~/src/deviac/agentic; absorbing ttod-bridge/cascade-forge into TTOD;
  renaming report-steward/ without a CI PR; committing the untracked
  lao-tzu-tao-compose/ pack before its privacy-watcher findings are sanitized.
Hard constraints: local Ollama only for any draft; landings stay thin;
  the repo is PUBLIC — run check_public_privacy.py on every tracked file you touch;
  Cathedral: Chicago cite only from the DevIAC guide's evaluator_safe=yes entry,
  re-verified live with `ahmes query --cite`; vector snippets stay DERIVED
  (discovery, never citation); ESR is metaphor, never evidence for studio pedagogy.
Resume: branch on report status DONE | PARTIAL | VERIFYING | COLD_REVIEW | BLOCKED.
Close each phase: VERIFYING → cascade-cold-reviewer → amend → REPORT.
```

---

## Resume rule

| Report status | Action |
| --- | --- |
| `DONE` | Skip to next phase |
| `PARTIAL` | Finish remaining acceptance lines only |
| `VERIFYING` | Do not start next phase; finish evidence |
| `COLD_REVIEW` | Wait for cold reviewer artifact |
| `BLOCKED` | Fill Blockers; stop |

---

## Closing protocol

Same as Phase W: no self-certified DONE.

### Legibility test (added 2026-09-20 — the check Phase W never ran)

Phase W's cold reviews asked "did the moves match the plan?" and never "is the tree legible?".
Every Phase Y cold review therefore also runs this, with the reviewer given **only**
`agentic/README.md` and the output of `find agentic -maxdepth 2` (not the plan, not this file):

1. Classify every top-level entry under `agentic/` as pack / other (**from Y5 on there are no leaves**; before Y5: pack / leaf rule / leaf skill / other),
   and every file under `.cursor/` and `.claude/` as landing or not.
2. Answer: "Where do I add (a) a new always-on YAML rule, (b) a new one-off workflow skill,
   (c) a new multi-file harness with a script?" (under Y5 every answer is "in a pack — an existing topic's `rules/`/`skills/`, or a new pack")
3. Answer: "What must I never rename, and why?"

**Amended 2026-09-21 (Y5):** a small model passing this test is not evidence the tree is legible to
the person who has to live in it. From Y5 the **human owner** is the primary reader; the model run
stays as a secondary check, and only the owner can mark the human gate passed.

Pass = every classification matches the criteria table and all three placement answers are
correct. Any miss is a README defect, fixed in the same phase. Cold review from
`~/src/.agents/agents/cascade-cold-reviewer.md` (or TTOD stub). Amend-on-surprise
in the same commit as the report when a live probe contradicts the plan.

---

## Layer map

| Layer | Read | Write |
| --- | --- | --- |
| `agentic/**` | all phases | Y0 README; Y2 moves; Y5 packs + PACK.md front matter |
| `.cursor`/`.claude` landings | Y2, Y5 | Y2, Y5: redirect target line only |
| CI `report-steward/scripts/...` | Y1–Y2, Y5 | none by default |
| `AGENTS.md`, `tests/test_agentic_tree.py` | Y5 | Y5: path lines + tree drawing; the new test |
| DevIAC vectors / Athanor / Ahmes | Y0 epigraph grounding | none |
| ttod-bridge `pending/` | Y3–Y4 | Y4 human accept path only |
| `ttod.yml` collections | Y4 | human only after accept |
