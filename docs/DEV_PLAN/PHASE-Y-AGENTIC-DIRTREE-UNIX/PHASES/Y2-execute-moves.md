# Y2 — Execute moves + landing retarget (may be a documented no-op)

**Depends on:** Y1 decision file frozen.

## Do

1. Apply only the moves Y1 authorized. If Y1 authorized none, write "no moves — by decision Y1,
   because the legibility test passed" in the report; that is a completed phase, not a skipped one.
2. Update `.cursor` / `.claude` landings if (and only if) paths changed; confirm every landing
   still resolves (`test -f` on each redirect target).
3. Re-run the unit tests and the privacy watcher on every tracked file touched.
4. Re-run the **legibility test** (see CASCADE) on the final tree with a fresh cold reviewer.

## Do not

- Rename `report-steward/` unless Y1 + a CI PR explicitly allow.
- Touch `services/mcp/`.
