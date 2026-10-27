# Technical director — Phase Z Redis shore store (Z0–Z6)

**Status:** PROPOSED · **amended 2026-10-27** (scope widened: accounts + proposals + shared client; was favorites-only Z0–Z3).
**Evidence:** [FINDINGS-2026-10-27.md](FINDINGS-2026-10-27.md) · **Shore map:** [REDIS-SHORE-MAP.md](REDIS-SHORE-MAP.md)

## Programme (do not invert)

| Step | File | Deliverable | Gate |
| ---- | ---- | ----------- | ---- |
| 0 | [PHASES/Z0-readiness-and-boundary.md](PHASES/Z0-readiness-and-boundary.md) | Freeze shore map, key taxonomy, dual-write rule for proposals, Compose durability knobs | READY until authorized; DONE when `PHASE-Z0-REPORT.md` cites REDIS-SHORE-MAP + knobs |
| 1 | [PHASES/Z1-compose-redis-bind-mount.md](PHASES/Z1-compose-redis-bind-mount.md) | Hardened `redis` service: bind mount, `redis.conf`, healthcheck, no host port, backend `REDIS_URL` | BLOCKED until Z0 DONE; DONE when compose config + restart AOF probe pass |
| 2 | [PHASES/Z2-redis-client-and-favorites.md](PHASES/Z2-redis-client-and-favorites.md) | Shared Redis client module + `FavoriteStore` (absorb #87) + `/health` reports redis | BLOCKED until Z1 DONE; DONE when favorites suite + import smoke green |
| 3 | [PHASES/Z3-accounts-users-sessions.md](PHASES/Z3-accounts-users-sessions.md) | User profile store + login against Redis; opaque session sid in Redis with TTL; env admin seed | BLOCKED until Z2 DONE; DONE when auth tests green and logout revokes session |
| 4 | [PHASES/Z4-proposals-dual-write.md](PHASES/Z4-proposals-dual-write.md) | Proposal API reads/writes Redis indexes; dual-write JSON files for CLI accept | BLOCKED until Z3 DONE; DONE when review queue survives backend restart and `proposal accept` still loads a file |
| 5 | [PHASES/Z5-docs-ci-and-pr87-land.md](PHASES/Z5-docs-ci-and-pr87-land.md) | Public docs (shore vs temple); visual-system sync; #87 disposition | BLOCKED until Z4 DONE; DONE when docs CI green and #87 disposition recorded |
| 6 | [PHASES/Z6-hardening-checklist.md](PHASES/Z6-hardening-checklist.md) | Connection pool, fail-closed 503 matrix, key isolation tests, optional PAT revoke sidecar | BLOCKED until Z5 DONE; DONE when hardening checklist evidence in report |

Harness Gate token = **first word** of Gate cell. Exit-gates: `PHASES/Zn.exit-gate.sh`.

## Master paste (start / resume)

```text
Implement Phase Z (Redis shore store) per
docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASE-Z-REDIS-RUNTIME-PERSISTENCE-CASCADE.md.

## Context
- Shore map: docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/REDIS-SHORE-MAP.md
- Evidence: docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/FINDINGS-2026-10-27.md
- Student tip: https://github.com/ruvebal/ttod/pull/87 (favorites only — absorb, then extend)
- Out of scope: mutating ttod.yml; quote bodies as Redis corpus; publishing Redis host port;
  Redis password for classroom stack; Postgres; cloud Redis; PWA drain; rate limits;
  Redis-only proposals that break cli.py proposal accept; committing data/redis/ dumps

## Programme
Execute the next incomplete phase only, in order Z0 → Z6.
After each phase: VERIFYING → cold subprocess review → PHASE-Zn-COLD-REVIEW.md →
triage/amend → PHASE-Zn-REPORT.md.
Do not start Z(n+1) until Zn status is DONE. Implementer must not self-certify DONE.

## Hard constraints
- Redis = shore. ttod.yml = temple. Never blur.
- Host bind mount ./data/redis:/data (or Z0-frozen path); AOF + appendfsync everysec;
  maxmemory-policy noeviction; no host ports.
- One shared redis client/pool in services/backend — no per-route from_url sprawl.
- Keys always ttod:{domain}:… per REDIS-SHORE-MAP.md.
- Proposals: Redis + dual-write to TTOD_PROPOSAL_DIR (CLI accept substrate).
- Empty REDIS_URL → memory/filesystem test backends; unit tests need no live Redis.
- Session cookie stays httpOnly; opaque sid; PAT secret remains distinct from session secret.
- Do not commit unless the human asks.
```

## Layer map

| Layer | Store | Phase |
| ----- | ----- | ----- |
| Governed corpus | `ttod.yml` / CLI accept | **never Redis-authored** |
| Proposal accept substrate | `TTOD_PROPOSAL_DIR` JSON files | Z4 dual-write target |
| Proposal runtime queue | Redis `ttod:proposal:*` | Z4 |
| Users / password hashes | Redis `ttod:user:*` | Z3 |
| Sessions / revoke | Redis `ttod:session:*` (+ optional `ttod:pat:*`) | Z3 / Z6 |
| Favorites | Redis `ttod:favorites:*` | Z2 |
| Compose durability | bind mount AOF | Z1 |

## Improved Redis implementation (product bar)

Not just “add a container.” Z must meet this bar:

1. **Dedicated microservice** in Compose (not Redis-inside-backend process).
2. **Bind-mounted AOF** under gitignored `data/redis/` (inspectable permanence).
3. **Checked-in `redis/redis.conf`** (or `services/redis/redis.conf`) mounted read-only — knobs in a file students can read, not only a long `command:` line.
4. **Shared client** (`services/backend/app/redis_client.py` or equivalent): decode_responses, pool from `REDIS_URL`, injectable for tests.
5. **Health:** backend `/health` (or sibling) reports `redis: ok|down` without leaking URLs with credentials.
6. **Fail-closed:** RedisError → 503 on shore writes/reads that need Redis when `REDIS_URL` is set.
7. **Indexes:** secondary sets for proposal list by status/user — no `KEYS *` in request paths.
8. **Seed, don’t hardcode:** bootstrap admin from env into Redis once; multi-user profiles afterward.

## Closing protocol

`BLOCKED → READY → IN_PROGRESS → VERIFYING → COLD_REVIEW → DONE`

Cold review: fresh `cascade-cold-reviewer` / Task; output `PHASE-Zn-COLD-REVIEW.md`.
Amend on surprise: same commit as report — orchestrator + downstream phases + shore map.

## Resume rule

Enum: `BLOCKED | READY | IN_PROGRESS | VERIFYING | COLD_REVIEW | PARTIAL | DONE`

- **DONE** → next phase · **PARTIAL** → finish current · **IN_PROGRESS** → resume, do not advance  
- **VERIFYING** → finish suite/probes → cold review · **COLD_REVIEW** → triage → DONE or back to IN_PROGRESS  
- **BLOCKED** → named blocker · **READY** → start (one IN_PROGRESS at a time)

## Relation to PR #87 and Accounts assignments

- #87 = favorites Protocol cut. Land via Z2; do not merge while docs CI is red.
- Accounts Team 5 (login/session, propose, review queue) **targets this shore** after Z3/Z4 — assignment tips should not invent a second DB. Point students at REDIS-SHORE-MAP.md once Z0 is authorized.
