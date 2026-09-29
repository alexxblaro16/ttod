# Y5 plan — cold review (2026-09-21)

**Scope:** the Y5 plan amendments only (decision, runbook, INDEX, CASCADE, Y1 banner) and the matching DevIAC AH amendments. No code was moved.
**Reviewer:** fresh `cascade-cold-reviewer` agent, no session context. **Verdict: AMEND** (0 P0, 6 P1, 10 P2). The reviewer did not mark anything DONE.

## Confirmed correct by the reviewer (re-run live)

The reader census, every cited line number, the relative-link analysis of the two moved files (`../AGENTS.md` → `../../../AGENTS.md`),
`translate_public_docs.py` computing its root from its own location (unaffected), the CI/Makefile/test lock paths, the loader glob being non-recursive, and the file inventory.

## Findings and dispositions

| # | Finding | Disposition |
| --- | --- | --- |
| P1-1 | Test gate used `pytest`, which is not installed; repo runs `unittest` (`Makefile:112`) | Fixed: gate and test are `unittest` |
| P1-2 | Invariant 3 unsatisfiable for `ide-mcp` (`.cursor/mcp.json` is JSON, not a stub); `surfaces` cannot name a file; a sibling-repo `lock` cannot exist on every machine | Fixed: `mirrors` field + parsed-JSON check; `surfaces` may name files; `external_readers` is unchecked free text |
| P1-3 | New test would be copied into student skeletons that have no `agentic/`; the generator already strips a sibling test for this reason | Fixed: test skips when `agentic/` absent; generator check added to gates |
| P1-4..6 | DevIAC side (missing Round 4, arithmetic, human reader only on as-is tree) | Fixed in the AH pack; see its `PLAN-AUDIT` § Round 4 |
| P2-1 | Y5 said it supersedes Y1 rows 1–2; row 1 (flat packs) is *kept* | Fixed: supersedes row 2 only; Y1 banner corrected |
| P2-2 | Y1's rejected option B silently re-adopted; "≥2 surfaces" criterion left contradicting the tree | Fixed: recorded as a knowing re-adoption; criterion rewritten to ≥1 surface |
| P2-3 | `AGENTS.md:191` legend and tree drawing stale | Fixed: added to step 5 |
| P2-4 | Privacy gate unsatisfiable (DEV_PLAN history has tilde paths) | Fixed twice: my first fix (scope `agentic` + `AGENTS.md`) was itself unsatisfiable — `AGENTS.md`, the moved skill and the watcher own files carry pre-existing findings. Now a per-file **delta** gate with a recorded baseline |
| P2-5 | CASCADE rubric still asks for leaf classes; two different things called "negative control"; the pre-Y5 tree cannot discriminate a model | Fixed: rubric, layer map, renamed "tree-test control", pre-Y5 control dropped with the reason |
| P2-6 | Human gate had no key, no failure path, an unanchored answer, and a self-editable checkbox | Fixed: key hashed first, non-verbatim hypotheticals, verbatim answers, a "still confusing" path, owner-authored tick |
| P2-7 | Invariant 5 vacuous; parser unspecified; existing `PACK.md` files have no front matter | Fixed: invariant 6 rewritten; tiny parser specified; front matter is prepended |
| P2-8 | "No stale readers" grep false-matches `report-steward/agents/` | Fixed: trailing slashes |
| P2-9/10 | DevIAC table and AH3/AH0 wording | Fixed in the AH pack |
| nit | Skeleton worktrees carry old landings; root `README.md`/`.gitignore` modified | Not Y5's; left alone. The two modified files are not part of this work |

## What this review shows

The reviewer found nothing wrong with the *facts* about the old tree and six things wrong with the *new mechanism* I invented (a test that cannot run, a schema that cannot describe one of
its own packs, a human gate an agent could tick). The same shape as Phase W: the plan was faithful to the tree it read and careless about the artifact it added.

## Second pass (2026-09-21) — verdict AMEND (0 P0, 3 P1, 8 P2)

The reviewer **built the mechanism** in a scratch copy: the planned tree, the tiny parser and a `unittest` implementing the invariant. Result: all five packs describable and passing (13 tests OK),
the tree-test control fails (6 failures), the skeleton skips (6 skipped), a stale landing fails. What it found is spec looseness, not design:

| # | Finding | Disposition |
| --- | --- | --- |
| P1-1 | Invariant 3 had no marker; "any backticked path exists" lets a stale landing pass (demonstrated) | Fixed: exact `Canonical:` regex, ≥1 match, target must resolve inside the declaring pack |
| P1-2 | Human gate still self-certifiable: provenance rule only on the checkbox; the key's timing unanchored; the rename question is answered verbatim by the README | Fixed: key hash in a message to the owner, answers and pass line owner-authored, rename question moved to reported-not-decisive |
| P1-3 | DevIAC arithmetic used 15 Q1 items; the key covers 19 files | Fixed in the AH pack (0.83 / 0.025, not 0.86 / 0.06) |
| P2-1 | `git mv` leaves empty `agentic/rules`, `agentic/skills`, failing the tree test | Fixed: `rmdir` step |
| P2-2 | Step-1 census omitted the `agent/report-steward.md` pattern | Fixed |
| P2-3 | Spec example had trailing comments though the parser forbids them; `[]` unspecified | Fixed: comment-free example, `[]` = empty list |
| P2-4 | Path bases unspecified; `mirrors` asymmetric; "call verify-ide-mcp.py" did not fit | Fixed: base column in the contract; the test compares JSON itself |
| P2-5 | `locks` existence-only; `surfaces` unchecked | Fixed: lock text must contain the pack name; invariant 6 checks surfaces |
| P2-6 | Delta gate keyed by line number | Fixed: keyed by (reason, line text) |
| P2-7 | CASCADE stale (negative control, layer map) | Fixed |
| P2-8 | DevIAC contract lacks `mirrors`/`external_readers`; says "1–4" | Fixed in the AH pack |
| nits | README banner wording, "Cost" line, INDEX "packs vs leaves" in header lines 2/15/67 | Banner and Cost fixed; INDEX header lines are the historical Y-phase description and are covered by the banner at the criteria table and the status line |

**Not re-reviewed a third time.** These are spec tightenings the reviewer itself prototyped; a third pass would be reviewing its own demands. The real test is Y5's own cold review, which must run the
implemented test, the negative control and the skeleton generator on a clean tree — three things this plan-stage review could not run.
