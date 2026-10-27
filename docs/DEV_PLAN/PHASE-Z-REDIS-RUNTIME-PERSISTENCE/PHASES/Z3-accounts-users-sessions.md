# PHASE-Z3: User profiles, login, and Redis sessions

> **Track:** `services/backend/app/auth.py` (+ new user/session store modules), Accounts login/session API, tests.
> **Status:** BLOCKED until Z2 DONE

## Goal

Accounts students use Redis as the user/profile database and as the server-side session store. Replace “one env admin + irrevocable signed cookie blob” with: seeded admin + multi-user capable profile hashes, and opaque session ids stored in Redis with TTL (logout deletes the key).

**Keep:** httpOnly cookie; distinct PAT secret; bcrypt via passlib; constant-time-ish verify with dummy hash when user missing.

## Deliverables

- `UserStore` Protocol: get-by-email, get-by-id, upsert profile fields; Redis + Memory implementations.
- Keys: `ttod:user:{id}`, `ttod:user:email:{email}` → id. Fields include `password_hash`, `roles`, `email`, optional `displayName`.
- Bootstrap: if Redis empty of users, seed from `TTOD_ADMIN_EMAIL` / `TTOD_ADMIN_PASSWORD_HASH` once.
- Sessions: cookie value = random `sid`; `ttod:session:{sid}` holds claims JSON + Redis TTL; `read_session` loads Redis; logout deletes key.
- Auth tests: login, me/session, logout revoke, wrong password, isolation between users.
- Cold review + report.

## Scope

**In:** users + sessions for browser login path.
**Out:** full registration UI polish (minimal API upsert OK); PAT revoke list (Z6 optional); proposals (Z4).

## Prompt (Implementation Agent)

```text
Implement PHASE-Z3 per
docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASES/Z3-accounts-users-sessions.md.

## Deliver
1. UserStore + SessionStore on the shared Redis client; Memory fallbacks when REDIS_URL empty.
2. AuthService.authenticate looks up user by email in UserStore; verifies bcrypt hash.
3. issue_session writes Redis sid+TTL and returns sid (cookie still named ttod_session).
4. Logout endpoint (if missing, add) deletes ttod:session:{sid}; subsequent session reads 401.
5. Preserve RequireSession cookie-only vs RequireAccessToken bearer-only separation.
6. Full auth test suite green; import smoke. Hand off for cold review — do NOT mark DONE.

## Constraints
- Never store plaintext passwords. Never put roles from the client body into the session without server lookup.
- Do not commit unless asked.
```

## Acceptance

- [ ] After login, session survives backend restart when Redis bind mount is up (Compose smoke in report).
- [ ] Logout then reuse cookie → 401 (**would fail** on signed-blob-only sessions).
- [ ] Two users’ favorites/session claims do not cross (key prefix isolation).
- [ ] Env admin still works after seed; unit tests run without live Redis.
- [ ] Cold review filed; blocking Fn closed.

## Risks

- Breaking Astro `auth.server.ts` cookie contract — keep cookie name and AuthUser JSON shape.
- Over-building registration UX — API + seed is enough for Z3.
