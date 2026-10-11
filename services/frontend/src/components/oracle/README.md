# Oracle terminal — streamed response rendering (Team 3, Task 1)

How `OracleTerminal.tsx` turns one prompt into one incrementally rendered answer.
Brief: [`docs/public/_tasks/oracle-task1.md`](../../../../../docs/public/_tasks/oracle-task1.md).

## Streaming state

1. `submit()` builds an `OracleQueryPayload` and calls `sendPayload()`, which appends an
   `Exchange` with `state: 'preparing'` and `POST`s to `/api/v1/oracle/stream`. The first chunk
   moves it to `streaming` (see the Task 5 section).
2. The response goes to `readOracleStream(response, onChunk)` from `sse.ts`, which splits the
   body on blank lines and validates each event with `parseSseEvent`. Both helpers are used
   unmodified (the parser is frozen).
3. `onChunk` calls `updateExchange()`, a functional `setExchanges` update, and `appendChunk()`
   either extends the last segment's text (same mode/citations/themes/tags) or opens a new segment.
4. After the stream ends the exchange becomes `complete` (or `queued` / `error`).

**Why one update per chunk:** the answer must never be buffered before first paint. React 18+
batches updates that fire in the same task, so the chunks decoded from one network read commit in
a single render (no layout thrashing), and each later read paints on its own.

## Busy guard

- `busy` is derived from state: any exchange still `preparing` or `streaming`. It disables the **Ask** button
  and makes `submit()` return early, so Ctrl/⌘+Enter and form submit are blocked too.
- `submittingRef` also blocks a second submit fired before React re-renders, so only one stream
  per terminal writes to `exchanges` at a time.

## Reduced motion

`useReducedMotion()` (framer-motion) disables the terminal's open/close transition and the
fade-in of each streamed exchange when `prefers-reduced-motion: reduce` is set. The streamed text
itself is never animated.

Accessibility follows the project's global Definition of Done. The live region announcement
belongs to Task 2 and the grounded/creative label and citation links belong to Task 3.

## Tests

`OracleTerminal.test.tsx` → *streamed rendering (Task 1)* mocks the SSE body with a
`ReadableStream`, checks that the first chunk paints before the stream closes, and checks that a
second submit mid-stream never reaches `fetch`.

```bash
cd services/frontend && npx vitest run src/components/oracle
```

# Live-region announcement (Team 3, Task 2)

Brief: [`docs/public/_tasks/oracle-task2.md`](../../../../../docs/public/_tasks/oracle-task2.md).

## Where the live region lives

Each exchange wraps its streamed segments in `div.oracle-answer` with `aria-live="polite"`,
`aria-atomic="false"` and `aria-busy` set while the exchange is `preparing` or `streaming`. It is the only
`aria-live` node in the terminal: `.oracle-log` used to be one, so the query echo, the "Listening…"
status and the notices were announced together with the answer. The status indicator is now a
sibling `role="status"` element outside the answer.

- **`polite`, not `assertive`:** a streaming answer produces many small updates. `assertive` would
  interrupt whatever the screen reader is saying on every chunk; `polite` queues them.
- **`aria-atomic="false"`:** only the changed text is announced, not the whole answer again on
  every chunk (or once more at the end).
- **`aria-busy`:** `true` while the SSE stream is open, `false` when it closes (complete, queued
  or error). It is scoped to the answer, so it never hides the notices or the proposal status.

The region is in the DOM, empty, before the first chunk arrives (the exchange is added before
`fetch`), because many screen readers ignore live regions that appear already filled.
`readOracleStream` / `parseSseEvent` are untouched; no polling or buffering was added.

## Limits to verify by ear

- Screen readers treat `aria-busy="true"` differently: VoiceOver may hold announcements until it
  turns `false`, while NVDA usually ignores it. That would contradict "announce as it arrives", so
  the real-screen-reader check below decides whether to keep it.
- Checked with `@guidepup/virtual-screen-reader` (run once, not a project dependency): each chunk is
  announced on its own ("The river" → "bends" → "around the stone."). This needs `appendChunk` to
  keep every chunk in `segment.parts` and render it as its own `<span>`; merging them into one
  text node made the reader repeat the whole paragraph on every chunk. The virtual reader
  follows the ARIA spec, not the quirks of NVDA or VoiceOver, so it does not replace the manual check.

**Manual check (step 4 of the brief):** with NVDA + Firefox/Chrome and VoiceOver + Safari, ask a
question with the terminal focused and note whether the answer is heard while it streams, whether
the query or "Listening…" are repeated, and whether the full answer is read again at the end.

## Test

`OracleTerminal.test.tsx` → *live-region announcement (Task 2)* streams two chunks and checks that
the single live region grows chunk by chunk, holds neither the query nor the status, and switches
`aria-busy` from `true` to `false` when the stream closes. It also checks that each chunk is its own
`<span>`.

# Grounded vs. creative disclosure (Team 3, Task 3)

Brief: [`docs/public/_tasks/oracle-task3.md`](../../../../../docs/public/_tasks/oracle-task3.md).

Two small sub-components live next to `OracleTerminal` in `OracleTerminal.tsx`:

- **`ModeLabel`** renders the mode as text ("Grounded in the TTOD corpus" / "Oracular voice — no
  strong TTOD match", localized) plus a glyph that differs in shape: `◆` grounded, `✦` creative.
  The glyph is `aria-hidden`, so screen readers hear only the words. Background and border colors
  are an extra cue, never the only one.
- **`CitationLinks`** renders `citedQuoteIds` as a list named "Cited quotes" / "Citas". Each id is
  a link to the real quote page `/{locale}/wisdom/{id}` (`pages/[locale]/wisdom/[slug].astro` looks
  the quote up by `id`) with `aria-label="View quote {id}"`. Only grounded segments show citations.

Each segment is a `role="group"` with `aria-labelledby` pointing at its `ModeLabel`, so a screen
reader moving through the answer hears which mode a paragraph belongs to. Because the label sits
inside the Task 2 live region, the mode is also announced when a segment starts streaming.
Accessibility follows the project's global Definition of Done.

**Manual check (step 5 of the brief):** in Chromium DevTools → Rendering → *Emulate vision
deficiencies* (achromatopsia, deuteranopia) the two modes must still differ by label and glyph.
Then do the screen reader check described in the Task 2 section.

**Test:** *grounded vs. creative disclosure (Task 3)* streams one grounded and one creative
segment and asserts by role and accessible name, not class names: each group is named by its
mode, the grounded group has a "Citas" list whose links point to `/es/wisdom/{id}`, and the
creative group has no links.

# Cold-start preparing state (Team 3, Task 5)

Brief: [`docs/public/_tasks/oracle-task5.md`](../../../../../docs/public/_tasks/oracle-task5.md).

An exchange is `preparing` from the moment the request fires until the first chunk arrives, then
`streaming`. The status is a text label ("Gathering wisdom…" / "Reuniendo sabiduría…") with
`role="status"`, a sibling of the answer live region. We chose a label over a generic spinner
because the terminal already says "Listening…" while streaming, and a spinner would not tell
"the Oracle is thinking" apart from "something is downloading". The pulse is opacity only and is
switched off under `prefers-reduced-motion`; the text stays.

**When the request fails immediately (brief §3.5):**

- If the browser already reports `navigator.onLine === false`, no request is made. The query goes
  straight to the offline queue and the exchange never enters `preparing`.
- Any other failure is only known after trying, because `navigator.onLine === true` does not prove
  the Oracle is reachable. The exchange is `preparing` until `fetch` settles and then moves to
  `queued` or `error`; it never stays in `preparing` after a failure.

**Tests:** *cold-start preparing state (Task 5)* covers the open stream with no chunk yet
(`role="status"`, Ask disabled), a `fetch` that rejects, and the already-offline case, where the
label is checked synchronously after the click and `fetch` is never called.

# Recovery/error state (Team 3, Task 6)

Brief: [`docs/public/_tasks/oracle-task6.md`](../../../../../docs/public/_tasks/oracle-task6.md).

Three situations look alike in the code and are deliberately **not** handled the same way:

| Situation | What the code sees | What the user gets |
| --- | --- | --- |
| Cold start, model still loading | request open, no chunk yet | the Task 5 `preparing` status ("Gathering wisdom…"), `role="status"` |
| The connection is gone | `fetch` rejects with a `TypeError` | the offline queue: the query is stored and replayed on `online` ("safely queued on this device") |
| The server answered 5xx | status ≥ 500 → `UnreachableOracleError` | `role="alert"` **plus a Retry button**, and the query is *not* queued |
| Any other rejected status (4xx) or a broken stream | any other `Error` | the same alert and Retry, with a generic message |

**Why the queue keeps the `TypeError` case:** a lost connection is not a broken Oracle. The query
survives and the reconnect flush replays it in order, so a Retry button there would only fail
again. Parking a **5xx** in that queue would be the opposite mistake: the server did answer, so
nothing was lost to the network, and hiding it would hide a real outage.

**No raw errors:** `error.message` — which contains the status code — goes to
`enqueueErrorReport` for diagnostics and never into the DOM; the UI only shows the localized
notices above. `Retry` re-runs the *same* exchange rather than appending a second card, so the
state machine stays `preparing → streaming → complete | error`, one card per question, and it
never leaves a stale alert sitting next to its own replacement.

**Test:** *recovery/error state (Task 6)* covers a queued entry whose retry fails (`TypeError` →
alert + Retry) and a 5xx answered by a live server (the "Unavailable" alert, no raw status code,
nothing queued), plus a recovery test where Retry streams normally.

# Unit and component tests (Team 3, Task 7)

Brief: [`docs/public/_tasks/oracle-task7.md`](../../../../../docs/public/_tasks/oracle-task7.md).

Run them exactly the way CI does:

```bash
npm --prefix services/frontend test      # or: cd services/frontend && npm test
```

`services/frontend/package.json` exposes `test` (`vitest run`, non-watch), and
`.github/workflows/ci.yml` runs it between `check` and `build`, so the brief's
"the tests pass in the CI pipeline" line is now something CI actually verifies rather than
something a reviewer has to take on trust. The workflow's `name:` is deliberately **not**
renamed: it is `main`'s required status check, and changing it would leave every PR blocked
on a check that never reports (see the comment at the top of that file).

## Which acceptance line each test proves

| Brief criterion | Test |
| --- | --- |
| SSE sequence handled, `[DONE]` ignored | `sse.test.ts` → *parses a valid envelope and ignores the done sentinel* |
| Chunks split across byte boundaries | `sse.test.ts` → *handles response chunks split across byte boundaries* |
| A malformed envelope is an error, not a silent drop | `sse.test.ts` → *delivers earlier chunks before failing on a malformed envelope* |
| A body-less response fails instead of resolving empty | `sse.test.ts` → *rejects a response with no body…* |
| State updates incrementally, never buffered until close | `OracleTerminal.test.tsx` → *streamed rendering (Task 1)*, plus the malformed-envelope unit test above |
| `aria-busy` / `aria-live` correct during and after streaming | `OracleTerminal.test.tsx` → *live-region announcement (Task 2)* |
| A rejected status (4xx) never leaks a raw HTTP code, and is never queued | `OracleTerminal.test.tsx` → *test coverage (Task 7)* |
| 5xx → "Unavailable" alert + Retry, nothing queued | `OracleTerminal.test.tsx` → *recovery/error state (Task 6)* |

The brief's illustrative `{ type: 'start' | 'delta' | 'end' }` envelope does not exist in this
codebase: the real contract is `OracleResponseChunk` (`mode` / `text` / `citedQuoteIds`) with
`[DONE]` or the stream closing as the terminator, and `sse.ts` is frozen by Task 4's brief.
These tests follow the real envelope rather than the illustrative one.
