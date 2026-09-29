# Y5 execution — cold review (2026-09-21)

**Reviewer:** fresh `cascade-cold-reviewer`, no session context; destructive checks run in a `/tmp` copy. **Verdict: AMEND** (0 P0, 2 P1, 4 P2, nits). It never marked anything DONE.

## Confirmed by the reviewer

The diff matches plan steps 1–7 (both moves are 100% renames; the only body change is the one relative link); nothing unauthorized was touched (`ttod.yml`, `services/`, `.github`, `Makefile`);
`lao-tzu-tao-compose/` stayed untracked; 226 tests, `verify-ide-mcp.py`, `make docs-privacy` all green; the three original controls reproduce; no stale readers anywhere in the studio; the Raymond cite
reproduces and the sentence is at the cited node; the human gate is correctly open and the key hash appears only in the report.

## Findings and dispositions

| # | Finding | Disposition |
| --- | --- | --- |
| P1-1 | The tree test was much weaker than its docs claimed: **fifteen** breakages stayed green (surface naming an empty dir or `..`; hidden/`__` dirs; stray file; dangling symlink; singular `agent/` inside a pack — the very defect that motivated Y5; unlisted surface; landing with no front matter; landing that is a full copy; `Canonical:` aimed at `PACK.md`; orphan landing; orphan mirror; mirror drift with `mirrors: []`; a lock satisfied by any mention of the pack name — a Makefile repointed to `agentic/renamed/…` still passed; a tautological test_7) | **Fixed.** Rewritten as a pure `check_tree(root)`; each breakage is now a permanent negative-control test on a temp copy (`AgenticTreeNegativeControls`, 16 cases; the fixture must start clean, so any catch is due to the mutation). Lock check now needs one line naming both `agentic` and the pack. test_7 removed. **Limits, stated:** the lock check is line-based (a comment on the same line could still fool it); `status` is value-checked, not compared to git |
| P1-2 | The skeleton gate is vacuous: the generator builds from the `skeleton/ts5-hello-world` **branch** (`git archive`), not the working tree, so the generated skeleton has no Y5 content; the plan's premise was wrong. Running it also needs a clean tree and no pre-existing local `skeleton/ts5-fresh-history` | **Fixed in the plan** (decision + runbook rewrite the premise; gate becomes an overlay of the new test onto a generated skeleton — result `OK (skipped=17)`). Not disclosed before: the generator was not run and would have refused |
| P2-1 | Programme `docs/DEV_PLAN/INDEX.md` row Y still described pack-vs-leaf and stopped at Y4 | Fixed |
| P2-2 | Two ungated docs gained tilde-path findings (CASCADE line 29; Y5 runbook line 23) | Fixed: repo-relative paths; CASCADE back to its 6 pre-existing findings |
| P2-3 | README: "never committed" overclaim; deleted sentences that carried facts (packs are not auto-loaded and `report-steward/agents/` has no doorway; `verify-ide-mcp.py` is the stricter mirror gate; the two-touchpoint sentence); "a doorway is never a second copy" sat above the one copy; no `PACK.md` example; `ide-mcp/README.md` missing from the tree | Fixed, all six. The README also gained a rule on what makes a topic fit an existing pack (see below) |
| P2-4 | Index is mixed: renames staged, the link fix is not; unrelated `README.md` and `.gitignore` edits sit in the tree | **Not a Y5 change; acted on by process:** the commit must be by explicit path and must exclude the root `README.md`, `.gitignore` and the untracked pack. No commit made |
| nits | Y1 banner "once accepted"; phase INDEX line 8 "stays a leaf"; report silent on why the generator refuses | Fixed |

## Also found by the secondary reader (not the reviewer)

A small model reading only the README placed a commit-message rule inside the existing `ttod-editing` pack. The README said "add to an existing pack if the topic already has one" without saying what
makes a topic fit — a real README defect (the reader's answer was reasonable given the text). Fixed with a `purpose`-line test and an unrelated example (CSS class naming — **not** the key's hypothetical).
Re-run on the amended README: see the report.

## Not verified by the reviewer

That the quoted owner authorization is a genuine owner message (outside the repo); any legibility outcome; the pre-edit privacy baseline (it reproduced the delta against HEAD instead).
