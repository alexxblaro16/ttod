# PHASE-S5E3 — exhaustive pair review

> **Track:** bilingual editorial judgment; canonical reads only.
> **Status:** BLOCKED until S5E2 is DONE and the owner-approved private ledger is available.
> **Depends on:** frozen S5E1 policy and adjudicated proposal queue.
> **Out of scope:** writing corrections into `ttod.yml`; model-determined verdicts.

## Goal

Review every in-scope English–Spanish pair under the frozen policy. Record two distinct judgments:
bilingual fidelity and Spanish editorial quality. One qualified person may perform both only if the
edition statement discloses that limitation. Human judgment owns the result; automation only builds
worklists and surfaces candidate anomalies.

## Deliverables

- Complete item-level private ledger at the S5E1-approved location.
- Redacted `PHASE-S5E3-REVIEW-SUMMARY.md` with dynamic denominator and completion counts.
- Human-approved correction list for S5E4, even when empty.
- Runnable exit gate, cold review, and post-review phase report.

## Prompt (Implementation Agent)

```text
Implement PHASE-S5E3 per
docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/PHASE-S5E3.md.

Read AGENTS.md, orchestrator, this file, approved policy/glossary/decision register, S5 plan §§7–8
and §12, and S5E2 disposition ledger. Use a fresh canonical export to build the in-scope pair list.
Review all pairs in two passes: (A) fidelity, agency, negation, modality, omissions/additions,
ambiguity, protected literals, form, and `teaches`; (B) Spanish idiom, punctuation, rhythm,
register, consistency, and pedagogical clarity. Record each pass with source and target digests,
reviewer, policy/glossary versions, outcome, severity, and rationale in the approved private ledger.

Models and scripts may flag candidates; they cannot write a human decision. Apply the signed owner
decision for “Coda con sabiduría,” not S4's superseded assessment. Do not change ttod.yml or proposal
states. Produce a redacted aggregate and human-approved correction list. If any item lacks a
decision, stop as PARTIAL. Run the gate through the external runner and stop at VERIFYING.
```

## Acceptance

- Every active in-scope Spanish pair has both passes in the private ledger, tied to current source
  and target digests.
- Ledger entries are unique by Spanish ID; item count equals the dynamically generated pair count.
- Every critical/major concern has a human disposition and owner; no finding is averaged away.
- Public summary exposes no private reviewer notes or local paths.
- No canonical or proposal file changed; `make check` passes.

## Risks

- A full editorial pass is human work and may span sessions. Save checkpoints and resume from the
  ledger's last completed quote ID.
- If the source witness changes, re-review affected pairs against the new digest.
