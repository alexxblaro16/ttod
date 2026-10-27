# PHASE-Z1: Compose Redis microservice (improved)

> **Track:** `docker-compose.yml`, `redis/redis.conf`, `.env.example`, `.gitignore`, `data/redis/`.
> **Status:** BLOCKED until Z0 DONE

## Goal

Ship Redis as a first-class Compose service with **inspectable host permanence** and a readable config file — upgrade over #87’s named volume + one-line `command:`.

## Deliverables

- `redis/redis.conf` (tracked): `appendonly yes`, `appendfsync everysec`, `dir /data`, `maxmemory-policy noeviction`, bind `0.0.0.0` **inside** the Compose network only (no host `ports:`).
- Compose `redis` service: `redis:7-alpine`, mount conf `:ro`, bind `./data/redis:/data`, healthcheck `redis-cli ping`, `restart: unless-stopped`.
- Backend `REDIS_URL` + `depends_on: redis: condition: service_healthy`.
- `.gitignore` for AOF/RDB under `data/redis/`; tracked `data/redis/README.md` (permanence pedagogy).
- Durability probe evidence in report.
- Cold review + report.

## Scope

**In:** Compose + conf + gitignore + env examples.
**Out:** Python stores (Z2+); docs CI land (Z5).

## Prompt (Implementation Agent)

```text
Implement PHASE-Z1 per
docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASES/Z1-compose-redis-bind-mount.md
using Z0-frozen knobs.

## Deliver
1. Add redis/redis.conf and wire Compose:
   command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
   volumes: ./redis/redis.conf:/usr/local/etc/redis/redis.conf:ro
            ./data/redis:/data
2. No ports: on redis. Backend waits on healthy redis.
3. If absorbing #87 Compose, replace ttod_redis_data named volume with the bind mount.
4. Verify: docker compose config; ping; SET/GET across restart; host files under data/redis.
5. Run PHASES/Z1.exit-gate.sh. Hand off for cold review — do NOT mark DONE.

## Constraints
- Do not commit unless asked.
```

## Acceptance

- [ ] Conf file exists and is mounted read-only; Compose does not rely only on ad-hoc CLI flags for AOF.
- [ ] Bind mount under `data/redis`; restart probe keeps key; AOF/appendonly file visible on host.
- [ ] No published host port; health gate before backend.
- [ ] Cold review filed; blocking Fn closed.

## Risks

- Docker Desktop file sharing excludes path → document; do not silently fall back to named volume without amending Z0.
