# Cohort PR scorecard — 2026-10-07

**Audience:** instructor only (not published under `docs/public/`).
**Rubric source:** [`PHASE-V-FEII-COHORT-COLLABORATION-AND-ASSESSMENT.md`](../PHASE-V-FEII-COHORT-COLLABORATION-AND-ASSESSMENT.md) §5 (PR) · §6 (oral defense, separate).
**Evidence layer on GitHub:** each PR has (1) `🤖 Automated review` via `make review-pr POST=1` and (2) `Instructor triage — review of the automated review`.

**How to use:** fill the six score columns (integers). Leave blank until you have verified that dimension. A missing AI Review Log makes the PR **incomplete** — do not award the full 10 process points until the table is present and honest.

---

## §5 rubric (100 pts / PR)

| Code | Dimension | Pts |
| --- | --- | ---: |
| C | Contract adherence | 25 |
| A | Correctness & acceptance criteria | 25 |
| T | Test coverage | 20 |
| X | Accessibility | 10 |
| CI | CI green | 10 |
| P | AI disclosure & process evidence | 10 |

**Score cells below:** `—` = not yet scored by human. Process notes are prefilled from the 2026-10-07 triage pass.

---

## Group → seam map

| Group | Seam (module) | Authors on open PRs | Stack shape |
| --- | --- | --- | --- |
| Equipo 1 | Content / i18n / proposals UI (R3b) | `gontugithub` | Plan landed (#28) + Bugbot amend **#43 MERGED**; feature tasks not yet |
| Equipo 2 | Knowledge graph (R4) | `gpfc-git` | Single task PR (#48) |
| Equipo 3 | Oracle terminal (R5) | `Andreavilaro0` | Cumulative #44→#45→#38→#39→#40→#41→#42 |
| Equipo 4 | PWA / local ops (R6) | `PRNovoa` | #51 replaces #37; then #46→#47→#49→#50 (still carry `.aws` on later tips) |
| Equipo 5 | Auth / favorites / public API | `alexxblaro16` | Cumulative #31→#32→#33→#34→#35 |

---

## Per-PR matrix

Legend for **Triage** column: process flags from instructor meta-review (not a grade).

| Group | PR | Task / branch | C/25 | A/25 | T/20 | X/10 | CI/10 | P/10 | Σ/100 | Triage (2026-10-07) | Bot + meta |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| E5 | [#31](https://github.com/ruvebal/ttod/pull/31) | accounts-task1 · `task/1-ssr-auth` | — | — | — | — | — | — | — | AI log missing; CHANGES_REQUESTED; CI green | [bot](https://github.com/ruvebal/ttod/pull/31) · meta posted |
| E5 | [#32](https://github.com/ruvebal/ttod/pull/32) | accounts-task2 · `task/2-personal-library` | — | — | — | — | — | — | — | AI log missing; mergeable UNKNOWN; CHANGES_REQUESTED | bot · meta |
| E5 | [#33](https://github.com/ruvebal/ttod/pull/33) | accounts-task3 · `task/3-proposal-endpoint` | — | — | — | — | — | — | — | AI log missing; verify 201+proposal id; bot TS→Python false positive | bot · meta |
| E5 | [#34](https://github.com/ruvebal/ttod/pull/34) | accounts-task4 · `task/4-review-pipeline` | — | — | — | — | — | — | — | AI log missing; verify `requireRole(reviewer)`; ignore favorites “scope creep” | bot · meta |
| E5 | [#35](https://github.com/ruvebal/ttod/pull/35) | accounts-task5 · `task/5-public-pat` | — | — | — | — | — | — | — | AI log missing; cookie-must-401 on `/wisdom/random` | bot · meta |
| E4 | [#37](https://github.com/ruvebal/ttod/pull/37) **CLOSED** | pwa-task1 · bad `main` head | — | — | — | — | — | — | — | Superseded by #51 | — |
| E4 | [#51](https://github.com/ruvebal/ttod/pull/51) | pwa-task1 · `pwa-task1-service-worker` | 24 | 24 | 20 | 10 | 10 | 9 | **97** | Replaces #37; tip at `v2` OK with E2E v1→v2; AI log filled; bot false positives dismissed | bot · triage 2026-10-08 |
| E4 | [#46](https://github.com/ruvebal/ttod/pull/46) | pwa-task2 · `pwa-task2-offline-oracle` | — | — | — | — | — | — | — | Verify oracle shell cached offline; drop `.aws`; AI log | bot · meta |
| E4 | [#47](https://github.com/ruvebal/ttod/pull/47) | pwa-task3 · `pwa-task3-cache-policies` | — | — | — | — | — | — | — | Verify cache-first static / network-first API; drop `.aws`; AI log | bot · meta |
| E4 | [#49](https://github.com/ruvebal/ttod/pull/49) | pwa-task4 · `pwa-task4-offline-queue` | — | — | — | — | — | — | — | Bot wrongly said db/sw missing — verify flush-on-online; OracleTerminal conflict; AI log | bot · meta |
| E4 | [#50](https://github.com/ruvebal/ttod/pull/50) | pwa-task5 · `pwa-task5-install-quality` | — | — | — | — | — | — | — | Canonical manifest name; install evidence; AI log | bot · meta |
| E3 | [#44](https://github.com/ruvebal/ttod/pull/44) | oracle-task1 · streamed rendering | — | — | — | — | — | — | — | CI not reported; strengthen chunk assertions; AI log | bot · meta |
| E3 | [#45](https://github.com/ruvebal/ttod/pull/45) | oracle-task2 · live region | — | — | — | — | — | — | — | CI not reported; describe-name NIT only | bot · meta |
| E3 | [#38](https://github.com/ruvebal/ttod/pull/38) | oracle-task3 · grounded/creative | — | — | — | — | — | — | — | CI not reported; dismiss prior-task test removal | bot · meta |
| E3 | [#39](https://github.com/ruvebal/ttod/pull/39) | oracle-task4 · session history | — | — | — | — | — | — | — | CI not reported; verify `sessionHistory` wire format | bot · meta |
| E3 | [#40](https://github.com/ruvebal/ttod/pull/40) | oracle-task5 · preparing state | — | — | — | — | — | — | — | CI not reported; preparing-vs-immediate-error | bot · meta |
| E3 | [#41](https://github.com/ruvebal/ttod/pull/41) | oracle-task6 · recovery/error | — | — | — | — | — | — | — | CI not reported; assert user-facing unavailable copy | bot · meta |
| E3 | [#42](https://github.com/ruvebal/ttod/pull/42) | oracle-task7 · unit/component in CI | — | — | — | — | — | — | — | CI not reported; suite retention is in-brief for Task 7 | bot · meta |
| E2 | [#48](https://github.com/ruvebal/ttod/pull/48) **APPROVED** | graph-task1 · `graph-task1-fetch-from-api` | 25 | 24 | 20 | 10 | 10 | 9 | **98** | `activeTag` removal in-brief; aside+E2E solid; behind main before merge | bot · triage · **APPROVE** |
| E1 | [#43](https://github.com/ruvebal/ttod/pull/43) **MERGED** 2026-10-08 | docs · `PLAN-EQUIPO1` Bugbot fixes (`docs/group-1-plan-amendments`) | 22 | 24 | 20 | 10 | 10 | 3 | **89** | Docs-only amend of #28 findings; empty AI log / template checkboxes; bot domain mismatch dismissed | bot · triage · anti-slop |

---

## Group rollup (fill after per-PR scores)

Aggregate only **scored** PRs. For cumulative stacks, either (a) score each tip PR as the task delta you verify, or (b) score the latest tip once against the whole seam — pick one policy and stick to it for every group.

| Group | PRs in wave | Mean Σ | Median Σ | Incomplete (no AI log / HOLD) | Notes |
| --- | --- | ---: | ---: | --- | --- |
| E1 Content | #43 (scored) | **89** | **89** | AI log empty on merge | Docs amend only; no feature PRs yet |
| E2 Graph | #48 (scored, approved) | **98** | **98** | — | Merge after updating branch if behind |
| E3 Oracle | #44 #45 #38 #39 #40 #41 #42 | — | — | — | Merge order fixed; CI evidence thin |
| E4 PWA | #51 (scored); #46 #47 #49 #50 open | **97** | **97** | later tips still have `.aws` | Merge **#51 → #46 → #47 → #49 → #50** |
| E5 Accounts | #31–#35 | — | — | — | CHANGES_REQUESTED already on all five |

---

## Recommended acceptance / merge order (conflicts)

Do **not** treat this as a grade order — it is merge safety only.

1. **#43** (docs) · **#48** (graph) — independent  
2. **Oracle:** #44 → #45 → #38 → #39 → #40 → #41 → #42  
3. **Accounts:** #31 → #32 → #33 → #34 → #35 (resolve #32 mergeability first)  
4. **PWA:** **#51** → #46 → #47 → #49 → #50 (rebase later tips after #51; also after Oracle before #49/#50)

---

## Companion CSV (import to Sheets)

Same columns; scores blank until filled. Path: [`COHORT-PR-SCORECARD-2026-10-07.csv`](./COHORT-PR-SCORECARD-2026-10-07.csv).

---

## Bot quality note (qwen2.5-coder:32b on #51)

Not “the prompt is broken” — the hybrid rubric already says AI log → MUST FIX only if empty, Task 5 owns icons, extras → STRETCH. On #51 the model still:

1. Flagged AI Review Log empty **while the table was filled** (read failure).
2. Invented an a11y MUST/NIT (`aria-label` on a live region that already has visible text + `role="status"` + `aria-live`) — classic cargo-cult.
3. Over-literal on “start at v1” despite E2E proving v1→v2 cleanup with tip at `v2`.
4. Vague MUST FIX on manifest installability when the brief already scopes icons to Task 5.

**Split:** ~60% model (shallow body/diff reading, a11y stereotypes); ~40% prompt hardenables (explicit “do not MUST FIX aria-label when visible text + status live region”; “tip CACHE_NAME may be v2 if tests prove bump”). Keep the triage comment layer — by design the bot is a first pass, not the grade.

---

## Scored rationale — [#48](https://github.com/ruvebal/ttod/pull/48) (APPROVED 2026-10-08)

**What it is:** Equipo 2 graph-task1. Hardens fetch → `joinTags` → `radialLayout` → SVG selection/`<aside>`. Removes tag filter, URL sync, and GSAP (explicitly out of Task 1 scope). Author `@gpfc-git`. CI `typecheck-and-build` green. Formal **APPROVE**.

| Dim | Pts | Why |
| --- | ---: | --- |
| C | **25**/25 | Uses published `domain.ts` graph/wisdom shapes; no parallel types; no backend edits. |
| A | **24**/25 | Meets all four success criteria; `activeTag` removal is correct per brief. −1: PR notes local `check`/`build` not run (CI covered it). |
| T | **20**/20 | Strong Playwright integration: mock APIs, layout coordinates, click/Enter/Space → aside, loading/empty/error. |
| X | **10**/10 | `role="button"` + labels; aside `aria-live="polite"`; legend text (not color-only). |
| CI | **10**/10 | Required check SUCCESS. |
| P | **9**/10 | AI Review Log filled and honest. −1: local verify gap admitted (not empty log). |
| **Σ** | **98**/100 | |

---

## Scored rationale — [#51](https://github.com/ruvebal/ttod/pull/51) (merged — score locked 2026-10-08)

**What it is:** Equipo 4 Task 1 replacement for closed #37. Branch `pwa-task1-service-worker`. Files: `sw.js`, `site.webmanifest`, `Page.astro` registration + `#ttod-network-boundary`, `e2e/pwa-lifecycle.spec.ts`. CI green. AI Review Log filled and honest.

| Dim | Pts | Why |
| --- | ---: | --- |
| C | **24**/25 | No parallel `domain.ts` shapes; minimal manifest (`name`/`start_url`/`display`) aligned with Task 1 vs Task 5 split. −1: no other contract surface to exercise. |
| A | **24**/25 | Lifecycle + Cache-First proof asset + bilingual online/offline banner + E2E v1→v2 cleanup. Tip at `v2` accepted given test proof (not a functional miss). |
| T | **20**/20 | Trophy-shaped Playwright lifecycle suite (offline CSS, update/cleanup, unrelated caches, Axe). |
| X | **10**/10 | Visible localized status, `role="status"`, `aria-live="polite"`, Axe in tests. |
| CI | **10**/10 | `typecheck-and-build` SUCCESS. |
| P | **9**/10 | Strong AI log + #37 remediation narrative. −1: unit-test checkbox left unchecked (correctly argued E2E instead — process nit only). |
| **Σ** | **97**/100 | |

---

## Scored rationale — [#43](https://github.com/ruvebal/ttod/pull/43) (MERGED 2026-10-08)

**What it is:** docs-only follow-up to instructor Bugbot notes on [#28](https://github.com/ruvebal/ttod/pull/28). Single file: `docs/DEV_PLAN/group-1/PLAN-EQUIPO1.md` (+76/−55). Author `@gontugithub`. CI `typecheck-and-build` green. No formal GitHub review event (merged after comment triage).

| Dim | Pts | Why |
| --- | ---: | --- |
| C | **22**/25 | Plan now matches live `main` (routes exist; auth not yet; `labels` ≠ slug dict; `content-task<N>-…` branch names; real `ASSIGNMENT-*` paths). Not a `domain.ts` code PR — scored as fidelity of the planning contract to the repo. −3: PR template checkboxes left unchecked. |
| A | **24**/25 | Explicitly closes the 3 high + 4 medium findings from the #28 Bugbot comment; commit message and opener cite that thread. −1: template “What this PR does” section left as HTML comments under the good opener. |
| T | **20**/20 | Docs-only — no new runtime behaviour; Trophy tests N/A. Full mark. |
| X | **10**/10 | Docs-only — a11y DoD N/A. Full mark. |
| CI | **10**/10 | Required check SUCCESS. |
| P | **3**/10 | Strong narrative in opener + commit (process evidence of *what* was fixed). **AI Review Log table empty** and rubric boxes unchecked → incomplete under Unit 6 / §5; cannot award full process points. |
| **Σ** | **89**/100 | |

**Policy note for docs PRs:** T and X are N/A→full when there is no UI/runtime surface. P stays strict (AI log) even for docs.

---

## Still required before locking grades

1. Human score of each PR against that task’s `ASSIGNMENT-*-taskN.md` (bot is first pass only).  
2. AI Review Log present on every scored PR (§5 P dimension).  
3. Equipo 3 CI actually green on the tip PRs.  
4. One behavioral spot-check per seam (Oracle stream, PWA offline, accounts curl guard, graph aside).  
5. §6 oral defense scored separately — not in this matrix.
