# PHASE-S5E0 — baseline and decision register

> **Track:** read-only evidence across TTOD and the Lao Tzu source pipeline.
> **Status:** DONE.
> **Depends on:** none.
> **Out of scope:** editing canonical/proposal state; changing or stopping the running sibling pipeline; new vault searches or injection.

## Goal

Recompute current TTOD coverage and queue state, inspect the Lao Tzu pipeline's current read-only
status, and record the product owner's decision that “Coda con sabiduría” is correct. The live
pipeline was in Ahmes batch according to `state.json`; determine whether that remains true when this
phase starts. This phase reconciles claims with stores, not reruns the pipeline.

## Deliverables

- Updated `FINDINGS-2026-11-08.md` with current dated evidence and exact commands summarized.
- `EDITORIAL-DECISIONS.md` entry `EDITORIAL-DECISION-2026-11-08-CODA`.
- Cascade Forge runner verify log, independent cold review, and post-review phase report.

## Prompt (Implementation Agent)

```text
Implement PHASE-S5E0 per
docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/PHASE-S5E0.md.

Use the Cascade Forge worktree opened for this phase; confirm .cascade-lane matches
PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT. Read AGENTS.md, the orchestrator, this phase file, the
grounding skill /Users/ruvebal/.codex/skills/ground-with-athanor-ahmes/SKILL.md, and the prior Y3 ops
note.

1. Recompute corpus counts, translation-pair uniqueness, proposal states, accepted-ID linkage,
   validation metadata, and pair structural parity from a fresh CLI export.
2. At phase start and end, read the Lao Tzu pipeline state, recent non-sensitive log tail, prior
   INJECT_DONE record, and process listing. Do not source .env, print credentials, or send new
   requests to any vault. Current snapshot: failed at `athanor_ready` after PostgreSQL refused the
   vector-ingest connection; injection was not evidenced. Do not restart the pipeline in S5E0.
3. Amend FINDINGS-2026-11-08.md with current dated evidence and exact command outputs summarized.
4. Add EDITORIAL-DECISIONS.md recording: img-086 wording “Coda con sabiduría”; decision=preserve;
   authority=Rubén Vega Balbás; decided=2026-11-08; rationale=product-owner intent; supersedes the
   S4 report's current recommendation while preserving that historical report unchanged.
5. Do not change ttod.yml, proposals, external vaults, the running pipeline, or public publication.

Run the phase exit gate only through the separate Cascade Forge runner. Run make check and the
bridge test as stated by the orchestrator. Leave work at VERIFYING; do not mark DONE, write the
post-review report, or continue to S5E1.
```

## Acceptance

- Fresh CLI export provides dynamic counts; every active Spanish translation resolves to one active
  English original, with no duplicate active sisters.
- Every accepted proposal ID resolves to a unique canonical quote ID.
- Strict validate, stats check, `make check`, and bridge test have real exit 0 evidence in runner
  verify log.
- Decision register states the “Coda” decision exactly and leaves PHASE-S4-REPORT.md unchanged.
- `git diff HEAD -- ttod.yml proposals` is empty.
- Pipeline state is reported as observed; no command changes sibling repositories, databases, queue
  files, or the running process.

## Risks

- Pipeline may finish or change stage during this phase. Re-read state and log at phase end.
- If process listing is unavailable, record the exact failure and leave live-process status PARTIAL.
- Unexpected proposal types or canonical changes block downstream phases until the cascade is amended.
