# PHASE-Z2: Shared Redis client + favorites store

> **Track:** `services/backend/app/redis_client.py` (name flexible), `favorites.py`, `main.py`, `config.py`, requirements, tests.
> **Status:** BLOCKED until Z1 DONE

## Goal

One injectable Redis client/pool for the whole backend, then land favorites permanence (absorb #87’s `FavoriteStore`) on that client — no `Redis.from_url` sprawl in route handlers.

## Deliverables

- Shared client factory from `REDIS_URL` (`decode_responses=True`, connection pool).
- `FavoriteStore` Protocol + Memory + Redis (`ttod:favorites:{user_id}`, HSETNX).
- `create_app` injection; 503 on `RedisError` when Redis configured.
- `/health` (or existing health payload) includes redis status when `REDIS_URL` set.
- Tests with FakeRedis / injected client; full favorites suite green.
- Cold review + report.

## Scope

**In:** client module + favorites path.
**Out:** users/sessions (Z3); proposals (Z4).

## Prompt (Implementation Agent)

```text
Implement PHASE-Z2 per
docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASES/Z2-redis-client-and-favorites.md.

## Deliver
1. Add shared redis client helper; favorites RedisFavoriteStore uses it (or accepts client=).
2. Port #87 FavoriteStore behavior; filter list to active wisdom ids; 404 unknown quotes.
3. Health reports redis ok/down without leaking secrets.
4. Import smoke + favorites/library tests; full backend suite of touched packages.
5. Hand off for cold review — do NOT mark DONE.

## Constraints
- Empty REDIS_URL → MemoryFavoriteStore. Do not commit unless asked.
```

## Acceptance

- [ ] Single client construction path; favorites do not open ad-hoc connections per request.
- [ ] FakeRedis tests: idempotent savedAt + per-user key isolation (**would fail** on shared-key bug).
- [ ] RedisError → 503 covered by test.
- [ ] Health reflects redis when configured.
- [ ] Cold review filed; blocking Fn closed.

## Risks

- Merging #87 Compose named volume without Z1 bind mount — fix on this branch before DONE.
