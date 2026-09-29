# PHASE-Y3-COLD-REVIEW.md

## Pass 1 — verdict AMEND (two P1)

Dry run reproduced (read-only; `ttod.yml` hash identical, 219 tests, strict validate green). But:
- **P1** the note's root cause ("slug never injected") was false — the ingest ran and wrote to the
  `athanor` database while the gateway reads `deviac` (1,164 vs 0 chunks).
- **P1** the pack, described everywhere as untracked, had been committed (`git add -A agentic`)
  against a hard constraint: public repo, 10 privacy-watcher findings.
- P2 "frozen harvests empty" true of only two files; lane 3's cause (mis-extracted title) missing;
  owner actions incomplete.

## Pass 2 — verdict PASS

Both P1s verified closed by re-running the checks: pack absent from `HEAD` history and index,
present and byte-identical on disk, no remote ref contains the bad commit, nothing pushed; chunk
counts and gateway `DATABASE_URL` re-confirmed; candour of the report confirmed. Residual, fixed
or recorded:
- P2 owner action overclaimed a cause ("`DATABASE_URL` leaked") the log does not show → reworded to
  "not established".
- P2 the watcher flags 8 tilde-path lines across Phase Y's own planning docs (cascade, Y0/Y2 reports,
  Y0/Y4 runbooks). Pre-existing convention in DEV_PLAN (CI scans only `docs/public`); **recorded for
  the owner, not changed**.
- Push hazard: `git push --all`/`--mirror` would have published the local backup branch. The backup
  (redundant — files identical on disk) was **deleted**.
