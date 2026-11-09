# PHASE-S5E5 — independent cold audit and edition package

> **Track:** release evidence; no publication in this phase.
> **Status:** BLOCKED until S5E3 DONE and S5E4 DONE.
> **Depends on:** complete review ledger and correction disposition.
> **Out of scope:** public release, deployment, unsupported citation claims.

## Goal

Independently test the reviewed edition and assemble evidence for a human release decision. Any
critical cold-sample finding reopens its stratum; it does not get averaged out.

## Deliverables

- Cold-review method, reproducible sample seed and strata, findings, and dispositions.
- `exports/bilingual-alignment.json` and coverage report from a fresh canonical export.
- `docs/editorial/EDITION-STATEMENT.md` and known-limitations register.
- Runnable exit gate, independent cold review, and post-review phase report.

## Prompt (Implementation Agent)

```text
Implement PHASE-S5E5 per
docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/PHASE-S5E5.md.

Read AGENTS.md, orchestrator, this file, policy/glossary/decision register, S5E3 summary, S5E4
report, and S5 plan §§9–13. Use a fresh reviewer not responsible for the item-level pass where
feasible. Re-review every high-risk pair and a reproducible stratified ordinary sample at least as
large as the S5 plan threshold. Inspect all corrected pairs and every glossary term across the
Spanish corpus. Include a monolingual Spanish read for voice drift.

Generate alignment and coverage from a fresh canonical export; include IDs, languages, relation,
current digests, and edition scope. Draft the edition statement and limitations, stating review
scope, reviewer-role concentration, model assistance, rights, legacy provenance, and any
[BIBLIO-GAP]. Do not publish. Stop for explicit EDITION_RELEASE_APPROVED.
```

## Acceptance

- The ordinary sample is reproducible and spans every section, level, reviewer, and drafting stratum.
- Every high-risk item and corrected pair has an independent disposition.
- Alignment has exactly one row per in-scope active Spanish sister and resolves every relation to
  an English original; coverage agrees with a fresh export.
- Edition statement distinguishes structural validation from editorial review and makes no
  unsupported source or reviewer-independence claim.
- Product owner records `EDITION_RELEASE_APPROVED` or a concrete blocker; nothing is published.

## Risks

- Critical findings reopen their stratum and block release. Amend the cascade if review or
  correction assumptions change.
- Keep the private item-level ledger out of public exports.
