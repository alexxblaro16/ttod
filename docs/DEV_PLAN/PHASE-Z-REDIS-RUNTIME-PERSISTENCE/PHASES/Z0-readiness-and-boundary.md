# PHASE-Z0: Readiness and shore-boundary freeze

> **Track:** architecture — Redis shore domains (accounts, sessions, favorites, proposals) vs temple.
> **Status:** READY (opens when product owner authorizes Phase Z)

## Goal

Freeze the widened shore before Compose or backend edits. Accounts/login students and proposal tips share **one** Redis DB — not ad-hoc files beside favorites.

Live permanence gaps on `main`:

- Favorites → process dict (lost on restart).
- Auth → single env admin + signed cookie (no multi-user profiles; logout ≠ server revoke).
- Proposals → JSON files only (OK for CLI; API queue does not use Redis yet).

## Deliverables

- `PHASE-Z0-REPORT.md` affirming [REDIS-SHORE-MAP.md](../REDIS-SHORE-MAP.md) (or amending it in the same commit).
- Frozen: bind path, `redis.conf` knobs, key prefixes, dual-write rule for proposals, session model (opaque sid + Redis TTL).
- Re-probe FINDINGS; amend if #87/`main` drifted.
- Cold review + report.

## Scope

**In:** decisions + cascade/shore-map text.
**Out:** code, Compose edits, merging #87.

## Prompt (Implementation Agent)

```text
Implement PHASE-Z0 per
docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASES/Z0-readiness-and-boundary.md.

## Deliver
1. Re-run FINDINGS live probes; mark unchanged or amend FINDINGS.
2. In PHASE-Z0-REPORT.md freeze:
   - bind: ./data/redis:/data
   - conf file path: redis/redis.conf (AOF, appendfsync everysec, dir /data, maxmemory-policy noeviction)
   - domains in-scope: users, sessions, favorites, proposals (+ dual-write)
   - deferred list from REDIS-SHORE-MAP (PWA drain, rate limits, …)
   - CLI accept must keep working via filesystem dual-write
3. Hand off for cold review — do NOT mark DONE yourself.

## Constraints
- No code/Compose in Z0. Do not commit unless asked.
```

## Acceptance

- [ ] Shore map domains for Z explicitly listed; deferred named.
- [ ] Dual-write rule for proposals stated with the CLI-accept reason.
- [ ] Session design: opaque sid in Redis with TTL; cookie httpOnly; PAT secret remains separate.
- [ ] Cold review filed; blocking Fn closed.

## Risks

- Temptation to make Redis-only proposals and break `cli.py proposal accept` — reject in cold review as P0.
