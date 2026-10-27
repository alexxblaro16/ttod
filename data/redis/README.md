# Redis data directory (shore permanence)

Host bind mount for the Compose `redis` service (`./data/redis:/data`).

AOF / RDB files created here are **runtime state** (users, sessions, favorites,
proposal drafts). They are gitignored — never commit them.

- Temple corpus remains `ttod.yml` (governed CLI accept only).
- Safe to delete this directory only when you intend to wipe classroom shore data.
- After wipe: `docker compose up -d redis` recreates empty AOF on next write.
