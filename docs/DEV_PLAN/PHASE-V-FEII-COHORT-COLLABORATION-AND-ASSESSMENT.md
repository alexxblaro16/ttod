# Phase V — FE II Cohort Collaboration, PR Workflow & Assessment Rubric

**Status:** ACTIVE — the plan is complete and its own prerequisite gate (§1) is green. Week 1
starts 2026-09-10. Three genuinely open items remain, all professor-only decisions with no
engineering dependency (§10: rubric point totals, research framing, the early-finisher policy) —
everything else this document originally gated on has since executed and is verified (§1).

**Owner:** `@crea-comm.net` teaching studio (professor as product owner)

**Depends on:** Phase U reaching TS4 (now TS4c) before Week 1 — **satisfied**, see §1 for evidence.
Also depends on Phase R's frozen R6 boundary (`DECISIONS/R6-DEFERRED-STUDENT-OWNED.md`, refined by
`DECISIONS/U0-2026-09-07-TEACHING-SKELETON-BOUNDARY.md`) — unaffected, still holds.

**Does not authorize:** treating this course activity as an *already cleared* empirical study
ready for publishable analysis (see `docs/research/ethics/` — protocol under ethics review;
Strand B analysis still gated), any Scaleway deployment or production-secret exposure to students, canonical `ttod.yml`
mutation by students, or course-repository edits (that remains Phase U's TS8 gate).

---

## 0.α Second-pass revision (this session) — what changed and why

Five corrections landed after the first draft, from direct product-owner feedback:

1. **Timeline is tighter than "Week 7."** The curriculum's own Units 1–7 pacing *is* the
   development calendar — there is no separate multi-month runway. Two sessions are already
   spent. See new §8.5.
2. **Agentic coding speed is a real threat to the pedagogy, not a hypothetical.** A student can
   plausibly one-shot a correctly-described module in "a couple of prompts" with a capable coding
   agent — the rubric must be designed assuming this happens, not assuming five weeks of organic
   struggle. See new §8.6.
3. **A sixth module, genuinely new (not a Phase R reduction): Auth, favorites library, and
   logged-in quote proposals**, grounded in FE I's own two authentication lessons so the cohort
   builds on curriculum they already have. See new §2.5, and its Week-0 seam:
   [`PHASES/U-TS4c-auth-hello-world.md`](PHASES/U-TS4c-auth-hello-world.md).
4. **A public, token-authenticated API surface plus a minimal external "bot" client** that proves
   the API works outside the browser — see new §2.6.
5. **The actual cohort is 8 students, not 10** — §2's table and the pairing math below are
   corrected for this.

**Two companion documents, also new this revision:**
[`PHASE-V-PRODUCT-BACKLOG-AND-JOURNEYS.md`](PHASE-V-PRODUCT-BACKLOG-AND-JOURNEYS.md) — this
document (§2 especially) says *how* engineering work is organized; that one says *why and for
whom*: personas, five user-journey diagrams, a full epics/stories backlog (MoSCoW-prioritized,
traceable back to §2's modules), and an explicit accessibility-as-philosophy section answering
what was previously only implicit in scattered `a11y`/`accessib` acceptance-criteria lines across
this dev plan. [`PHASE-V-SPRINT-SESSIONS-AND-METHODOLOGY.md`](PHASE-V-SPRINT-SESSIONS-AND-METHODOLOGY.md)
— says *when*: §8.5 below gives week-sized sprint boundaries, that document breaks each week into
its real class sessions (grounded in FE II's actual per-session Duration/Lab-Hours data, not
assumed) and makes explicit the theory → team-meeting → lab-time rhythm every session runs, with a
task pull-list per session sourced from the backlog document's epics.

Everything below this point is the original document, revised in place; §0 (below) and §1–§10
are the first-pass reasoning this revision builds on, not replaced by it.

## 0.β Completion pass (2026-09-09, later the same day) — the gate closed

Between the second-pass revision above and this pass, Phase U's Week-0 actually executed — seven
lanes, cold-audited independently rather than taken on faith (§1 now carries the evidence, not a
projection). This pass closes the document out accordingly: the header status moved from PROPOSED
to ACTIVE, §1's prerequisite gate is rewritten from "must be true" to "verified true, here's how,"
and §10 dropped from five open questions to three — the two that were really about *whether Week-0
would happen* are closed, the three that remain are pedagogical/administrative calls with no
engineering dependency, safe to leave until they're actually load-bearing (grading time, not
Week 1). Nothing in §§2–9's actual plan content changed — this pass is status and evidence, not a
third redesign.

---

## 0. What this document reconciles

The professor supplied a first-draft assignment plan: five domain modules, ten students in
pairs, isolated feature branches into one shared repository, a PR-review workflow, and a request
to frame the term as a "production engineering simulator." Two corrections were requested before
conversion into a plan: the PWA/service-worker seam was missing from the draft, and the task
model should let every student touch every domain, not just their own silo.

Both corrections turn out to already have frozen answers in this repository, from a plan the
draft's author (an external AI, working from the codebase name alone) had no visibility into:

- **The five domain modules are not new — they are Phase U's "five seams."** `PHASE-U-FEII-TEACHING-SKELETON-CASCADE.md` §0 already names them: **R3b** (Astro content/i18n), **R4**
  (Svelte graph island), **R5** (React Oracle island), **R6** (PWA/front-end operations), **R7**
  (testing, continuous/cross-cutting). The PWA seam the draft was missing is R6 — it already has
  a full engineering runbook (`PHASES/R6-pwa-cicd-audit.md`), just scoped for the rich instructor
  reference, not FE II Deliverable 1. §2 below re-scopes it down.
- **"Everyone learns every field" already has a designed mechanism — it just isn't a rotation.**
  Phase U's own calendar (§6) ends every unit block at a **Week 7 gate: "run integrated local
  product and oral/diff review."** R7 (testing) is explicitly documented as *continuous,
  cross-cutting, pairs with every lane as it lands* — not a sixth isolated silo. Between the
  defense (which requires whole-system fluency) and testing/review being woven through every
  module rather than boxed into one team, breadth-of-understanding is already the design intent.
  §3 operationalizes it into concrete, gradable requirements instead of leaving it as an
  aspiration.

This document does **not** reopen or contradict Phase U, R6's deferral, or the official FE II
grading scheme (`how-to-pass-this-track`). It operationalizes a gap between them: Phase U designs
*what students build*; nothing yet specifies *how a shared-repository PR workflow is run,
evaluated, and defended*. That is this document's job.

---

## 1. Prerequisite gate — GREEN, verified 2026-09-09

**Status when this section was first written:** Phase U was PROPOSED, TS0 VERIFYING, TS1–TS8
BLOCKED — the five hello-world seams this plan assigns students to extend did not exist as a
buildable artifact. **That is no longer true.** All seven lanes (TS1 plus the new TS4c) executed
2026-09-09, each independently cold-audited against the live repo (not just claimed) before Week 1:

| Gate | What it means | Evidence |
| --- | --- | --- |
| TS1 frozen | Subtraction contract exists for all six seams | `PHASE-U-TS1-REPORT.md` — subtraction table grounded live; `domain.ts` frozen at 67 lines on `skeleton/ts1-contracts` |
| TS3 done | R3b/R4/R5 reduced to hello-world depth, each with its own `ASSIGNMENT.md` | `skeleton/ts3a-r3b` (`955198fc`), `skeleton/ts3b-r4` (`bfea9da7`), `skeleton/ts3c-r5` (`5a16a98f`) — facet-route cuts, GSAP/filter cuts, and offline-queue/propose cuts all independently verified live, not just claimed |
| TS4 done | R6/R7 hello-world seams added, TS4c (Auth) built new | `skeleton/ts4a-r6` (`4b2db64e`, `sw.js`+manifest), `skeleton/ts4b-r7` (`bcdd5438`, four test layers), `skeleton/ts4c-auth` (`445f3257`, `auth.py`+`User`/`FavoriteEntry` types) |
| Shared contract published | `src/types/domain.ts` exists on the baseline branch students fork from | Frozen on `skeleton/ts1-contracts`; every TS3/TS4 lane forks from that branch, not `main` |
| CI skeleton live | Lint/build gate and branch protection on the repo students will PR into | [PR #1](https://github.com/ruvebal/ttod/pull/1) `typecheck-and-build` green; branch protection on `main` confirmed live via `gh api` (1 review + required check, no force-push) |

**The three leftovers named above are now resolved**, not just tracked — `PHASE-U-TS5-REPORT.md`
(status `PARTIAL`, `skeleton/ts5-hello-world`, all seven lane tips merge-assembled cleanly) records
the actual decisions: TS4c's `User`/`FavoriteEntry`/`UserRole` types **accepted** into the frozen
contract; the 460-node graph **deliberately left uncapped** — performance is R4's assignment
depth, not a bug to fix in the skeleton; `OracleTerminal.test.tsx` **rewritten** for hello-world
depth, the queue/propose assertions removed rather than papered over. TS5 itself remains `PARTIAL`
— fresh orphan history, the privacy watcher, and the TS2 rich-reference tag are still open, and
`main` was not touched by any of it — but the specific leftovers this document once deferred to
TS5 are closed.

**Two infra bugs found and fixed in the same pass** (`PHASE-U-TS1-REPORT.md` §5's addenda): the
required `typecheck-and-build` check didn't exist on `main` at all, and once added, its
`pull_request` trigger was path-filtered — either gap would have silently blocked *any* future PR
into `main` from merging. Both fixed; confirmed live on two independent PRs.

**The plan each lane executed against** (for reference — this is now historical, not pending):
one sequential contract-freezing lane
([`PHASES/U-TS1-subtraction-and-contracts.md`](PHASES/U-TS1-subtraction-and-contracts.md)) and six
lane runbooks delegated in parallel once TS1 went green
([`PHASES/U-TS3a-r3b-content-hello-world.md`](PHASES/U-TS3a-r3b-content-hello-world.md),
[`U-TS3b-r4-graph-hello-world.md`](PHASES/U-TS3b-r4-graph-hello-world.md),
[`U-TS3c-r5-oracle-hello-world.md`](PHASES/U-TS3c-r5-oracle-hello-world.md),
[`U-TS4a-r6-pwa-hello-world.md`](PHASES/U-TS4a-r6-pwa-hello-world.md),
[`U-TS4b-r7-testing-hello-world.md`](PHASES/U-TS4b-r7-testing-hello-world.md),
[`U-TS4c-auth-hello-world.md`](PHASES/U-TS4c-auth-hello-world.md) — the new Auth module, §2.5,
the one lane with no existing code to reduce and the only one permitted to touch
`services/backend/**`). Each runbook's own report (`PHASE-U-TS*-REPORT.md`) is the actual evidence
cited in the table above, not the runbook's prose. **Delegation note:** the orchestration's own §5
answer asked for local Ollama `qwen3.8:27b` where possible; in practice the six lanes ran as
Cursor agent sessions (the tooling available at execution time could not target Ollama directly) —
worth recording honestly rather than silently letting the plan's stated intent stand as if it
were what happened.

**One re-scoping this document makes to R6 specifically:** `PHASES/R6-pwa-cicd-audit.md` as
written targets the *rich instructor reference* — it includes a Scaleway `stg` deploy workflow,
real API tokens, and a signed deploy-decision record. **None of that belongs in the student
artifact.** Per that same document's own §2.4, production secrets are "instructor-only, never
distributed" — students' R6 module is the PWA/offline half plus a *local* CI workflow (lint,
typecheck, unit/component tests, Playwright), never the deploy job. §2 below reflects this.

---

## 2. The six modules — corrected assignment table

Search & filter (the draft's module 04) is folded into the content module rather than kept
separate: the reference build already implements it as Astro dynamic routes
(`wisdom/sections/[section].astro`, `wisdom/tags/[tag].astro`, `wisdom/levels/[level].astro`) —
it is the content domain, not its own seam, and Phase U never names it as a separate lane. Auth
(§2.5–§2.6, TS4c) *is* a genuine sixth seam — the one module with no existing reference to reduce.
Testing/performance/a11y is reframed from an isolated team into a cross-cutting role (see §3)
while still anchoring the shared CI workflow's ownership, matching R7's and R6's documented split
("R6 owns CI orchestration, R7 owns what tests actually assert").

| # | Module (Phase U seam) | Framework | Task & responsibilities | Interface contract | Curriculum unit | Team |
| - | --- | --- | --- | --- | --- | --- |
| 01 | Wisdom Content, i18n, Search/Filter & Proposals UI (**R3b**) | Astro (zero-JS) | Static/dynamic routes (`/wisdom/[id]`), mandatory `es`+`en` routing, content collections, section/tag/level filters, breadcrumbs; the logged-in "propose a quote" form (§2.5) lives here, since it's a content-authoring surface | Astro Content Collections schema (Zod) + `WisdomEntry` from `domain.ts` | U2–U3 | **Pair** (2) |
| 02 | Knowledge Graph (**R4**) | Svelte + GSAP | Interactive SVG node/edge graph: click, drag, selection reflected in accessible text | `fetch('/api/v1/graph')` → `{ nodes: [], links: [] }` | U3 | **Solo** (1) |
| 03 | Oracle Terminal (**R5**) | React | Streamed chat UI over SSE: grounded/creative mode, cited-quote path, blinking cursor, history | `POST /api/v1/oracle/stream` → SSE chunks | U3 | **Pair** (2) |
| 04 | PWA & Local Operations (**R6**, re-scoped — no deploy) | Service worker + Compose | `public/sw.js` (Cache-First static / Network-First `/api/*`), install manifest, offline queue flush, one observable offline boundary | Extends the existing `OfflineLogEntry` shape | U4 | **Solo** (1) |
| 05 | Auth, Favorites Library & the Public API (**new**, §2.5–§2.6) | FastAPI + Astro SSR | Login/session (cookie) + bearer tokens, favorites CRUD, the API docs page, the bot test app | `User`/`FavoriteEntry` in `domain.ts`; `Authorization: Bearer` on `/api/v1/*` | *reuses FE I's auth lessons; U4 (operations framing)* | **Pair** (2) |

Testing/performance/a11y (**R7**) is **not** a sixth team this revision — with 8 students and a
new module to fit, the cleanest allocation drops the dedicated testing pair and keeps R7's
already-continuous, cross-cutting design as *everyone's* responsibility (§3), enforced by the
rubric's test-coverage line (§5) and the defense (§6) rather than by a dedicated owner. This is
not a downgrade: R7's own runbook already says testing "pairs with each lane owner as their
feature lands," never that it needs a dedicated team.

**8 students → 2+1+2+1+2 = 8.** Pairs go to the three richest, most contract-heavy modules
(content/proposals, oracle, auth); solos go to the two most bounded ones (graph, PWA — both
already scoped by their Week-0 runbooks to a small, well-defined hello-world reduction, which is
exactly what makes a single owner realistic). If your actual roster differs, keep the module
boundaries fixed and resize the pair/solo split, not the module count.

---

## 2.5 Backlog — auth, a personal favorites library, and logged-in proposals

Grounded in FE I's own two authentication lessons (`react-authentication` and
`react-framework-mode-auth-i18n`) — not a new pattern, the *next* one the cohort already has
fresh. The Week-0 seam is [`PHASES/U-TS4c-auth-hello-world.md`](PHASES/U-TS4c-auth-hello-world.md);
this section is the *assignment-depth* backlog Module 05 builds on top of that seam.

**Two credential surfaces, reused deliberately from FE I's own client↔server mapping table:**

| Surface | Pattern | Used by |
| --- | --- | --- |
| Session cookie (httpOnly, signed) | FE I's *Framework Mode* pattern — verified server-side in Astro frontmatter before any HTML is sent, no flash of protected content | TTOD's own pages: `/library`, `/propose` |
| Bearer token ("personal access token") | FE I's *Declarative Mode* pattern — `Authorization` header, no cookie needed | The public API (§2.6) and the bot test app — anything that isn't a browser session |

**Backlog items:**

1. **Personal favorites library.** A logged-in user can save/remove quotes to a personal list and
   view it at `/[locale]/library`. New backend store — favorites are per-user preference data, not
   canonical quote data, so they do **not** live in `ttod.yml`; a small dedicated store (mirroring
   the existing `services/backend/data/proposals/` pattern already named in `AGENTS.md`'s
   `TTOD_PROPOSAL_DIR`) keeps this cleanly separate from the governed corpus.
2. **Propose a quote while logged in.** A web form at `/[locale]/propose`, gated by
   `requireUser()`. Submitting it calls `ttod_core.proposals.create_proposal(...)` — the *exact*
   existing primitive `cli.py proposal create` already uses — with `proposer_kind='human'` and
   `proposer_id=<the logged-in user's id>`. **This reuses 100% of the existing proposal
   infrastructure; it adds a web front door to it, it does not build a parallel one.** What
   happens to that proposal next is §2.7's job.
3. **Role-gated reviewer view** (stretch, pairs well with FE I's `RoleGuard`/`requireRole`
   lesson content): a `/[locale]/review` page visible only to `role: 'reviewer'` users, listing
   open proposals — a thin UI over data the CLI can already produce, not a new review engine.

## 2.6 The public API, bearer-token auth, and the bot test app

**Every `/api/v1/*` route this module adds or fronts requires `Authorization: Bearer <token>`** —
including reads. This is a deliberate teaching choice, not a technical requirement of the existing
read endpoints (`/api/v1/wisdom/sample`, `/api/v1/graph` stay open for the SSR app itself, which
already trusts its own backend call) — the *public-facing* API surface this module documents is
where token auth is enforced, so students experience the full request lifecycle FE I's lesson
diagrams: obtain a token while logged in → send it → get verified → get data.

1. **`GET /api/v1/wisdom/random`** (new, bearer-required) — returns one random accepted
   `WisdomEntry`. Small, real, and the natural target for a demo client.
2. **API documentation page**, `/[locale]/api-docs` (Astro, static) — generated from the same
   `domain.ts` shapes already governing every other module (dogfooding "types are the contract"
   one more time): endpoint list, required header, example request/response, and a "get your
   token" link to the account page TS4c's seam already builds.
3. **The bot test app** — a small, *separate* script (e.g. `examples/quote-bot/index.mjs`, plain
   Node, no framework) that takes a token as an environment variable, calls
   `GET /api/v1/wisdom/random` with it, and prints the quote. This is the assignment's proof that
   the API genuinely works outside the browser — a student who can only demo it through their own
   web UI has not actually shown the API is an API. Keep it deliberately small; this is a
   five-minute script, not a second application.

## 2.7 CI/CD for community proposals — a GitHub reaction, not an email

Answering directly: **the web form should not write straight into the tracked `proposals/`
directory from a running server process** (that directory is version-controlled precisely so every
proposal has a reviewable diff and an audit trail — a live server writing to it directly bypasses
both). Instead, reuse GitHub's own review UI, which students are already using for every other
module's PRs (§4) — one mechanism, one set of skills, for both "review my code" and "review this
quote":

```text
Logged-in user submits /propose
        │
        ▼
Backend calls ttod_core.proposals.create_proposal(...)          (existing primitive — unchanged)
        │
        ▼
Backend opens a branch + commits the proposal JSON under
proposals/, opens a PR: "Proposal: <section> — <text excerpt>"   (new: a small bot step)
        │
        ▼
A human reviewer sees it in GitHub's own PR queue — comments,
requests changes, or approves. No email system to build.
        │
        ▼
On PR **approval** (not merge — approval is the unambiguous human
signal), a GitHub Action runs:
  cli.py proposal accept --reviewer-id <the approver's GitHub login>
                                                                   (only this step touches ttod.yml)
        │
        ▼
The Action pushes the resulting ttod.yml diff onto the SAME PR —
which predictably clears the approval (branch protection dismisses
stale reviews). That is not a bug to route around: it separates
"I approve this proposal" from "I approve this exact canonical
diff." A second, human approval + merge click is what actually
lands it in ttod.yml.
```

**Implemented, not just designed** — [`.github/workflows/proposal-accept.yml`](../../.github/workflows/proposal-accept.yml).
Built and reasoned through against this repo's *real* branch protection (required review +
`dismiss_stale_reviews: true`), which made the original "auto-merge once `accept` exits 0" sketch
above unworkable as literally written: a bot push after approval clears that same approval, so
nothing can auto-merge without either re-approving itself (no) or bypassing protection (worse).
The two-touchpoint design converts that constraint into the safety property `AGENTS.md` already
wants — a human approves the *diff* that actually writes `ttod.yml`, not just the original
proposal text — without any bypass or elevated token.

**Why approval, not merge, is the trigger:** merging is sometimes a maintenance action performed
by someone other than the reviewer (rebasing, batching); *approval* is the unambiguous "a named
human accepted this" event `AGENTS.md`'s own rule requires (`--reviewer-id` must name a real
person). If your workflow prefers merge-as-trigger instead, that is a one-line change to the
Action's trigger event — flag your preference and I will build whichever you choose.

**What this does not change:** `cli.py proposal accept` remains the only command that ever writes
`ttod.yml`, running in CI under the repo-scoped `GITHUB_TOKEN` (never a student's own credentials,
never a PAT), and only ever computes a diff — a human's own merge click is what lands it. Students'
own module PRs (§4/§5) and this quote-proposal pipeline share the review *mechanism* (GitHub PRs)
but never the write *authority*.

**Team ownership:** this pipeline is Module 05's (Auth) build, since it is the module that already
owns the backend proposal-submission endpoint — but it is explicitly one of the required
cross-module contributions (§3 item 2) for whichever pair does not own it, since it touches CI
(Module 04's territory) and the review UX every other module's PRs also use.

### The rest of the agentic pack

Built alongside the proposal-accept workflow, same session, all reusing infrastructure already
specified elsewhere in this document rather than inventing new criteria:

- [`.github/pull_request_template.md`](../../.github/pull_request_template.md) — the student-side
  routine, a direct checklist form of §5's PR rubric (contract adherence, acceptance criteria, test
  coverage, the backlog doc's accessibility Definition of Done, Unit 6's AI Review Log) — nothing
  on it that wasn't already graded, just checkable per-PR instead of only at the end.
- [`scripts/gh-review-queue.sh`](../../scripts/gh-review-queue.sh) — professor-side, read-only:
  lists PRs awaiting your review, proposal PRs specifically, and everything else open, via `gh pr
  list`. Never merges, approves, or comments.
- **GitHub Projects (the sprint doc's §4 recommended board): blocked, not built.** The
  authenticated `gh` token here lacks the `project` scope — `gh auth refresh -s project` is an
  interactive device-code flow only you can complete. Once refreshed, the board is a `gh project
  create` plus the four columns (Backlog / This Session / In Review / Done) the sprint doc already
  specifies — justified (the backlog doc already has ~20 ready stories to seed it), just not
  something this session could finish unattended.

---

## 3. Assignment model — depth *and* breadth, made gradable

Fixed 2-per-module ownership alone would reproduce exactly the silo problem you flagged. Three
concrete, gradable mechanisms close it — none require literal rotation through all five modules,
which a single ~6-week Entrega-1 window does not comfortably fit:

1. **Primary ownership (depth).** Each pair owns one module's PRs — this is where their deepest,
   most-graded work lives.
2. **Cross-module contribution (breadth, PR-level).** Every pair must open **at least one** PR
   into a module they do not own — a real fix or small enhancement, not a drive-by typo commit —
   and complete **at least one** formal review (using the module's interface contract as the
   review checklist) on a PR outside their own module. This is graded as process evidence (§5),
   not extra credit.
3. **Testing pairing (breadth, continuous).** Module 05's pair does not work in isolation writing
   their own separate feature — per R7's existing design, they pair with each other module's
   owners *as each feature lands*, co-authoring tests inside those modules' own PRs. This means
   every student sees at least one other module's code up close through review, not just theory.
4. **Oral defense (breadth, verified).** §6's defense rubric requires explaining the *whole*
   system's architecture (using the existing `ttod-feii-architecture` diagram as the shared
   reference artifact) and answering one examiner question about a module the student did not
   own. A student who can only explain their own silo does not pass this component — this is the
   actual enforcement mechanism, not the honor system.

---

## 4. Repository & PR guardrails

Adapting the professor's own three guardrails, reconciled with what already exists in this repo:

1. **Branch protection.** Block direct commits to the teaching-baseline `main`. Require ≥1
   approval and a passing CI check before merge. (`.github/workflows/public-docs-pages.yml`
   already demonstrates this repo's Actions conventions — the new student-facing workflow should
   follow the same style: explicit permissions, no inline secrets, path-scoped triggers.)
2. **`src/types/domain.ts` as the shared contract.** Publish before Week 1 (part of the TS1/TS3
   gate in §1), not "before assigning tasks on Tuesday" — the contract must predate the branches
   that depend on it, not arrive the same week. Every module's interface column in §2 traces back
   to a type in this file.
3. **Automated PR previews.** Vercel/Cloudflare/GitHub Pages preview-per-PR is a genuine
   force-multiplier for review load with 10 students — recommended as-is from the draft. This is
   independent of `docs/public`'s existing Pages lane (`U1-2026-09-07-PUBLIC-DOCS-PAGES-BOUNDARY.md`) and must not be confused with it: student app previews are ephemeral, PR-scoped,
   and ephemeral; the `docs/public` Pages deployment is the separate, already-decided
   documentation lane.
4. **No production secrets in student CI, ever.** Restated from R6's own §2.4: nothing a student
   PR triggers should need a real credential. The shared CI workflow (§2, module 05) runs
   build/lint/test only — no deploy job exists in the student artifact at all, so this can't be
   gotten wrong by omission.

---

## 5. PR evaluation rubric

Proposed 100-point scale per PR, scored by the professor or a designated peer reviewer against
the module's own interface contract and acceptance criteria (from that module's `ASSIGNMENT.md`,
produced during Phase U's TS3/TS4):

| Dimension | Points | What it checks |
| --- | --- | --- |
| Contract adherence | 25 | Uses the published `domain.ts` types / API shape exactly; does not invent a parallel shape |
| Correctness & acceptance criteria | 25 | The `ASSIGNMENT.md` acceptance tests pass; the feature does what the interface promises |
| Test coverage | 20 | Unit/component tests exist for the change (co-authored with module 05 where applicable); no untested new behavior |
| Accessibility | 10 | Semantic HTML, keyboard operation, visible focus, non-color cues — per the FE II shared baseline |
| CI green | 10 | Lint, typecheck, and the shared test workflow pass without a maintainer override |
| AI disclosure & process evidence | 10 | Unit 6's AI Review Log entry is present and honest (what was AI-assisted, what was human-verified) — reuse that unit's existing template and workflow verbatim, do not invent a parallel one |

A PR missing its AI Review Log entry is incomplete, not merely under-documented — Unit 6 already
frames this as due-at-Entrega-1 evidence, not optional metadata.

---

## 6. Oral defense rubric ("diff review")

This is the same event Phase U's calendar already names at the Week 7 gate ("run integrated
local product and oral/diff review") — this section gives it a gradable structure rather than
leaving it as a calendar label. Proposed 100-point scale, ~15 minutes per student:

| Dimension | Points | What it checks |
| --- | --- | --- |
| Own-module deep dive | 30 | Walks through their actual diff, explains a specific design decision and its alternative |
| Whole-system fluency | 30 | Uses the `ttod-feii-architecture` diagram (or draws it from memory) to explain where rendering, state, trust, and offline behavior live *outside* their own module |
| Cross-examination | 20 | Answers one examiner question about a module they did not own — the direct test of §3's breadth claim |
| Process evidence | 10 | Points to their AI Review Log, iteration history, and at least one rejected/revised AI suggestion they can explain why they rejected |
| Recovery under question | 10 | When wrong or uncertain, reasons visibly rather than guessing — "I'd check X" is a valid, gradable answer |

---

## 7. Weight mapping to the official FE II grading scheme

This rubric operates **inside** the already-frozen official weights from
`how-to-pass-this-track` (verified this session: **Entrega 1 — Astro Architecture, Units 2–6:
25% · Week 7**; **Mid-term, Units 1–7: 15% · Week 7**) — it does not add a new top-level
percentage line, and this document cannot change those official figures on its own.

**Proposed internal split** (yours to finalize in the official grading document, not mine to
set):

- Within Entrega 1's 25%: **PR contribution & process** (§5, aggregated across the term's PRs)
  ≈ 15 pts of the 25; **defense of own-module work** (§6, own-module dimension only) ≈ 10 pts.
- The Mid-term's 15% — already described as "declarative use of the system, defence of process,
  understanding of the code, not a black-box demo" — is naturally satisfied by §6's
  *whole-system fluency* and *cross-examination* dimensions. Recommendation: run one defense
  session that serves both lines rather than two separate exams, since the rubric content is the
  same check twice.

---

## 8. Curriculum alignment check (Units 1–7)

Verified against the actual lesson files, not assumed from unit titles:

- **Unit 1 (Kickoff)** — frontier/system-of-interfaces framing; no assignment content, sets up
  Weeks 2–7.
- **Units 2–3 (Astro)** — content collections, mandatory i18n routing, multi-framework
  integration: exactly module 01's scope.
- **Unit 4 (PWA/offline)** — Service Worker lifecycle, Cache-First/Network-First/
  Stale-While-Revalidate, Web App Manifest: exactly module 04's scope. This is the unit whose
  seam the original draft omitted.
- **Unit 5 (Testing strategy)** — Testing Trophy (not Pyramid), flakiness causes, CI wall-clock
  budget (**PR feedback under 5 minutes**, already specified verbatim in R6/R7's own runbooks —
  reuse this number, don't reinvent it), contract testing, accessibility-in-the-suite. Its own
  practice exercise is explicitly labeled "builds Entrega 1" — module 05 should teach directly
  from this lesson's CI workflow example rather than a generic template.
- **Unit 6 (AI-assisted code review)** — already ships a working `.github/workflows/ai-review.yml`
  pattern and an "AI Review Log — Entrega 1" template, with the explicit rule **the AI never
  approves or merges, only comments; a human approves.** §5's AI-disclosure line reuses this
  exactly. The lesson states outright: **"Entrega 1 is due here."**
- **Unit 7 (Performance)** — Core Web Vitals, bundle/asset optimization, performance budgets:
  module 05's Lighthouse and "measured performance change" requirement draws directly from this
  unit's content, consistent with the existing teaching-page claim that Unit 7 requires
  "measure before claiming."

No fabricated content was added beyond what these seven lesson files and the two official
grading/curriculum sources already establish.

## 8.5 The real calendar — recalibrated against the confirmed session cadence

`PHASE-U-WEEK0-ORCHESTRATION.md` §5 is now answered on disk: this orchestration is approved as
written, and **Week 1 of student collaboration starts 2026-09-10.** The exact session cadence is
also now confirmed, directly, superseding this section's earlier flat "five weeks" estimate:
**tomorrow's session runs 2h; every session from the following week onward is a strict single 4h
meeting per week — never two.** Recomputing the calendar against real per-unit hours
(`PHASE-V-SPRINT-SESSIONS-AND-METHODOLOGY.md` §1.5) against that constraint shows six units
(U2–U7) genuinely need **six weekly sessions, not five** — no two adjacent units fit inside one 4h
week, so the original Week-4 double-unit compression (U5+U6) isn't schedulable as this document
first assumed. Concretely:

| Session | Dates | Curriculum unit | What must be true by the end |
| --- | --- | --- | --- |
| 0 (now) | 2026-09-09 → 2026-09-10 | — | TS1 freezes contracts; TS3a/b/c + TS4a/b/**c** (the new auth lane) branches exist, hello-world depth confirmed |
| 1 (2h) | 2026-09-10 | U2 (Astro basics) | Teams formed (§2's 2+1+2+1+2), each pair/solo has opened their first draft PR against their own module |
| 2 (4h) | week of 09-17 | U3 (content/graph/oracle) | Modules 01–03 functionally working at assignment depth; module 05 (auth) has login/logout working end to end |
| 3 (4h) | week of 09-24 | U4 (PWA/offline) | Module 04 (PWA) working offline boundary; module 05's favorites library + propose form live |
| 4 (4h) | week of 10-01 | U5 (testing) | Every module has the R7/a11y test-coverage line (§5) satisfied |
| 5 (4h) | week of 10-08 | U6 (AI review) | §2.7's CI proposal pipeline is live end to end; **Entrega 1 checkpoint** (curriculum's own "Entrega 1 is due here") |
| 6 (4h) | week of 10-15 | U7 (performance — measure the built app) | Lighthouse pass, PR rubric complete, oral defense scheduled |
| Defense | week of 10-22 (TBD) | — | Oral "diff review" defense (§6) — a distinct event, not a content session |

**This revises the "five weeks, ending ~2026-10-15" framing from this section's first pass to six
content sessions plus a following defense week, ending closer to 2026-10-22.** The cause is the
confirmed cadence itself (strictly one session per week from Week 2 on rules out the double-session
compression this document originally proposed for Week 4), not scope creep — the module count and
content are unchanged. If reclaiming a week is preferred over accepting this extension, that's a
professor's calendar decision (options and trade-offs in
`PHASE-V-SPRINT-SESSIONS-AND-METHODOLOGY.md` §6 item 3), not one this document makes unilaterally.

**This table is the sprint boundary, not the session plan** — each row above is one actual class
meeting, running the theory → team-meeting → lab-time rhythm and pulling specific backlog stories;
see [`PHASE-V-SPRINT-SESSIONS-AND-METHODOLOGY.md`](PHASE-V-SPRINT-SESSIONS-AND-METHODOLOGY.md) §3
for that level of detail. §8.6 addresses the one force that could make this schedule easier than
it looks: students moving faster than the calendar assumes.

## 8.6 Designing against one-shot agentic completion

A real risk this cohort's tooling creates that the original draft did not anticipate: a student
using an agentic coding assistant can plausibly describe an entire module's requirements in a
prompt or two and get a working implementation back well inside Week 1 — the better-specified this
document makes each module (and it is now *very* well specified), the *easier* that one-shot path
becomes, not harder. Left unaddressed, that collapses five weeks of intended learning into one
sitting and defeats the pacing this whole document is built around. The rubric and process already
in this document are the actual defense — this section just names why and points back to them:

1. **The oral defense (§6) is the primary check, not the PR.** A one-shot AI-generated module can
   pass CI and look complete in a diff; it cannot survive "explain why you chose this file
   boundary" or "walk me through what happens when the token expires" from someone who never made
   those decisions. §6's rubric already scores understanding, not output — this revision changes
   nothing there, it just underlines that the defense is load-bearing *because* of this risk, not
   despite it.
2. **Multiple small PRs, not one large one (§4).** A student who lands a whole module in one PR
   after one prompt has an easy tell: no incremental history to defend. Require the module to land
   as a sequence of reviewable PRs across the weeks in §8.5's table — the AI-disclosure line (§5,
   from Unit 6's own template) already asks what was AI-generated per PR; a five-PR-in-one-day
   pattern with identical disclosure text across all five is itself a signal worth raising in the
   defense, not grounds for penalty on its own.
3. **The cross-module contribution requirement (§3 item 2) cannot be one-shotted by definition.**
   It requires a student to genuinely read and modify a teammate's code later in the timeline —
   an agentic tool can write module 03 quickly, but it cannot manufacture the Week-3/4 cross-module
   PR without the student actually engaging with code they did not originally write.
4. **Do not fight the tool — redirect the saved time.** If a pair genuinely finishes their module's
   baseline early via agentic assistance, that is not cheating; treat the freed time as budget for
   §3's breadth mechanisms (cross-module PRs, the CI/CD proposal pipeline in §2.7, deeper Unit 7
   performance work) rather than as time to stop. The rubric should reward *depth used*, not
   *hours spent* — a module finished in Week 2 with real Week 3–5 breadth contributions on top
   scores higher than one that trickles in at exactly rubric-minimum pace.

---

## 9. Research framing — Strand B under ethics review

The course activity is ordinary Front-End II pedagogy. **Strand B**
([`docs/research/STRAND-B-PEDAGOGICAL-DESIGN.md`](../research/STRAND-B-PEDAGOGICAL-DESIGN.md))
asks whether developer participation in this real, agentic-assisted cohort product can be a
learning activity with pedagogical outcomes (*learning by doing*). Philosophical Strand A is
parked and separate.

**"Students approved participating in the project"** covers pedagogical/project participation
(consent form item A). **Research consent** for secondary pseudonymized use of process artifacts
(item B) is separate — see [`docs/research/ethics/`](../research/ethics/). Templates live in the
repo; signed forms do not. Analysis of student work as research data remains gated on ethics
clearance, valid consent, and filing of relevant grades. Course grading never depends on
research participation.

What can happen now as ordinary engineering / teaching-design observation (not publishable
learning claims without protocol): PR iteration counts, CI failure counts, and per-PR performance
deltas already visible in GitHub history.

---

## 10. Open questions — three left, all yours, none engineering

**Closed since the last pass** (kept here for the record):

- **Week-0 timeline & execution.** Approved, dated (Week 1 = 2026-09-10), and *done* — all seven
  lanes executed and cold-audited (§1). Delegation happened via Cursor agent sessions rather than
  local Ollama, since the tooling at hand couldn't target it directly — noted honestly in §1
  rather than silently treating the plan's stated intent as what occurred.
- **Cohort size.** 8, not 10 — §2's 2+1+2+1+2 table.
- **CI trigger for §2.7's proposal pipeline.** Built as *approval*-triggered
  (`.github/workflows/proposal-accept.yml`), refined during implementation into a two-touchpoint
  design (§2.7) once GitHub's real `dismiss_stale_reviews` behavior ruled out literal auto-merge.
  If you'd still prefer merge-as-trigger over this two-approval flow, that's a real redesign now
  (not the one-line change it would have been before implementation) — flag it if so, otherwise
  this is decided.

**Still open — three items, no engineering dependency, safe to leave until they're actually
needed** (none block Week 1; §7's split only needs to be final before grades are entered, §9 only
matters if you want to pursue research framing, §8.6 only bites the first time a pair visibly
finishes early):

1. **Rubric point totals.** §7 proposes an internal split within the existing 25%/15% lines —
   confirm or adjust the exact numbers before it becomes the official grading document.
2. **Research framing.** Strand B ethics dossier and consent templates are in
   `docs/research/ethics/`; confirm committee submission and independent custody of signed
   forms. Analysis remains gated — this document does not clear that gate alone.
3. **§8.6's early-finisher policy.** Confirm the "reward depth used, not hours spent" framing is
   how you want to grade a pair that visibly one-shots their baseline — an alternative is a hard
   floor (no credit for work landed before a named week), which is simpler to enforce but does not
   reward the redirected-breadth behavior §8.6 is trying to encourage.
