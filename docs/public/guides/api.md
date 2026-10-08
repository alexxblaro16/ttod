---
title: API authentication and client
eyebrow: External integrations
description: The TTOD Accounts API contract and a runnable bearer-token example.
permalink: /guides/api/
---

# Accounts API

The backend exposes a small HTTP API at `http://localhost:8000` by default. The examples below
describe the implementation in
[`services/backend/app/main.py`](../../../services/backend/app/main.py), with field names checked
against [`domain.ts`](../../../services/frontend/src/types/domain.ts).

## Authentication model

TTOD uses two different signed credentials:

1. **Session credential** — `POST /api/v1/auth/login` returns a `session_token`. Browser code stores
   that value in the `ttod_session` cookie. Session-protected routes accept that cookie, or a
   `Bearer` session token for server-side requests.
2. **API access token** — `POST /api/v1/auth/token` accepts the `ttod_session` cookie and returns a
   separate short-lived `access_token`. Bearer-only API routes require
   `Authorization: Bearer <access_token>`; a session cookie is not accepted there.

The login response currently returns the session token in JSON; it does not set a `Set-Cookie`
header. An external client must therefore copy it into the `ttod_session` cookie when requesting
the access token.

## Endpoints

### `POST /api/v1/auth/login`

Authenticate the configured admin account.

Request:

```json
{
  "email": "admin@ttod.local",
  "password": "your-password"
}
```

Response (`200`):

```json
{
  "session_token": "<signed-session-token>",
  "token_type": "Session",
  "expires_in": 3600,
  "user": {
    "id": "usr-001",
    "email": "admin@ttod.local",
    "role": "admin",
    "roles": ["reviewer", "instructor"]
  }
}
```

Invalid credentials return `401`.

### `POST /api/v1/auth/token`

Exchange a valid session cookie for an API token:

```http
Cookie: ttod_session=<signed-session-token>
```

Response (`200`):

```json
{
  "access_token": "<signed-api-token>",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

The endpoint is deliberately cookie-only. Missing, invalid, or expired sessions return `401`.

### `GET /api/v1/auth/session`

Return the current session identity:

```http
Cookie: ttod_session=<signed-session-token>
```

or, for a server-side caller:

```http
Authorization: Bearer <signed-session-token>
```

Response (`200`) is the `AuthUser` shape:

```json
{
  "id": "usr-001",
  "email": "admin@ttod.local",
  "role": "admin",
  "roles": ["reviewer", "instructor"]
}
```

The current implementation names this route `/api/v1/auth/session`, not `/api/v1/auth/me`.
Clients should use `/session`; `/me` is not an exposed endpoint.

### `GET /api/v1/wisdom/sample`

Return the public wisdom snapshot. No authentication is required. The response is an array of
wisdom entries, each containing fields such as `id`, `section`, `level`, `text`, `teaches`, `tags`,
`related`, `origin`, `lang`, and `rights`.

### `GET /api/v1/wisdom/random`

Return one public wisdom entry. This is the authenticated endpoint used by the external example:

```http
Authorization: Bearer <access-token>
```

Missing, malformed, or expired bearer tokens return `401`.

## Domain types

The frontend source of truth currently exports `AuthUser`, not a `User` interface. Its fields are:

| Field | Type |
| --- | --- |
| `id` | `string` |
| `email` | `string` |
| `role` | `'admin' \| 'user'` |
| `roles` | `('student' \| 'reviewer' \| 'instructor')[]` |

`FavoriteEntry` is also defined in `domain.ts`:

| Field | Type |
| --- | --- |
| `userId` | `string` |
| `quoteId` | `string` |
| `savedAt` | `string` |

The repository does not currently define `User.displayName`; documentation and clients must not
assume that field exists.

## External client

The minimal client at [`examples/api_client.py`](../../../examples/api_client.py) performs the
complete non-browser flow: login, session-cookie exchange, then bearer-authenticated wisdom
request. It uses only Python's standard library and exits non-zero on any failed request.

Configure the same admin password used by the backend and run:

```bash
export TTOD_PASSWORD='your-password'
python examples/api_client.py
```

For a different backend URL or account:

```bash
TTOD_BASE_URL=http://localhost:8000 \
TTOD_EMAIL=admin@ttod.local \
TTOD_PASSWORD='your-password' \
python examples/api_client.py
```

Expected output is one JSON wisdom entry, for example:

```json
{
  "id": "wis-001",
  "text": "..."
}
```

To run locally, configure `TTOD_ADMIN_PASSWORD_HASH` with a bcrypt hash, start the backend with
`uvicorn services.backend.app.main:app --host 0.0.0.0 --port 8000`, then run the client command
above.
