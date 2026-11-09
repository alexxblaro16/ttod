# PHASE-S5E1 — Cold Review

| Field | Value |
| --- | --- |
| **phase** | PHASE-S5E1 |
| **worktree** | `/Users/ruvebal/src/ttod-PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT-1` |
| **`.cascade-lane`** | `PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT` (confirmed) |
| **base commit** | `b579fe80` |
| **reviewer role** | cascade-cold-reviewer (did not implement) |
| **reviewed_at** | 2026-11-08 |
| **implementer report** | treated as claim list only |
| **verify evidence** | `PHASE-S5E1-VERIFY-LOG.md` (runner-owned; exit 0; exit-gate PASSED after `.venv/bin/python` fix) |
| **DONE decision** | not made here — owner/orchestrator only |

## Diff scope reviewed

Tracked pack delta vs `b579fe80` under `docs/` (status / gate / whitespace):

- `INDEX.md`, `PHASE-S5E-CASCADE.md`, `PHASE-S5E0-COLD-REVIEW.md`
- `PHASE-S5E1.md`, `PHASE-S5E1.exit-gate.sh` (`python` → `.venv/bin/python`)
- Trailing-space cleanup on `PHASE-S5E2.md`…`PHASE-S5E6.md`

Untracked editorial pack (deliverables):

- `docs/editorial/EDITORIAL-TRANSLATION-POLICY.md`
- `docs/editorial/TTOD-ES-GLOSSARY.yml`
- `docs/editorial/EDITORIAL-DECISIONS.md`
- `docs/editorial/EDITORIAL-REVIEW-LEDGER.schema.json`

Untracked runner / implementer artifacts: `PHASE-S5E1-VERIFY-LOG.md`, `PHASE-S5E1-REPORT.md`.

Gitignored local ledger (not required tracked):

```text
.gitignore:8:_private/   → _private/editorial/EDITORIAL-REVIEW-LEDGER.json
```

Root `.gitignore` ignores `_private/` only. Tracked `private/ttod.yml.pre-q6-backup` is a different convention (`git check-ignore` does not ignore it). Owner was told this; decisions note records it.

Store invariant:

```text
git diff HEAD -- ttod.yml proposals   # empty (0 bytes)
git diff HEAD -- docs/DEV_PLAN/PHASE-S4-REPORT.md   # empty (0 bytes)
```

## Acceptance checklist (independent evidence)

| # | Acceptance item | Result | Evidence |
| --- | --- | --- | --- |
| A1 | Policy, glossary, decision register, and JSON Schema validate with the project's parsers | **PASS with gap** | Cold re-run: `PHASE-S5E1.exit-gate.sh` → exit 0; `yaml.safe_load` on glossary OK; `json.tool` on schema OK. Project already uses `jsonschema` (`ttod_core/validation.py`); exit gate does **not** Draft-validate the schema or a ledger instance (see F2). Markdown decisions are presence-grepped, not schema-parsed. |
| A2 | Ledger schema requires both review passes and rejects a missing quote ID or source/target digest | **PASS** | Schema `ledgerEntry.required` includes `translation_id`, `source_id`, `source_digest`, `target_digest`, `fidelity_pass`, `spanish_pass`. Cold `Draft202012Validator` probe: missing `translation_id` → `'translation_id' is a required property`; missing `source_digest` → `'source_digest' is a required property`; missing `spanish_pass` → `'spanish_pass' is a required property`. Empty local ledger skeleton validates. Gate itself does not run these negative fixtures (F2). |
| A3 | Policy names intentional ambiguity and the `img-086` owner decision as binding precedent | **PASS** | `EDITORIAL-TRANSLATION-POLICY.md` §3 “Intentional ambiguity (binding)” cites `img-086` “Coda con sabiduría” and `EDITORIAL-DECISION-2026-11-08-CODA`. |
| A4 | `EDITORIAL_POLICY_APPROVED` in decision register with identity, policy/glossary versions, ledger path/access, date | **PASS (product path)** | `docs/editorial/EDITORIAL-DECISIONS.md` block has token, Rubén Vega Balbás, `1.0.0-draft` / `0.0.0`, `_private/editorial/EDITORIAL-REVIEW-LEDGER.json`, access + `TTOD_EDITORIAL_LEDGER`, `2026-11-08`, plus `EDITORIAL-DECISION-2026-11-08-LEDGER-LOCATION`. Pack mirror lacks these (F1). |
| A5 | No quote or proposal state changed | **PASS** | `git diff HEAD -- ttod.yml proposals` empty; porcelain has no `ttod.yml` / `proposals/` / `sources/` dirty paths. Cold `cli.py validate --strict --json` → `is_valid: true`. |

Hard constraints / out of scope: Coda preserve recorded in policy + product decisions; no `ttod.yml`/proposal edits; no Lao Tzu / Ahmes / Athanor / Ollama / bridge-pending mutation in the diff; item-level notes not under tracked `docs/`; phase left at VERIFYING (not DONE). Empty glossary `terms: []` is an explicit human freeze (`0.0.0`), not invented terms.

## Agentic-change failure modes (§§1–6)

| § | Check | Result |
| --- | --- | --- |
| 1 Import/load | No Python product modules edited; cold `cli.py validate --strict --json` loads and returns `is_valid: true` | N/A / PASS |
| 2 Full suite | VERIFY-LOG contains only the exit-gate success line (no unittest / `make check` / bridge). S5E1 Acceptance does not require the S5E0 suite; store invariant empty. Cold review did not re-run full `make check` | GAP vs generic checklist — acceptable for this docs/policy gate if owner accepts A1–A5 + F2 |
| 3 Tautological new tests | No new tests added | N/A |
| 4 Unpack arity / return shapes | No callee-signature code changes | N/A |
| 5 Discriminated mode fields | Ledger passes are distinct fields (`fidelity_pass` / `spanish_pass`); severity/decision enums separate | PASS |
| 6 Doc ↔ code | `TTOD_EDITORIAL_LEDGER` is read by `PHASE-S5E3.exit-gate.sh` (future load-bearing). Policy §16 still claims freeze “remains blocked” after owner approval (F3). Dual decisions registers disagree (F1) | FAIL on F1/F3 |

## Findings

### F1 — Dual decision registers out of sync (pack mirror missing S5E1 approvals)

| | |
| --- | --- |
| **Severity** | P1 |
| **Blocks DONE?** | **Yes** |
| **Evidence** | Product path `docs/editorial/EDITORIAL-DECISIONS.md` states: “Pack mirror (historical S5E0 location; keep in sync on substance, do not erase)” pointing at `docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT/EDITORIAL-DECISIONS.md`. Pack file still ends after CODA only (22 lines). Cold probe: `pack_has_APPROVED False`, `pack_has_LEDGER False`. Product path has `EDITORIAL-DECISION-2026-11-08-LEDGER-LOCATION` and `EDITORIAL_POLICY_APPROVED`. S5E0 exit gate still greps the pack path for CODA; anyone following that register into S5E2 will not see policy/ledger approval. |
| **Cascade amend?** | **Yes — same triage commit.** Append LEDGER-LOCATION + `EDITORIAL_POLICY_APPROVED` to the pack mirror (preferred: keep CODA historical wording including the S5E0 byte-identical note), **or** replace pack body with a one-screen redirect to `docs/editorial/EDITORIAL-DECISIONS.md` and update INDEX/CASCADE/S5E0 pointers so there is a single live register. Do not leave two live registers that disagree. |

### F2 — Exit gate under-asserts schema rejection / JSON Schema parsing

| | |
| --- | --- |
| **Severity** | P2 |
| **Blocks DONE?** | No (A2 independently verified with `jsonschema` this review) |
| **Evidence** | `PHASE-S5E1.exit-gate.sh` runs `.venv/bin/python -m json.tool` on the schema file (JSON parse only) and `yaml.safe_load` on the glossary. It greps `EDITORIAL_POLICY_APPROVED` and CODA; it does **not** grep `LEDGER-LOCATION`, does not validate a ledger instance, and does not apply negative fixtures. Project already depends on `jsonschema`. Cold `Draft202012Validator` confirms required-field rejection (see A2). VERIFY-LOG transcript is only the success echo after the exit-gate fix. |
| **Fix** | Optional before S5E3: gate should `Draft202012Validator` empty ledger + one missing-`translation_id` / missing-digest / missing-`spanish_pass` fixture, and grep `EDITORIAL-DECISION-2026-11-08-LEDGER-LOCATION`. Not required to close S5E1 once F1 is fixed and A2 stands. |

### F3 — Policy §16 still says approval is blocked

| | |
| --- | --- |
| **Severity** | P2 |
| **Blocks DONE?** | No |
| **Evidence** | `EDITORIAL-TRANSLATION-POLICY.md` lines 153–154: “Until the owner records path and access in `EDITORIAL-DECISIONS.md`, policy freeze (S5E1 policy-approval gate token) remains blocked.” Owner recorded LEDGER-LOCATION + `EDITORIAL_POLICY_APPROVED` on 2026-11-08. Doc instruction is now false (agentic §6). |
| **Fix** | Replace with past-tense pointer to the two decision IDs and the `_private/` path / `TTOD_EDITORIAL_LEDGER` env. Same amend commit as F1 preferred. |

### F4 — Absolute ledger path names main checkout; worktree also holds a copy

| | |
| --- | --- |
| **Severity** | P2 |
| **Blocks DONE?** | No |
| **Evidence** | Decisions `absolute_path` = `/Users/ruvebal/src/ttod/_private/editorial/EDITORIAL-REVIEW-LEDGER.json`. Cold `ls` shows that file and the worktree twin both exist (148 bytes); `cmp` → byte-identical empty skeleton. Gitignore covers both via `_private/`. S5E3 gates will require `TTOD_EDITORIAL_LEDGER` set explicitly — correct — but two local copies invite drift if S5E3 writes only one. |
| **Fix** | After integrate: treat `/Users/ruvebal/src/ttod/_private/...` as canonical; delete or stop writing the worktree copy. Document in S5E3 handoff that gates must export `TTOD_EDITORIAL_LEDGER` to the owner path. No cascade runbook rewrite required beyond a one-line note if desired. |

## Verdict for orchestrator triage

- **Finding count:** 4 (1× P1, 3× P2).
- **P0:** none.
- **DONE blocked by cold review?** **Yes** — F1 (dual decision registers / broken sync contract) must be amended before promotion.
- Cold reviewer does **not** mark the phase DONE.
- After F1 (and preferably F3) amend: re-run exit gate; no need to reopen policy substance if only the pack mirror / §16 prose moves.

## Claims falsified / confirmed from implementer report

| Implementer claim | Cold-review result |
| --- | --- |
| Lane / VERIFYING / stores unchanged | Confirmed |
| Owner approved `_private/` ledger; gitignore `_private/` ≠ tracked `private/` | Confirmed |
| `EDITORIAL_POLICY_APPROVED` recorded with versions + path/access | Confirmed on `docs/editorial/`; **falsified** for pack mirror (F1) |
| Schema requires IDs, digests, both passes | Confirmed (jsonschema reject probe) |
| Policy names intentional ambiguity + `img-086` Coda | Confirmed |
| Exit gate exit 0 after `.venv/bin/python` fix | Confirmed (`PHASE-S5E1-VERIFY-LOG.md` + cold re-run) |
| “Keep pack mirror in sync” | **Falsified** (F1) |

## Amend recommendations (orchestrator)

1. **Required for DONE:** sync or retire pack `EDITORIAL-DECISIONS.md` (F1).
2. **Same commit preferred:** fix policy §16 stale “remains blocked” (F3).
3. **Optional:** harden S5E1 exit gate with jsonschema negative fixtures + LEDGER-LOCATION grep (F2); note canonical absolute ledger path for S5E3 (F4).
4. Downstream `PHASE-S5E2.md`…`S5E6` status prose needs no semantic rewrite beyond normal VERIFYING→DONE once F1 clears — S5E2 already blocks on `EDITORIAL_POLICY_APPROVED`.

Skipped this review: full second `make check` / bridge suite (not in S5E1 Acceptance or VERIFY-LOG); live Lao Tzu pipeline process inspection; writing to the private ledger. Risk: until F1 is fixed, S5E0-path readers can miss that policy/ledger location are approved.
