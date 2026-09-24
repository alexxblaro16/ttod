# PHASE-AG4-COLD-REVIEW.md

**Reviewer:** `cascade-cold-reviewer` (fresh subagent session, zero prior context on this
implementation) · 2026-09-18
**Reviewed deliverable:** `docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/PHASE-AG4-REPORT.md`
**Verdict:** **PASS**. Zero findings, no P0/P1/P2 issues. Safe to promote to DONE.

## Acceptance audit

| Acceptance bullet | Verdict | Evidence |
| --- | --- | --- |
| `AGENTS.md` states `agentic/` as edit-home, `.cursor`/`.claude` as landings | PASS | Path table matches |
| Discovery map (harness / `services/mcp/` / Astro as client) without claiming Astro/`agentic/` contain the server | PASS | Verbatim match to `RATIONALE.md`/W0 frozen wording; explicit "do not relocate under `agentic/`" |
| `agentic/README.md` links back, one-lines `services/mcp/` | PASS | Confirmed still true, unmodified by AG4 as claimed |
| `git grep` negative check for the old `.cursor` instruction | PASS | Exit 1, no match |
| Privacy watcher path unchanged in CI, script exists | PASS | 4 occurrences in workflow, file present |
| Generator dry-run / documented copy list | PASS (documented, not edited) | See judgment call below |
| Full suite green | PASS | 219 tests OK |
| `validate --strict` | PASS | `is_valid: true`, exit 0 |
| `services/mcp` not moved under `agentic/` | PASS | Confirmed both ways |
| No `ttod.yml` diff | PASS | Confirmed empty |

## Additional independent checks

- `git show skeleton/ts5-hello-world:.cursor/rules/ttod-editing.mdc | wc -l` → 153 lines,
  confirmed full body, matching the report's claim exactly.
- `scripts/generate-cohort-starter.sh` has no `.cursor`/`agentic` coupling — confirmed clean.
- `git diff --stat -- AGENTS.md` → 29 insertions/4 deletions, 1 file — the only file this
  phase's own diff touches. All other modified/untracked files pre-date AG4 (verified against
  AG1's own report content). No historical `PHASE-*-REPORT.md` was touched.
- The `FAIL: 2 public-privacy finding(s)` stderr line is a negative-fixture assertion inside
  `tests/test_public_privacy_watcher.py`, not a suite failure — the run still ends OK.

## Judgment call — generator script (independent verdict, not deferred to the report)

Agree: "verified non-issue, documented, not edited" is correct, reached independently, not
accepted on the report's say-so. Two load-bearing facts confirmed directly: the source branch
is pre-fork and genuinely unaffected today (153-line full body), and the sibling generator has
zero `.cursor`/`agentic` coupling. Patching the generator now for a hypothetical future rebase
would be speculative and untestable against current state — correctly deferred with a
documented tripwire for whoever regenerates that baseline post-AG5-merge.

## Result

Every acceptance bullet has runnable evidence behind it, not just the report's assertion.
