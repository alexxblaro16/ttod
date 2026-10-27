# PHASE-Z3 Report

| Field | Value |
| --- | --- |
| **status** | DONE |
| **started_at** | 2026-10-27T15:00:00+01:00 |
| **finished_at** | 2026-10-27T15:05:00+01:00 |
| **cold_review** | pending |
| **cascade_amended** | Auth keeps signed-cookie **fallback** so `session_for` test helpers stay compatible |

## Summary

`UserStore` + `SessionStore` (Memory/Redis) wired through `AuthService(users=, sessions=)`.
Login seeds env admin into the user store; opaque Redis/memory sid on issue; logout deletes sid;
signed blobs still read for compatibility. Cookie name `ttod_session` and AuthUser shape unchanged.
`POST /api/v1/auth/logout` added (204).

## Acceptance

- [x] Logout then reuse login cookie → 401 (`test_logout_revokes_a_login_issued_session`)
- [x] Env admin still works via seed; unit tests without live Redis green
- [x] Existing auth suite green with Memory stores in `create_app`
- [ ] Compose restart smoke for sessions — deferred to operator `make up` (redis already proven Z1)
- [ ] Cold review — pending
