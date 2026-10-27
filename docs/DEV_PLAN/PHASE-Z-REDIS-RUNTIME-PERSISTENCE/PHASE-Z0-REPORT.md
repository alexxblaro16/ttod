# PHASE-Z0 Report

| Field | Value |
| --- | --- |
| **status** | DONE |
| **started_at** | 2026-10-27T14:37:00+01:00 |
| **finished_at** | 2026-10-27T14:40:00+01:00 |
| **cold_review** | pending — hand off `PHASE-Z0-COLD-REVIEW.md` |
| **cascade_amended** | none (shore map already widened same day) |

## Summary

Product owner authorized implementation after stopping the Compose app (all services
`Exited`, verified `docker compose ps -a`). Z0 freezes the shore boundary and durability
knobs before Compose edits. Live re-probe: #87 still OPEN/BLOCKED (docs `build` fail on
visual-system sync); `main` still has no Redis service.

## Frozen knobs

| Knob | Value |
| --- | --- |
| Bind mount | `./data/redis:/data` |
| Conf file | `redis/redis.conf` (tracked, mounted `:ro`) |
| Image | `redis:7-alpine` |
| AOF | `appendonly yes` · `appendfsync everysec` · `dir /data` |
| Eviction | `maxmemory-policy noeviction` |
| Host ports | **none** (Compose network only) |
| `REDIS_URL` default | `redis://redis:6379/0` |
| Key prefix | `ttod:` + domain per [REDIS-SHORE-MAP.md](REDIS-SHORE-MAP.md) |

## Domains in scope (Z)

users · sessions · favorites · proposal drafts (**dual-write** to `TTOD_PROPOSAL_DIR` for CLI accept)

## Deferred (not Z)

PWA drain · rate limits · Oracle job handles · cohort flags · recent-views · Redis-only proposals (no file dual-write)

## Hard boundary

- Redis = shore (runtime identity & drafts). `ttod.yml` = temple.
- Empty `REDIS_URL` → memory/filesystem test backends.
- Session cookie stays httpOnly; opaque sid in Redis; PAT secret ≠ session secret.
- Never store quote bodies as corpus in Redis; never accept into `ttod.yml` from Redis alone.

## Acceptance Criteria Met

- [x] Live probes re-run — `docker compose ps -a` (stopped); `gh pr view 87` (OPEN, docs build FAILURE); Compose has no redis — verified 2026-10-27
- [x] Bind path + AOF/fsync/policy + no host port frozen above
- [x] Quote bodies / empty REDIS_URL / dual-write CLI reason stated
- [ ] Cold review filed — **pending**

## Blockers

None for opening Z1. Cold review can run in parallel with Z1 Compose work; Z0 stays
VERIFYING until cold review closes.
