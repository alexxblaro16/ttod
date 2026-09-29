<!--
TTOD as a research line — episteme, objectives, methodology, venue ladder.
Author: Rubén Vega Balbás, PhD (drafted with Claude) · 2026-09-04.
Structural shape (gap → asset inventory → episteme → RQs → methodology → risk
register → venue ladder → what-not-to-claim) is a documented pattern in the
author's own teaching-research practice; the content below is authored fresh
for TTOD and independent of any other case study. Verification discipline:
[V] confirmed against a live source this session, [U] unverified/needs a
fresh check, [I] interpretive judgement, not a citable fact.
-->

# TTOD as a Research Line — design & venue projection

> **Supersession note (2026-09-25):** for the active **Strand B** ethics submission and
> learning-by-doing case, use
> [`STRAND-B-PEDAGOGICAL-DESIGN.md`](STRAND-B-PEDAGOGICAL-DESIGN.md) and
> [`ethics/`](ethics/). Philosophical work is parked in
> [`STRAND-A-PHILOSOPHICAL-PARKED.md`](STRAND-A-PHILOSOPHICAL-PARKED.md). This file remains
> useful for the broader RQ set, risk register, and venue ladder — treat its “pre-consent”
> prose as historical where Strand B documents say otherwise.
>
> Evidence base to (re-)verify before citing as current: Athanor project
> `profield-frontend-pedagogy` (Ahmes-extracted literature corpus) — see
> [`PHASE-R-TTOD-ORACLE-PLATFORM-CASCADE-PROMPT.md`](../DEV_PLAN/PHASE-R-TTOD-ORACLE-PLATFORM-CASCADE-PROMPT.md)
> §13.2 for the exact refresh/query commands. Nothing below that cites a specific study should be
> treated as final until pulled fresh from that vault — this draft states the *shape* of the
> claim, not a re-verified citation table.

---

## 0. Is there a gap? Two, at different maturity

**Gap A — inherited, field-level, `[U]` pending a fresh Athanor pull.** The studio's own
frontend-pedagogy literature corpus is understood to show that AI-assisted-teaching mechanisms
(deferred assistance, metacognitive scaffolds, in-workflow AI code review) have been validated in
general-programming and data-science cohorts far more often than in a front-end/interface-layer
cohort, and that a Spanish cohort is essentially absent from that corpus. This is background
motivation, not this document's contribution — verify it fresh via `athanor search` (§13.2 of the
cascade doc) before citing it in anything submitted externally.

**Gap B — TTOD-specific, `[I]` interpretive but original to this document.** Documented,
cold-review-gated, multi-agent-orchestrated cascade development — an instructor-forged "walking
skeleton" handed to a small cohort that then works in parallel, disjoint-path lanes under a
mandatory post-phase review gate (`PHASE-R-...-CASCADE-PROMPT.md` §0, §6.1) — does not appear to
have a CER literature home at all. This is not a claim that agentic/AI-assisted team-development
pedagogy is unstudied in general (it plainly is being studied, fast, everywhere); it is a claim
that *this specific, fully-documented instance*, with a real report trail per phase, is a
concrete case worth writing up regardless of what the wider literature turns out to already say —
the documentation itself is the asset, not novelty-by-assertion.

---

## 1. Asset inventory — why this cohort, why now

| Asset | Why it is research-grade |
| --- | --- |
| **A real, graded deliverable, not a synthetic exercise.** | Entrega 1 (FE II, 25%, Week 7/October 2026) already requires everything the case needs to observe: Astro islands, i18n, a real test suite, CI/CD, and an AI-code-review workflow. No measurement demand was added to the syllabus for the study's sake. |
| **The development method is designed to be instrumented.** | The instructor reference build already has phase reports and recorded cold-review evidence for its completed lanes; R7 is PARTIAL and R6 is deliberately absent. The cohort will produce a separate report and cold-review trail for its own assessed build from the walking skeleton. Together these can produce a dated, falsifiable trace of claims and review findings, but only consented cohort artifacts may become research data. |
| **A governed data layer with its own audit trail.** | The platform's own subject (`ttod.yml`) went through a fully reported, phase-gated development programme (Phase Q, DONE 2026-08-18) before this cohort. Separately, the instructor completed an R3b/R4/R5 reference implementation to validate the architecture; students do not extend that implementation, but independently implement their assessed R3b–R7 scope from an isolated R1/R2/R3a walking-skeleton handoff. |
| **Small, bounded cohort (n=7).** | Closes the door to statistical inference and opens the one that actually fits: a longitudinal, qualitative-dominant case study where every trajectory is knowable, not just aggregatable. |
| **Reflexive subject matter.** | The platform students build *teaches developer wisdom*; they build it while narrating their own AI-assisted authorship in real time. That reflexivity is worth naming as a framing device, not a research claim in itself. |
| **Versioned, publication-ready artifact.** | The private repository, cascade plan, and phase reports are auditable in git history. A sanitized artifact may later be published under the recorded licenses, but public availability is not yet established and must not be claimed as a present fact. |

**To confirm before finalizing this section:** whether the 2026-27 FE II cohort spans both the
Full-Stack and Data Science & AI degrees (as this course has in prior cycles) or Full-Stack only
this year — this determines whether RQ2 below is answerable at all.

---

## 2. Research episteme

**Not** positivist effect-hunting — n=7 will not support it, and it would misrepresent the design.

**Design-Based Research (DBR)**: an iterative learning-environment design, studied in situ,
producing *design principles* rather than universal effects. Paired with **critical technical
practice**: the interface layer, and now the *development-methodology* layer (the cascade itself),
treated as sites where technical choices carry pedagogical and social consequence.

Two lineages worth claiming rather than inventing:

- **Studio-based learning in computing** (Hundhausen and the broader CER studio-pedagogy
  tradition) — the course's own ATELIER methodology, already in use for FE I/II independent of
  this study, is a studio-based instructional model; framing it as such inherits a citable
  tradition rather than asserting novelty for a teaching format that already exists.
- **Process-based, artefact-centred assessment** — FE II's existing instrumentation (AI-use
  declarations, `decisions.md`/`iterations.md`-style logs, oral defence) is already this kind of
  assessment; this research line adds structure and consent, not new bureaucracy.

**Epistemic commitment to state in every output:** claims are tagged by evidence strength,
absences are reported as findings, and the underlying vault/report trail is disclosable.

---

## 3. Research questions

**RQ1 — Transfer.** Do AI-assisted-teaching mechanisms validated in general-programming cohorts
(deferred assistance, metacognitive scaffolds, in-workflow AI code review) behave the same in a
front-end, multi-framework-islands cohort? A replication in a documented gap is publishable even
when null.

**RQ2 — Cross-degree legibility** *(pending §1's confirmation)*. If the cohort spans two degrees,
does interface-layer framing produce different engagement/outcomes between them?

**RQ3 — Longitudinal durability.** Across FE I → FE II, which competences persist when the
underlying framework changes (React → Astro islands → Svelte → a locally-hosted LLM interface)?

**RQ4 — Authorship and agency under ambient AI** *(co-investigator-led, qualitative)*. How do
students narrate authorship, competence, and responsibility in their AI-use declarations, when the
artifact they are narrating about is itself an AI-oracle interface? The reflexivity noted in §1 is
a hypothesis generator here, not a conclusion.

**RQ5 — Cascade methodology** *(new, original to TTOD, the pilot's own payoff)*. Does an
instructor-forged walking skeleton, cascade-orchestrated parallel lanes, and a mandatory
post-phase cold-review gate (the actual method documented in
`PHASE-R-TTOD-ORACLE-PLATFORM-CASCADE-PROMPT.md`) produce observable differences — in integration
defects, in how confidently students can explain code they did not personally write, in how
cold-review findings do or do not make it into the next phase's runbook — relative to an
unscaffolded team project? Output = design principles for agentic-cascade team pedagogy, explicitly
labelled as a first proposal, not a validated framework.

---

## 4. Methodology

**Design:** DBR, one FE II semester cycle (2026-27), with FE I (prior year, same students) as
longitudinal context per RQ3.

**Data already produced** (needs consent + structure, not new bureaucracy):

| Instrument | Already exists? | Research use |
| --- | --- | --- |
| AI Use Declaration | ✅ (FE II rubric) | RQ1, RQ4 |
| Commit / PR narrative per lane | ✅ (git history, one repo) | RQ1, RQ3, RQ5 |
| `PHASE-Rx-REPORT.md` + cold-review findings | ✅ (§6.1 of the cascade doc — TTOD-specific, does not exist in a generic FE II project) | RQ5 primarily; RQ1 secondarily |
| `docs/testing-strategy.md` (Unit 5 deliverable) | ✅ | RQ1 |
| Oral defence + diff questions | ✅ (Unit 12) | RQ1, RQ3 |

**Data to add** (co-investigator's design, not invented here): entry/exit survey, semi-structured
interviews (purposive sample within n=7), one capstone focus group, optional think-aloud for RQ4.
No new psychometric instrument should be invented; use validated scales where they already exist.

**Analysis:** qualitative-dominant. Thematic analysis of declarations/interviews (co-investigator
led); descriptive tracing of process artefacts (cold-review pass/fail counts, cross-phase finding
propagation); no causal language.

**Primary construct:** the oral defence already operationalises "can you explain and modify this
on the spot." Score it consistently from the first defence onward.

---

## 5. Risk register

| Risk | Severity | Mitigation |
| --- | --- | --- |
| **Teacher–researcher conflict of interest** | 🔴 | Consent collected and administered by an independent co-investigator, never the instructor. Data pseudonymised and withheld from analysis until grades are filed. State this in every output's ethics note. |
| **Coercion risk** | 🔴 | Explicit opt-in/opt-out, zero grade consequence, opt-out status invisible to the instructor until after grading. |
| **GDPR / data protection** | 🔴 | Legal basis, retention period, pseudonymisation at ingest, institutional data-protection sign-off before any consented data collection begins. |
| **Institutional ethics approval** | 🟠 | Confirm whether an institutional ethics committee applies; if not, adopt and cite an external protocol (e.g. ACM SIGCHI ethics guidance). |
| **Small n** | 🟠 | Frame as DBR / case study / experience report. Null results are publishable in a documented gap. |
| **"Innovación docente" ≠ research merit** in Spanish accreditation practice | 🟠 | Target indexed CER venues (§6), not internal teaching-innovation calls, for merit-bearing outputs. |
| **Novelty overclaim** | 🟡 | RQ1/RQ3/RQ4 replicate known mechanisms in a new cohort — say so plainly. RQ5 is the one genuinely new claim, and it is scoped to design principles, not a validated framework. |

> **If one line survives from this document:** consent and data governance must be in place before
> any process evidence is treated as research data — the engineering work (Phase R) proceeds
> regardless, per the cascade doc §13's own framing.

---

## 6. Venue ladder (CER / open education — generic, not fashion/design-specific)

Field facts as last checked in the studio's own literature pass; **re-verify every date before
submitting anything** — conference windows move.

| Tier | Venue | Fit | Note |
| --- | --- | --- | --- |
| Entry / Spanish | **JENUI** (AENUI) | University CS teaching, Spanish-language | Hosts a national teaching-innovation prize track |
| Mid / international | **ITiCSE** (ACM) | European CER | Recent Spanish edition — a nearby CER network worth cultivating |
| Mid / thematic | **ASSETS** — experience-reports track | Accessibility-in-teaching | Natural home for the a11y-in-suite work already in R7 |
| High / methodological | **ICER** | Rigorous CER | Cycle-2 target once the two-cycle (FE I + FE II) dataset exists |
| Open artefact | **OEGlobal Awards** | Nominates the published, open (CC BY-NC-SA) curriculum/platform | No research data required — the fastest merit path |
| Journal / open | **Education Sciences** (MDPI) | Fast, open access | Has published comparable web-cohort CER work before |
| Journal / prestige | **ACM TOCE**, **Computer Science Education** (T&F), **IEEE ToE** | Merit-bearing | Target with a full-cycle dataset, not a pilot note |
| Journal / Spanish | **RIED** (AIESAD), **IE Comunicaciones** | Spanish-language indexed | Accreditation breadth |

---

## 7. What will and will not be claimed

**Will:** a documented replication of known AI-assisted-teaching mechanisms in an under-studied
cohort type; a first, explicitly-labelled design-principles proposal for cascade-orchestrated,
cold-review-gated team pedagogy (RQ5); a disclosable, auditable evidence trail.

**Will not:** effect sizes, causality, a validated framework, or a claim that the cascade
methodology is novel in the wider AI-assisted-development literature — only that this fully
documented instance of it is a concrete, citable case. Null results will be published as findings,
not omitted.

---

## 8. Honest verdict

The gap in Gap B is genuinely this document's own — it did not exist as a framed research question
before Phase R's cascade plan existed this session. Gap A is inherited background and needs a
fresh Athanor pull, not a re-typed citation, before it appears in anything submitted externally.
The n=7 case-study framing is the right fit for what a single cohort can actually support; the
single hard precondition, per §5, is that consent and data governance are in place **before** any
process evidence already being produced is treated as research data — the engineering deliverable
itself needs none of this to proceed.
