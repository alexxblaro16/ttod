<!--
Inheritance from Profield STEM-code meta-research runs into TTOD Strand B.
Operator-readable; cites Profield digests as discovery maps — Chicago public cites
only where DOIs are already confirmed in those digests or TTOD public methodology.
Author: Rubén Vega Balbás, PhD · 2026-09-25.
-->

# Profield STEM-code inheritance → TTOD Strand B

**Sources (operator paths, not public citations):**

| Profield run | What it is | Maturity in Profield |
| ------------ | ---------- | -------------------- |
| `runs/stem-code-research-methodology/` | Omnibus meta-field + Pass 1–3 digest | Digested 20260818 (130 rows; CER backbone confirmed) |
| `runs/stem-code-cohort-case-study-design/` | Child FieldSpec: small-n CER / consent / process evidence | Pass-1 prompt only (scope carried via omnibus + CR2) |
| `runs/stem-code-grounding-provenance/` | Child FieldSpec: discover≠cite / page-addressable evidence | Pass-1 prompt only (scope carried via omnibus digest) |
| `runs/stem-code-ai-epistemology-critique/` | Child FieldSpec: normative vs empirical; manifesto vs evidence | Digested 20260819 |

**Parent scoping note:** `runs/stem-code-research-methodology/00-field-scope.md` — three literatures
must not be mashed into one “methods tip sheet.” TTOD Strand B **composes** them; it does not
collapse them.

---

## 1. Durable core (must appear in every Strand B output)

From `00-field-scope.md` and the verified omnibus digest:

1. **Discover ≠ cite** — vector/GraphRAG hits are discovery; cite-grade needs a stable source
   object and a supporting passage.
2. **Consent before secondary use** — instructional collection ≠ research eligibility;
   custodian independence for teacher-researchers.
3. **Small n → depth and honesty** — not effect sizes, causal claims, or population inference.
4. **Pre-consent process data = design context**, not analytic research data.
5. **Null results and documented gaps are publishable** when reported honestly.
6. **Normative instruments ≠ empirical measurements** (UNESCO/policy ≠ learning effects).

---

## 2. What Strand B takes from each child

### 2.1 Cohort / case-study design (`stem-code-cohort-case-study-design` + CR2 + omnibus)

| Inherited rule | Operationalization in TTOD |
| -------------- | -------------------------- |
| Case boundary + unit of analysis (McGill et al. 2023) | Case = FE II 2026–27 TTOD Oracle cohort; unit = **pair/solo seam work** nested in **cohort as case** |
| Rich vs big data (Brown & Guzdial 2024) | Prefer rich process traces over large anonymous submission dumps |
| Programming process data + consent (Fischer et al. 2024) | Treat git/PR/AI-declaration/defence as process data under ethics + consent forms A/B |
| Secondary use ≠ original collection | Ethics package C1/B item; analysis after grades |
| Independent custody / temporal blinding | `SIGNED-CONSENTS-CUSTODY.md`; instructor blind until grades filed |
| Null/gap as finding (McGill) | Reporting plan requires disconfirming cases |
| Experience report / design principles from declared pilots | Primary publication genre for cycle 1 |
| Individual vs collective unit | Report both: seam-level trajectories **and** cohort-level collaboration patterns; no false equivalence across degrees until composition confirmed |
| Bilingual instruments | ES primary for ethics/participants; EN for international venues |
| Open artefact auditability | Versioned teaching spine + phase reports as pre-approval verification of the *object*, not of learning claims |

### 2.2 Grounding / provenance (`stem-code-grounding-provenance` + omnibus)

| Inherited rule | Operationalization in TTOD |
| -------------- | -------------------------- |
| Discover ≠ cite; retrieval jitter | Literature section uses DOI-verified warrants; DevIAC/Athanor hits stay in discovery notes |
| Two audit trails | (1) how sources entered the bibliography; (2) which passage supports each claim |
| PROV / FAIR / RO-Crate as *representation* ideals | Research corpus packaging: pseudonym map, inclusion log, codebook version — **without** open-publishing student traces |
| Similarity ≠ entailment | Never cite a vector snippet as Chicago evidence |
| Fabricated DOI worse than declared gap | Claim registry + `[UNVERIFIED-GAP]` discipline |

### 2.3 AI epistemology critique (`stem-code-ai-epistemology-critique`)

| Inherited rule | Operationalization in TTOD |
| -------------- | -------------------------- |
| Code produced ≠ learning demonstrated | Oral defence + process triangulation mandatory; product polish alone is not an outcome |
| Scaffolding vs cognitive offloading (Liu, Fan & Pan 2026) | RQ-B2/B3 sensitize to offloading without treating GT findings as TTOD effects |
| Learning visibility / measurement (Davalos & Zhang 2026) | Process traces as *visibility*, not surveillance theatre |
| Normative ≠ empirical | Ethics/UNESCO/CS2023 motivate scope; do not count as efficacy |
| Manifesto ≠ evidence | TTOD aphorisms and agentic “governance rhetoric” are pedagogical objects, not CER warrants |
| HITL accept/reject under agentic PRs | Cold-review / human merge gates are part of the *intervention description* |
| Post-introductory GenAI less mature than CS1 | **Positioning advantage:** FE II is post-intro interface engineering — fits the ITiCSE 2026 WG-declared gap |

---

## 3. Confirmed methodological backbone (DOI-safe for congress Methods)

Prefer these as *methods warrants* (already Pass-2 confirmed in the omnibus digest):

| Source | DOI | Use in Strand B |
| ------ | --- | --------------- |
| Runeson & Höst 2009 (Empir. Softw. Eng.) — SE case-study guidelines | 10.1007/s10664-008-9102-8 | Compact case process + checklists (Ahmes coat `…30849aa9`) |
| Runeson, Höst, Rainer & Regnell 2012 (Wiley) — *Case Study Research in Software Engineering* | 10.1002/9781118181034 | Full handbook; cited from Wohlin Ch. 5 as [146]; **no separate Ahmes coat yet** — bibliographic cite OK |
| Wohlin, Runeson, Höst, Ohlsson, Regnell & Wesslén 2012 — *Experimentation in Software Engineering* | 10.1007/978-3-642-29044-2 | Strategy map (survey/experiment/case); Ch. 5 case studies; refuse experimental overclaim (Ahmes coat `…764e4900`) |
| Heckman et al. 2022 (TOCE) — empiricism & reporting norms | 10.1145/3470652 | CER reporting checklist |
| Brown & Guzdial 2024 (SIGCSE) — rich vs big data | 10.1145/3626252.3630813 | Epistemic stance for small n |
| McGill et al. 2023 (ITiCSE WG) — sound CER | 10.1145/3623762.3633495 | Transferability, consent reporting, null results |
| Fischer et al. 2024 (ICER) — process data + consent | 10.1145/3632620.3671125 | Process-data ethics architecture |
| Prather et al. 2024 (ICER) — benefits/harms | 10.1145/3632620.3671116 | Separating performance from learning (motivation) |
| Liu, Fan & Pan 2026 | 10.1186/s40594-025-00592-w | Scaffolding/offloading sensitizing concepts |
| Generative AI in Post-introductory Computing (ITiCSE WG 2026) | 10.1145/3760545.3783970 | Gap positioning for FE II |

Domain/motivation sources already on TTOD public methodology remain (Shihab 2025, López-Pernas 2025,
Garcia 2025, Nikolić 2026, Davalos & Zhang 2026, CS2023).

---

## 4. What Strand B refuses (from “What the field refuses to treat as evidence”)

- Working program / polished UI / high mark ≠ evidence of cognitive process.
- Local classroom observation ≠ effect-size for “students” in general.
- Vector snippet ≠ scholarly citation.
- UNESCO / institutional AI policy ≠ learning effect.
- Vendor tutorial / manifesto ≠ empirical CER.
- Student self-report that AI “helped” ≠ demonstrated learning gain (alone).
- “Platform already logged it” ≠ consented research use.
- Missing result from one query ≠ demonstrated research gap (needs systematic procedure).

---

## 5. Publication consequence

Cycle-1 contribution is a **declared pilot / experience report / design-principles note** with
full ethics and claim boundaries — not an efficacy RCT. That is the genre that is both
**honest to n** and **fundable as a congress research product** (see
[`STRAND-B-CONGRESS-PUBLICATION-PLAN.md`](STRAND-B-CONGRESS-PUBLICATION-PLAN.md)).
