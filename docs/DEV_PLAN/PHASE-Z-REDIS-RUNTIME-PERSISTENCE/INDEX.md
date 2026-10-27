<!--
PHASE-Z — Redis shore for accounts, sessions, favorites, proposal drafts (Compose + bind mount).
Amended 2026-10-27: broadened beyond favorites-only. Author: Rubén Vega Balbás PhD
-->

# Phase Z — Redis runtime permanence (shore store)

**Status:** AUTHORIZED 2026-10-27 · **Z0–Z6 DONE** (cold-reviewed; F1 503 matrix fixed) · PR #87 closed superseded with credit.
**Depends on:** Phase R stack on `main`; Phase V Accounts/Library/Proposals API live; tip [#87](https://github.com/ruvebal/ttod/pull/87) as favorites evidence.
**Programme letter:** Z.
**Author:** Rubén Vega Balbás PhD · drafted 2026-10-27 · **amended same day** (accounts + proposals + shared Redis module).

## One-sentence claims

- **Product:** Student logins, profiles, library, and proposal drafts survive Compose restarts without touching `ttod.yml`.
- **Engineering:** One Redis microservice (AOF on a host bind mount) + one shared backend Redis client; Protocol stores per domain; proposals **dual-write** so CLI accept stays file-based.
- **Pedagogy:** Accounts team uses the same shore as favorites — Redis is the database for *runtime identity and drafts*, not a second corpus.

## How to read this pack

| Face | File |
| ---- | ---- |
| Index (this) | entry + live snapshot |
| Shore map (what else?) | [REDIS-SHORE-MAP.md](REDIS-SHORE-MAP.md) |
| Evidence | [FINDINGS-2026-10-27.md](FINDINGS-2026-10-27.md) |
| Orchestrator | [PHASE-Z-REDIS-RUNTIME-PERSISTENCE-CASCADE.md](PHASE-Z-REDIS-RUNTIME-PERSISTENCE-CASCADE.md) |
| Phases | [PHASES/](PHASES/) Z0→Z6 |

## Live snapshot (2026-10-27)

| Fact | Value | Where checked |
| ---- | ----- | ------------- |
| Open tip PRs | **1** — #87 favorites Redis | `gh pr list` |
| Auth today | single env admin + **signed cookie** (no server session store); no multi-user profile DB | `auth.py` |
| Favorites today | process `_favorites` dict | `favorites.py` |
| Proposals today | JSON files via `ttod_core.repository.ProposalStore` (CLI accept depends on this) | `repository.py`, `cli.py` |
| `main` Compose Redis | absent | `docker-compose.yml` |

## Decision

**Yes — Redis is the classroom DB for shore state**, including Accounts (profiles/login/sessions) and proposal drafts. Not Postgres. Not “Redis for favorites only.”

Authorize **Z0** to freeze the shore map + improved Compose knobs before code.
