<!--
Strand B — pedagogical / CER research design for TTOD Front-End II.
Author: Rubén Vega Balbás, PhD · ruvebal@crea-comm.net · 2026-09-25.
Elevated with Profield STEM-code meta-research inheritance (methodology, cohort
case design, grounding provenance, AI epistemology critique) to congress-
publication level. See PROFIELD-STEM-CODE-INHERITANCE.md and
STRAND-B-CONGRESS-PUBLICATION-PLAN.md.
-->

# Strand B — Pedagogical research design

## Learning by doing in a real, agentic-assisted product cohort

**Institution:** UDIT (Universidad de Diseño, Innovación y Tecnología)  
**Course context:** Front-End II (post-introductory; academic year 2026–27)  
**Product under construction:** TTOD Oracle Platform (this repository’s teaching spine)  
**PI / instructor:** Rubén Vega Balbás, PhD  
**Ethics package:** [`ethics/`](ethics/)  
**Congress plan:** [`STRAND-B-CONGRESS-PUBLICATION-PLAN.md`](STRAND-B-CONGRESS-PUBLICATION-PLAN.md)  
**Profield inheritance:** [`PROFIELD-STEM-CODE-INHERITANCE.md`](PROFIELD-STEM-CODE-INHERITANCE.md)  
**Sibling (parked):** [`STRAND-A-PHILOSOPHICAL-PARKED.md`](STRAND-A-PHILOSOPHICAL-PARKED.md)

---

## 0. Case boundary (McGill-aligned)

| Element | Definition |
| ------- | ---------- |
| **Phenomenon** | Learning-by-doing under ambient agentic AI in authentic product development |
| **Case** | The FE II 2026–27 TTOD Oracle cohort delivery |
| **Unit of analysis (primary)** | Student pair/solo **seam trajectories** (PR cycles, declarations, defence) |
| **Unit of analysis (secondary)** | The **cohort collaboration system** (review culture, cold-review gates, merge discipline) |
| **Context** | Spanish higher-ed design/tech university; post-introductory front-end; bilingual teaching materials possible; AI use declared |
| **Transferability claim** | Design principles may transfer to similar post-intro studio cohorts with real products and process assessment — **not** to CS1 tool trials or population effects |

---

## 1. Research question (primary)

> **How can participation as a developer in a real application — developed with agentic AI
> assistance, inside a cohort of peer developers — constitute a learning activity with
> pedagogical outcomes for students who learn by doing?**

Subsidiary questions (answerable only from consented, protocol-gated evidence):

| ID | Question | Evidence forms | Sensitizing literature |
| -- | -------- | -------------- | ---------------------- |
| **RQ-B1** | What process traces make AI-assisted contributions *explainable* and *reviewable*? | Pseudonymized commits/PRs/reviews; defence structure | Fischer et al. 2024; Davalos & Zhang 2026 |
| **RQ-B2** | How do students negotiate authorship, agency, and responsibility when the product is itself an AI-oracle interface? | AI-use declarations; defence; optional interview (separate consent) | Liu/Fan/Pan 2026; Prather et al. 2024 |
| **RQ-B3** | Which design principles of walking-skeleton + cascade + cold-review appear to support or hinder learning-by-doing? | Phase/PR reports; defect patterns; triangulation | Brown & Guzdial 2024; ITiCSE WG 2026 post-intro gap |
| **RQ-B4** | Where do *code produced* and *learning demonstrated* diverge in this cohort? | Defence ↔ artefact disagreements | Prather et al. 2024; “Fast and Forgettable” 2026 (frontier) |

**Out of scope for this cycle:** effect sizes; causal “AI improves learning”; Strand A theses;
analysis of non-consented work; pre-consent telemetry as analytic data.

---

## 2. Episteme and design type

| Choice | Rationale | Profield / CER warrant |
| ------ | --------- | ---------------------- |
| **Design-Based Research (DBR) / bounded educational case study** | Real intervention studied in situ; output = design principles | Runeson & Höst 2009; Runeson et al. 2012 (Wiley handbook); McGill et al. 2023 (CER transferability) |
| **Rich-data qualitative-dominant** | Small n; contextual density over statistical confidence | Brown & Guzdial 2024 |
| **Programming-process evidence as first-class data** | Git/PR/declarations/defence — not product polish alone | Fischer et al. 2024 |
| **Learning-by-doing / studio-cognate** | Real product, peer cohort, professional review rituals | Experience-report genre |
| **Critical AI epistemology** | Normative ≠ empirical; manifesto ≠ evidence; code ≠ learning | `stem-code-ai-epistemology-critique` digest |
| **Not a controlled experiment** | No treatment assignment, no experimental control for causal inference | Wohlin et al. 2012 — empirical strategies map (survey / experiment / case study); use to refuse experimental claim language |

This is **not** a laboratory experiment, **not** an A/B tool trial, and **not** a CS1 Copilot
efficacy study. Wohlin et al. (2012) place case studies and experiments as different empirical
strategies with different control and inferential ceilings — Strand B stays on the case-study /
observational side. Positioning within CER: **post-introductory** GenAI computing education
(ITiCSE WG 2026 gap, DOI 10.1145/3760545.3783970).

---

## 3. Pedagogical activity (what students do)

Students participate as **developers** in the TTOD Oracle Platform cohort:

1. Work from the isolated teaching skeleton / cohort handoff (not the instructor’s rich
   reference build).
2. Collaborate in pairs/solos on frozen front-end seams (Astro, islands, UI, data, tests, PWA,
   auth — per Phase U/V plans).
3. Use agentic AI assistance under an explicit declaration and review discipline.
4. Submit PRs, survive peer/instructor review, and defend selected decisions orally.
5. Experience the project’s own **cold-review / human-merge** habit as part of the learning
   environment (HITL accept/reject under agentic assistance — intervention description, not
   efficacy proof).

**Departmental pedagogical authorization** precedes the research layer. Teaching proceeds
whether or not any artifact is analysed as research data.
See [`DEPARTMENT-DECISION-BRIEF.md`](DEPARTMENT-DECISION-BRIEF.md).

---

## 4. What is (and is not) research data

| Layer | Status | Access |
| ----- | ------ | ------ |
| **Ordinary coursework** | Teaching / assessment | Instructor & academic systems |
| **Engineering telemetry** | Teaching-design observation | Instructor; **not** publishable learning claims without protocol |
| **Pre-consent process records** | **Design context only** (Profield durable core) | Not analytic research data |
| **Research corpus** | After ethics clearance **and** consent B; **pseudonymized** | Separate custody; analysis after relevant grades filed |

Coursework consent to *participate as developers* (form **A**) ≠ research consent for secondary
use (form **B**). Signed research consent: [`ethics/SIGNED-CONSENTS-CUSTODY.md`](ethics/SIGNED-CONSENTS-CUSTODY.md).

---

## 5. Data minimization (summary)

Full statement: [`ethics/DATA-MINIMIZATION-STATEMENT.md`](ethics/DATA-MINIMIZATION-STATEMENT.md).

> No special-category personal data; no private-life surveys; research use limited to
> **pseudonymized programming-process traces** already produced for assessment; grades and
> identifiers outside the research corpus; residual GDPR re-identification risk acknowledged
> via confidential retention — never “open anonymous data.”

Open-everything is **not** a research-integrity rule for student process traces (McGill et al.;
ACM human-participant policy; FAIR ≠ publish PII).

---

## 6. Method (procedures)

1. **Version** RQs, codebook skeleton, inclusion rules before examining the research corpus
   (`docs/research/ethics/analysis/` when opened — no PII in git).
2. **Assemble** only consent-B participants’ artifacts into a pseudonymized corpus after grades
   for relevant components are filed (temporal blinding).
3. **Analyse** thematic coding + descriptive process tracing; retain disconfirming cases;
   triangulate product behaviour ↔ written record ↔ oral defence (disagreement = evidence).
4. **Report** design principles, transferability limits, null/mixed findings. No causal language.
5. **Ground literature** with discover≠cite discipline: DevIAC/Athanor for discovery; DOI-
   verified sources for Chicago warrants ([`PROFIELD-STEM-CODE-INHERITANCE.md`](PROFIELD-STEM-CODE-INHERITANCE.md) §3).

Optional instruments (survey, interview, recording) need separate consent items and are **off**
by default in the minimal ethics submission.

---

## 7. Safeguards (non-negotiable)

- Grading never depends on research participation or withdrawal.
- Instructor blind to research-consent status until grades filed (independent custodian).
- Teaching repository ≠ research dataset.
- Withdrawal without academic consequence; aggregate publications cannot be unpublished.
- Rich instructor reference isolated from student artifact (history-isolation gate).
- Strand A philosophical claims never imported as empirical warrants.
- TTOD quotes are pedagogical epigraphs, never CER evidence.

---

## 8. Literature that motivates (does not validate) this design

### 8.1 Methods backbone (congress Methods section)

| Source | DOI | Role |
| ------ | --- | ---- |
| Runeson & Höst 2009 | 10.1007/s10664-008-9102-8 | Compact SE case-study process + researcher/reader checklists |
| Runeson, Höst, Rainer & Regnell 2012 | ISBN 978-1-118-10435-4 · DOI 10.1002/9781118181034 | Extended case-study handbook (guidelines + examples); protocol, data, reporting depth |
| Wohlin et al. 2012 | 10.1007/978-3-642-29044-2 | Empirical SE strategies; Ch. 5 case-study process; **contrast** with controlled experiments (Ahmes coat present) |
| Heckman et al. 2022 | 10.1145/3470652 | CER reporting / empiricism norms |
| Brown & Guzdial 2024 | 10.1145/3626252.3630813 | Rich vs big data; small-n legitimacy |
| McGill et al. 2023 | 10.1145/3623762.3633495 | Transferability, consent reporting, null findings |
| Fischer et al. 2024 | 10.1145/3632620.3671125 | Programming-process data + consent architecture |
| ITiCSE WG 2026 (post-introductory GenAI) | 10.1145/3760545.3783970 | Gap positioning |

### 8.2 Domain / phenomenon warrants (already on public methodology)

Shihab et al. 2025; López-Pernas et al. 2025; Liu, Fan & Pan 2026; Garcia 2025;
Nikolić & Basta Nikolić 2026; Davalos & Zhang 2026; *Computer Science Curricula 2023*;
Prather et al. 2024 (benefits/harms — performance ≠ learning).

### 8.3 Grounding discipline (how we cite)

Discover ≠ cite; page-addressable preference; no fabricated DOIs; vector similarity ≠ entailment
(Profield `stem-code-grounding-provenance` + omnibus digest). Studio discovery notes stay out of
public Chicago lists unless resolved to DOI-safe sources.

---

## 9. Outputs — congress-first, fundable research product

See [`STRAND-B-CONGRESS-PUBLICATION-PLAN.md`](STRAND-B-CONGRESS-PUBLICATION-PLAN.md) and
[`CONGRESS-ABSTRACTS-DRAFT.md`](CONGRESS-ABSTRACTS-DRAFT.md).

| Cycle-1 product | Claim ceiling |
| --------------- | ------------- |
| Ethics-cleared protocol | Integrity capacity |
| JENUI (ES) experience / evidence note | Design principles + transferability |
| ITiCSE/SIGCSE experience report (EN) | Same, international |
| Sanitized teaching artefact (optional) | Replicable object without student PII |

Later: ICER / journal only with deeper analytic package or second cycle.

---

## 10. Status board (2026-09-25)

| Gate | State |
| ---- | ----- |
| Strand A separation | Done (parked) |
| Profield STEM-code inheritance mapped | Done — `PROFIELD-STEM-CODE-INHERITANCE.md` |
| Congress publication plan + abstracts | Done — drafts pending fill-ins |
| Department pedagogical framing | Asserted — file confirmation with ethics package |
| Consent templates | `ethics/` |
| Signed consents | Private custody log |
| Ethics committee submission | Prepared |
| Research analysis | **Blocked** until clearance + consent B + grades filed |
| Congress submit | Blocked on analysis + checklist |

---

## 11. Relation to older RQs in `RESEARCH-LINE.md`

`RESEARCH-LINE.md` RQ1–RQ5 remain a **broader programme**. Operative set for ethics and
congress cycle 1: **RQ-B / RQ-B1–B4**. Do not expand the dossier with unanswered cross-degree
RQ2 until cohort composition is institutionally confirmed.
