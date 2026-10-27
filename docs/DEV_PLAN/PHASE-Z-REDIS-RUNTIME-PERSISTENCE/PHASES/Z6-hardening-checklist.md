# PHASE-Z6: Redis hardening checklist

> **Track:** cross-cutting — pool, 503 matrix, key isolation, optional PAT revoke.
> **Status:** BLOCKED until Z5 DONE

## Goal

Close the “improved Redis implementation” bar from the orchestrator: not a pile of one-off clients, no silent empty success on outage, no cross-user key leaks, optional PAT denylist sidecar.

## Deliverables

- Checklist evidence in `PHASE-Z6-REPORT.md` (commands + exits):
  1. One pool/client factory used by favorites, users, sessions, proposals.
  2. 503 matrix table: which routes fail closed when Redis is down and `REDIS_URL` is set.
  3. Isolation tests: user A cannot read B’s favorites/sessions/proposals via API.
  4. No `KEYS` / `FLUSHDB` / `FLUSHALL` in application code (grep clean).
  5. Optional: `ttod:pat:{jti}` revoke on logout-all / explicit revoke endpoint — if skipped, defer with decision one-liner.
- Cold review + report.

## Prompt (Implementation Agent)

```text
Implement PHASE-Z6 per
docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASES/Z6-hardening-checklist.md.

## Deliver
1. Grep and fix any Redis.from_url outside the shared client.
2. Fill the 503 matrix with real tests or documented Compose kill-redis probes.
3. Isolation tests for at least favorites + proposals (+ session revoke from Z3).
4. PAT revoke sidecar only if small; otherwise defer explicitly.
5. Hand off for cold review — do NOT mark DONE.

## Constraints
- Do not expand into rate limits / PWA drain. Do not commit unless asked.
```

## Acceptance

- [ ] Checklist items 1–4 evidence-backed in the report.
- [ ] Item 5 done or deferred with named reason.
- [ ] Full suite of touched packages green.
- [ ] Cold review filed; blocking Fn closed.

## Risks

- Scope creep into “also rate limits” — out of scope; park on REDIS-SHORE-MAP deferred table.
