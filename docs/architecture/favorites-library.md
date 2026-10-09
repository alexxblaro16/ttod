# Personal favorites library

Favorites are per-user preference data. They are deliberately **not** stored in
`ttod.yml`, and this document records why.

## Why a separate store

`ttod.yml` is the governed corpus: every quote in it has been proposed,
reviewed and accepted through `cli.py proposal accept --reviewer-id …`, and it
carries provenance, rights and review metadata. A favorite carries none of
that. It is a row that says "this user liked this quote today", it changes
without ceremony, and it is meaningless to anyone but its owner.

Mixing the two would mean a user action mutating a reviewed artefact, and it
would force the corpus to know that users exist at all. The dependency runs the
other way: the favorites store knows quote identifiers, the corpus knows nothing
about favorites.

The current adapter is an in-memory dictionary guarded by an `RLock`
(`services/backend/app/favorites.py`). It is enough for the current scope and
keeps the boundary explicit; swapping it for SQLite or any user database is a
change behind the same three functions, with no effect on the HTTP contract.

## The contract

`FavoriteEntry` in `services/frontend/src/types/domain.ts` is the single shape
shared by both sides — `userId`, `quoteId`, `savedAt` (ISO 8601, UTC). The
backend returns exactly those keys and no others, so the frontend never needs a
parallel type of its own.

| Endpoint | Guard | Answer |
| --- | --- | --- |
| `POST /api/v1/favorites` | session cookie | `201` with the `FavoriteEntry` |
| `GET /api/v1/favorites` | session cookie | `200` with the caller's entries |
| `DELETE /api/v1/favorites/{quoteId}` | session cookie | `204`, or `404` if it was not saved |

## Who the favorite belongs to

The owner is always `claims.user_id`, taken from the signed session cookie by
the `RequireSession` dependency in `services/backend/app/auth.py`. The request
body carries only `quoteId`. A client that sends `userId` in the payload is
ignored, which is covered by a test — this is what keeps one user from writing
into another user's bucket.

Anonymous requests never reach the store: `RequireSession` answers `401` before
the route body runs, so an unauthenticated `curl` of the list endpoint returns
no rows. The page at `/[locale]/library` applies the matching server-side guard
(`requireUser` from `services/frontend/src/lib/auth.server.ts`) in the Astro
frontmatter, so the redirect happens before anything renders.

## How to verify

```bash
python -m unittest services.backend.tests.test_favorites
npm --prefix services/frontend run check && npm --prefix services/frontend run build
```

`services/backend/tests/test_favorites.py` covers the auth gate on all three
routes, the save/list/remove cycle, duplicate saves, isolation between two
users, the ownership rule above, and that saving a favorite leaves `ttod.yml`
byte-for-byte unchanged.
