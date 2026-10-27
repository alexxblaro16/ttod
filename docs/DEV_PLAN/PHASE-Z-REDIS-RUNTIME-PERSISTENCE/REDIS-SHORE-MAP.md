<!--
Shore map — what belongs in Redis vs what must never. Author: 2026-10-27 (amended same day).
-->

# Redis shore map — what goes in, what stays out

**Temple (never Redis as source of truth):** `ttod.yml`, schema, governed accept/erase, quote bodies as canonical text.

**Shore (Redis + host bind mount):** per-user and operational state that must survive container restart without entering the corpus.

## In scope for Phase Z (Accounts team + permanence)

| Domain | Redis keys (sketch) | Why Redis | Notes |
| --- | --- | --- | --- |
| **User profiles / login** | `ttod:user:{id}` hash (`email`, `password_hash`, `roles`, `displayName`, `createdAt`); `ttod:user:email:{email}` → `id` | Multi-student accounts today are a single env admin; profiles need a real store | Store **bcrypt hashes only**. Seed env admin into Redis on first boot if missing. |
| **Sessions (login)** | `ttod:session:{sid}` hash + TTL = session TTL; cookie holds opaque `sid` (still httpOnly) | Logout/revocation; survive backend restart; same teaching story as FE I server sessions | Keep **two secrets**: session vs PAT. Signed-blob-only cookies (current) cannot revoke without waiting for expiry. |
| **PAT revoke / jti** | `ttod:pat:{jti}` string + TTL = PAT TTL | Stolen PAT can be denylisted before natural expiry | Issue flow still uses distinct `pat_secret`; Redis is revoke sidecar, not a second signer. |
| **Favorites library** | `ttod:favorites:{user_id}` hash → `quoteId → savedAt` | Already in #87 | Quote **ids** only. |
| **Proposal drafts (API)** | `ttod:proposal:{id}` JSON string; `ttod:proposals:status:{status}` set; `ttod:proposals:user:{user_id}` set | Drafts are shore, not temple; must survive restart for review queue | **Dual-write** (disk first, then Redis) so `cli.py proposal accept` keeps reading files without putting `redis` into `ttod_core`. If Redis fails after disk write, API returns 503 and the file remains CLI-loadable. |

## Explicitly deferred (same medium, later cascade or tip)

| Domain | Sketch | Why defer |
| --- | --- | --- |
| PWA offline-queue drain idempotency | `SET NX` + TTL on flush ids | Needs PWA contract freeze; not Accounts Week scope |
| Rate limits / abuse budgets | `INCR` + `EXPIRE` per user/IP | Easy to mis-tune in class; add after permanence works |
| Oracle in-flight job handles | short-TTL hashes | Oracle lane owns it |
| Feature / cohort lab flags | strings with class-window TTL | Instructor ops, not student assignment |
| Recent-views / continue reading | sorted sets | Nice-to-have library UX |
| Full Redis-only proposals (drop file dual-write) | CLI reads Redis | Requires `ttod_core` or CLI adapter decision — do **not** silently break `proposal accept` |

## Hard rules (all Redis writers)

1. Never write quote `text` / `teaches` as corpus source of truth into Redis.
2. Never accept a proposal into `ttod.yml` from Redis alone — human `proposal accept --reviewer-id` remains the temple gate.
3. Passwords: bcrypt (existing passlib) only; never log or commit plaintext.
4. Key prefix always `ttod:` + domain; no bare keys.
5. Empty `REDIS_URL` → in-memory (or filesystem for proposals) backends for unit tests — no live Redis required in CI unit jobs.
