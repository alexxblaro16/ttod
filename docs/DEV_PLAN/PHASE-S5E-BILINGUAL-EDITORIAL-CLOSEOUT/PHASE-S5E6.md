# PHASE-S5E6 — programme reconciliation and closeout

> **Track:** programme documentation and final verification.
> **Status:** BLOCKED until S5E5 is DONE and the product-owner release decision is recorded.
> **Depends on:** complete cold audit and edition package.
> **Out of scope:** publishing, merging, tagging, or adding a new corpus milestone.

## Goal

Bring the Phase S row in `docs/DEV_PLAN/INDEX.md`, the S5 plan's current-status header, and S5E
reports into alignment. Preserve dated historical baselines; state current counts dynamically or
omit them from prose.

## Deliverables

- Reconciled Phase S/S5 programme index and links to editorial artifacts.
- Runnable exit gate, cold review, and final phase report.
- Product-owner closeout decision: DONE with release approval, or PARTIAL with named blocker.

## Prompt (Implementation Agent)

```text
Implement PHASE-S5E6 per
docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/PHASE-S5E6.md.

Read AGENTS.md, orchestrator, this runbook, all S5E reports/cold reviews, editorial policy,
decision register, alignment/coverage artifacts, and edition statement. Update the Phase S row in
docs/DEV_PLAN/INDEX.md and the S5 plan status header so current claims match the evidence. Keep
dated baselines as history. Link the S5E cascade and final package. Remove contradictory present-tense
claims that S5 was never executed or that “Coda con sabiduría” is unresolved, while preserving the
historical S4 report unchanged.

Run `make check`, `make docs-privacy`, `git diff --check`, and the bridge test. Do not publish,
commit, push, merge, or create a release. Stop at VERIFYING for product-owner closeout.
```

## Acceptance

- Current Phase S/S5 docs agree with canonical and review evidence; dated reports remain intact.
- Current docs preserve the owner-approved “Coda” decision and state S5 only to the level proven.
- No hardcoded live quote total is added.
- `make check`, `make docs-privacy`, bridge test, and `git diff --check` exit 0.
- Product owner records DONE or a named PARTIAL blocker; no publication occurs.

## Risks

- Old reports are historical evidence. Amend current summaries, not the original S4 assessment.
- Privacy checks may identify pre-existing findings outside touched paths. Record the baseline and
  gate on no new findings caused by this phase.
