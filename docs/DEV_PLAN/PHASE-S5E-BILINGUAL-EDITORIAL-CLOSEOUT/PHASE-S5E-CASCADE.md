# Technical director — TTOD bilingual editorial closeout (S5E0–S5E6)

**Status:** ACTIVE. Execute one phase at a time, in order. The phase prompts and exit gates are
separate files in this directory.
**Evidence:** [INDEX.md](INDEX.md) · [RATIONALE.md](RATIONALE.md) ·
[FINDINGS-2026-11-08.md](FINDINGS-2026-11-08.md).
**Parent plan:** [`PHASE-S5-BILINGUAL-CORPUS-TRANSLATION-PLAN.md`](../PHASE-S5-BILINGUAL-CORPUS-TRANSLATION-PLAN.md).

## Programme (do not invert)

The Gate cell's first word is the Cascade Forge runner's state token. S5E0–S5E1 are DONE; S5E2 is
READY after this worktree is integrated into the harness base. Private ledger canonical path:
`/Users/ruvebal/src/ttod/_private/editorial/EDITORIAL-REVIEW-LEDGER.json` via
`TTOD_EDITORIAL_LEDGER`. Accepted-ID linkage denominator is 230; blackbox-validation denominator is
229 (plus 1 studio: `wis-033`).

| Step | File | Deliverable | Gate |
| ---: | --- | --- | --- |
| 0 | [PHASE-S5E0.md](PHASE-S5E0.md) | Read-only baseline, current vault run state, and editorial decision record | DONE — cold review F1–F3 P2; verify log exit 0 |
| 1 | [PHASE-S5E1.md](PHASE-S5E1.md) | Frozen editorial policy, glossary, decision register, ledger schema/location | DONE — cold review F1 fixed; verify exit 0 |
| 2 | [PHASE-S5E2.md](PHASE-S5E2.md) | Human disposition for each residual alternate proposal | READY — EDITORIAL_POLICY_APPROVED; integrate worktree before start |
| 3 | [PHASE-S5E3.md](PHASE-S5E3.md) | Two-pass human review of every in-scope pair | BLOCKED — queue adjudicated and private ledger approved |
| 4 | [PHASE-S5E4.md](PHASE-S5E4.md) | Approved corrections applied atomically, or verified NOT_NEEDED | BLOCKED — CANONICAL_CORRECTIONS_APPROVED or empty signed list |
| 5 | [PHASE-S5E5.md](PHASE-S5E5.md) | Independent cold audit, alignment/coverage files, edition statement | BLOCKED — S5E3 DONE and S5E4 DONE |
| 6 | [PHASE-S5E6.md](PHASE-S5E6.md) | Programme index reconciled and Phase S closeout recorded | BLOCKED — EDITION_RELEASE_APPROVED or named release blocker |

Exit scripts `PHASE-S5E<n>.exit-gate.sh` turn each phase's acceptance criteria into a command that
the separate Cascade Forge runner executes. Reports are filed after cold-review triage. The
runner's verify log is the evidence of the gate command's real output.

## Master paste (start / resume)

```text
Execute the next incomplete phase only of the TTOD bilingual editorial closeout, in order S5E0 →
S5E6. Controlling docs:

- Orchestrator: docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/PHASE-S5E-CASCADE.md
- Index and live state: docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/INDEX.md
- Product rationale: docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/RATIONALE.md
- Live evidence snapshot: docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/FINDINGS-2026-11-08.md
- Historical translation plan: docs/DEV_PLAN/PHASE-S5-BILINGUAL-CORPUS-TRANSLATION-PLAN.md
- Canonical contract: AGENTS.md

Use Cascade Forge: execute exactly one phase package; the runner must open its worktree; stop at
VERIFYING; then a separate, context-clean cold reviewer checks the diff and runner verify log. The
orchestrator triages findings and updates the phase report/status. Never self-certify DONE.

## Programme
Do not start a later phase until the current phase is DONE after cold review. Re-read live state at
each phase start; do not trust old counts or process state in prose.

## Hard constraints
- “Coda con sabiduría” (`img-086`) is correct and intentional per the product owner on 2026-11-08.
  Preserve it; keep the historical S4 report intact; no model or reviewer may silently normalize it.
- `ttod.yml` is human-governed. Never hand-edit it. Use a tested repository transaction only.
- Never delete a quote or proposal record. Use governed deprecation and append-only review actions.
- Human reviewers make every acceptance, rejection, withdrawal, correction, and release decision.
- A model may search, compare, or draft. It cannot decide correctness, accept, dispose, or release.
- Derive live counts from a fresh CLI export. Do not hardcode corpus totals into current-state prose.
- Keep item-level editorial notes in the product-owner-approved private ledger. Public reports contain
  only approved aggregate evidence and necessary provenance.
- The Lao Tzu/Ahmes pipeline is a separate running process. S5E must not stop, restart, edit, or
  inject into Ahmes, Athanor, Postgres, DevIAC, Ollama, or the ttod-bridge pending directory.
- Taoist sources guide composition and metaphor; they do not substantiate software, education,
  Athanor, or WPL factual claims. Use full Ahmes pages and a cite-safe resolver result for any
  scholarly citation. Preserve `[BIBLIO-GAP]` where unresolved.
- Do not push, publish, open a PR, merge, commit, or tag without an explicit human request.

## Out of scope
- New corpus-wide translation generation or model benchmarking.
- New Lao Tzu source ingestion, vault injection, database routing changes, or citation-metadata edits.
- Changing canonical TTOD quote wording before the S5E3 ledger and explicit correction approval.
- Publishing the bilingual edition before S5E5 and product-owner approval.

## Resume rule

Closed phase/report status enum: `BLOCKED | READY | IN_PROGRESS | VERIFYING | COLD_REVIEW | PARTIAL | DONE`.
Use `outcome: NOT_NEEDED` inside a report when no canonical correction is required; the phase still
passes through `VERIFYING → COLD_REVIEW → DONE`.

- `DONE`: skip to the next phase whose entry gate is met; update `INDEX.md` so only that next phase
  is READY.
- `PARTIAL`: resume the same phase from its report's exact safe resume point; later phases stay
  BLOCKED.
- `IN_PROGRESS`: resume the named bounded work; do not restart a ledger or batch already in
  progress and do not advance.
- `VERIFYING`: run the external exit gate and full suite; then hand the runbook, diff, verify log,
  and constraints to a fresh cold reviewer.
- `COLD_REVIEW`: wait for the independent report, triage each Fn, amend this orchestrator and
  downstream assumptions if the world changed, then file the report as DONE or PARTIAL.
- `BLOCKED`: resolve the named human decision, process dependency, or data blocker before advancing.
- `READY`: use Cascade Forge `start` for this phase only; do not open another lane worktree.

The executor must confirm `.cascade-lane` matches this cascade. If not, stop and hand off without
making changes.

## Closing protocol

`BLOCKED → READY → IN_PROGRESS → VERIFYING → COLD_REVIEW → DONE`

1. Implementer follows [cascade-phase-executor](../../../.claude/agents/cascade-phase-executor.md)
   and stops at VERIFYING. It does not run or self-approve the exit gate.
2. Runner runs the phase's executable `PHASE-S5E<n>.exit-gate.sh` and records stdout/exit in the
   verify log.
3. A fresh reviewer follows
   [cascade-cold-reviewer](../../../.claude/agents/cascade-cold-reviewer.md), receives the
   exact phase prompt, diff, full-suite transcript, runner verify log, and these hard constraints.
   It files `PHASE-S5E<n>-COLD-REVIEW.md`; it does not edit or mark DONE.
4. Orchestrator triages findings, amends downstream runbooks in the same change if assumptions
   broke, then files `PHASE-S5E<n>-REPORT.md` after review. Only the product owner/orchestrator
   records DONE.
5. Do not commit unless the human asks. Stage by explicit file paths if later authorized; the local
   generated Lao Tzu pack is untracked and must never be swept in with `git add -A agentic`.
   Before starting the next phase, the product owner must integrate the reviewed phase branch into
   the base commit used by Cascade Forge; otherwise the next fresh worktree will not contain the
   prior phase's accepted artifacts.

## Data and evidence layer map

| Layer | Role | S5E authority |
| --- | --- | --- |
| `ttod.yml` | canonical quotes, IDs, lifecycle, relations | Repository transaction only |
| `proposals/*.json` | accepted history and residual TTOD proposals | CLI review/accept only; append-only human activities |
| Editorial policy/glossary/decision register | human editorial authority | product owner approves |
| Private review ledger | item-level editorial notes and decisions | human reviewers; access-controlled location approved at S5E1 |
| Ahmes extraction DBs | full source nodes, page anchors, source metadata | inspect/cite only; this cascade does not mutate |
| Athanor project `scholar-lao-tzu` | searchable project pointers | read-only search only; no injection in S5E |
| DevIAC vectors | derived discovery/search | read-only discovery; prior database mismatch is a known limitation |
| ttod-bridge pending | candidate proposals from compose lens | out of scope for S5E |

## Shared verification commands

```bash
cd /Users/ruvebal/src/ttod
git status --short --branch
git rev-parse HEAD
shasum -a 256 ttod.yml
.venv/bin/python cli.py validate --strict --json
.venv/bin/python cli.py stats --check
make check
/Users/ruvebal/src/ttod/.venv/bin/python \
  /Users/ruvebal/src/.cursor/skills/ttod-bridge/scripts/tests/test_ttod_bridge.py
```

Run full repository checks after any code or canonical changes. Documentation-only phases still
run the relevant `make check`, `git diff --check`, and public privacy gate when public paths change.

## Amend on surprise

If a phase finds a changed canonical denominator, an unexpected proposal type, a missing source
page, a changed pipeline state, a previously unresolved citation becoming cite-safe, or a failed
translation relation, record the evidence and amend this orchestrator plus every downstream phase
whose assumptions changed before proceeding. Do not patch around a changed upstream contract in a
later phase.

## Runner commands

The Cascade Forge runner lives outside this repository at
`/Users/ruvebal/src/.cursor/skills/cascade-forge/scripts/cascade-harness.sh`.

```bash
CASCADE=/Users/ruvebal/src/ttod/docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT
RUNNER=/Users/ruvebal/src/.cursor/skills/cascade-forge/scripts/cascade-harness.sh

"$RUNNER" next "$CASCADE"
"$RUNNER" start "$CASCADE"
# Implement one phase inside the returned worktree, then stop at VERIFYING.
"$RUNNER" verify "$CASCADE" PHASE-S5E0.md /path/printed/by/start
```

The runner opens a new worktree from committed `HEAD`; the cascade pack must be committed before
using `start`. `next` is read-only and can inspect an uncommitted pack. This plan has not opened a
worktree or committed anything.
