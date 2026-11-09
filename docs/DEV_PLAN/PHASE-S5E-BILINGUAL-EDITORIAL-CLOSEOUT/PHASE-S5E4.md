# PHASE-S5E4 — governed canonical corrections

> **Track:** atomic TTOD repository transaction, only if the approved list is nonempty.
> **Status:** BLOCKED until S5E3 DONE and an itemized correction list exists.
> **Depends on:** explicit product-owner approval of exact items and text.
> **Out of scope:** hand-editing YAML, accepting unreviewed text, deleting/reusing quote IDs.

## Goal

Apply only human-approved corrections from S5E3. If the correction list is empty, record outcome
`NOT_NEEDED`; still run the exit gate and cold review before the orchestrator marks this phase DONE.

## Deliverables

- If required, the smallest repository-level atomic translation-supersession transaction and tests.
- Disposable-copy rehearsal with rollback injection.
- Live mutation evidence only after human approval of the exact diff.
- Runnable exit gate, cold review, and post-review phase report.

## Prompt (Implementation Agent)

```text
Implement PHASE-S5E4 per
docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/PHASE-S5E4.md.

Read AGENTS.md, orchestrator, this file, S5E3 report, signed correction list, and repository
transaction APIs. If the list is empty, make no code or data changes; record outcome NOT_NEEDED,
run the exit gate, and stop at VERIFYING.

If corrections exist, the current CLI lacks an atomic translation replacement operation. Implement
only the smallest transaction needed. It must lock/reload, validate the human-reviewed proposal,
allocate the successor ID inside the transaction, accept the successor, deprecate the old sister
with that ID, recompute digests/meta, validate the whole database, and roll back canonical and
proposal state on injected failure. Rehearse with disposable copies. Import touched modules, run
targeted regressions, then run the full suite. Stop before live writes until the product owner
approves the exact diff, proposal IDs, old/new IDs, and reviewer IDs. Never hand-edit ttod.yml or
delete an old record.
```

## Acceptance

- Empty correction list is reported NOT_NEEDED with no code/data changes; OR approved corrections
  have a passing atomic transaction rehearsal and rollback proof.
- No live write occurs before explicit approval of the exact diff and reviewer IDs.
- Any live transaction records before/after hashes, proposal and quote IDs, reviewer decisions,
  validation, test exits, and rollback evidence.
- Validate, stats, full suite, bridge suite, and translation uniqueness pass after mutation.

## Risks

- Separate deprecate/accept calls can create a coverage gap or omit `deprecated_by`; do not use two
  loosely coupled live commands for replacement.
- Injected rollback must leave canonical bytes and proposal status unchanged.
