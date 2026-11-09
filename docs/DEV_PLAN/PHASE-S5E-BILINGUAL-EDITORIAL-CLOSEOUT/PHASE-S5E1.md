# PHASE-S5E1 — editorial policy and ledger contract

> **Track:** editorial policy and review tooling.
> **Status:** DONE.
> **Depends on:** S5E0 cold review and human-approved decision record.
> **Out of scope:** reviewing or mutating quotes/proposals; calling models or vaults.

## Goal

Freeze the rules reviewers will apply before judging the canonical Spanish edition. The policy must
distinguish fidelity from preference and protect intentional ambiguity and wordplay, including the
approved `img-086` phrasing.

## Deliverables

- `docs/editorial/EDITORIAL-TRANSLATION-POLICY.md`.
- `docs/editorial/TTOD-ES-GLOSSARY.yml`, human-curated.
- `docs/editorial/EDITORIAL-DECISIONS.md` with the S5E0 decision preserved.
- `docs/editorial/EDITORIAL-REVIEW-LEDGER.schema.json` plus owner-approved private ledger location
  and access decision.
- Runnable exit gate, cold review, and post-review phase report.

## Prompt (Implementation Agent)

```text
Implement PHASE-S5E1 per
docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/PHASE-S5E1.md.

Read AGENTS.md, orchestrator, this runbook, S5 plan §§4, 7–8, 11–12, and EDITORIAL-DECISIONS.md.
Use the Cascade Forge worktree and stop at VERIFYING.

Write policy for target variety, ambiguity, register, Taoist language, wordplay, technical literals,
lineation, punctuation, `text` vs `teaches`, translation rights, severity, adjudication, and reviewer
independence. Freeze glossary schema and include only human-approved terms. Preserve “Coda con
sabiduría” as an intentional example. Define a ledger record for quote IDs, source/target digests,
separate fidelity and Spanish-edit passes, severity, decision, rationale, reviewer, timestamp,
policy version, and glossary version.

Do not invent where item-level notes will be stored. Present a concrete private-location/access
choice to the product owner; record their decision in EDITORIAL-DECISIONS.md. Do not put reviewer
notes under public docs. Stop at VERIFYING for the literal gate token EDITORIAL_POLICY_APPROVED;
do not proceed to S5E2.
```

## Acceptance

- Policy, glossary, decision register, and JSON Schema validate with the project's parsers.
- Ledger schema requires both review passes and rejects a missing quote ID or source/target digest.
- Policy names intentional ambiguity and the `img-086` owner decision as binding precedent.
- `EDITORIAL_POLICY_APPROVED` appears in the decision register with reviewer identity, policy and
  glossary versions, ledger path/access decision, and date.
- No quote or proposal state changed.

## Risks

- A public repository is not a private ledger. If the owner has not selected an access-controlled
  location, remain BLOCKED rather than writing personal notes into tracked docs.
- Do not turn one person's review into a claim of independent dual review.
