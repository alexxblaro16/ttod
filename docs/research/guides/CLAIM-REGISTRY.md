# T0 claim registry

**State:** DONE for T0 baseline classification  
**Frozen committed revision:** `8e73116299d29dd78b59f1717283f39eaca5fcea`  
**Freeze time:** 2026-09-06 (Europe/Madrid)  
**Authority order:** repository state and filed engineering decisions; research proposal prose;
interpretive research framing.

This registry controls wording for T1–T7. Labels are closed:
`verified | interpretive | pending evidence | obsolete`.

| ID | Canonical claim | Label | Evidence / qualification | Canonical home |
| --- | --- | --- | --- | --- |
| C-001 | Phase Q Q0–Q6 is complete. | verified | `docs/DEV_PLAN/INDEX.md` and Q reports | DEV plan index |
| C-002 | Phase S is complete through S4; S5 is only a proposed continuation. | verified | `docs/DEV_PLAN/INDEX.md`; the uncommitted S5 plan is not part of the frozen revision | DEV plan index |
| C-003 | Phase R R0–R5 is complete; R3b/R4/R5 constitute an instructor reference/architectural-validation build on `main`. | verified | Phase R closure report and index | Phase R closure report |
| C-004 | R6 is unimplemented, deferred, and student-owned. | verified | `DECISIONS/R6-DEFERRED-STUDENT-OWNED.md` | R6 decision |
| C-005 | R7 is PARTIAL; completed reference-build testing does not close its R6-dependent gates. | verified | Phase R closure report and `PHASE-R7-REPORT.md` | R7 report |
| C-006 | Students are intended to inherit R1/R2/R3a and independently implement their assessed R3b–R7 scope. | verified | R6 decision, closure report, generator script, local `cohort-starter` branch | R6 decision |
| C-007 | A local `cohort-starter` branch exists, but it is not the verified distribution artifact. | verified | local branch listing; closure report says it was not pushed and later amendments require regeneration | closure report |
| C-008 | Students will be unable to inspect the instructor reference build. | pending evidence | No isolated student remote/artifact has passed T4's `git log --all` and `git branch -a` test | T4 report when tested |
| C-009 | The current GitHub repository is private with `main` as default and one shared `origin`. | verified | Repository check recorded in the audited forge plan; local `git remote -v` confirms one origin. This is time-sensitive and must be rechecked before distribution. | T0 report / T4 refresh |
| C-010 | The repository will become public when the owner judges the project ready. | pending evidence | Owner's stated intention on 2026-09-06; no publication action or release criterion is yet verified | maintainer/release decision |
| C-011 | Students run TTOD on their own laptops or university-lab machines; Tanit and Lilith are not student services. | verified | Phase R closure report, R6 decision, research overview | closure report |
| C-012 | TTOD is mature as an engineering object and documented teaching design. | interpretive | Supported by phase reports and tests, but “mature” is an evaluative synthesis | maintainer guide / PI brief |
| C-013 | The TTOD study is a proposal, pre-pitch and pre-collection, without institutional approval. | obsolete | Superseded 2026-09-25 by two-strand map: Strand B has ethics dossier + consent templates; analysis still gated on committee clearance. Use C-028–C-032 | research INDEX / Strand B |
| C-014 | Teaching may proceed without research approval; use of student artifacts as research data may not. | verified | Explicit project governance decision; institutional/legal validity still requires institutional review | research overview |
| C-015 | Student developer and research participant are separate roles; research refusal must not affect teaching or grading. | verified | Adopted project governance rule in the plan/proposal; implementation remains subject to institutional approval | cohort proposal / ethics forms |
| C-016 | The proposed study is a small, qualitative-dominant DBR/case study and does not support causal or effect-size claims. | interpretive | Methodological position requiring T1 evidence and PI review | research line |
| C-017 | The 2026–27 cohort contains seven students. | pending evidence | Repeated in research prose but no frozen institutional roster evidence is in this repository | institutional input |
| C-018 | Entrega 1 is 25%, due Week 7/October 2026, with the stated Astro/i18n/testing/CI/AI-review requirements. | pending evidence | Research docs point outside this repository to course material; T0 did not verify that source | course specification |
| C-019 | The cohort spans Full-Stack and Data Science & AI degrees. | pending evidence | Explicitly marked “to confirm” in `RESEARCH-LINE.md` | institutional input |
| C-020 | The intended cascade can produce useful process evidence. | interpretive | Design rationale, not an observed outcome; only consented artifacts may be analyzed | research line |
| C-021 | Every R1–R7 phase is closed and every report has an independent cold review. | obsolete | R6 is absent and R7 is PARTIAL; replaced by distinct instructor-reference and future cohort trails | this registry |
| C-022 | A complete instructor reference implementation already exists. | obsolete | R6 is deliberately absent and R7 is PARTIAL; use C-003–C-005 | this registry |
| C-023 | The research initiative has formally launched. | obsolete | Conflicts with pre-pitch/unapproved status; it is a proposal for review | research overview |
| C-024 | Front-end/interface pedagogy under ambient AI and Spanish cohorts are underrepresented, and this cascade lacks a CER literature home. | pending evidence | Gap A requires evaluator-safe T1 evidence; Gap B is currently interpretive and must not be promoted to novelty | T1 evidence ledger |
| C-025 | TTOD quotes are pedagogical material, not independent evidence for research claims. | verified | Repository `AGENTS.md` constitutional rule | repository governance |
| C-026 | `ground-with-athanor-ahmes` and `profield-ahmes-athanor` both exist and have distinct grounding and ingestion responsibilities. | verified | Both `SKILL.md` files were read at their current filesystem paths during T0 cold audit | guide-forge plan |
| C-027 | The guide programme will include a Spanish research pitch organized with the MSCA Part B Excellence–Impact–Implementation logic; it is not an MSCA application or funding/eligibility claim. | verified | Owner instruction dated 2026-09-07 and amended guide-forge contract | guide-forge plan T5 |
| C-028 | TTOD research has two strands: A philosophical/cybernetic (parked) and B pedagogical CER / learning-by-doing (active). | verified | `docs/research/INDEX.md`, Strand A/B docs dated 2026-09-25 | research INDEX |
| C-029 | Strand B primary RQ: can developer participation in a real agentic-assisted cohort product be a learning activity with pedagogical outcomes (learning by doing)? | verified | `STRAND-B-PEDAGOGICAL-DESIGN.md` | Strand B |
| C-030 | Participant information sheets and consent form templates exist under `docs/research/ethics/`; signed consents are never stored in git. | verified | ethics package created 2026-09-25; prior audit found taxonomy only | ethics README |
| C-031 | Strand B asserts no special-category student personal data are collected for research; research corpus is pseudonymized process artifacts only; GDPR residual risk of re-identification is acknowledged. | verified | `DATA-MINIMIZATION-STATEMENT.md` | ethics |
| C-032 | Research analysis of student artifacts remains blocked until ethics-committee clearance, valid consent, and relevant grades filed. | verified | Strand B §10; ethics submission | Strand B / ethics |
| C-033 | Strand B inherits Profield STEM-code durable core: discover≠cite; consent before secondary use; small-n depth; pre-consent≠analytic; null/gaps publishable; normative≠empirical. | verified | `PROFIELD-STEM-CODE-INHERITANCE.md` from runs 20260818/19 | research inheritance |
| C-034 | Cycle-1 publication genre is experience report / design-principles case study (JENUI then ITiCSE/SIGCSE), not efficacy RCT; claim ceiling forbids effect sizes and population inference. | verified | `STRAND-B-CONGRESS-PUBLICATION-PLAN.md` | congress plan |
| C-035 | FE II case is positioned in the post-introductory GenAI computing-education gap (ITiCSE WG 2026, DOI 10.1145/3760545.3783970) rather than as a CS1 Copilot trial. | interpretive | Gap DOI from Profield omnibus digest; re-verify before external submission | Strand B §2 |
| C-036 | Strand B methods backbone includes Runeson & Höst 2009 (DOI 10.1007/s10664-008-9102-8) for SE case-study process/checklists; Ahmes coat under `scholar-research-methodology`. | verified | Added 2026-09-26; public methodology EN/ES | Strand B / public methodology |
| C-037 | Strand B also cites Runeson et al. 2012 Wiley case-study handbook (DOI 10.1002/9781118181034) and Wohlin et al. 2012 *Experimentation in Software Engineering* (DOI 10.1007/978-3-642-29044-2): Wiley for case depth; Wohlin for strategy contrast (not a controlled experiment). Wohlin has Ahmes coat; Wiley book not yet a separate coat. | verified | Added 2026-09-26 | Strand B / inheritance |

## Usage rule

Downstream documents must cite a claim ID or reproduce its canonical wording. A pending or
interpretive claim must retain that status. Time-sensitive claims C-009, C-010, and C-017–C-019
must be refreshed at the point of use.
