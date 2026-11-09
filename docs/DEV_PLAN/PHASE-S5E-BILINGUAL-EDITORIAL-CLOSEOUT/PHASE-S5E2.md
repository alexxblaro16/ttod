# PHASE-S5E2 — residual proposal adjudication

> **Track:** proposal review only.
> **Status:** BLOCKED until `EDITORIAL_POLICY_APPROVED`.
> **Depends on:** S5E1 DONE.
> **Out of scope:** canonical mutation, acceptance, deleting proposal history, blanket rejection.

## Goal

Explain and resolve every open alternate translation proposal. The last audit found open alternates
whose source records already have Spanish sisters; recompute the queue when this phase starts. An
open state may remain only with an identified human decision, reason, owner, and review date.

## Deliverables

- `PROPOSAL-DISPOSITION-LEDGER.md` listing every live open translation proposal ID and decision.
- CLI review activities appended for human decisions that map to reject, withdraw, or revision.
- Runnable exit gate, cold review, and post-review phase report.

## Prompt (Implementation Agent)

```text
Implement PHASE-S5E2 per
docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/PHASE-S5E2.md.

Read AGENTS.md, orchestrator, this file, approved editorial policy/glossary, and S5E0 findings.
Recompute every proposed/needs_revision translation proposal from the store. For each, show the
English source, active Spanish sister, candidate, provenance, and relevant decisions in a review
packet. Do not infer dispositions. Obtain the named human's decision for each proposal; record it
append-only through `cli.py proposal review` when the CLI action represents that choice. For a held
alternate, keep its proposal status but record owner, rationale, and next review date in the ledger.
Never accept an alternate just to clear the queue.

Adjudicate the “Codifica” alternate for img-071 under EDITORIAL-DECISION-2026-11-08-CODA; it cannot
supersede img-086 without separate approval. Do not delete proposal files or mutate ttod.yml. Run
the phase gate only through the external runner and stop at VERIFYING.
```

## Acceptance

- Every current open translation proposal appears exactly once in the disposition ledger.
- Every decision has a named human, date, rationale, and action; holds have an owner and review date.
- CLI review actions appear in each proposal's append-only activity log.
- No proposal was accepted, no file deleted, and canonical SHA-256 is unchanged.
- `make check` and bridge suite exit 0.

## Risks

- The current CLI has no `hold` state. Record a human hold without fabricating a schema status; report
  the workflow limitation for later design.
- Do not reuse the prior queue count or IDs without recomputing them.
