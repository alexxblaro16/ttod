# PHASE-Z5: Docs, CI land gate, PR #87 disposition

> **Track:** `docs/public/**`; visual-system sync; GitHub #87.
> **Status:** BLOCKED until Z4 DONE

## Goal

Teach the shore map in public docs; clear docs CI; credit and close or merge #87 against the improved Redis stack.

## Deliverables

- EN (+ ES twins if already paired): Redis as accounts/library/proposal **shore**; bind path; 503 troubleshooting; temple boundary; dual-write one-liner for instructors.
- `sync_visual_system.py --check` green; public-docs build green on tip.
- #87 merged into cascade tip **or** closed superseded with authorship credit.
- Cold review + report.

## Prompt (Implementation Agent)

```text
Implement PHASE-Z5 per
docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASES/Z5-docs-ci-and-pr87-land.md.

## Deliver
1. Docs match bind mount + shore domains (users, sessions, favorites, proposals) — not favorites-only.
2. Clear visual-system drift; privacy watcher PASS.
3. Disposition #87 with credit. Hand off for cold review — do NOT mark DONE.
4. Do not merge to main unless the human asks.

## Constraints
- Do not commit unless asked.
```

## Acceptance

- [ ] Docs name shore domains + temple boundary + bind path.
- [ ] `python3 scripts/sync_visual_system.py --check` exits 0.
- [ ] #87 disposition URL/reason in `PHASE-Z5-REPORT.md`.
- [ ] Cold review filed; blocking Fn closed.

## Risks

- Docs still describing named volume after Z1 bind mount — treat as doc↔code P1.
