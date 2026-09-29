<!--
TTOD cohort case-study proposal — request to co-investigator and department/
degree coordination. Author: Rubén Vega Balbás, PhD · 2026-09-04.
Updated pointer 2026-09-25: operative Strand B design + ethics package supersede
status claims here about "no consent documents yet"; §6 consent taxonomy remains
authoritative. See docs/research/INDEX.md.
-->

# Proposal — TTOD Oracle Platform (Front-End II) as a documented cohort case study

> **2026-09-25:** For the ethics committee and current Strand B RQ, start at
> [`STRAND-B-PEDAGOGICAL-DESIGN.md`](STRAND-B-PEDAGOGICAL-DESIGN.md) and
> [`ethics/`](ethics/). This proposal’s §6 taxonomy still defines C1–C4.

**From:** Rubén Vega Balbás, PhD · Prof. Desarrollo Web Front-End I/II · UDIT
**To:** co-investigator (research design/qualitative methods) · Front-End II degree
coordination · UDIT academic direction
**Date:** 2026-09-04 · **Academic year affected:** 2026-27
**Sibling document:** [`RESEARCH-LINE.md`](RESEARCH-LINE.md) (full episteme, RQs, methodology,
risk register, venue ladder — this document does not repeat it)

---

## 1. The request, in one sentence

Authorization for Front-End II's 2026-27 delivery — specifically the 7-student cohort building
the **TTOD Oracle Platform** as Entrega 1 — to constitute a documented case study, with informed
consent, external custody of research data, and output at CER conferences/journals, **without
changing the teaching that would happen anyway.**

---

## 2. The gap

Summarized here; full evidentiary treatment (and the caveat that it needs a fresh vault pull
before external citation) is in [`RESEARCH-LINE.md`](RESEARCH-LINE.md) §0. Two threads: an
inherited, field-level gap (front-end/interface-layer pedagogy under ambient AI is thin in the
literature relative to general programming/data science), and a gap original to this cohort
(documented, cold-review-gated, cascade-orchestrated team development has no evident CER
literature home at all).

---

## 3. Why this cohort, and not a synthetic one

1. **The deliverable already exists and is already graded.** Entrega 1 — Astro islands, i18n,
   testing, CI/CD, AI-assisted code review — is FE II's own Week 7/October 2026 requirement (25%
   of the grade). No measurement demand was added for the study's sake.
2. **The development method is self-documenting.** Every build phase closes with a report, every
   report closes with an independent cold review (`PHASE-R-...-CASCADE-PROMPT.md` §6.1). This
   produces a dated, falsifiable process trace that a conventional team project does not generate.
3. **The cohort is small and bounded (n=7).** This closes the door to statistical inference and
   opens a longitudinal, depth-first case-study design where every trajectory is knowable.
4. **The platform already carries a governed development history.** `ttod.yml`'s own schema and
   tooling went through a fully reported, phase-gated programme (Phase Q, complete 2026-08-18)
   before this cohort touched it — the cohort extends a disciplined codebase, which is a variable
   worth naming, not hiding.

**To confirm before this proposal is finalized:** whether the 2026-27 FE II cohort spans both the
Full-Stack and Data Science & AI degrees, as in prior cycles of this course, or Full-Stack only
this year (affects `RESEARCH-LINE.md` RQ2's answerability, not the rest of the design).

---

## 4. The artifacts are versioned and auditable

Unlike many teaching-innovation proposals, the object of study is already version-controlled and
auditable in a private instructor repository. Publication or student distribution remains a
separate, gated action:

| Artifact                                                 | Where                                                                                                                              |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| TTOD repository (code + governed quote database)         | this repository, MIT (code) / CC BY-NC-SA 4.0 (content)                                                                            |
| Development cascade plan, all phase runbooks and reports | `docs/DEV_PLAN/PHASE-R-TTOD-ORACLE-PLATFORM-CASCADE-PROMPT.md` and `docs/DEV_PLAN/PHASES/R*.md` (generated per that document's §0) |
| Testing-strategy deliverable                             | `docs/testing-strategy.md` (produced by R7, per FE II Unit 5's own required shape)                                                 |
| Course track and grading structure                       | `web-atelier-udit/.../tracks/en/udit/2627-feii/`                                                                                   |

**Consequence for coordination:** authorized reviewers can verify the proposal before approval.
The recorded code/content licenses permit a future publication path, but reproducibility by third
parties and any open-education nomination require a sanitized artifact to be published first;
neither is asserted as complete here.

---

## 5. What is asked of each party

**Of the co-investigator:**

- Design and validate research instruments (entry/exit survey, semi-structured interview guide,
  focus group).
- Lead qualitative analysis of the AI-use-declaration corpus (RQ4) — the discourse-analysis
  competence a CS-only author does not bring.
- **Independent custody of consent and data.** This resolves the teacher/researcher conflict of
  interest and cannot sit with the instructor.

**Of Front-End II degree coordination:**

- Conformity for the subject to operate as a documented case study under informed consent.
- Liaison with UDIT's data-protection officer.
- Recognition of the associated research time.

**Explicitly not requested:** no change to the FE II syllabus, no added mandatory workload for
the cohort, no grade conditioned on research participation.

---

## 6. Consent taxonomy

Four distinct consents, each with different legal weight — administered by the co-investigator,
never by the instructor:

| #      | Consent                                                         | Object                                                                                                                              | Nature and safeguard                                                                                            |
| ------ | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **C1** | Secondary research use of evidence already produced for grading | Commits/PRs, AI-use declarations, `PHASE-Rx-REPORT.md` cold-review findings, `docs/testing-strategy.md`, oral-defence rubric scores | Opt-in. These artifacts are produced regardless, to be graded; consent covers pseudonymised reuse for research. |
| **C2** | New instruments                                                 | Survey, interview, focus-group data                                                                                                 | Independent opt-in from C1. Voluntary, no grade effect, revocable at any time.                                  |
| **C3** | Recording                                                       | Oral defence / interviews (voice, possibly image)                                                                                   | Separate, stricter consent; participation without recording remains possible; explicit retention period.        |
| **C4** | Diffusion of student artifacts                                  | Repository screenshots, code excerpts, direct quotes                                                                                | Per-artifact consent, attribution-or-anonymity choice retained by the student author.                           |

**Non-negotiable safeguards:** administered by the co-investigator, not the instructor; the
instructor is blind to who has and has not consented until grades are filed; pseudonymisation at
source; revocable at any time without academic consequence; data-protection sign-off before any
consented collection begins; a check for any additional safeguard needed given the group's actual
composition (minors, vulnerable students).

> **The risk these safeguards neutralize:** a grader asking the people they grade for data. If
> coordination reviews only one section of this proposal, it should be this one.

---

## 7. Calendar

Anchored to Phase R's own build calendar (`PHASE-R-...-CASCADE-PROMPT.md` §0.1.6, §9):

| Window                    | Work                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Sep 2026                  | Consent instruments frozen, data-protection sign-off sought, cohort start gate opens (R1/R2/R3a green)                                                                                                                                                                                                                                                                               |
| Sep–Oct 2026              | From the isolated `cohort-starter` handoff, the cohort independently implements its assessed R3b–R7 scope; this is distinct from the instructor's already-built R3b/R4/R5 reference implementation on `main`. Student cold-review reports accumulate as their own phases close; Entrega 1 is due Week 7/October 2026. R6 remains student-owned and the reference R7 remains PARTIAL. |
| Oct–Dec 2026              | Analysis of consented process evidence begins only after grades for the relevant components are filed                                                                                                                                                                                                                                                                                |
| per `RESEARCH-LINE.md` §6 | Venue submissions, once a draft or dataset exists — not before                                                                                                                                                                                                                                                                                                                       |

---

## 8. What will and will not be affirmed

Per `RESEARCH-LINE.md` §7: a documented replication of known mechanisms in an under-studied
cohort, plus a first, explicitly-labelled design-principles proposal for the cascade methodology
itself. Not effect sizes, not causality, not a validated framework. Null results are publishable
findings in a documented gap, not a failed study.

---

## 9. Note on teaching load

This proposal must not delay or distort teaching. The build calendar in §7 is the FE II calendar
that would run regardless of this proposal's approval; the only research-specific addition is
consent administration and instrument design, both owned by the co-investigator, not the
instructor. Teaching goes first; research is built on top of it, not the reverse.
