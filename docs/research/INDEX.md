<!--
TTOD research map — two strands, one ethics package.
Author: Rubén Vega Balbás, PhD · ruvebal@crea-comm.net · 2026-09-25.
-->

# TTOD research — map and current status

This folder is the **internal** research home. Public-facing summaries live under
[`../public/research/`](../public/research/). Do not treat TTOD quotes as research evidence
(`AGENTS.md`).

---

## Two strands (do not entangle)

| Strand | Question family | Status | Canonical doc |
| ------ | --------------- | ------ | ------------- |
| **A — Philosophical / cybernetic** | How do eternal, ontological, gnoseological, epistemological, and transcendental knowledge traditions relate to cybernetics and contemporary technical practice? | **Parked.** Design and corpus work continue; no ethics submission, no student participants, no empirical claims from this strand. | [`STRAND-A-PHILOSOPHICAL-PARKED.md`](STRAND-A-PHILOSOPHICAL-PARKED.md) |
| **B — Pedagogical / CER (Front-End II)** | Can participation as a developer in a real, agentic-assisted application, inside a cohort of peers, function as a learning activity with observable pedagogical outcomes — *learning by doing*? | **Active.** Pedagogical framing approved by the department in advance; cohort informed consent obtained for participation as described in the ethics package; **institutional ethics-committee review in progress** (submission prepared 2026-09). | [`STRAND-B-PEDAGOGICAL-DESIGN.md`](STRAND-B-PEDAGOGICAL-DESIGN.md) |

| [`DEPARTMENT-DECISION-BRIEF.md`](DEPARTMENT-DECISION-BRIEF.md) | Internal pedagogical decision brief (context) |
| [`institutional/`](institutional/) | **Separate pack** — formal A1 letter to Sandra/Fernando + production budget ≥24 mo + PDF |

Strand A never uses student coursework as evidence. Strand B never imports Strand A's
philosophical claims as empirical warrants.

---

## Ethics and consent package (Strand B)

| Document | Role |
| -------- | ---- |
| [`ethics/README.md`](ethics/README.md) | Package index, custody rules, what is / is not in git |
| [`ethics/CHECKLIST-COMITE-ETICA-ES.md`](ethics/CHECKLIST-COMITE-ETICA-ES.md) | Map vs Comité de Ética comunicado requirements |
| [`ethics/ETHICS-COMMITTEE-SUBMISSION-ES.md`](ethics/ETHICS-COMMITTEE-SUBMISSION-ES.md) | Cover letter / solicitud |
| [`ethics/PROTOCOLO-INVESTIGACION-COMPLETO-ES.md`](ethics/PROTOCOLO-INVESTIGACION-COMPLETO-ES.md) | Full protocol (ES) |
| [`ethics/INSTRUMENTOS-RECOLECCION-DATOS-ES.md`](ethics/INSTRUMENTOS-RECOLECCION-DATOS-ES.md) | Data-collection instruments inventory |
| [`ethics/AUTORIZACIONES-INSTITUCIONALES-ES.md`](ethics/AUTORIZACIONES-INSTITUCIONALES-ES.md) | Institutional authorizations checklist |
| [`ethics/PLAN-MANEJO-DATOS-ES.md`](ethics/PLAN-MANEJO-DATOS-ES.md) | Data management plan |
| [`ethics/DATA-MINIMIZATION-STATEMENT.md`](ethics/DATA-MINIMIZATION-STATEMENT.md) | What is processed, what is not |
| [`ethics/PARTICIPANT-INFORMATION-SHEET-ES.md`](ethics/PARTICIPANT-INFORMATION-SHEET-ES.md) | Participant information sheet (ES) |
| [`ethics/PARTICIPANT-CONSENT-FORM-ES.md`](ethics/PARTICIPANT-CONSENT-FORM-ES.md) | Consent form template (ES) |
| [`ethics/PARTICIPANT-INFORMATION-SHEET-EN.md`](ethics/PARTICIPANT-INFORMATION-SHEET-EN.md) | Participant information sheet (EN) |
| [`ethics/PARTICIPANT-CONSENT-FORM-EN.md`](ethics/PARTICIPANT-CONSENT-FORM-EN.md) | Consent form template (EN) |
| [`ethics/SIGNED-CONSENTS-CUSTODY.md`](ethics/SIGNED-CONSENTS-CUSTODY.md) | Where **signed** forms live (never in this repository) |

**Finding (2026-09-25 audit):** before this package, the repository contained consent *taxonomy*
and *requirements* (`COHORT-CASE-PROPOSAL.md` §6) but **no** participant information sheet and
**no** consent form template. Those documents are created here. Signed originals must remain
outside git — see custody note.

---

## Profield inheritance and congress product

| Document | Role |
| -------- | ---- |
| [`PROFIELD-STEM-CODE-INHERITANCE.md`](PROFIELD-STEM-CODE-INHERITANCE.md) | What Strand B takes from the four STEM-code Profield runs |
| [`STRAND-B-CONGRESS-PUBLICATION-PLAN.md`](STRAND-B-CONGRESS-PUBLICATION-PLAN.md) | Fundable congress publication plan, checklist, venues |
| [`CONGRESS-ABSTRACTS-DRAFT.md`](CONGRESS-ABSTRACTS-DRAFT.md) | JENUI (ES) + ITiCSE/SIGCSE (EN) abstract drafts |

---

## Keeping public docs updated (when internal research changes)

Internal research (`docs/research/**`) does **not** auto-publish. Public readers see only
[`docs/public/`](../public/) (EN) and [`docs/public/es/`](../public/es/) (ES).

**Workflow whenever Strand B / ethics / methods claims change:**

1. **Edit English first** under `docs/public/…` (e.g. `research/methodology.md`, `research/index.md`).
   Preserve hedges; no phase shorthand (`R6`, `Q4`); no student PII; DOIs stay untranslated.
2. **Mirror Spanish** under `docs/public/es/…` — use skill
   [`agentic/public-docs-i18n/skills/public-docs-i18n/SKILL.md`](../../agentic/public-docs-i18n/skills/public-docs-i18n/SKILL.md)
   (Cursor landing: `.cursor/skills/public-docs-i18n/`). Translate the English sibling, not a plan
   dump; optional helper `scripts/translate_public_docs.py` (Ollama `qwen3.8:27b`), then human
   Pass B cold-read.
3. **Wire nav** if a new page: `docs/public/_data/navigation.yml` (EN + ES).
4. **Privacy gate:** `make docs-privacy` (or
   `python3 agentic/report-steward/scripts/check_public_privacy.py docs/public`).
5. **Build:** `make docs` · serve locally with `make docs-serve`.
6. **Link check (as CI):** htmlproofer with `--swap-urls '^/ttod/:/'` on the built site
   (see `public-artifact-privacy` skill).
7. **Do not** paste internal paths (`PROFIELD-…`, Ahmes coat IDs, signed-consent custody) into
   public prose — keep those in `docs/research/` only.

**What stays internal-only:** ethics templates with operational custody tables, claim registry
labels, Profield run paths, signed-consent locations.

---

## Legacy / supporting docs (still useful; status superseded where noted)

| Doc | Use now |
| --- | ------- |
| [`overview.md`](overview.md) | Institutional cover letter — updated to point at Strands A/B |
| [`RESEARCH-LINE.md`](RESEARCH-LINE.md) | Older RQ set; **superseded for Strand B framing** by `STRAND-B-…`; keep for venue ladder / risk register |
| [`COHORT-CASE-PROPOSAL.md`](COHORT-CASE-PROPOSAL.md) | Department request history; consent taxonomy still authoritative |
| [`DEPARTMENT-DECISION-BRIEF.md`](DEPARTMENT-DECISION-BRIEF.md) | Pedagogical authorization brief |
| [`PI-RESEARCH-BRIEF.md`](PI-RESEARCH-BRIEF.md) | Research-group note |
| [`PITCH-INVESTIGACION-TTOD-ES.md`](PITCH-INVESTIGACION-TTOD-ES.md) | Decision pitch (update status against Strand B) |
| [`guides/CLAIM-REGISTRY.md`](guides/CLAIM-REGISTRY.md) | Claim wording control |

---

## Studio method (how this package was (re)grounded)

1. **Profield STEM-code meta-field** (`stem-code-research-methodology` + three children) —
   durable core and DOI-confirmed methods backbone (Runeson lineage + Wohlin contrast; Heckman, Brown & Guzdial, McGill, Fischer);
   mapped in `PROFIELD-STEM-CODE-INHERITANCE.md`.
2. **Discovery (not citation):** DevIAC vector search over `profield-frontend-pedagogy` /
   related Ahmes-derived indexes.
3. **Public warrants DOI-listed** in [`../public/research/methodology.md`](../public/research/methodology.md)
   — methods backbone now includes Runeson & Höst 2009 / Runeson et al. 2012 (Wiley) /
   Wohlin et al. 2012 / Heckman / Brown & Guzdial / McGill / Fischer / Prather.
4. **Athanor cite-grade pass:** preferred when `DATABASE_URL` is available; re-run before journal
   submission.
5. **Privacy:** no signed consents, student names, emails, or grade sheets in this repo.

---

## One-sentence status for external readers

Strand B is a **design-based, rich-data case study** of learning-by-doing in a real
agentic-assisted front-end product, with **department pedagogical approval**, **participant
informed consent**, **ethics-committee review underway**, and a **congress-first publication
plan** (JENUI → ITiCSE/SIGCSE) grounded in Profield STEM-code methodology inheritance; Strand A
remains a separate philosophical programme with **no human subjects**.
