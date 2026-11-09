<!-- Phase S5E — bilingual editorial closeout for TTOD; created 2026-11-08. -->

# Phase S5E — bilingual editorial closeout

**Status:** ACTIVE cascade; S5E0–S5E1 DONE; S5E2 is READY.
**Product claim:** TTOD has complete English–Spanish structural coverage; this cascade builds the
review evidence and decisions needed to describe and release that edition responsibly.
**Engineering claim:** seven ordered phases use runnable Cascade Forge gates, preserve canonical
governance, and stop for human decisions at each boundary.

## How to read this pack

| Artifact | Purpose |
| --- | --- |
| [RATIONALE.md](RATIONALE.md) | Product rationale and the role/limits of Lao Tzu sources |
| [PHASE-S5E-CASCADE.md](PHASE-S5E-CASCADE.md) | Orchestrator, master prompt, resume rule, constraints, and approval gates |
| [FINDINGS-2026-11-08.md](FINDINGS-2026-11-08.md) | Live TTOD and Lao Tzu/Ahmes/Athanor evidence checked this session |
| [EDITORIAL-DECISIONS.md](EDITORIAL-DECISIONS.md) | Append-only product-owner editorial decisions |
| [PHASE-S5E0.md](PHASE-S5E0.md) … [PHASE-S5E6.md](PHASE-S5E6.md) | One paste-ready prompt per subphase |
| `PHASE-S5E<n>.exit-gate.sh` | Runnable acceptance check for the external Cascade Forge verifier |
| `PHASE-S5E<n>-COLD-REVIEW.md` | Independent review output |
| `PHASE-S5E<n>-REPORT.md` | Phase report after cold-review triage |

Begin with [S5E0](PHASE-S5E0.md). Do not skip or parallelize phases. The legacy executive-harness
file in the parent directory links to this pack.

## Programme

Only the first unfinished phase may be READY; later phases remain BLOCKED until entry gates pass.
Cascade Forge reads the first word of the Gate cell.

| Step | File | Deliverable | Gate |
| ---: | --- | --- | --- |
| 0 | [PHASE-S5E0.md](PHASE-S5E0.md) | Reconciled baseline and adjudication register | DONE — cold review F1–F3 P2; verify log exit 0 |
| 1 | [PHASE-S5E1.md](PHASE-S5E1.md) | Approved editorial policy, glossary, and ledger design | DONE — cold review F1 fixed; verify exit 0 |
| 2 | [PHASE-S5E2.md](PHASE-S5E2.md) | Human decisions for residual translation proposals | READY — EDITORIAL_POLICY_APPROVED; integrate worktree before start |
| 3 | [PHASE-S5E3.md](PHASE-S5E3.md) | Exhaustive human review ledger for every in-scope pair | BLOCKED — S5E2 DONE, ledger location approved |
| 4 | [PHASE-S5E4.md](PHASE-S5E4.md) | Approved corrections or verified NOT_NEEDED outcome | BLOCKED — correction list approved |
| 5 | [PHASE-S5E5.md](PHASE-S5E5.md) | Cold audit and edition evidence package | BLOCKED — S5E3 and S5E4 DONE |
| 6 | [PHASE-S5E6.md](PHASE-S5E6.md) | Programme docs reconciled and Phase S closed | BLOCKED — release decision recorded |

## Live snapshot — 2026-11-08 (S5E0 recheck)

| Fact | Observed value | Where checked |
| --- | --- | --- |
| Canonical corpus | 460 active records, evenly split by `en`/`es`; 230 translation edges; validation and metadata checks clean | CLI export, strict validate, stats check, `make check` |
| Proposal state | 230 accepted IDs resolve uniquely (229 blackbox + 1 studio); 11 open alternates target sources with existing active Spanish sisters | `proposals/*.json` joined to canonical export |
| Editorial decision | `img-086`: “Coda con sabiduría” is correct and intentional | `EDITORIAL-DECISION-2026-11-08-CODA` |
| Prior Lao Tzu injection | `INJECT_DONE` records successful completion on 2026-09-19; smoke checks used exit codes only | Sibling `INJECT_DONE` and `run-pipeline.sh` |
| Current Lao Tzu batch | `status=failed`, `stage=athanor_ready` (`2026-11-08T11:38:31Z`); no live pipeline processes; Postgres `127.0.0.1:5432` refused | Sibling `state.json`, `pipeline.log`, process listing, TCP probe |
| Current Athanor injection | Not evidenced for the 2026-11-08 run (failed before inject) | Sibling `PIPELINE_FAILED` / log |
| Search/citation limitation | Prior Y3 evidence: Athanor CLI returned hits; vector gateway read the wrong database; Blakney Ahmes cite remained `[BIBLIO-GAP]` | [Y3 ops note](../PHASE-Y-AGENTIC-DIRTREE-UNIX/OPS-dear-tree-compose.md) |
| Worktree | S5E0 docs updated in lane worktree; `ttod.yml` / `proposals` unchanged vs `HEAD` | `git diff HEAD -- ttod.yml proposals` |

Values above are a dated snapshot, not constants. Recompute corpus counts and process state at
execution time.
