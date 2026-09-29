# TTOD development plan index

**Repository:** `/Users/ruvebal/src/ttod`

**Programme status:** Q0–Q6 DONE (Phase Q complete — 2026-08-18)

**Canonical entry point:**
[`PHASE-Q-TTOD-CONTRACT-REPAIR-CASCADE.md`](PHASE-Q-TTOD-CONTRACT-REPAIR-CASCADE.md)

**Shared studio protocol:**
[`deviac/docs/DEV_PLAN/TTOD-BRIDGE-INTEROPERABILITY-CONTRACT.md`](../../../deviac/docs/DEV_PLAN/TTOD-BRIDGE-INTEROPERABILITY-CONTRACT.md)

TTOD owns canonical quote identity; the studio protocol supplies reusable REST, offline-bundle,
and graph/RDF bindings. Counts, coverage, and collection totals are generated dynamically from a
snapshot rather than hardcoded in instructions.

TTOD is the studio-owned pedagogical quotation system. `ttod.yml` remains its canonical
human-governed database. Athanor may serve a versioned TTOD snapshot and may return proposed
quotes to a review inbox, but no model, Athanor adapter, WPL process, or sibling repository may
write canonical quote records directly.

## Incoming cross-repo work

TTOD's canonical authority stays here, but two studio contracts land TTOD-side deliverables from
outside this repository. These rows are pointers — the cascade files live where their gateway
lives — but the TTOD-owned deliverables and their state are TTOD's responsibility to track.

| Origin | Cascade | TTOD sub-lane | State | Notes |
| --- | --- | --- | --- | --- |
| DevIAC | [`deviac/docs/DEV_PLAN/PHASE-CH/PHASE-CH-STUDIO-CONSUMPTION-HARNESS-CASCADE.md`](../../../deviac/docs/DEV_PLAN/PHASE-CH/PHASE-CH-STUDIO-CONSUMPTION-HARNESS-CASCADE.md) | **CH1** — `clients.yaml` + `schema/clients.schema.json` + `ttod_core/clients.py` + four new `bridge` CLI verbs (`issue-token`, `revoke-token`, `list-clients`, `export-registry-verifier`) + `docs/CONSUMERS.md` + rewrite of `AGENTS.md` § Integration | **BLOCKED** on CH0 product-owner sign-off ([`PHASE-CH0-READINESS-REPORT.md`](../../../deviac/docs/DEV_PLAN/PHASE-CH/PHASE-CH0-READINESS-REPORT.md) §5) | CH1 runbook: [`PHASE-CH1.md`](../../../deviac/docs/DEV_PLAN/PHASE-CH/PHASE-CH1.md). Zero new network surface added by TTOD; `services/mcp/server.py:3001` stays as-is. The DevIAC gateway (CH2) is what exposes it. |
| DevIAC | [`deviac/docs/DEV_PLAN/TTOD-BRIDGE-INTEROPERABILITY-CONTRACT.md`](../../../deviac/docs/DEV_PLAN/TTOD-BRIDGE-INTEROPERABILITY-CONTRACT.md) | Phase Q4 (Athanor bridge) already discharged the initial TTOD-side implementation; Phase CH extends it to N consumers | DONE (Q4) · extended by CH | Same shared studio protocol link at the top of this file. |

**F1 fix on Q4 CLI surface (2026-09-10):** DevIAC Phase CH0 readiness verification surfaced a P1
defect on TTOD `main` — `bridge_app` was defined but never `app.add_typer(bridge_app, name="bridge")`,
leaving `cli.py bridge quote-out` and `cli.py bridge proposal-in` as dead code from the CLI surface.
Fixed in the same commit as the CH0 readiness report; regression test `test_bridge_subtyper_registered`
added in `tests/test_cli_integration.py`. Full TTOD suite: **219/219 OK.** Details:
[`deviac/docs/DEV_PLAN/PHASE-CH/PHASE-CH0-READINESS-REPORT.md`](../../../deviac/docs/DEV_PLAN/PHASE-CH/PHASE-CH0-READINESS-REPORT.md) § F1.
This does not reopen Phase Q; it corrects one shipped wiring defect that no test asserted.

## Active programme

Each row's runbook is a self-contained agent prompt — see
[`PHASE-Q-TTOD-CONTRACT-REPAIR-CASCADE.md`](PHASE-Q-TTOD-CONTRACT-REPAIR-CASCADE.md) §5 for how
they relate to the master contract. Hand one runbook to one agent session; do not hand the whole
cascade document and ask it to "do Q3."

| Phase | Purpose                                                        | Mode                   | State                                                  | Runbook                                                                            |
| ----- | -------------------------------------------------------------- | ---------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| Q0    | Freeze the measured baseline and v3 contract decisions         | sequential blocker     | DONE (2026-08-18; report filed at PHASE-Q0-REPORT.md)  | [`PHASES/Q0-schema-authority-freeze.md`](PHASES/Q0-schema-authority-freeze.md)     |
| Q1    | Schema, compatibility model, and golden fixtures               | sequential             | DONE (2026-08-18; completion pass closed exact-code + origin if/then; PHASE-Q1-REPORT.md) | [`PHASES/Q1-schemas-contract-fixtures.md`](PHASES/Q1-schemas-contract-fixtures.md) |
| Q2V   | Strict validation and invariant engine                         | parallel lane          | DONE (2026-08-18; completion pass: origin+digest on validate_root; PHASE-Q2V-REPORT.md) | [`PHASES/Q2V-validation-core.md`](PHASES/Q2V-validation-core.md)                   |
| Q2E   | Canonical serialization, exports, and digests                  | parallel lane          | DONE (2026-08-18; completion pass: C14N writes, graph export, tamper tests; PHASE-Q2E-REPORT.md) | [`PHASES/Q2E-canonical-export-digests.md`](PHASES/Q2E-canonical-export-digests.md) |
| Q2P   | Proposal and human-review workflow                             | parallel lane          | DONE (2026-08-18; report filed at PHASE-Q2P-REPORT.md) | [`PHASES/Q2P-proposals-review.md`](PHASES/Q2P-proposals-review.md)                 |
| Q3    | Atomic repository and CLI integration                          | sequential integration | DONE (2026-08-18; PHASE-Q3-REPORT.md)               | [`PHASES/Q3-atomic-repository-cli.md`](PHASES/Q3-atomic-repository-cli.md)         |
| Q4    | Athanor-mediated quote-out / proposal-in bridge                | cross-repo integration | DONE (2026-08-18; PHASE-Q4-REPORT.md; TTOD + Athanor sub-lanes) | [`PHASES/Q4-athanor-bridge.md`](PHASES/Q4-athanor-bridge.md)                       |
| Q5    | Independence, provenance, rights, and erasure sensors          | parallel by sensor     | DONE (2026-08-18; PHASE-Q5-REPORT.md; 9 sensors, 21 tests) | [`PHASES/Q5-policy-provenance-sensors.md`](PHASES/Q5-policy-provenance-sensors.md) |
| Q6    | Migration, end-to-end verification, documentation, and release | sequential closeout    | DONE (2026-08-18; PHASE-Q6-REPORT.md; live ttod.yml v3) | [`PHASES/Q6-migration-e2e-docs.md`](PHASES/Q6-migration-e2e-docs.md)               |

## Evidence and status

- [`PHASE-Q0-READINESS-REPORT.md`](PHASE-Q0-READINESS-REPORT.md) records the read-only
  2026-08-14 audit, exact input hashes, observed failures, and the safe resume point.
- [`DECISIONS/Q0-2026-08-18-RIGHTS-LICENSE-NC.md`](DECISIONS/Q0-2026-08-18-RIGHTS-LICENSE-NC.md)
  freezes the repository split license (code MIT, content CC BY-NC-SA 4.0) and the default
  `rights.license` for new/unresolved TTOD quotes as **CC BY-NC-SA 4.0**. Q6 rewrote
  `ttod.yml` header and `AGENTS.md`; `../LICENSE-CODE` and `../LICENSE-CONTENT` remain
  authoritative.
- A phase is not `DONE` because this plan exists. Each phase must file a verified report at
  `docs/DEV_PLAN/PHASE-Qx-REPORT.md` with commands, exits, artifacts, negative tests, and a
  provenance transfer matrix, per its runbook's "Report requirements" section.
- **2026-08-18 Q1/Q2 completion pass:** independent audit found Q1/Q2V/Q2E overstated as DONE
  (exact error codes not asserted, missing `origin` matched the blackbox `if/then`,
  `validate_root()` skipped origin/digest, exports were not C14N, no graph export, no digest
  tamper test). Those gaps are closed in the amended Q1/Q2V/Q2E reports. Full suite: 107 tests
  OK. Live `ttod.yml` was strictly invalid until Q6 migration (215 `ORIGIN_UNRESOLVED`) —
  detecting that drift was success; Q6 closed it.
- **2026-08-18 Q6:** migration closeout DONE — live `ttod.yml` v3.0.0, strict validate 0
  errors, **161 tests** OK, bridge round-trip + rollback injection on pre-migration backup,
  arch-052 live adversary confirmed. Report: [`PHASE-Q6-REPORT.md`](PHASE-Q6-REPORT.md).

## Verification (current)

```bash
cd ~/src/ttod && . .venv/bin/activate
python cli.py validate --strict --json   # exit 0
python cli.py stats --check              # exit 0
python -m unittest discover -s tests -p 'test_*.py'   # 161 tests, exit 0
```
- **2026-08-18 Q3:** atomic repository + CLI integration DONE — `ttod_core/repository.py`,
  full CLI rewrite, rollback/concurrency tests on disposable copies; 125 tests OK at Q3 close.
  Report: [`PHASE-Q3-REPORT.md`](PHASE-Q3-REPORT.md).
- **2026-08-18 Q4:** Athanor bridge DONE — transport schemas, `ttod_core/bridge.py`, Athanor
  read-only adapter, round-trip fixture + 133 TTOD / 6 Athanor tests. Report:
  [`PHASE-Q4-REPORT.md`](PHASE-Q4-REPORT.md).
- **2026-08-18 Q5:** policy sensors DONE — nine deterministic sensors in `ttod_core/sensors/`,
  17 fixtures under `tests/fixtures/q5_*`, 21 sensor tests + 154 total suite OK. arch-052
  adversary confirmed (`SELF_DERIVED_NOT_EVIDENCE`). Report: [`PHASE-Q5-REPORT.md`](PHASE-Q5-REPORT.md).
- **2026-08-18 planning-repair session:** this plan-document tree was restructured (not the
  canonical data) — the redundant root-level copy of the cascade document was removed (the
  `docs/DEV_PLAN/` copy is canonical), the root `INDEX.md` was rewritten to stop duplicating this
  file's status table, and this file's phase table gained the `PHASES/` runbook links. No
  `ttod.yml`, `cli.py`, `schema/`, or `sources/` content was touched. `git init` was completed
  separately, closing the "no recoverable baseline" gap the 2026-08-14 readiness report flagged.

## Proposed programme (Phase S DONE through S4; Phase R reference built; Phases T/U/V active or proposed; Phase W proposed)

**Cross-surface technical proposal (2026-09-15, planning only):**
[`TECHNICAL-PROPOSAL-2026-09-15-SEMANTIC-TAGS-AND-TAO-ALIGNMENT.md`](TECHNICAL-PROPOSAL-2026-09-15-SEMANTIC-TAGS-AND-TAO-ALIGNMENT.md)
— transform TTOD `tags[]` → studio `semantic_tags` (themes · cidoc · getty_aat · dcterms · skos),
and add TTOD pedagogy/provenance axes (`section` / `subsection` / `level` / `teaches` /
`show_when` / `origin` / `rights` / relations) to the CT Tao of Creativity monograph.
Does **not** authorize schema migration, `ttod.yml` mutation, or invent accept. Suggested
future packages W0–W6; blocked on a W0 freeze decision.

The research-and-documentation continuation is planned separately in
[`../research/GUIDE-FORGE-PLAN.md`](../research/GUIDE-FORGE-PLAN.md). It does not reopen Phase R,
authorize R6, generate guides, or authorize research use of student work. Its paste-ready
execution prompt is
[`../research/PROMPT-FORGE-TTOD-GUIDES.md`](../research/PROMPT-FORGE-TTOD-GUIDES.md).

| Phase | Purpose | Mode | State | Cascade prompt |
| ----- | ------- | ---- | ----- | --------------- |
| S | TTOD bilingual content model — per-quote `lang` field + `translation_of` relation (separate IDs, not locale-keyed text), with validator invariants, full read-path propagation (proposal/transport/bridge/exporter), and assisted translation drafting; prerequisite for Phase R's R1 contract freeze | single orchestrator, sequential S1′→S2′→S3′, S4′ after S1′ | **S DONE through S4′.** S0 decision FROZEN 2026-09-04, amended 2026-09-05 and 2026-09-06; S1′ DONE 2026-09-04 (PHASE-S1-REPORT.md); S2′ DONE 2026-09-04 (PHASE-S2-REPORT.md — live `ttod.yml` migrated, `lang: en` on all 229 records, `meta.version: 3.1.0`); S3′ DONE 2026-09-04 (PHASE-S3-REPORT.md); **S4′ DONE 2026-09-04** (PHASE-S4-REPORT.md — `cli.py translate-draft` works as specified; 9/10 pilot pass rate on `qwen3.8:27b`, one flagged semantic-fidelity failure on `img-071`; discovered but did not fix the live `accept_proposal()` reviewer_id gap, now the explicit prerequisite gate for S5 below). **Proposed corpus-completion continuation:** [`PHASE-S5-BILINGUAL-CORPUS-TRANSLATION-PLAN.md`](PHASE-S5-BILINGUAL-CORPUS-TRANSLATION-PLAN.md) — a scholarly translation plan only; no bulk Ollama run, proposal staging, canonical mutation, or acceptance is authorized by its existence. | [`PHASE-S-TTOD-BILINGUAL-CONTENT-MODEL.md`](PHASE-S-TTOD-BILINGUAL-CONTENT-MODEL.md) |
| R | TTOD Oracle Platform — Astro control plane (Svelte graph + React oracle islands) over FastAPI/FastMCP/Ollama, wrapping the existing governed `ttod_core`/`cli.py` data layer read-only. **R0–R5 DONE** (R1 backend, R2 FastMCP, R3a walking skeleton — all instructor-built and cohort-start gate open; R3b content engine, R4 Svelte graph, R5 React oracle terminal — built and cold-reviewed as a **reference/architectural-validation build on `main`, not the student deliverable**). **R6 deliberately deferred, reserved for student ownership — see [`DECISIONS/R6-DEFERRED-STUDENT-OWNED.md`](DECISIONS/R6-DEFERRED-STUDENT-OWNED.md); continued momentum on other phases is not authorization to build it.** R7 PARTIAL — continues testing the reference build; closing gates (Chromium/axe E2E, measured CI wall time) correctly wait on R6. Students receive R1/R2/R3a only via the generated `cohort-starter` branch (`scripts/generate-cohort-starter.sh`), not this reference tree — see [`PHASE-R-CLOSURE-AND-COHORT-HANDOFF-REPORT.md`](PHASE-R-CLOSURE-AND-COHORT-HANDOFF-REPORT.md). | generator prompt → per-phase runbooks (R0–R7) | **R0–R5 DONE, R7 PARTIAL, R6 DEFERRED/STUDENT-OWNED** — see the closure report for the full state table and exact test evidence. | [`PHASE-R-TTOD-ORACLE-PLATFORM-CASCADE-PROMPT.md`](PHASE-R-TTOD-ORACLE-PLATFORM-CASCADE-PROMPT.md) · [`PHASE-R-CLOSURE-AND-COHORT-HANDOFF-REPORT.md`](PHASE-R-CLOSURE-AND-COHORT-HANDOFF-REPORT.md) |
| T | Public Release, Partnership, and Teaching Excellence — converts the 2026-09-07 cold audit into independent public-source, partner-demo, and student-distribution gates. Covers public documentation, measured repository treeshaking and disclosure review, application trust boundaries, a genuinely history-isolated cohort artifact, partner rehearsal, novice onboarding trials, and independent release verification. It **does not authorize publication, deployment, canonical quote mutation, or any student-owned R6 implementation**. Internal steps are `RC0`–`RC7` ("Release Cascade"), renamed 2026-09-07 from an initial `T0`–`T7` draft that collided with `docs/research/GUIDE-FORGE-PLAN.md`'s own unrelated `T0`–`T7` task labels — no scope, order, or dependency changed. | orchestrated gated cascade; RC1–RC4 may run in parallel after RC0 in separate worktrees; RC7 is independent review | **PROPOSED; RC0 BLOCKED (cold review found the baseline stale), RC1–RC7 BLOCKED by declared dependencies.** RC0's original baseline/decisions are in [`PHASE-RC0-REPORT.md`](PHASE-RC0-REPORT.md); [`PHASE-RC0-COLD-REVIEW.md`](PHASE-RC0-COLD-REVIEW.md) (2026-09-11) found `ttod.yml`'s digest and `HEAD` had both moved 22 commits since — including real canonical-data mutation — and that the report cannot be promoted as-written. The safe next action is a fresh RC0 pass against current `HEAD`, not independent verification of the existing one. | [`PHASE-T-PUBLIC-RELEASE-EXCELLENCE-CASCADE.md`](PHASE-T-PUBLIC-RELEASE-EXCELLENCE-CASCADE.md) |
| U | FE II End-to-End Teaching Skeleton — preserves a rich instructor feasibility reference outside student reach while refactoring the distributed teaching product so R3b–R7 all exist as complete, testable hello-world vertical slices, plus a new TS4c seam (Auth) with no existing reference to reduce. The instructor first deploys and explains the entire front-end journey; students then grow the same six seams as assessed work. Includes research rationale/calendar reconciliation, a strict privacy watcher, an independent `docs/public` Jekyll publication lane, and a later gated synchronization of localized FE II course tracks. | sequential teaching gates with TS3/TS4(a/b/c) parallel after the subtraction contract; documentation-only Pages lane is independent; cross-repository synchronization only at TS8 | **PROPOSED; TS0 VERIFYING, Week-0 DONE, TS1–TS4c DONE, TS5 PARTIAL** ([`PHASE-U-TS5-REPORT.md`](PHASE-U-TS5-REPORT.md) — `skeleton/ts5-hello-world` assembled; fresh-history/TS2/privacy open). Seven lane tips + assembly branch, none merged to `main`. Draft [PR #1](https://github.com/ruvebal/ttod/pull/1) is CI evidence only. Local deployment evidence: [`PHASE-TS0-REPORT.md`](PHASE-TS0-REPORT.md). Public-docs boundary: [`DECISIONS/U1-2026-09-07-PUBLIC-DOCS-PAGES-BOUNDARY.md`](DECISIONS/U1-2026-09-07-PUBLIC-DOCS-PAGES-BOUNDARY.md). | [`PHASE-U-FEII-TEACHING-SKELETON-CASCADE.md`](PHASE-U-FEII-TEACHING-SKELETON-CASCADE.md) · [`PHASE-U-WEEK0-ORCHESTRATION.md`](PHASE-U-WEEK0-ORCHESTRATION.md) · [`PHASE-U-TS1-REPORT.md`](PHASE-U-TS1-REPORT.md) · [`PHASES/U-TS5-fresh-history-assembly.md`](PHASES/U-TS5-fresh-history-assembly.md) |
| V | FE II Cohort Collaboration, PR Workflow & Assessment Rubric — converts the professor's PR-driven collaboration draft into a plan reconciled with Phase U's frozen seams (R3b/R4/R5/R6/R7) plus a new sixth module (Auth, TS4c) grounded in FE I's own SSR-auth lessons. Corrects the original draft's headcount (8 students, not 10 → 2+1+2+1+2 pairs/solos, R7 folded into everyone's continuous responsibility rather than a dedicated team) and its missing PWA seam (R6, re-scoped, no deploy/secrets). Adds a logged-in favorites-library + propose-a-quote backlog (§2.5), a bearer-token public API + bot test app (§2.6), a GitHub-native CI/CD proposal-review pipeline reusing the existing `ttod_core.proposals`/`cli.py proposal accept` primitives (§2.7), a calendar anchored to the confirmed 2026-09-10 Week-1 start and recalibrated to the confirmed real session cadence — tomorrow's session is 2h, every week after is a strict single 4h session, which needs six weekly content sessions plus the defense rather than five weeks (§8.5) — and an explicit defense against one-shot agentic completion (§8.6). Defines the PR-evaluation rubric, the oral "diff review" defense rubric, and how both map inside the already-official Entrega 1 (25% · Week 7) and Mid-term (15% · Week 7) weights. Explicitly gates any research framing behind the still-pre-protocol status recorded in `docs/public/research/methodology.md`. | single planning document; its own prerequisite gate (Phase U TS1 through TS4c) is now green, evidence in §1 | **ACTIVE — plan complete, prerequisite gate green (§0.β, §1).** All seven Week-0 lanes executed and independently cold-audited 2026-09-09 (not just claimed); the dirty-`domain.ts` blocker was resolved (committed, then frozen at 67 lines on `skeleton/ts1-contracts`); branch protection and a green CI skeleton are live on `main`, confirmed via `gh api`. The §2.7 proposal-accept pipeline and a small reviewer/student agentic pack (PR template, `gh` review-queue script) are built, not just designed — open as PRs #2/#3. Companion docs: the backlog doc (personas, five `mermaid journey` diagrams, MoSCoW epics, accessibility-as-philosophy) and the sprint doc (session-level chart, real per-session hours, theory/team-meeting/lab-time rhythm). **Three open items remain, all professor-only, none blocking Week 1:** rubric point totals, research framing, the early-finisher grading policy (§10). The three code leftovers flagged during the cold audit (stale oracle test, TS4c's domain types, the uncapped 460-node graph) are already resolved per `PHASE-U-TS5-REPORT.md` (accept / rewrite / deliberately-uncapped respectively) — TS5 itself stays `PARTIAL` (fresh orphan history, privacy watcher, TS2 tag still open; `main` untouched). | [`PHASE-V-FEII-COHORT-COLLABORATION-AND-ASSESSMENT.md`](PHASE-V-FEII-COHORT-COLLABORATION-AND-ASSESSMENT.md) · [`PHASE-V-PRODUCT-BACKLOG-AND-JOURNEYS.md`](PHASE-V-PRODUCT-BACKLOG-AND-JOURNEYS.md) · [`PHASE-V-SPRINT-SESSIONS-AND-METHODOLOGY.md`](PHASE-V-SPRINT-SESSIONS-AND-METHODOLOGY.md) · [`PHASE-V-DEV-SPRINT-AND-HACKATHON-TIMELINE.md`](PHASE-V-DEV-SPRINT-AND-HACKATHON-TIMELINE.md) (2026-09-11, supersedes the sprint doc's Sessions 3–6 against confirmed faster-than-planned pacing) |
| W | Agentic Homogenization — make `agentic/` the tool-neutral edit-home for TTOD rules/skills/agents (extending the existing `report-steward` pack shape); reduce `.cursor/` and `.claude/` to thin **landings** (real frontmatter + redirect). Reconciles the split-brain with studio `~/src/.agents/` via an AG0 naming freeze. Includes a planned branch `agentic/homogenize-landings` (not created by the planning pack) and a pedagogical merge isomorphism to the Phase V quote-proposal accept/merge ritual. **AG6** adds project-level student IDE MCP (Astro docs + official Svelte MCP + vendored `llms.txt`) with existence verification — Docker `services/mcp` stays application-level only. **Does not** mutate `ttod.yml`, migrate all studio skills, ship React Smithery MCP by default, or claim a wired frontier+Ollama validator fleet for AG0–AG5. | gated cascade AG0→AG6; branch only after AG0+AG1 authorization | **COMPLETE.** AG0–AG5 merged via [PR #21](https://github.com/ruvebal/ttod/pull/21); AG6 merged via [PR #22](https://github.com/ruvebal/ttod/pull/22) (`main`@`1ca1e686`, 2026-09-19; decision frozen at [`DECISIONS/W0-2026-09-18-AGENTIC-HOME.md`](DECISIONS/W0-2026-09-18-AGENTIC-HOME.md)). Committed IDE MCP config for Astro/Svelte/Playwright/`filesystem` on `main`, official-only allowlist mechanically enforced, a live MCP handshake against every server (4/4, independently reproduced by cold review), and a complete human-run manual walkthrough with real per-server tool calls. Product's own Compose MCP (`services/mcp`) separately sanity-checked live and confirmed working, untouched by this cascade. Seven independent cold reviews across AG0–AG6, zero unresolved findings. | [`PHASE-W-AGENTIC-HOMOGENIZATION/INDEX.md`](PHASE-W-AGENTIC-HOMOGENIZATION/INDEX.md) · [`PHASE-W-AGENTIC-HOMOGENIZATION-CASCADE.md`](PHASE-W-AGENTIC-HOMOGENIZATION/PHASE-W-AGENTIC-HOMOGENIZATION-CASCADE.md) · [`RATIONALE.md`](PHASE-W-AGENTIC-HOMOGENIZATION/RATIONALE.md) · [`FINDINGS-2026-09-18.md`](PHASE-W-AGENTIC-HOMOGENIZATION/FINDINGS-2026-09-18.md) · [`AGENTIC-HARNESS.md`](PHASE-W-AGENTIC-HOMOGENIZATION/AGENTIC-HARNESS.md) |
| X | Public Docs: Agentic IDE/MCP Guides — two public pages sourced from Phase W's merged AG6 work: a developer/collaborator guide (connect an IDE to TTOD's MCP servers, verify it's actually wired) and a research/pedagogy guide (why this cascade governs agentic development the way it does, hedged the same way `research/methodology.md` hedges its own claims). Cites TTOD quotes `arch-049`/`arch-050`/`arch-058` by ID (all public, CC-BY-NC-SA-4.0, unforced matches) and Athanor's Law L8 as a governance parallel — no fabricated "Athanor teaching rationale," confirmed none exists. **Does not** authorize a research study, translate to Spanish in this pass (`alt_lang_missing: true`, same accepted pattern as `reviewing-cohort-prs.md`), or restyle the site beyond two pages + one diagram. | single cascade doc, steps X0→X5, branch only after X0 authorization | **DONE-with-MERGE_DEFERRED (2026-09-19).** X0–X5 all executed on branch `docs/agentic-dev-mcp-guides`; X1's `qwen2.5-coder:32b` draft pass ran for real (~117s, subprocess). Four independent cold reviews (X1+X2, X3, X4, and a final whole-branch holistic pass), zero P0/P1 findings across all of them; two P2s found and fixed same-session. **[PR #23](https://github.com/ruvebal/ttod/pull/23) open against `main`**, not yet merged. Real side-findings: a citation's PDF-extraction artifact caught via direct arXiv verification, and a stale DevIAC MCP venv (broken by a Homebrew Python upgrade) found and fixed. | [`PHASE-X-AGENTIC-DEV-MCP-GUIDES-CASCADE.md`](PHASE-X-AGENTIC-DEV-MCP-GUIDES-CASCADE.md) · [`PHASE-X-REPORT.md`](PHASE-X-REPORT.md) |
| Y | Agentic dirtree Unix tidy (“Dear Tree”) — one-axis tree (Y5: every child of `agentic/` is a topic pack; leaves abolished; enforced by `tests/test_agentic_tree.py`) after first trying explicit pack-vs-leaf criteria; README legend + Cathedral/Bazaar Tri-Anchor epigraph; optional layout moves; then `lao-tzu-tao-compose` → ttod-bridge proposals for collection `dear_tree`. **Does not** invent `~/src/deviac/agentic`, absorb studio skills, or mutate `ttod.yml` without human accept. | mini-cascade Y0→Y5; branch only after Y0+Y1 auth | **Y0–Y3 DONE, Y4 agent work DONE (2026-09-20)** — branch `agentic/dear-tree-tidy`, PR pending. Plan audited (9 inconsistencies), legend README + `ide-mcp/PACK.md`, Y0–Y4 left the layout unchanged on model-legibility evidence, which the human owner then overruled — **Y5 executed 2026-09-21 (human gate open, cold review AMEND fixed)**, compose lens measured (2 of 3 lanes dead). **Open for a named human:** accept/reject the 5 staged `blackbox` proposals (their printed accept commands are stale — verified recipe in `PHASE-Y4-REPORT.md`), and decide whether `collections.dear_tree` is ever created (no CLI verb; hand-edit forbidden). | [`PHASE-Y-AGENTIC-DIRTREE-UNIX/INDEX.md`](PHASE-Y-AGENTIC-DIRTREE-UNIX/INDEX.md) · [`PHASE-Y-AGENTIC-DIRTREE-UNIX-CASCADE.md`](PHASE-Y-AGENTIC-DIRTREE-UNIX/PHASE-Y-AGENTIC-DIRTREE-UNIX-CASCADE.md) |

The independent public-documentation candidate is `VERIFYING`; its source/render/privacy evidence
and exact deployment prerequisites are recorded in
[`PHASE-PUBLIC-DOCS-SITE-REPORT.md`](PHASE-PUBLIC-DOCS-SITE-REPORT.md). This does not promote RC1,
deploy the application, or change repository visibility.

Phase U's TS1/TS3/TS4 generator pass is DONE (documents only — no branch, worktree, or code
change is authorized by their existence; see each runbook's own entry/exit gates): evidence is in
[`PHASE-U-WEEK0-REPORT.md`](PHASE-U-WEEK0-REPORT.md). It produced
[`PHASE-U-WEEK0-ORCHESTRATION.md`](PHASE-U-WEEK0-ORCHESTRATION.md) (lane dependency graph and the
exact keep/cut table grounded against the live `main` tree) and seven self-contained runbooks —
[`PHASES/U-TS1-subtraction-and-contracts.md`](PHASES/U-TS1-subtraction-and-contracts.md) (sequential,
blocks the rest), [`PHASES/U-TS3a-r3b-content-hello-world.md`](PHASES/U-TS3a-r3b-content-hello-world.md),
[`PHASES/U-TS3b-r4-graph-hello-world.md`](PHASES/U-TS3b-r4-graph-hello-world.md),
[`PHASES/U-TS3c-r5-oracle-hello-world.md`](PHASES/U-TS3c-r5-oracle-hello-world.md) (TS3a gates TS3b/TS3c,
which may then run parallel to each other),
[`PHASES/U-TS4a-r6-pwa-hello-world.md`](PHASES/U-TS4a-r6-pwa-hello-world.md) /
[`PHASES/U-TS4b-r7-testing-hello-world.md`](PHASES/U-TS4b-r7-testing-hello-world.md) (parallel to all
of TS3, gated only on TS1), and
[`PHASES/U-TS4c-auth-hello-world.md`](PHASES/U-TS4c-auth-hello-world.md) (added in the Phase V
second-pass revision — a genuinely new build, no existing rich reference to reduce, and the only
lane authorized to touch `services/backend/**`; also parallel to TS3, gated only on TS1). This is
the "Week-0 prerequisite" Phase V §1 names as blocking student Week 1 — the orchestration
document's §5 product-owner gate is **answered on disk**, **TS1–TS4c are DONE**, and **TS5
minimum assembly is PARTIAL** on `skeleton/ts5-hello-world`
([`PHASE-U-TS5-REPORT.md`](PHASE-U-TS5-REPORT.md); runbook
[`PHASES/U-TS5-fresh-history-assembly.md`](PHASES/U-TS5-fresh-history-assembly.md)). Draft
[PR #1](https://github.com/ruvebal/ttod/pull/1) remains CI evidence, not a merge. Nothing merges
hello-world reductions into `main`; the rich reference stays on `main`. Full TS5 (fresh history,
TS2 isolation, privacy probes) is still open.

Phase R's R0 (generator) pass is DONE: it produced
[`PHASES/R1-backend-bridge.md`](PHASES/R1-backend-bridge.md),
[`PHASES/R2-fastmcp-server.md`](PHASES/R2-fastmcp-server.md),
[`PHASES/R3a-walking-skeleton.md`](PHASES/R3a-walking-skeleton.md),
[`PHASES/R3b-astro-content-engine.md`](PHASES/R3b-astro-content-engine.md),
[`PHASES/R4-svelte-graph-island.md`](PHASES/R4-svelte-graph-island.md),
[`PHASES/R5-react-oracle-terminal.md`](PHASES/R5-react-oracle-terminal.md),
[`PHASES/R6-pwa-cicd-audit.md`](PHASES/R6-pwa-cicd-audit.md), and
[`PHASES/R7-testing-strategy.md`](PHASES/R7-testing-strategy.md) — mirroring how Phase Q's
`PHASES/` runbooks work. §0.1's decisions are frozen as of 2026-09-04, revised 2026-09-06 — Rubén
personally builds R1 (backend), R2 (FastMCP), and R3a (walking-skeleton scaffold: hello-world + one
live quote through the full pipeline); 7 students start only once that cohort-start gate is green,
one owner per remaining lane except R4/R5's natural two-role split; R7 is a continuous
cross-cutting testing lane, not terminal; a three-tier Ollama placement (bare-metal dev on each
student's own machine, Lilith — instructor-only, never student-reachable, corrected 2026-09-06 —
and Scaleway `stg`); and a single Scaleway staging environment (no separate prod, no blue/green).
Repo placement (item 7) is treated as closed per §0.1.7's own text — see `PHASE-R0-REPORT.md`'s
judgment-call log for a stale contradiction found in the master document's §11 prompt text on this
exact point.

**Phase R has since moved past the generator stage.** R1 (backend), R2 (FastMCP server), and R3a
(walking skeleton — hello-world + one live quote through the full pipeline) are DONE and
instructor-built, opening the cohort-start gate; see `PHASE-R1-REPORT.md`, `PHASE-R2-REPORT.md`,
`PHASE-R3a-REPORT.md`, and the independent `PHASE-R1-R3A-CASCADE-REVIEW.md`. R3b, R4, and R5 are
also DONE, built as a **reference/architectural-validation build on `main`** (proof the plan is
buildable), not the artifact handed to students. R7 is PARTIAL, continuing to test that reference
build. R6 is **deliberately not implemented** — see
[`DECISIONS/R6-DEFERRED-STUDENT-OWNED.md`](DECISIONS/R6-DEFERRED-STUDENT-OWNED.md). Students
receive R1/R2/R3a only, via the generated `cohort-starter` branch
(`scripts/generate-cohort-starter.sh`) — not the `main` reference tree. Full state table and test
evidence: [`PHASE-R-CLOSURE-AND-COHORT-HANDOFF-REPORT.md`](PHASE-R-CLOSURE-AND-COHORT-HANDOFF-REPORT.md).

## Constitutional boundary

The Athanor and WPL development processes may reference the same immutable Athanor evidence
snapshot, including ingested research and governed field-research records. They must not quote,
cite, or summarize each other's draft output as evidence. TTOD quotes are pedagogical material,
not independent corroboration. A quote derived from an Athanor plan, including `arch-052`, must
never be fed back to Athanor or WPL as support for that plan.
