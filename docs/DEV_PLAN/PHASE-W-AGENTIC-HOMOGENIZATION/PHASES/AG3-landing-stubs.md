# AG3 — Convert `.cursor` / `.claude` into landings

**Status:** DONE (2026-09-18) — `.cursor` rule/skill hollowed to 3-line redirect stubs;
`.claude` correctly left untouched per W0 §2; cold-reviewed PASS, no findings. See
`../PHASE-AG3-REPORT.md` and `../PHASE-AG3-COLD-REVIEW.md`.  
**Depends on:** bodies present under `agentic/` — satisfied, see `../PHASE-AG2-REPORT.md`

## Goal

Replace proprietary-tree **bodies** with thin **landings**: keep each tool’s real
frontmatter (so discovery still works); body becomes “read the canonical file now.”
Mirror the stub pattern already used by `ttod/.claude/agents/cascade-*.md`.

## Deliverables

1. `.cursor/rules/*.mdc` and `.cursor/skills/*/SKILL.md` as stubs → `agentic/…`.
2. `.claude/agents/*.md` stubs remapped per AG0 (studio `.agents` and/or
   `ttod/agentic/agents/`).
3. Grep proof: no multi-paragraph procedure remains under landings.

## Scope

| In | Out |
| --- | --- |
| Stub rewrite of TTOD landings | Deleting `.cursor` or `.claude` directories |
| Frontmatter validity | Changing Cursor/Claude product behavior beyond redirect |

## Prompt (paste when executing)

```text
Execute AG3 only. Hollow .cursor and .claude landings to redirects per AG0.
Keep frontmatter fields each tool needs. Verify stub targets exist on disk.
Run full suite. Stop at VERIFYING. Do not mark DONE; hand off for cold review.
```

## Acceptance

- [ ] Each landing file’s non-frontmatter body is ≤ ~15 lines and contains an
      explicit canonical path.
- [ ] `test -f` (or equivalent) for every redirect target exits 0.
- [ ] Cursor rule frontmatter still has `description` (and `globs`/`alwaysApply` as
      before); Claude agent frontmatter still has `name`/`description`/`tools`/`model`
      as required by AG0.
- [ ] Full suite green.
- [ ] Negative check: `rg -n 'Never delete quotes' .cursor/rules/` returns no match
      (body moved); same string **does** match under `agentic/rules/`.

## Risks

- Stub that says “read canonical” but points at a missing file — silent agent failure.
- Claude Code agents that ignore the redirect instruction (known convention risk;
  document as residual risk in AG5).
