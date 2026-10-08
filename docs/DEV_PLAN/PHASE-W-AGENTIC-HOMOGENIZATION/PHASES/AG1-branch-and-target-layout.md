# AG1 — Branch creation plan and target layout freeze

**Status:** DONE (2026-09-18) — target tree + branch name frozen, cold-reviewed clean; branch
`agentic/homogenize-landings` created at explicit human authorization from `main` @
`7a738caefddc4b75fab2a7bf98e4c39f77342cfb`. See `../PHASE-AG1-REPORT.md` and
`../PHASE-AG1-COLD-REVIEW.md`.  
**Depends on:** `DECISIONS/W0-2026-09-18-AGENTIC-HOME.md` — frozen  
**Does not authorize (until product owner says so):** actually running `git switch -c`

## Goal

Freeze the **target directory tree** and the **branch name**, and write the exact
commands a human or authorized agent will use to open the branch. This planning
session (2026-09-18) does **not** create the branch; AG1 execution may create it
only after explicit authorization in the phase report’s entry gate.

## Deliverables

1. Frozen target tree (paths) matching orchestrator §7 as amended by AG0.
2. Frozen branch name (default proposal: `agentic/homogenize-landings`).
3. `PHASE-AG1-REPORT.md` recording `git rev-parse HEAD` of the intended base and
   either (a) proof the branch exists, or (b) “creation deferred” with the exact
   command block left for the human.

## Scope

| In | Out |
| --- | --- |
| Layout sketch + branch naming | Migrating file bodies (AG2) |
| Documenting `git switch -c …` | Push/merge |
| Optional worktree via cascade-harness | Touching `ttod.yml` |

## Prompt (paste when executing)

```text
Execute AG1 only per
docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/PHASES/AG1-branch-and-target-layout.md.

Confirm AG0 DONE. Freeze the target tree and branch name in the report.
If — and only if — the human’s paste explicitly says “create the branch now”,
run from a clean main:
  git rev-parse HEAD
  git switch -c agentic/homogenize-landings
Otherwise record the same commands as deferred. Do not push. Do not move files.
Stop at VERIFYING. Do not mark DONE; hand off for cold review.
```

## Acceptance

- [ ] Branch name recorded and ≠ `agentic/gh-pack`.
- [ ] Base commit SHA recorded.
- [ ] Target tree lists `agentic/rules`, `agentic/skills`, `agentic/agents` (or
      AG0-approved equivalent) plus preserved `agentic/report-steward/`.
- [ ] Either branch exists locally **or** report status PARTIAL/DONE with deferred
      creation and no accidental branch.
- [ ] `git status` clean aside from any AG1 doc edits the human authorized.

## Risks

- Creating the branch before AG0 freeze locks the wrong layout into history.
- Reusing `agentic/gh-pack` mixes unrelated gh-pack commits into the cleanup story.
