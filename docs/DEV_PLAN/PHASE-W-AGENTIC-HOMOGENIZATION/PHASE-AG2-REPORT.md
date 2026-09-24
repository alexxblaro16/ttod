# PHASE-AG2-REPORT.md

**Status:** DONE (2026-09-18) — cold-reviewed PASS, zero discrepancies. See
[`PHASE-AG2-COLD-REVIEW.md`](PHASE-AG2-COLD-REVIEW.md).
**Runbook:** [`PHASES/AG2-migrate-bodies-into-agentic.md`](PHASES/AG2-migrate-bodies-into-agentic.md)
**Branch:** `agentic/homogenize-landings` (created in AG1, `main`@`7a738caefddc4b75fab2a7bf98e4c39f77342cfb`)
**Depends on:** AG1 DONE — satisfied

## What was done

1. Copied two TTOD-scoped bodies into `agentic/`, byte-identical, no content edits:
   - `.cursor/rules/ttod-editing.mdc` → `agentic/rules/ttod-editing.md`
   - `.cursor/skills/public-docs-i18n/SKILL.md` → `agentic/skills/public-docs-i18n/SKILL.md`
2. Did **not** touch `.cursor/` originals — they still hold full bodies; hollowing them into
   landings is AG3's job, not this one (AG2's own scope explicitly separates move-first from
   stub-second so rollback is one revert).
3. Did **not** create anything under `agentic/agents/` — per W0 §2, `cascade-phase-executor`
   and `cascade-cold-reviewer` are cross-repo infrastructure, not TTOD-scoped content, and stay
   canonical at `~/src/.agents/agents/`. That directory remains absent, matching the decision
   record and AG1's frozen target tree exactly.
4. Left `agentic/report-steward/` completely untouched — confirmed at the same path CI expects.
5. Wrote `agentic/README.md` — a short map of `agentic/`'s contents, what's TTOD-scoped vs
   reserved vs deliberately absent, and the required back-link to `AGENTS.md` (the actual
   `AGENTS.md` edit is AG4's job; this file only points at it).

## Byte-identity proof (Acceptance bullet 2)

```
sha256(.cursor/rules/ttod-editing.mdc)               = 9fdb21827aaeab22827af516cf28397617a77ec4a55040215b7af658cdc2c6b6
sha256(agentic/rules/ttod-editing.md)                = 9fdb21827aaeab22827af516cf28397617a77ec4a55040215b7af658cdc2c6b6
sha256(.cursor/skills/public-docs-i18n/SKILL.md)     = fc693a9c41d29b1661b4849f672bcd0ed694bc8dec2b19115d9ad31e7b1171a6
sha256(agentic/skills/public-docs-i18n/SKILL.md)     = fc693a9c41d29b1661b4849f672bcd0ed694bc8dec2b19115d9ad31e7b1171a6
```

`diff -u` between each pair is empty. Spot-read three non-empty paragraphs from both moved
files at the new path — content intact (v3 required fields, bilingual `translation_of`
invariants for `ttod-editing`; skill-stack table and page rules for `public-docs-i18n`), not
truncated.

## Verification

- `python cli.py validate --strict --json` → `{"is_valid": true, "errors": [], "warnings": []}`, exit 0.
- `python -m unittest discover -s tests -p 'test_*.py'` → **219 tests, OK**. (One test emits a
  `FAIL: 2 public-privacy finding(s)` line to stderr — that is a negative-case assertion inside
  the privacy-watcher test itself, not a suite failure; the overall run reports OK.)
- `test -f agentic/report-steward/scripts/check_public_privacy.py` → exit 0, path unchanged.
- `git status --porcelain` shows only: two new directories (`agentic/rules/`, `agentic/skills/`),
  one new file (`agentic/README.md`), plus this session's pre-existing AG0/AG1 doc-status edits.
  No `.cursor` file was modified or deleted. No `ttod.yml` diff.

## Amend-on-surprise note

`.cursor/rules/ttod-editing.mdc` line 9 links `[AGENTS.md](../AGENTS.md)` — this resolves to
`.cursor/AGENTS.md`, which does not exist; the correct relative path from `.cursor/rules/` would
be `../../AGENTS.md`. This is a **pre-existing bug in the source file**, unrelated to Phase W and
not introduced by this move. Per AG2's own risk note ("editing bodies while we are here hides
migration bugs — forbid drive-by edits"), the bug was copied byte-for-byte into
`agentic/rules/ttod-editing.md` rather than silently fixed. Flagging here for AG4 (which owns
evergreen reference rewrites) to correct in both the new canonical body and, after AG3, whatever
the landing stub says — not fixed in this report.

## Acceptance

- [x] Every AG0 "move" row has a file at the new path.
- [x] `diff` of body text (ignoring path) is empty vs pre-move copy.
- [x] `agentic/report-steward/scripts/check_public_privacy.py` still exists at the same path.
- [x] Full unittest suite exit 0; `cli.py validate --strict` exit 0.
- [x] Spot-read three non-empty paragraphs from both moved files at the new path — confirmed
      not truncated (see § Byte-identity proof).

Cold review found zero discrepancies against independently re-run verification (suite,
validate, hashes, diffs) and confirmed the line-9 bug is real and correctly deferred, not
missed. Promoted to DONE.
