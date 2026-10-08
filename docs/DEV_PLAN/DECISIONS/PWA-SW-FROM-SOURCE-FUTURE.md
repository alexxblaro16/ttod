# Future: compile the service worker from source (not `public/sw.js`)

**Status:** PARKED — do not implement until the instructor explicitly opens this work.  
**Recorded:** 2026-10-08 (after merge of PR #51).  
**Owner:** maintainer (`@crea-comm.net`), not a student Equipo 4 task.

## Why this exists

PR #51 correctly landed Task 1 as `services/frontend/public/sw.js` + register `/sw.js` — that matches `ASSIGNMENT-pwa-task1` and MDN-style pedagogy. It is **not** a defect.

For a growing PWA (TS, shared cache constants, build-time version injection, later Workbox), the better product shape is:

- source under `services/frontend/src/pwa/`
- Vite/Astro build emits `/sw.js` as an artifact
- no hand-edited worker committed in `public/`

## Decision when this is opened

Prefer **light Vite multi-entry / small plugin** (option A) over `vite-plugin-pwa`/Workbox (option B) until Equipo 4’s later tasks have landed or been rebased. Workbox can wait.

## Target layout

```text
services/frontend/src/pwa/
  sw.ts              # install / activate / fetch
  cache.ts           # CACHE_PREFIX, PROOF_ASSET (shared)
  register.ts        # navigator.serviceWorker.register('/sw.js')
public/site.webmanifest   # may stay static initially
# remove public/sw.js once build emits /sw.js
```

## Implementation checklist (when un-parked)

1. Branch off current `main`: e.g. `chore/pwa-sw-from-source`.
2. Wire Vite/Astro so `astro build` and `astro dev` both serve `/sw.js` (dev often needs write-to-public or an equivalent serve path — document which).
3. Keep register URL `/sw.js` (origin-root scope).
4. Move inline registration / network-boundary script from `Page.astro` into `register.ts` (+ small helper if clean).
5. Update `e2e/pwa-lifecycle.spec.ts` to assert against source or built worker; keep v1→v2 cleanup proof.
6. Amend `ASSIGNMENT-pwa-task*` + contributing: source of truth is `src/pwa/`; `/sw.js` is a build artifact.
7. Coordinate Equipo 4 open tips (#46→#47→#49→#50): rebase onto this tip **or** merge this **before** those land, so they stop editing `public/sw.js`.

## Acceptance (for the future PR)

- [ ] `astro build` produces `/sw.js`; `public/sw.js` not committed
- [ ] `astro dev` registers a working worker
- [ ] Lifecycle E2E green (offline proof CSS + activate cleanup)
- [ ] Optional stretch: build-time cache version via `define` / `import.meta.env`
- [ ] Assignment / review-bot paths updated

## Timing note

Cleanest cohort order: land this maintainer PR **before** Equipo 4 rebases #46+, so students extend the compiled SW once.

## Non-goals (for the parked plan)

- Do not rewrite student grades for #51.
- Do not require Equipo 4 to re-submit Task 1 solely for this move.
- Do not adopt Workbox in the first maintainer PR unless product needs force it.
