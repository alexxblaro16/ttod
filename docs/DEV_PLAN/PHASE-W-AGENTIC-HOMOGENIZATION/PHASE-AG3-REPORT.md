# PHASE-AG3-REPORT.md

**Status:** DONE (2026-09-18) — cold-reviewed PASS, no findings. See
[`PHASE-AG3-COLD-REVIEW.md`](PHASE-AG3-COLD-REVIEW.md).
**Runbook:** [`PHASES/AG3-landing-stubs.md`](PHASES/AG3-landing-stubs.md)
**Branch:** `agentic/homogenize-landings`
**Depends on:** AG2 DONE — satisfied

## What was done

1. `.cursor/rules/ttod-editing.mdc` — kept its real frontmatter (`description`, `globs:
   ttod.yml`, `alwaysApply: false`) unchanged; replaced the full body with a 3-line redirect
   naming `agentic/rules/ttod-editing.md` as canonical.
2. `.cursor/skills/public-docs-i18n/SKILL.md` — kept its real frontmatter (`name`,
   `description`) unchanged; replaced the full body with a 3-line redirect naming
   `agentic/skills/public-docs-i18n/SKILL.md` as canonical.
3. **`.claude/agents/cascade-phase-executor.md` and `cascade-cold-reviewer.md` — left
   untouched.** AG3's deliverable #2 ("stubs remapped per AG0") is satisfied by *not*
   remapping them: W0 §2 already froze that these point at `~/src/.agents/agents/` correctly,
   since the two subagents are cross-repo cascade-forge infrastructure, not TTOD-scoped
   content. Re-pointing them at `ttod/agentic/agents/` (which stays empty per W0) would
   contradict the frozen decision, not fulfill it.
4. Did not delete `.cursor` or `.claude` directories — landings only, per scope.

## Verification

- `test -f agentic/rules/ttod-editing.md` and `test -f agentic/skills/public-docs-i18n/SKILL.md`
  — both exit 0 (redirect targets exist).
- Non-frontmatter body line count: 3 lines in each stub (well under the ~15-line ceiling), each
  containing an explicit canonical path.
- Frontmatter validity: Cursor rule retains `description`/`globs`/`alwaysApply`; Cursor skill
  retains `name`/`description`. (Claude agent frontmatter unchanged — see point 3 above; no
  `name`/`description`/`tools`/`model` fields were touched because no `.claude` file changed.)
- Negative check: `rg -n 'Never delete quotes' .cursor/rules/` → no match (body moved).
  `rg -n 'Never delete quotes' agentic/rules/` → matches `agentic/rules/ttod-editing.md:18`.
- `python -m unittest discover -s tests -p 'test_*.py'` → 219 tests, OK.
- `python cli.py validate --strict --json` → `is_valid: true`, exit 0.
- `git status --porcelain` shows exactly the two `.cursor` files modified, plus this session's
  pre-existing AG0–AG2 doc artifacts and the AG2-created `agentic/` additions. No `.claude`
  file touched. No `ttod.yml` diff.

## Residual risk (carried from the runbook, not new)

The runbook's own risk list names "Claude Code agents that ignore the redirect instruction" as
a known convention risk to document in AG5 — restated here for continuity, not newly
discovered. The pre-existing broken relative link inside `ttod-editing`'s body (flagged in
`PHASE-AG2-REPORT.md`) now also exists inside the `agentic/rules/ttod-editing.md` canonical
copy only — the stub itself does not repeat that link, so AG3 introduces no new instance of
the bug.

## Acceptance

- [x] Each landing file's non-frontmatter body is ≤ ~15 lines and contains an explicit
      canonical path.
- [x] `test -f` for every redirect target exits 0.
- [x] Cursor rule frontmatter still has `description`/`globs`/`alwaysApply`; Cursor skill
      frontmatter still has `name`/`description`. Claude agent frontmatter unchanged (not
      touched — correctly, per W0 §2).
- [x] Full suite green.
- [x] Negative check passes as specified.

Cold review found no discrepancies, independently confirmed "`.claude` untouched" against
W0's own frozen inventory table (not the report's own spin), and re-ran the full suite,
`validate --strict`, and both negative/positive `rg` checks itself. Promoted to DONE.
