<!--
Congress / fundable publication plan for Strand B.
Elevates the pedagogical case to a submission-ready research product.
Author: Rubén Vega Balbás, PhD · 2026-09-25.
-->

# Strand B — Congress publication plan (fundable research product)

**Goal:** turn the FE II TTOD cohort case into a **congress-grade, fundable research output** —
not a blog of teaching tips, and not a premature efficacy claim.

**Depends on:** ethics clearance + consented pseudonymized corpus
([`ethics/`](ethics/)) · design ([`STRAND-B-PEDAGOGICAL-DESIGN.md`](STRAND-B-PEDAGOGICAL-DESIGN.md)) ·
Profield inheritance ([`PROFIELD-STEM-CODE-INHERITANCE.md`](PROFIELD-STEM-CODE-INHERITANCE.md)).

---

## 1. Contribution statement (one paragraph — paste into abstracts)

> We report a **declared design-based pilot** in post-introductory front-end engineering
> education: a small cohort develops a real, multi-framework web product
> (*The Tao of Development* Oracle platform) under agentic AI assistance, peer PR review, and a
> mandatory cold-review / human-merge discipline. Using **rich programming-process evidence**
> (commits, PRs, AI-use declarations, oral defence) under an explicit consent and
> data-minimization architecture, we derive **situated design principles** for learning-by-doing
> in authentic agentic cohorts. We do **not** claim causal learning gains or population effects;
> we contribute a transferable case boundary, an ethics-aware process-evidence protocol, and an
> honest account of what the design supports and forbids — addressing a documented gap in
> **post-introductory** GenAI computing education.

---

## 2. Paper type and claim ceiling

| Allowed | Forbidden |
| ------- | --------- |
| Bounded case study / experience report | Effect sizes, A/B “AI improves grades” |
| Design principles (labelled as first proposal) | Validated general framework |
| Process mechanisms & triangulation patterns | Population prevalence |
| Null / mixed findings | Selective omission of failures |
| Ethics & consent architecture as method contribution | “Students already logged → free to research” |
| Transferability statements (McGill) | Silent generalisation |

**Genre:** ACM-style **Experience Report** or **Case Study** (ITiCSE / SIGCSE / ICER companion);
Spanish track **JENUI** experience / innovation-with-evidence. Follow with a longer journal
article only after a second cycle or multi-site extension.

---

## 3. Venue ladder (submission-ready order)

| Priority | Venue | Why it fits Strand B | Target window |
| -------- | ----- | -------------------- | ------------- |
| 1 | **JENUI** (AENUI) | Spanish-language CER teaching track; first public research product | Next open call after ethics clearance + Term analysis |
| 2 | **ITiCSE** experience / short paper | European CER; post-intro GenAI WG gap (DOI 10.1145/3760545.3783970) | Annual — draft EN abstract as soon as corpus exists |
| 3 | **SIGCSE TS** experience report | Broader audience; rich-data framing peers (Brown & Guzdial) | After JENUI or parallel if calendar allows |
| 4 | **ICER** (later cycle) | Only with stronger analytic depth / second cohort | Cycle 2 |
| 5 | Journal (*TOCE*, *CSE*, *Education Sciences*) | After congress feedback | Cycle 2+ |

**Funding / institutional value (honest):** a congress paper with ethics clearance, DOI warrants,
and a reproducible *method* package is the unit that research groups and competitive calls
(teaching-innovation, CER capacity, regional R&D) actually count. This plan **does not** assert
MSCA or other eligibility; it produces the **research asset** those calls require.

---

## 4. Reporting checklist (congress Methods section)

Aligned with the SE case-study lineage — Runeson & Höst 2009
(DOI 10.1007/s10664-008-9102-8) and Runeson, Höst, Rainer & Regnell 2012 (Wiley;
DOI 10.1002/9781118181034) — plus CER reporting (Heckman et al. 2022;
McGill et al. 2023). Use Wohlin et al. 2012 (DOI 10.1007/978-3-642-29044-2) to
**keep experimental claim language out** of a case-study paper:

- [ ] Phenomenon, **case boundary**, and **unit of analysis** stated (Runeson design / Wiley handbook)
- [ ] Context: course level (post-intro FE II), language, AI policy, starter-code depth
- [ ] Sampling / cohort size and rationale (rich data, not power analysis — not Wohlin-style subject assignment)
- [ ] Ethics review status + consent process + consent rates (when known)
- [ ] Teacher–researcher dual role + custodianship / temporal blinding
- [ ] Data collection procedures mapped to Runeson collect/analyse steps (paper + Wiley depth)
- [ ] Data sources as **programming process data** classes (Fischer et al. 2024)
- [ ] Pseudonymization, retention, what was *excluded*
- [ ] Analysis procedures (codebook version, triangulation, negative cases)
- [ ] Scope of **transferability** (not statistical generalisability) — McGill; not experimental external validity language from Wohlin experiment chapters
- [ ] Limitations and threats to validity (case-study threats, not only experimental threats)
- [ ] Null / mixed findings reported
- [ ] Reporting structure readable against Runeson reader checklist / Wiley reporting guidance
- [ ] Explicit statement: **not** a controlled experiment (Wohlin strategy distinction)
- [ ] AI assistance in the *research writing* disclosed (publisher rules)

---

## 5. Evidence package for submission (artefacts)

| Artefact | Location / rule |
| -------- | ---------------- |
| Protocol + RQs | `STRAND-B-PEDAGOGICAL-DESIGN.md` (version pin by git SHA) |
| Ethics dossier | `ethics/` (templates public; signed forms offline) |
| Inclusion log | `ethics/analysis/` (create at analysis open — no PII) |
| Codebook | versioned markdown/YAML under `ethics/analysis/` |
| Pseudonym map | offline custody only |
| Quote/excerpt permissions | Consent item F / C4 per artefact |
| Teaching spine identity | git SHA of cohort handoff; history-isolation proof |

---

## 6. Abstract skeletons

### 6.1 Spanish — JENUI (≈200–250 words)

**Título (borrador):** *Aprender haciendo en un grupo agéntico: caso de diseño en ingeniería
front-end post-introductoria*

**Cuerpo:** contexto FE II · producto real TTOD · IA agentica + revisión humana · pregunta de
aprendizaje haciendo · diseño de caso / DBR · n pequeño y datos ricos · consentimiento y
minimización · fuentes de proceso (git, PRs, declaraciones IA, defensa) · análisis cualitativo
tras notas · principios de diseño (no efectos causales) · transferencia acotada · ética.

### 6.2 English — ITiCSE / SIGCSE (≈150–200 words)

**Title (draft):** *Learning by Doing in an Agentic Development Cohort: A Design-Based Case in
Post-Introductory Front-End Engineering*

**Body:** post-introductory gap · real product · agentic assistance under cold-review gates ·
rich process evidence · consent architecture for secondary use · case boundary and
transferability · design principles · explicit non-claims (no effect sizes).

Full expandable drafts: [`CONGRESS-ABSTRACTS-DRAFT.md`](CONGRESS-ABSTRACTS-DRAFT.md).

---

## 7. Work packages to a submittable paper

| WP | Deliverable | Gate |
| -- | ----------- | ---- |
| WP-E | Ethics clearance + custody log complete | Committee decision |
| WP-T | Teaching cycle completes; grades filed | Academic calendar |
| WP-C | Pseudonymized corpus + inclusion log | Consent B only |
| WP-A | Codebook v1 + thematic/process analysis | Preregistered questions |
| WP-W | Paper draft + cold review (independent reader) | Checklist §4 green |
| WP-S | Submit JENUI then EN venue | Abstract word limits |

---

## 8. What “fundable” means here

| Asset produced | Why funders / research groups care |
| -------------- | ---------------------------------- |
| Ethics-cleared protocol | Demonstrates research integrity capacity |
| Congress paper with DOI-backed methods | Countable research output |
| Open (sanitized) teaching artefact | Replicable object without leaking student PII |
| Claim registry + null honesty | Distinguishes this from hype/manifesto pedagogy |
| Positioning in post-intro GenAI gap | Competitive niche vs saturated CS1 Copilot studies |

Subsequent competitive applications may **cite** this paper and protocol; they are not invented
here.
