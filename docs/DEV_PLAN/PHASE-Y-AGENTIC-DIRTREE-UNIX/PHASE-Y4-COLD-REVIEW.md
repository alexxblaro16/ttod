# PHASE-Y4-COLD-REVIEW.md

Fresh reviewer, own sandbox (deleted afterwards), 2026-09-20. Verdict: **PASS for the agent's work; human
gate still open.** No P0/P1.

Verified by re-running: `ttod.yml` SHA-256 `9503e81d…` before/after; `git status` on `ttod.yml` and
`proposals/` empty; no live proposal accepted (242 files, 230 accepted, unchanged); exactly five
staged files, all `blackbox`/`pending_human_review`/no `validated_by`; the staged `acceptance.command`
fails with "No such option: --subsection"; the appendix converter → `proposal import` →
`proposal accept --reviewer-id DRYRUN-NOT-A-HUMAN` chain reproduced (460 → 465 quotes, `validate
--strict` valid, `stats --check` OK, `subsection`/`teaches` preserved); `cli.py --help` has no
collections verb and no documented way to add one (existing collections use `ids:`, `filter:`+`count:`,
or both); 219 tests OK. Content: cc-033 adjacency is real; no candidate is a near-duplicate (best
character-level match 0.47, best word overlap 0.18); no candidate misstates Phase Y's layout facts.

| # | Sev | Finding | Disposition |
| --- | --- | --- | --- |
| 5 | P2 | Converter asserts `lang`, a rights block, an `authorship_assertion` and a `generation_method` the staged files did not contain; report did not flag the rights block for human confirmation | Disclosed in the report; human told to confirm rights and `lang` |
| 6 | P3 | The runbook's collection snippet used a JS-style comment (`[/* … */]`, invalid YAML); a comment in a collections edit also changes the snapshot's collection-policy digest | Snippet fixed and annotated |
| 8 | P2 | A stray `/tmp/y4_convert.py` survived the "sandbox deleted" claim | Deleted |
| 9 | - | Report says what the agent did not do; no overclaim; IDs marked provisional | none needed |
