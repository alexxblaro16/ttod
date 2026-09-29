# Y5 report — one-axis tree

**Status: VERIFYING (human gate open) · cold review AMEND → fixed, not re-reviewed** (see [`PHASE-Y5-COLD-REVIEW.md`](PHASE-Y5-COLD-REVIEW.md)). Not DONE: the agent does not certify its own phase, and the owner has not yet read the tree.

## Authorization

The owner's message, quoted verbatim (2026-09-21), is the tick the decision file requires:

> Y5 decision — one axis: every child of `agentic/` is a topic pack ACCEPTED by operator

Scope executed: Y5 only, on branch `agentic/dear-tree-tidy`, **uncommitted, unpushed, unmerged**. `ttod.yml`, `services/mcp/`, and the frozen paths are untouched.

## What changed (working tree)

| Change | Evidence |
| --- | --- |
| `agentic/rules/ttod-editing.md` → `agentic/ttod-editing/rules/ttod-editing.md` (`git mv`); relative link `../AGENTS.md` → `../../../AGENTS.md` | link resolves |
| `agentic/skills/public-docs-i18n/` → `agentic/public-docs-i18n/skills/public-docs-i18n/` (`git mv`) | landing target resolves |
| `report-steward/agent/` → `report-steward/agents/` (`git mv`); `PACK.md` row updated | fresh census: only its `PACK.md` and the README read it |
| `rmdir agentic/rules agentic/skills` | tree test passes |
| `PACK.md` front matter on `report-steward`, `ide-mcp`, and locally on `lao-tzu-tao-compose` (`status: local-untracked`, **not staged**); new `PACK.md` for `ttod-editing`, `public-docs-i18n` | tree test |
| Two `.cursor` landings retargeted; `AGENTS.md`: four path lines + tree drawing | grep + `test -f` |
| `tests/test_agentic_tree.py` (new, `unittest`): a pure `check_tree(root)` run on the real tree and on **16 deliberately broken copies** (permanent negative controls); skip when `agentic/` absent. First version passed 15 breakages the cold review found; rewritten | 24 tests OK with the watcher's |
| `agentic/README.md` rewritten: one rule, annotated tree first | links resolve; Raymond cite re-verified live |

## Gate evidence

| Gate | Result |
| --- | --- |
| Fresh census (step 1) | Matches the plan: `.cursor` ×2, `AGENTS.md` ×4 lines, `agentic/README.md`, `report-steward/PACK.md`; **null** in the studio home, `deviac`, `athanor`, `ahmes`, `profield`, `MSCA` |
| Tests (re-run after the review fixes) | `unittest tests.test_agentic_tree tests.test_public_privacy_watcher`: 24 OK. `make test`: **236 OK** (was 226 before the hardening). `verify-ide-mcp.py` offline: all checks passed |
| Tree-test controls (all recorded, all restored) | (1) temporary top-level `agentic/rules/` → tests 1 and 2 fail; (2) landing reverted to the old path → test 3 fails "canonical target missing"; (3) a `locks` entry that does not name the pack → test 5 fails |
| Skeleton | Overlay method: `tests/test_agentic_tree.py` alone in a directory with no `agentic/` → `OK (skipped=17)`. **The generator itself was not run here, and could not exercise Y5 anyway:** it builds from the `skeleton/ts5-hello-world` *branch*, needs a clean tree (the untracked pack makes it refuse) and no pre-existing local `skeleton/ts5-fresh-history`. The reviewer ran it in a `/tmp` copy: 200 skeleton tests OK. The guard matters after that branch is rebased |
| Privacy (delta, keyed by reason) | Baseline taken before any edit; after: identical, plus the two new `PACK.md` files clean. `AGENTS.md` still has its 7 pre-existing findings, the moved skill its 2, no new ones |
| No stale readers | `git grep` (trailing-slash patterns) outside `docs/DEV_PLAN`: empty |
| Frozen paths | `.github`, `Makefile`, `tests/test_public_privacy_watcher.py` unchanged; `make docs-privacy` PASS through the locked path |
| Raymond cite | `ahmes query --cite` → `(Raymond 2001, 42)`, `page_index=41`, `scheme=pdf_order`, `evaluator_safe=yes` |

## Human gate — open

Answer key written before the owner read the README; **sha256 `3d593a482de4ec78f35bbe37d286d02640f7f16224a38c803602d1adfd5f1031`**, stated to the owner in the hand-off message. Three decisive hypotheticals (H1–H3) the README does not answer verbatim; the
"what must never be renamed" question is reported separately (L1) because the README states it by design. The key is revealed only after the owner answers; the owner's answers and the pass/fail line must be
the owner's own words. It tests README + tree together, not the tree alone.

## Amended after review

The README was amended after the small-model reader missed H2 (it stretched `ttod-editing` to cover a commit-message rule) and after the reviewer's README findings. **You will read the amended README.** The
answer key and its hash are unchanged: the key was written before either change, and the README's new example (CSS class naming) is deliberately not one of the key's hypotheticals.

## Secondary (model) reader — two runs, neither is the gate

Haiku, given only the README and `find agentic -maxdepth 2`. **Run 1** (before the README amendment): A, B, D, E correct; **C missed** — it put a commit-message rule into the existing `ttod-editing` pack.
**Run 2** (after): all correct — slides → new pack with `skills/`; commit style → a new pack with `rules/`; no top-level `rules/`; both locked names with their reasons; "nothing" confusing.
One sample per run, the same small model; the miss-then-fix loop means run 2 is not independent of the amendment. It shows the README no longer *induces* that error. It does not show the owner will read it correctly.

## Test limits, stated

Local only — `.github/workflows/ci.yml` runs no Python tests; `make test` is the sole enforcer. The lock check is line-based; `status` is not compared to git; skipping when `agentic/` is absent means a
checkout that moves the directory silently passes.

## Commit hygiene (nothing committed)

Renames are staged but the link fix is not, and unrelated edits to the root `README.md` (its watcher findings rise by 4 emails vs HEAD) and `.gitignore` sit in the tree. A Y5 commit must be by explicit path and
exclude those and the untracked pack.

## Not done / open

- A second cold review of the fixes (not done; the plan-stage precedent was one re-review, and Y5's own gate is the owner's read).
- The human gate above.
- Nothing committed. `lao-tzu-tao-compose/` stays untracked by design.
