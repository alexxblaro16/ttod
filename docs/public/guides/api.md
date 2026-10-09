---
title: Use the API
eyebrow: API guide
description: The TTOD HTTP surface, its two separate credentials, and a runnable example client that proves them apart.
permalink: /guides/api/
---

# Two credentials, and why they are two

TTOD issues two credentials and they are not interchangeable. Getting this
right is most of what there is to know about the API.

A **session cookie** (`ttod_session`) is what the server-rendered pages use. It
is `HttpOnly`, it travels only in the `Cookie` header, and it identifies a
person browsing the site.

A **bearer token** — a personal access token, or PAT — is what a script uses.
It travels in `Authorization: Bearer …`, it is minted from an existing session
at `POST /api/v1/auth/token`, and it is signed with a different secret and a
different salt from the session.

The consequence is deliberate: a stolen cookie cannot be replayed as a bearer
token, and a leaked PAT cannot open a browser session. Every cross-use is a
`401`. The example client below asserts exactly that.

## Endpoints

Base URL is the application itself — `http://localhost:8080` for a local
Compose run — because Caddy proxies `/api/*` through to the backend.

| Method & path | Credential | Answer |
| --- | --- | --- |
| `POST /api/v1/auth/login` | none (email + password) | `200` with `AuthLoginResponse`; `401` if the credentials are wrong |
| `GET /api/v1/auth/session` | session cookie | `200` with `AuthUser`; `401` without a valid cookie |
| `POST /api/v1/auth/token` | session cookie | `200` with `access_token`, `token_type: "Bearer"`, `expires_in` |
| `GET /api/v1/wisdom/random` | **bearer only** | `200` with one `WisdomEntry`; `401` to anything else |
| `GET /api/v1/wisdom/sample` | none | `200` with the public corpus |
| `POST /api/v1/proposals` | session cookie | `201` with `{ proposal_id, status }` |
| `GET /api/v1/schema/definitions` | none | `200` with the schema definitions |
| `GET /health` | none | `200` with `{ status, ttod_version }` |

## The shapes are the shared types

The JSON on the wire is the same contract the frontend compiles against, in
`services/frontend/src/types/domain.ts`. Nothing here invents a shape.

`AuthUser` — what `GET /api/v1/auth/session` returns, and what sits under
`user` in a login response:

```json
{ "id": "usr-001", "email": "admin@ttod.local", "roles": ["reviewer", "instructor"] }
```

`roles` is a list of `SessionRole`: `student`, `reviewer` or `instructor`.
There is no `role` singular and no `admin` — a client branching on either is
reading an older contract.

`AuthLoginResponse` adds the session material around that user:

```json
{ "session_token": "…", "token_type": "Session", "expires_in": 3600, "user": { … } }
```

`WisdomEntry` is a corpus quote: `id`, `section`, `level`, `text`, `teaches`,
`tags`, plus optional `subsection` and a `rights` block. `POST /api/v1/proposals`
answers with `proposal_id` and `status` and nothing else — the server owns
`origin` and the proposer identity, so sending them is rejected with `422`.

## Walk it with curl

Log in and keep the session token:

```bash
SESSION=$(curl -s -X POST http://localhost:8080/api/v1/auth/login \
  -H 'content-type: application/json' \
  -d '{"email":"admin@ttod.local","password":"'"$TTOD_ADMIN_PASSWORD"'"}' \
  | python -c 'import json,sys; print(json.load(sys.stdin)["session_token"])')
```

Mint a bearer token from it, then call the bearer-only route:

```bash
PAT=$(curl -s -X POST http://localhost:8080/api/v1/auth/token \
  -b "ttod_session=$SESSION" \
  | python -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')

curl -s http://localhost:8080/api/v1/wisdom/random -H "Authorization: Bearer $PAT"
```

Now try to use each credential where the other belongs. All four return `401`:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/api/v1/wisdom/random -b "ttod_session=$SESSION"
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/api/v1/wisdom/random -H "Authorization: Bearer $SESSION"
curl -s -o /dev/null -w '%{http_code}\n' -X POST http://localhost:8080/api/v1/auth/token -H "Authorization: Bearer $PAT"
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080/api/v1/wisdom/random
```

Submitting a proposal needs the session, and answers `201`:

```bash
curl -s -X POST http://localhost:8080/api/v1/proposals \
  -b "ttod_session=$SESSION" -H 'content-type: application/json' \
  -d '{"text":"A quote worth proposing.","section":"wisdom","level":"intermediate","lang":"en"}'
# {"proposal_id":"7b0445e8-92f4-436e-a5b3-8b43594d6a57","status":"proposed"}
```

A proposal is a draft. It never reaches `ttod.yml` from here — publishing runs
through the review pipeline and `cli.py proposal accept --reviewer-id …`, which
the [contributing guide]({{ '/guides/contributing/' | relative_url }}) describes.

## How to verify

`examples/api_client.py` is the same walk as a single script, with no
dependencies beyond the standard library. Run it against a live instance:

```bash
python examples/api_client.py \
  --base-url http://localhost:8080 \
  --password "$TTOD_ADMIN_PASSWORD"
```

Expected output:

```
1. logged in as admin@ttod.local with roles ['reviewer', 'instructor']
2. the cookie resolves to AuthUser usr-001
3. minted a bearer token valid for 3600s
4. rrp-019 (remote-repo): Un informe para gobernarlos a todos, un gráfico para hallarlos...
5. all four cross-credential attempts were refused with 401

The API honours the documented contract.
```

The quote in step 4 changes on every run — that endpoint is random by design.
If any step disagrees with this page, the script prints `CONTRACT BROKEN:` with
the status it got and exits non-zero, so it is usable as a smoke test in a
pipeline and not only by a human reading the output.
