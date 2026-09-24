# AG2 — Migrate TTOD-scoped bodies into `agentic/`

**Status:** DONE (2026-09-18) — bodies moved byte-identical to `agentic/rules/` and
`agentic/skills/public-docs-i18n/`; `agentic/README.md` seeded; cold-reviewed PASS. See
`../PHASE-AG2-REPORT.md` and `../PHASE-AG2-COLD-REVIEW.md`.  
**Depends on:** AG0 map; AG1 target paths — both satisfied, see `../PHASE-AG1-REPORT.md`

## Goal

Move **bodies** of TTOD-scoped rules and skills into `agentic/` without changing
their substance. Leave `agentic/report-steward/` pack structure intact. Do not yet
hollow out `.cursor`/`.claude` (that is AG3) unless AG0 requires atomic
move+stub — default is move first, stub second, so rollback is one revert.

## Deliverables

1. Bodies at AG0-approved paths (e.g. `agentic/rules/ttod-editing.md`,
   `agentic/skills/public-docs-i18n/SKILL.md`).
2. Pre/post digests or `diff -u` proof bodies match.
3. `agentic/README.md` map (short): packs vs flat rules/skills/agents.

## Scope

| In | Out |
| --- | --- |
| TTOD-local `.cursor` bodies listed in AG0 | Studio `~/src/.cursor/skills/*` wholesale |
| Optional copy of TTOD-needed agent defs into `agentic/agents/` | Rewriting stub landings (AG3) |
| | `ttod.yml`, proposal accept |

## Prompt (paste when executing)

```text
Execute AG2 only on branch agentic/homogenize-landings (or AG1’s frozen name).
Move TTOD-scoped bodies into agentic/ per AG0/AG1. Do not hollow landings yet.
Do not touch report-steward paths CI uses. Run make check / full unittest.
Stop at VERIFYING. Do not mark DONE; hand off for cold review.
```

## Acceptance

- [ ] Every AG0 “move” row has a file at the new path.
- [ ] `diff` of body text (ignoring path) is empty vs pre-move copy.
- [ ] `agentic/report-steward/scripts/check_public_privacy.py` still exists at the
      same path; CI workflow path string unchanged or intentionally updated in AG4 only.
- [ ] Full unittest suite exit 0; `cli.py validate --strict` exit 0.
- [ ] This exact check would fail if a body were truncated during move: spot-read
      three non-empty paragraphs from `ttod-editing` and `public-docs-i18n` at the
      new path.

## Risks

- Moving studio-shared skills into the repo forks them from `~/src/.cursor/skills/`.
- Editing bodies “while we are here” hides migration bugs — forbid drive-by edits.
