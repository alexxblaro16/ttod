# Phase Z (Redis shore) — combined cold review

| Field | Value |
| --- | --- |
| **Reviewer** | cascade-cold-reviewer (fresh session; did not implement Phase Z) |
| **Date** | 2026-10-27 |
| **Scope** | Z0–Z6 per `PHASE-Z-REDIS-RUNTIME-PERSISTENCE-CASCADE.md`, diff paths listed in orchestrator handoff |
| **Verdict** | **Not ready for product-owner DONE** — see findings below (no P0 temple/CLI break, several P1/P2 gaps) |

This document does **not** mark any phase `DONE`. Triage findings before closing VERIFYING → DONE.

---

## Method

1. Read cascade hard constraints, `REDIS-SHORE-MAP.md`, phase runbooks (Acceptance), and Z0–Z6 reports (claims not trusted).
2. Read implementation under diff scope (`docker-compose.yml`, `redis/redis.conf`, backend shore modules, public docs EN/ES).
3. Agentic-change checks: import touched modules; run backend tests via package module path; grep docs↔code; grep `ttod_core` for `redis`; grep app for `KEYS`/`FLUSH*`/`from_url` sprawl.
4. Re-run selected probes (Z1 exit-gate, Redis restart durability, visual-system check, PR #87 state).

---

## Verification transcript (commands run in `/Users/ruvebal/src/ttod`)

### Import smoke (8 modules)

```text
$ .venv/bin/python -c "… import services.backend.app.{redis_client,favorites,users,sessions,proposal_drafts,auth,main,config} …"
IMPORT_OK 8
```

### Backend unit tests (full touched package suite)

```text
$ .venv/bin/python -m unittest \
    services.backend.tests.test_auth \
    services.backend.tests.test_shore_stores \
    services.backend.tests.test_favorites \
    services.backend.tests.test_library \
    services.backend.tests.test_api \
    services.backend.tests.test_review_pipeline \
    services.backend.tests.test_backend -v
…
Ran 77 tests in 44.336s
OK
```

**Note:** `python -m unittest discover -s services/backend/tests -p 'test_*.py'` produced **3 ImportErrors** (relative imports in `test_auth`, `test_library`, etc.). See **F5**.

### Z1 exit-gate + durability (cold re-probe)

```text
$ ./docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASES/Z1.exit-gate.sh
Z1 exit-gate OK

$ docker compose exec -T redis redis-cli SET ttod:cold:probe cold-review-ok
OK
$ docker compose restart redis && sleep 2
$ docker compose exec -T redis redis-cli GET ttod:cold:probe
cold-review-ok
$ ls data/redis/
README.md  appendonlydir/
```

### Docs / CI helpers

```text
$ python3 scripts/sync_visual_system.py --check
PASS: shared visual system is synchronized
EXIT:0

$ .venv/bin/python agentic/report-steward/scripts/check_public_privacy.py docs/public
PASS: no public-privacy findings
EXIT:0
```

### PR #87

```text
$ gh pr view 87 --repo ruvebal/ttod --json state,closed
{"closed":true,"state":"CLOSED"}
```

Owner comment records **superseded by Phase Z** with favorites Protocol credit (`#issuecomment-6444022960`).

### Boundary greps

| Check | Result |
| --- | --- |
| `redis` under `ttod_core/` | **none** |
| `KEYS` / `FLUSHDB` / `FLUSHALL` under `services/backend/app/` | **none** |
| `Redis.from_url` under `services/backend/app/` | **only** `redis_client.py:16` |
| Compose `ttod_redis_data` named volume | **absent**; `./data/redis:/data` bind present |
| Redis service `ports:` | **none** (internal `6379/tcp` only) |

---

## Per-phase acceptance audit

Legend: **Met** = runnable evidence this review; **Partial** = code or doc only / report claim not re-run; **Not met** = gap.

### Z0 — Readiness and boundary

| Criterion | Status | Evidence |
| --- | --- | --- |
| Shore domains + deferred listed | **Met** | `REDIS-SHORE-MAP.md`, `PHASE-Z0-REPORT.md` align with cascade |
| Dual-write + CLI accept reason | **Met** | Shore map § proposal drafts; Z0 report |
| Session: opaque sid, httpOnly, PAT ≠ session | **Met** | Map + Z0 report; implemented in Z3 |
| Cold review filed | **Met** | this file |

Z0 is documentation-only; no code expected.

### Z1 — Compose Redis bind mount

| Criterion | Status | Evidence |
| --- | --- | --- |
| Tracked `redis.conf`, AOF knobs, ro mount | **Met** | `redis/redis.conf`; compose `command` + volumes |
| Bind mount + restart probe | **Met** | exit-gate + cold `SET`/`GET` after restart |
| No host port; backend `depends_on` healthy | **Met** | `docker compose config` via exit-gate; compose lines 59–60, 85–97 |
| Cold review | **Met** | this file |

### Z2 — Shared client + favorites

| Criterion | Status | Evidence |
| --- | --- | --- |
| Single client path | **Met** | `create_redis_client`; `_build_shore` one `shore_client` |
| FakeRedis idempotent + per-user keys | **Met** | `test_redis_favorite_store_is_idempotent_and_persistent`, `test_redis_keys_are_isolated_per_user` (in 77-test run) |
| RedisError → 503 | **Met** | `test_redis_outage_returns_503` |
| Health reflects redis when configured | **Partial** | `main.py` `/health` adds `redis` key; **no test** asserts payload — **F6** |
| Cold review | **Met** | this file |

### Z3 — Users + Redis sessions

| Criterion | Status | Evidence |
| --- | --- | --- |
| Logout → reuse cookie 401 | **Met** | `test_logout_revokes_a_login_issued_session` (login path uses `MemorySessionStore` via `create_app`) |
| Env admin seed; tests without live Redis | **Met** | `test_seeded_credentials_issue_a_session…`; shore store tests |
| Session survives backend restart (Compose) | **Partial** | Z1 Redis key survives restart; **no** backend login → restart backend → `/auth/session` probe — **F2** |
| Two users isolation (sessions/favorites) | **Partial** | Favorites cross-user API test uses default memory favorites; session isolation not API-tested on Redis — **F4** |
| Signed-cookie fallback preserved | **Met** | `auth.read_session` lines 137–138; Z3 report |
| Cold review | **Met** | this file |

### Z4 — Proposals dual-write

| Criterion | Status | Evidence |
| --- | --- | --- |
| List uses sets, not `KEYS` | **Met** | `proposal_drafts.py` `smembers` on status/user sets; grep clean |
| Dual-write Redis + file after POST | **Met** | `test_dual_write_proposal_leaves_cli_loadable_file` |
| `ProposalStore.load` on written file | **Met** | same test |
| RedisError → 503 create/list | **Partial** | Handlers in `main.py`; **no** HTTP test — **F1** |
| Cold review | **Met** | this file |

### Z5 — Docs, CI, #87

| Criterion | Status | Evidence |
| --- | --- | --- |
| Docs: shore domains, temple, bind path, 503 | **Met** | `docs/public/guides/local-setup.md`, `docs/public/platform/index.md` (+ ES twins) |
| `sync_visual_system.py --check` | **Met** | exit 0 (cold run) |
| #87 disposition + credit | **Met** | PR CLOSED; superseded comment |
| Cold review | **Met** | this file |

### Z6 — Hardening checklist

| # | Item | Status | Evidence |
| --- | --- | --- | --- |
| 1 | One pool/client factory | **Met** | `redis_client.py`; `_build_shore` |
| 2 | 503 matrix | **Not met** | Only favorites POST tested — **F1** |
| 3 | Isolation tests | **Partial** | Favorites memory API + Redis unit keys; proposals/sessions Redis API isolation thin — **F4** |
| 4 | No KEYS/FLUSH | **Met** | grep |
| 5 | PAT revoke | **Deferred** | Z6 report (acceptable if explicit) |
| Full suite green | **Met** | 77 tests OK (module path) |
| Cold review | **Met** | this file |

---

## Findings

### F1 — Z6 503 matrix mostly unproven at HTTP layer

| | |
| --- | --- |
| **Severity** | **P1** |
| **Blocks DONE?** | **Yes — Z6** (acceptance item 2: “503 matrix table … real tests”) |
| **Evidence** | `grep 503/RedisError/BrokenRedis services/backend/tests` → only `test_favorites.py::test_redis_outage_returns_503`. Z6 report lists login, logout, proposals create/list; `main.py` wraps those routes in `except redis.RedisError` → 503, but **no failing test** was run for them. |
| **Fix** | Add TestClient cases injecting a shared `BrokenRedis` (or patch `shore_client`) via `create_app(..., redis_client=broken)` and assert 503 + detail string for: `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, `POST/GET /api/v1/proposals`. |

### F2 — Z3 “session survives backend restart” not end-to-end probed

| | |
| --- | --- |
| **Severity** | **P2** |
| **Blocks DONE?** | **Partial — Z3** acceptance checkbox (Compose smoke) |
| **Evidence** | Z3 report defers to operator `make up`. Cold review confirmed **Redis** persistence (F1 probe), not **opaque session cookie** after **backend** restart with `REDIS_URL` set. |
| **Fix** | Documented Compose smoke: login → record cookie → `docker compose restart backend` → `GET /api/v1/auth/session` → 200; attach transcript to Z3 report. |

### F3 — Dual-write: Redis failure after disk success leaves filesystem orphan

| | |
| --- | --- |
| **Severity** | **P2** |
| **Blocks DONE?** | No (Z4 warns); accept or document repair |
| **Evidence** | `DualWriteProposalDraftStore.save()` calls `self._files.save(proposal)` then Redis pipeline; on `redis.RedisError` raises → API 503 (`main.py`), but file remains under `TTOD_PROPOSAL_DIR`. |
| **Fix** | Either: (a) test + report note for operators; (b) optional compensating delete on Redis failure; or (c) list endpoint documents filesystem fallback behavior (`list()` already falls back when Redis index empty). |

### F4 — Z6 isolation evidence thinner than checklist implies

| | |
| --- | --- |
| **Severity** | **P2** |
| **Blocks DONE?** | **Partial — Z6** item 3 |
| **Evidence** | `test_one_user_cannot_read_or_remove_another_users_favorites` runs against default **Memory** favorites. Redis isolation proven only in `RedisFavoriteStoreTests.test_redis_keys_are_isolated_per_user`. No cross-user proposal queue test with `DualWriteProposalDraftStore` + FakeRedis at API layer. |
| **Fix** | One API test: two users, two proposal ids in FakeRedis sets; reviewer A must not see B’s draft unless shared queue policy intended. |

### F5 — `unittest discover` on `services/backend/tests` fails import

| | |
| --- | --- |
| **Severity** | **P2** |
| **Blocks DONE?** | No if CI uses module path; yes if someone copies discover incantation from generic docs |
| **Evidence** | `python -m unittest discover -s services/backend/tests -p 'test_*.py'` → `ImportError: attempted relative import with no known parent package` for `test_auth`, `test_library`, … (3 errors). Module-path run: 77 OK. |
| **Fix** | Document canonical command in Z6 report or add `services/backend/tests/__init__.py` / runner shim (only if studio standard requires discover). |

### F6 — `/health` redis field untested

| | |
| --- | --- |
| **Severity** | **P2** |
| **Blocks DONE?** | **Partial — Z2** |
| **Evidence** | `test_health_schema_and_public_projections` checks status 200 only; no assertion on `"redis": "ok"|"down"`. |
| **Fix** | `create_app(settings_with_redis_url, redis_client=FakeRedis())` → GET `/health` → assert `"redis" in body`. |

### F7 — Signed-session fallback vs server revoke (known split)

| | |
| --- | --- |
| **Severity** | **P2** |
| **Blocks DONE?** | No (Z3 documents intentional compat) |
| **Evidence** | `AuthService.read_session` falls back to `_read_signed_session` when store miss (`auth.py` 137–138). `support.session_for()` builds cookies via `AuthService` **without** `SessionStore` → signed blobs; logout does not invalidate those. Login API path uses opaque sid + `test_logout_revokes_a_login_issued_session` passes. |
| **Fix** | Keep as-is for test helpers; optional doc one-liner in shore map: “production login uses opaque sid; signed fallback is legacy/test-only.” |

### F8 — Private import from `ttod_core`

| | |
| --- | --- |
| **Severity** | **P2** |
| **Blocks DONE?** | No |
| **Evidence** | `proposal_drafts.py` imports `_proposal_from_dict` from `ttod_core.repository` (private symbol). |
| **Fix** | Export a public deserializer on `ttod_core` or duplicate minimal parse in backend (only if boundary policy requires). |

---

## Hard constraints (cascade) — spot check

| Constraint | Result |
| --- | --- |
| Redis = shore; `ttod.yml` = temple | **OK** — favorites/proposals store ids/drafts only; corpus read via `SnapshotService` |
| Bind mount `./data/redis`, AOF, no host ports | **OK** — see Z1 evidence |
| One shared client in backend | **OK** |
| Keys `ttod:{domain}:…` | **OK** — favorites, user, session, proposal modules |
| Proposals dual-write + CLI accept | **OK** — `test_dual_write_proposal_leaves_cli_loadable_file`; no `redis` in `ttod_core` |
| Empty `REDIS_URL` → memory/filesystem | **OK** — `_build_shore` branches |
| PAT secret ≠ session secret | **OK** — `AuthService.__init__` guard |
| #87 superseded with credit | **OK** — gh CLOSED + comment |

---

## Summary for product owner

- **Temple / CLI accept path:** No P0 — dual-write file loadable by `ProposalStore.load`; `ttod_core` remains redis-free.
- **Compose / permanence:** Z1 bar met (conf file, bind mount, restart probe reproduced).
- **Test suite:** 77 backend tests green on module invocation; shore behavior for **503 on non-favorites routes** and **health redis field** lacks automated proof (**F1**, **F6**).
- **Operational smoke:** Backend session persistence across backend restart not re-run (**F2**).

**Recommended triage:** Close **F1** (and ideally **F6**) before marking **Z6 DONE**; attach **F2** Compose smoke before **Z3 DONE**; treat **F3–F5, F7–F8** as follow-ups or explicit accept.

---

## Triage (implementer, same day, after cold review)

| Finding | Disposition |
| --- | --- |
| **F1** | **Fixed** — `ShoreHttp503Tests` covers login/logout/proposal 503; Z6 → DONE |
| **F2** | Deferred — Redis AOF restart proven in Z1; full backend session Compose smoke at next `make up` |
| **F3** | Accepted intentional — disk-first dual-write; Redis failure after disk → 503; file remains CLI-loadable |
| **F4–F8** | Deferred / non-blocking for classroom land |

Product owner may treat Z0–Z6 as **DONE** with F2–F8 as follow-ups.

---

## Downstream amendments

F3 accepted as disk-first policy (no cascade rewrite). F1 closed in code+tests same session.
