# PHASE-Z6 Report

| Field | Value |
| --- | --- |
| **status** | DONE |
| **cold_review** | [PHASE-Z-COLD-REVIEW.md](PHASE-Z-COLD-REVIEW.md) — F1 fixed same session |
| **cascade_amended** | none |

## Hardening checklist

| # | Item | Evidence |
| --- | --- | --- |
| 1 | One pool/client factory | `redis_client.create_redis_client`; shared `shore_client` in `main._build_shore` |
| 2 | 503 matrix | favorites + `ShoreHttp503Tests` (login/logout/proposals) |
| 3 | Isolation | favorites FakeRedis per-user keys; logout revoke; dual-write user index keys |
| 4 | No KEYS/FLUSH | `rg` clean under `services/backend/app` except `from_url` in `redis_client.py` |
| 5 | PAT revoke sidecar | **Deferred** — signed PAT TTL remains; session revoke shipped in Z3 |

## Cold-review triage

- **F1 (P1)** fixed: `test_login_returns_503_when_session_store_raises`, `test_logout_returns_503_when_session_delete_raises`, `test_proposal_create_returns_503_when_dual_write_redis_fails`
- **F2–F6 (P2)** deferred: Compose session restart smoke; dual-write orphan note (disk-first is intentional); discover path; health redis field test — not blocking classroom land

## Acceptance

- [x] Checklist 1–4 evidence-backed
- [x] Item 5 deferred with reason
- [x] Cold review filed; blocking F1 closed
