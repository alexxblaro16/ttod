# Cohort PR scorecard — updated 2026-10-17 (post-defense PR close-out)

**Audience:** instructor only (not published under `docs/public/`).
**Rubric:** §5 — C25 · A25 · T20 · X10 · CI10 · P10 = 100.
**Evidence pack:** [`pr-status-2026-10-11/`](./pr-status-2026-10-11/INDEX.md) (archive; live gates below).
**Mail draft:** [`MAIL-PENDIENTES-DEFENSA-2026-10-15.es.md`](./MAIL-PENDIENTES-DEFENSA-2026-10-15.es.md) (historical).  
**AI-critical usage (instructor):** [`ai-critical-usage-2026-10-25/index.html`](./ai-critical-usage-2026-10-25/index.html) · [`AI-CRITICAL-USAGE-CONCLUSIONS-2026-10-25.md`](./AI-CRITICAL-USAGE-CONCLUSIONS-2026-10-25.md).

**Snapshot:** **0** student tip PRs open. Content #65/#67/#68 merged 2026-10-15.  
**Complete seams (product):** Content Tasks 1–6 · Graph Tasks 1–8 · Oracle · PWA · Accounts.  
**Instructor waiver (2026-10-15, class):** **not required** — (a) formal review of another team's PR, and (b) PR / commits into another team's module. Already-delivered cross-module tips (Graph #78) keep their scores.  
**No tip PR for design-decision Task 10** (Graph / Oracle / PWA / Accounts) — Content T9 shipped as #68. Oral-only memos (if any) are outside this PR matrix.

---

## Group → seam map (current)

| Group | Seam | Authors | Open stack |
| --- | --- | --- | --- |
| E1 | Content | `gontugithub` | #43✓→#61✓→…→#68✓ · Tasks 7–8 **WAIVED** · **seam tip PRs complete** |
| E2 | Graph | `gpfc-git` | #48✓→…→#78✓ · Task 9 **WAIVED** · Task 10 no tip PR |
| E3 | Oracle | `Andreavilaro0` / fork `nbfrodri/ttod_team3` | **complete** product (#42) · Tasks 8–9 **WAIVED** · Task 10 no tip PR |
| E4 | PWA | `PRNovoa` | **complete** (+ #74) · Tasks 8–9 **WAIVED** · Task 10 no tip PR |
| E5 | Accounts | `alexxblaro16` / `Gonsiii11` on #58 | **complete** · Tasks 8–9 **WAIVED** · Task 10 no tip PR |

✓ = already **MERGED**.

---

## Per-PR matrix

| Group | PR | Task / branch | C/25 | A/25 | T/20 | X/10 | CI/10 | P/10 | Σ/100 | Triage / notes | Live CI · merge · decision |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| E1 | [#43](https://github.com/ruvebal/ttod/pull/43) **MERGED** 2026-10-08 | docs-plan-bugbot · `docs/group-1-plan-amendments` | 22 | 24 | 20 | 10 | 10 | 3 | **89** | MERGED; empty AI log; docs amend | — |
| E1 | [#61](https://github.com/ruvebal/ttod/pull/61) **MERGED** 2026-10-12 | content-task1 · `content-task1-facet-routes` | 24 | 24 | 20 | 10 | 10 | 8 | **96** | MERGED; sibling facets; empty-tag 404 | — |
| E1 | [#62](https://github.com/ruvebal/ttod/pull/62) **MERGED** 2026-10-12 | content-task2 · `content-task2-breadcrumbs` | 24 | 25 | 20 | 10 | 10 | 9 | **98** | MERGED; Breadcrumbs + copy.notFound | — |
| E1 | [#63](https://github.com/ruvebal/ttod/pull/63) **MERGED** 2026-10-11 | content-task3 · `content-task3-empty-error-states` | 25 | 25 | 20 | 9 | 10 | 9 | **98** | MERGED; EmptyState+loadWisdom+tests | — |
| E1 | [#64](https://github.com/ruvebal/ttod/pull/64) **MERGED** 2026-10-11 | content-task4 · `content-task4-propose-form` | 25 | 25 | 20 | 10 | 10 | 9 | **99** | MERGED; propose form a11y+gate | — |
| E1 | [#65](https://github.com/ruvebal/ttod/pull/65) **MERGED** 2026-10-15 | content-task5 · `content-task5-provenance` | 24 | 25 | 20 | 10 | 10 | 9 | **98** | MERGED post-amend; ProvenanceBlock on index/facets/detail + tests | — |
| E1 | [#67](https://github.com/ruvebal/ttod/pull/67) **MERGED** 2026-10-15 | content-task6 · `content-task6-content-tests` | 24 | 24 | 20 | 10 | 10 | 9 | **97** | MERGED post-amend; ProposeForm component test + frequencies() | — |
| E1 | [#68](https://github.com/ruvebal/ttod/pull/68) **MERGED** 2026-10-15 | content-task9 · `content-task9-design-decision` | 24 | 24 | 18 | 10 | 10 | 9 | **95** | MERGED post-amend; `DECISION-T9-error-handling.md` aligned to this tip | — |
| E1 | — **WAIVED** 2026-10-15 | content-task8 · formal review of another team's PR | — | — | — | — | — | — | — | Instructor: not required (class waiver) | — |
| E1 | — **WAIVED** 2026-10-15 | content-task7 · PR into a module you don't own | — | — | — | — | — | — | — | Instructor: not required (class waiver — no cross-team commits) | — |
| E2 | [#48](https://github.com/ruvebal/ttod/pull/48) **MERGED** 2026-10-08 | graph-task1 · `graph-task1-fetch-from-api` | 25 | 24 | 20 | 10 | 10 | 9 | **98** | MERGED | — |
| E2 | [#52](https://github.com/ruvebal/ttod/pull/52) **MERGED** 2026-10-14 | graph-task2 · `graph-task2-accessible-node-selection` | 24 | 24 | 18 | 10 | 10 | 9 | **95** | MERGED; spatial arrow focus nav | — |
| E2 | [#55](https://github.com/ruvebal/ttod/pull/55) **MERGED** 2026-10-14 | graph-task3 · `graph-task3-task-filter-interaction` | 24 | 25 | 18 | 9 | 10 | 9 | **95** | MERGED; preserve selection across filter | — |
| E2 | [#71](https://github.com/ruvebal/ttod/pull/71) **MERGED** 2026-10-14 | graph-task4 · `graph-task4-url-state-selection` | 25 | 24 | 20 | 9 | 10 | 9 | **97** | MERGED; `urlState.ts` + deep-link e2e | — |
| E2 | [#75](https://github.com/ruvebal/ttod/pull/75) **MERGED** 2026-10-14 | graph-task5 · `graph-task5-layout-and-performance` | 24 | 22 | 18 | 10 | 10 | 9 | **93** | MERGED; O(n) section grouping + scale e2e (no DevTools shots) | — |
| E2 | [#76](https://github.com/ruvebal/ttod/pull/76) **MERGED** 2026-10-14 | graph-task6 · `graph-task6-keyboard-operabililty` | 24 | 24 | 18 | 10 | 10 | 9 | **95** | MERGED; `focusable` + focus-visible + keyboard e2e | — |
| E2 | [#77](https://github.com/ruvebal/ttod/pull/77) **MERGED** 2026-10-15 | graph-task7 · `graph-task7-graph-island-tests` | 24 | 24 | 20 | 10 | 10 | 9 | **97** | MERGED; GraphIsland component test (+ early index tag pills) | — |
| E2 | [#78](https://github.com/ruvebal/ttod/pull/78) **MERGED** 2026-10-15 | graph-task8 · `graph-task8-pr-into-different-module` | 24 | 24 | 18 | 9 | 10 | 9 | **94** | MERGED; related-wisdom links on detail (cross-module) | — |
| E2 | — **WAIVED** 2026-10-15 | graph-task9 · formal review of another team's PR | — | — | — | — | — | — | — | Instructor: not required (class waiver) | — |
| E2 | — **NO TIP PR** | graph-task10 · design-decision doc for defense | — | — | — | — | — | — | — | No tip PR filed (oral-only if any) | — |
| E3 | [#44](https://github.com/ruvebal/ttod/pull/44) **CLOSED** 2026-10-13 | oracle-task1 · `oracle-task1-streamed-response-rendering` | 24 | 24 | 18 | 9 | 10 | 8 | **93** | CLOSED superseded by #42 (Task 1 on main via cumulative) | — |
| E3 | [#45](https://github.com/ruvebal/ttod/pull/45) **CLOSED** 2026-10-13 | oracle-task2 · `oracle-task2-live-region-announcement` | 24 | 24 | 18 | 10 | 10 | 8 | **94** | CLOSED superseded by #42 | — |
| E3 | [#38](https://github.com/ruvebal/ttod/pull/38) **CLOSED** 2026-10-13 | oracle-task3 · `oracle-task3-grounded-creative-disclosure` | 24 | 24 | 18 | 10 | 10 | 8 | **94** | CLOSED superseded by #42 | — |
| E3 | [#39](https://github.com/ruvebal/ttod/pull/39) **CLOSED** 2026-10-13 | oracle-task4 · `oracle-task4-session-history` | 24 | 24 | 18 | 9 | 10 | 8 | **93** | CLOSED superseded by #42 | — |
| E3 | [#40](https://github.com/ruvebal/ttod/pull/40) **CLOSED** 2026-10-13 | oracle-task5 · `oracle-task5-preparing-state` | 24 | 24 | 18 | 9 | 10 | 8 | **93** | CLOSED superseded by #42 | — |
| E3 | [#41](https://github.com/ruvebal/ttod/pull/41) **CLOSED** 2026-10-13 | oracle-task6 · `oracle-task6-recovery-error-state` | 24 | 24 | 18 | 9 | 10 | 8 | **93** | CLOSED superseded by #42 | — |
| E3 | [#42](https://github.com/ruvebal/ttod/pull/42) **MERGED** 2026-10-11 | oracle-task7 · `oracle-task7-unit-component-tests` | 25 | 25 | 20 | 10 | 10 | 10 | **100** | MERGED; **cumulative Tasks 1–7** (stack explicitly on 1–6) | — |
| E3 | — **WAIVED** 2026-10-15 | oracle-task9 · formal review of another team's PR | — | — | — | — | — | — | — | Instructor: not required (class waiver) | — |
| E3 | — **WAIVED** 2026-10-15 | oracle-task8 · PR into a module you don't own | — | — | — | — | — | — | — | Instructor: not required (class waiver — no cross-team commits) | — |
| E4 | [#37](https://github.com/ruvebal/ttod/pull/37) **CLOSED** | pwa-task1-bad · `main` | — | — | — | — | — | — | — | CLOSED; superseded by #51 | — |
| E4 | [#51](https://github.com/ruvebal/ttod/pull/51) **MERGED** 2026-10-08 | pwa-task1 · `pwa-task1-service-worker` | 24 | 24 | 20 | 10 | 10 | 9 | **97** | MERGED | — |
| E4 | [#46](https://github.com/ruvebal/ttod/pull/46) **MERGED** 2026-10-11 | pwa-task2 · `pwa-task2-offline-oracle` | 24 | 24 | 18 | 10 | 10 | 9 | **95** | MERGED | — |
| E4 | [#47](https://github.com/ruvebal/ttod/pull/47) **MERGED** 2026-10-11 | pwa-task3 · `pwa-task3-cache-policies` | 24 | 24 | 18 | 10 | 10 | 9 | **95** | MERGED | — |
| E4 | [#49](https://github.com/ruvebal/ttod/pull/49) **MERGED** 2026-10-12 | pwa-task4 · `pwa-task4-offline-queue` | 25 | 25 | 18 | 9 | 10 | 9 | **96** | MERGED; flush-on-online | — |
| E4 | [#50](https://github.com/ruvebal/ttod/pull/50) **MERGED** 2026-10-12 | pwa-task5 · `pwa-task5-install-quality` | 24 | 24 | 16 | 10 | 10 | 10 | **94** | MERGED; Brave install evidence | — |
| E4 | [#60](https://github.com/ruvebal/ttod/pull/60) **MERGED** 2026-10-11 | pwa-task6 · `pwa-task6-performance` | 25 | 25 | 18 | 10 | 10 | 10 | **98** | MERGED; LCP budget | — |
| E4 | [#69](https://github.com/ruvebal/ttod/pull/69) **MERGED** 2026-10-12 | pwa-task7 · `pwa-task7-offline-tests` | 24 | 24 | 20 | 10 | 10 | 9 | **97** | MERGED; db.test + Page.test | — |
| E4 | [#74](https://github.com/ruvebal/ttod/pull/74) **MERGED** 2026-10-13 | docs(pwa) · `docs/team-4-ai-use` | 25 | 24 | 16 | 10 | 10 | 10 | **95** | MERGED; `docs/uso-ia-team-4.md` AI-use memo (rejected `tsc` drop) | — |
| E4 | — **WAIVED** 2026-10-15 | pwa-task9 · formal review of another team's PR | — | — | — | — | — | — | — | Instructor: not required (class waiver) | — |
| E4 | — **WAIVED** 2026-10-15 | pwa-task8 · PR into a module you don't own | — | — | — | — | — | — | — | Instructor: not required (class waiver — no cross-team commits) | — |
| E5 | [#31](https://github.com/ruvebal/ttod/pull/31)–[#35](https://github.com/ruvebal/ttod/pull/35) **CLOSED** | accounts-task1–5 old | — | — | — | — | — | — | — | CLOSED; replaced by #53/#58/#57/#72/#56 | — |
| E5 | [#53](https://github.com/ruvebal/ttod/pull/53) **MERGED** 2026-10-13 | accounts-task1 · `accounts-task1-ssr-auth` | 24 | 24 | 16 | 8 | 10 | 9 | **91** | MERGED; empty login reject + `requireUser` | — |
| E5 | [#58](https://github.com/ruvebal/ttod/pull/58) **MERGED** 2026-10-13 | accounts-task2 · `accounts-task2-personal-library` | 24 | 24 | 16 | 9 | 10 | 9 | **92** | MERGED; FavoriteButton on detail only | — |
| E5 | [#57](https://github.com/ruvebal/ttod/pull/57) **MERGED** 2026-10-13 | accounts-task3 · `accounts-task3-proposal-endpoint` | 25 | 24 | 16 | 8 | 10 | 9 | **92** | MERGED; server origin/author + ProposalStore | — |
| E5 | [#72](https://github.com/ruvebal/ttod/pull/72) **MERGED** 2026-10-13 | accounts-task4 · `accounts-task4-review-pipeline` | 24 | 24 | 14 | 8 | 10 | 9 | **89** | MERGED; reviewer role gate | — |
| E5 | [#56](https://github.com/ruvebal/ttod/pull/56) **MERGED** 2026-10-13 | accounts-task5 · `accounts-task5-public-pat` | 25 | 24 | 18 | 8 | 10 | 9 | **94** | MERGED; Bearer PAT only on /wisdom/random | — |
| E5 | [#73](https://github.com/ruvebal/ttod/pull/73) **MERGED** 2026-10-11 | accounts-task6 · `accounts-task6-api-guide` | 24 | 24 | 16 | 8 | 10 | 9 | **91** | MERGED; API guide EN/ES + api_client | — |
| E5 | [#59](https://github.com/ruvebal/ttod/pull/59) **MERGED** 2026-10-11 | accounts-task7 · `accounts-task7-auth-library-api-tests` | 24 | 24 | 20 | 8 | 10 | 9 | **95** | MERGED; feature-organized tests + npm test in CI | — |
| E5 | — **WAIVED** 2026-10-15 | accounts-task9 · formal review of another team's PR | — | — | — | — | — | — | — | Instructor: not required (class waiver) | — |
| E5 | — **WAIVED** 2026-10-15 | accounts-task8 · PR into a module you don't own | — | — | — | — | — | — | — | Instructor: not required (class waiver — no cross-team commits) | — |

---

## Group rollup (scored PRs only)

| Group | Scored n | Mean Σ | Median Σ | Notes |
| --- | ---: | ---: | ---: | --- |
| E1 Content | 8 | 96 | 98 | #43+#61–#68 merged; Tasks 7–8 waived |
| E2 Graph | 8 | 96 | 95 | Tasks 1–8 merged (#78 scored); Task 9 waived; Task 10 no tip PR |
| E3 Oracle | 7 | 94 | 93 | **seam complete** (#42); Tasks 8–9 waived; Task 10 no tip PR |
| E4 PWA | 8 | 96 | 96 | **seam complete** (+ #74); Tasks 8–9 waived; Task 10 no tip PR |
| E5 Accounts | 7 | 92 | 92 | **seam complete**; Tasks 8–9 waived; Task 10 no tip PR |

---

## Remaining (non-PR)

All student tip PRs that were filed are merged. Design-decision Task 10 for Graph / Oracle / PWA / Accounts has **no tip PR** in this repo (Content T9 = #68). Waived process tips stay waived.

Instructor Update branch / conflict resolve is merge hygiene — not a student reject reason.

### Waiver note (2026-10-15)

Professor told the cohort that tips requiring either (a) a **formal review of another team's PR**, or (b) a **PR / commits into another team's module**, are **not required**.

| Kind | Tips waived |
| --- | --- |
| Formal peer-PR review | Content 8 · Graph 9 · Oracle 9 · PWA 9 · Accounts 9 |
| Cross-team code PR | Content 7 · Graph 8* · Oracle 8 · PWA 8 · Accounts 8 |

\*Graph Task 8 already **MERGED** as #78 — score stands; waiver only excuses teams that never filed.

### Oracle note (2026-10-13)

Per-task PRs #44/#45/#38/#39/#40/#41 looked unmergeable (`DIRTY` / `CHANGES_REQUESTED`) only as stale branches. Product work for Tasks 1–6 was already on `main` via #42’s stacked commits. Closed as superseded; scores credit the work that shipped.

---

## Companion CSV

[`COHORT-PR-SCORECARD-2026-10-07.csv`](./COHORT-PR-SCORECARD-2026-10-07.csv) (rewritten same snapshot).

_Updated: 2026-10-17 — Content #65/#67/#68 scored MERGED; 0 open student tip PRs._
