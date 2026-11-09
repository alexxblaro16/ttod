# S5E editorial decisions (pack mirror)

**Live product register:** [`docs/editorial/EDITORIAL-DECISIONS.md`](../../editorial/EDITORIAL-DECISIONS.md).
Keep this pack mirror in sync on substance; do not erase historical CODA wording.

Append decisions; never rewrite a historical decision to make it appear that the earlier review
reached the same conclusion.

## EDITORIAL-DECISION-2026-11-08-CODA

| Field | Value |
| --- | --- |
| **quote_id** | `img-086` |
| **canonical wording** | “Coda con sabiduría” |
| **decision** | Preserve; the wording is correct and intentional |
| **authority** | Rubén Vega Balbás, product owner / author |
| **decided_at** | 2026-11-08 |
| **rationale** | Product-owner intent: the authored Spanish wording is correct and intentional |
| **effect** | Supersedes the S4 report's current recommendation for this item |
| **historical record** | Keep `PHASE-S4-REPORT.md` unchanged as evidence of the earlier assessment |
| **constraint** | Do not automatically promote the “Codifica” alternate proposal |

The earlier S4 response judged the phrase through a literal-translation lens. The product owner has
confirmed the authored phrase. Future reviewers must treat this as intent, not an open defect.
`PHASE-S4-REPORT.md` remains byte-identical to `HEAD` (verified `git diff HEAD -- docs/DEV_PLAN/PHASE-S4-REPORT.md` empty during S5E0).

## EDITORIAL-DECISION-2026-11-08-LEDGER-LOCATION

| Field | Value |
| --- | --- |
| **decision_id** | `EDITORIAL-DECISION-2026-11-08-LEDGER-LOCATION` |
| **status** | APPROVED |
| **path** | `_private/editorial/EDITORIAL-REVIEW-LEDGER.json` (repo-relative) |
| **absolute_path** | `/Users/ruvebal/src/ttod/_private/editorial/EDITORIAL-REVIEW-LEDGER.json` |
| **access** | Product owner + named human reviewers only |
| **gate_env** | `TTOD_EDITORIAL_LEDGER` = absolute path to that file |
| **schema** | `docs/editorial/EDITORIAL-REVIEW-LEDGER.schema.json` |
| **authority** | Rubén Vega Balbás, product owner |
| **decided_at** | 2026-11-08 |
| **rationale** | Owner: private review lives under `_private/` (gitignored). Item-level notes never under tracked `docs/`. |
| **note** | Root `.gitignore` ignores `_private/` only. The tracked `private/` tree is a different convention (auditable backups); do not put this ledger there. Canonical absolute path is the main checkout; do not treat worktree `_private/` copies as authoritative. |

## EDITORIAL_POLICY_APPROVED

| Field | Value |
| --- | --- |
| **token** | `EDITORIAL_POLICY_APPROVED` |
| **authority** | Rubén Vega Balbás, product owner / general editor |
| **decided_at** | 2026-11-08 |
| **policy_id** | `TTOD-ES-POLICY` |
| **policy_version** | `1.0.0-draft` |
| **glossary_version** | `0.0.0` (schema frozen; terms empty until human curation) |
| **ledger_path** | `_private/editorial/EDITORIAL-REVIEW-LEDGER.json` |
| **ledger_access** | Owner + named human reviewers; gates via `TTOD_EDITORIAL_LEDGER` |
| **coda_precedent** | `EDITORIAL-DECISION-2026-11-08-CODA` remains binding |
| **effect** | Unblocks S5E1 VERIFYING / exit gate; S5E2 may open after S5E1 DONE |
