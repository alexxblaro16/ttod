# Personal Favorites Library

The personal favorites library keeps user state separate from the canonical TTOD
corpus.

## Architectural boundary

- [`ttod.yml`](../../ttod.yml) is the canonical, human-governed collection of
  wisdom. Favorites must never be appended to, edited in, or used to allocate
  canonical quote identifiers.
- [`services/backend/app/favorites.py`](../../services/backend/app/favorites.py)
  owns the user-state storage boundary. Each record contains only `userId`,
  `quoteId`, and the UTC `savedAt` timestamp.
- The favorites API derives the user identity from the authenticated request and
  scopes every read, create, and delete operation to that identity.
- The library page reads favorite records and joins them with the public wisdom
  snapshot for display. The join does not copy or mutate canonical content.

The current storage adapter is an in-memory dictionary protected by an
`RLock`. This keeps the boundary explicit and is suitable for the current
application/test scope; production deployment should replace the adapter with a
durable user-state database without changing the API contract.

## Contracts and authentication

- `FavoriteEntry` in
  [`services/frontend/src/types/domain.ts`](../../services/frontend/src/types/domain.ts)
  defines the frontend/backend record shape.
- [`services/frontend/src/pages/[locale]/library.astro`](../../services/frontend/src/pages/%5Blocale%5D/library.astro)
  applies the SSR `requireUser` guard before loading the library.
- The backend routes in
  [`services/backend/app/main.py`](../../services/backend/app/main.py) apply
  `require_session_user` to all favorites operations.
- The focused tests in
  [`services/backend/tests/test_favorites.py`](../../services/backend/tests/test_favorites.py)
  cover storage behavior, unauthenticated requests, successful CRUD operations,
  and multi-user isolation.

## Oral defense points

- **Boundary separation:** `ttod.yml` is canonical pedagogical content;
  favorites are mutable per-user application state.
- **Contract:** `FavoriteEntry` keeps the record shape explicit across the
  Astro frontend and FastAPI backend.
- **Auth strategy:** the SSR library guard prevents anonymous page access, and
  backend dependencies enforce authentication independently of the browser.
- **Isolation:** the authenticated user ID is supplied by the request context,
  not by the favorite payload, so users cannot select another user's storage
  bucket.
- **Evolution:** the storage implementation can move from memory to SQLite or
  another user database while preserving the endpoint and type contracts.
