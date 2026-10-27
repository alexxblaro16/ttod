# PHASE-Z1 Report

| Field | Value |
| --- | --- |
| **status** | DONE |
| **started_at** | 2026-10-27T14:38:00+01:00 |
| **finished_at** | 2026-10-27T14:40:00+01:00 |
| **cold_review** | pending |
| **cascade_amended** | `PHASES/Z1.exit-gate.sh` (match Compose `source:`/`target:` bind form); `redis/redis.conf` dropped invalid Redis 7.4 directive `aof-load-truncateded` |

## Summary

Compose `redis` service added with tracked `redis/redis.conf`, host bind `./data/redis:/data`,
no host ports, backend `REDIS_URL` + `depends_on: redis: condition: service_healthy`.
Durability probe: SET → restart redis → GET returned `survives-restart`; host shows
`data/redis/appendonlydir/` (Redis 7 multi-part AOF).

## Acceptance Criteria Met

- [x] `docker compose config` exit 0; bind `…/data/redis` → `/data`
- [x] Healthcheck + backend waits on `service_healthy`
- [x] Durability probe passed (`PROBE_OK`); AOF visible on host
- [x] No `ports:` on redis; `.gitignore` keeps README only under `data/redis/`
- [x] `PHASES/Z1.exit-gate.sh` OK
- [ ] Cold review filed — pending

## Commands

```bash
./docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASES/Z1.exit-gate.sh  # OK
docker compose up -d redis
docker compose exec -T redis redis-cli SET ttod:z1:probe survives-restart
docker compose restart redis
docker compose exec -T redis redis-cli GET ttod:z1:probe  # survives-restart
```

## Blockers

None for Z2. Leave redis container running for later smoke tests; full app stack still stopped.