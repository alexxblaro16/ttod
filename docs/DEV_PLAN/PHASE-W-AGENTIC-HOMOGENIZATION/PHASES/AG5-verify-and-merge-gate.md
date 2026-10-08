# AG5 — Verify, pedagogical merge note, and human merge gate

**Status:** DONE, MERGED (2026-09-18/19) — full verification green, pedagogical note landed
in `AGENTS.md`, PR [#21](https://github.com/ruvebal/ttod/pull/21) cold-reviewed PASS with zero
blocking findings, then merged into `main` by the product owner via
`gh pr merge 21 --merge --delete-branch --admin` (the required `typecheck-and-build` check
hadn't run against the branch). See `../PHASE-AG5-REPORT.md` § Merge decision.  
**Depends on:** AG0–AG4 complete on `agentic/homogenize-landings` — satisfied, see
`../PHASE-AG4-REPORT.md`

## Goal

Prove the homogenized tree works; file the pedagogical “doorway / room / merge”
note; open (or prepare) the PR; **stop before merge**. Merge is a named human act —
the classroom analogue of the second approval that lands a quote-accept diff.

## Deliverables

1. Verification transcript: `make check` (or validate + stats --check + full
   unittest), privacy watcher on `docs/public` if touched, import smoke for any
   Python under `agentic/report-steward/scripts/`.
2. Short pedagogical paragraph landed in `AGENTS.md` or
   `docs/public/teaching/…` per AG0 (orchestrator §6 classroom phrasing).
3. PR body checklist linking Phase W INDEX + cold-review docs.
4. Product-owner merge decision line in `PHASE-AG5-REPORT.md` (`MERGE_APPROVED` /
   `MERGE_DEFERRED` / `MERGE_REJECTED`) — agent never sets `MERGED` itself.
5. Optional `AG6_DEFERRED` or `AG6_FOLLOW_ON` flag if student IDE harness ships in a
   second PR after layout merge.

## Scope

| In | Out |
| --- | --- |
| Verify + docs note + PR preparation | `git merge` / `gh pr merge` by the agent |
| Recording the pedagogical isomorphism | Running `cli.py proposal accept` |

## Prompt (paste when executing)

```text
Execute AG5 only. Run full verification. Add the pedagogical merge note.
Prepare PR description from the orchestrator §5–§6. Push the branch and open
the PR with `gh pr create` (commands below). Do not merge. Do not force-push.
Stop at VERIFYING with MERGE_* decision left for the human.
Do not mark DONE; hand off for cold review. After cold review, only a named
human may record MERGE_APPROVED and perform the merge.
```

## Commands (exact — agent runs PR creation only, never merge)

```bash
# Agent, after verification is green and the PR body is drafted in the report:
git push -u origin agentic/homogenize-landings   # only if the human asked for a push
gh pr create --base main --head agentic/homogenize-landings \
  --title "agentic: homogenize rules/skills/agents; .cursor/.claude as landings" \
  --body-file <path to the PR-body section drafted in PHASE-AG5-REPORT.md>

# HUMAN ONLY — never run by the agent, never in the same session that opened the PR:
# 1. Read PHASE-AG5-COLD-REVIEW.md; confirm no blocking findings remain.
# 2. Confirm `git diff main...agentic/homogenize-landings -- ttod.yml` is empty.
# 3. Record MERGE_APPROVED in PHASE-AG5-REPORT.md.
# 4. gh pr merge --merge --delete-branch   # or --squash, human's call
```

## Acceptance

- [ ] Full suite + strict validate + stats --check exit 0 on the branch.
- [ ] Privacy watcher exit 0 on the paths AG4 touched (if any public docs).
- [ ] Pedagogical note present and does **not** claim layout PRs call
      `proposal accept`.
- [ ] PR checklist includes: landings thin, bodies under `agentic/`, CI path
      preserved, no `ttod.yml` diff.
- [ ] `git diff main...HEAD -- ttod.yml` is empty.
- [ ] Cold-review doc filed; blocking findings closed.
- [ ] Report status is DONE only when human recorded merge decision; if merge
      deferred, status may be DONE for the *verification* work with
      `MERGE_DEFERRED` explicit.
- [ ] `gh pr merge` never appears in this phase's own execution transcript —
      only in the report as a command block left for the human.

## Pedagogical merge checklist (for the human)

Use this when teaching or when merging:

1. Open the PR — treat it like a proposal under review.
2. Read cold review — another agent/mind already audited Acceptance.
3. Confirm `ttod.yml` unchanged — this PR is layout governance, not corpus accept.
4. Merge only if landings are doorways and `agentic/` is the room.
5. Tell students: *same discipline as quote accept; different write surface.*

## Risks

- Merging with a non-empty `ttod.yml` diff smuggles corpus changes into a layout PR.
- Self-merging by an agent collapses the two-touchpoint lesson Phase V already paid for.
