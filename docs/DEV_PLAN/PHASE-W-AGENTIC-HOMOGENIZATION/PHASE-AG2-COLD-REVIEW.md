# PHASE-AG2-COLD-REVIEW.md

**Reviewer:** `cascade-cold-reviewer` (fresh subagent session, zero prior context on this
implementation) · 2026-09-18
**Reviewed deliverable:** `docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/PHASE-AG2-REPORT.md`
**Verdict:** **PASS**. Zero discrepancies between the report's claims and independently
verified disk/CI state. No amendment required.

## Acceptance audit

| # | Check | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Branch is `agentic/homogenize-landings` | PASS | `git branch --show-current` |
| 2 | `.cursor/rules/ttod-editing.mdc` == `agentic/rules/ttod-editing.md` | PASS | `diff -u` empty; SHA-256 recomputed independently, matches report |
| 3 | `.cursor/skills/public-docs-i18n/SKILL.md` == `agentic/skills/public-docs-i18n/SKILL.md` | PASS | `diff -u` empty; SHA-256 recomputed independently, matches report |
| 4 | `.cursor` originals unmodified/undeleted | PASS | No entry for either path in `git status --porcelain`; both files present with correct content |
| 5 | `agentic/agents/` does not exist | PASS | Confirmed absent |
| 6 | `agentic/report-steward/scripts/check_public_privacy.py` exists, untouched | PASS | Present at exact path, no working-tree diff |
| 7 | `agentic/README.md` links `../AGENTS.md`, does not claim `services/mcp/` under `agentic/` | PASS | Explicitly states product MCP lives at `../services/mcp/` and "is never nested here" |
| 8 | Full unittest suite OK (219 tests) | PASS | "Ran 219 tests … OK"; the `FAIL: 2 public-privacy finding(s)` line is a negative-case assertion inside one test, not a suite failure — confirmed |
| 9 | `cli.py validate --strict --json` exit 0 | PASS | `is_valid: true`, no errors |
| 10 | `git status --porcelain` — no `ttod.yml` diff, no `.cursor` changes | PASS | Only new `agentic/` additions + pre-existing doc edits |
| 11 | Pre-existing broken link in `ttod-editing.mdc` line 9 | CONFIRMED REAL | `../AGENTS.md` from `.cursor/rules/` resolves to a nonexistent `.cursor/AGENTS.md`; correct path is `../../AGENTS.md` |
| 12 | Spot-read 3 non-empty paragraphs each file, not truncated | PASS | Both files read through to their actual end, no mid-section cutoff |

## On deferring the line-9 fix

Correct call. AG2's own runbook names "editing bodies while we are here hides migration
bugs" as a risk to forbid; reference correction is AG4's explicit remit. Fixing it now would
also need re-applying consistently across the `.cursor` original, the new `agentic/` canonical,
and the eventual AG3 stub — better done once, by the phase that owns it.

## Result

All five AG2 Acceptance bullets verified true against runnable evidence, not the report's own
checkmarks. Safe to promote to DONE.
