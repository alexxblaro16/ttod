<!--
Declaración de minimización de datos — Strand B.
-->

# Data minimization and personal-data posture (Strand B)

**Purpose:** support the ethics-committee submission and any DPO consultation.  
**Related:** [`ETHICS-COMMITTEE-SUBMISSION-ES.md`](ETHICS-COMMITTEE-SUBMISSION-ES.md),
[`../STRAND-B-PEDAGOGICAL-DESIGN.md`](../STRAND-B-PEDAGOGICAL-DESIGN.md).

---

## 1. Claim for the committee (careful wording)

The study is designed so that **student personal data are not placed at stake** as an object of
**research** interest (the analysis corpus):

- No special-category data (health, ideology, religion, sexual life, biometrics, ethnic origin).
- No research survey of private life, family, finances, or health.
- No research collection of location tracking, device fingerprinting, or covert monitoring.
- No publication of student names, emails, photographs, or identifiable GitHub handles
  **inside the research corpus or research papers** as identifiers of research subjects.
- Research analysis, if authorized, uses a **pseudonymized process corpus** derived from
  artifacts already produced for assessment.

**Product authorship is a separate plane:** cohort developers are **named as authors** in the
repository *README* (*Development Team*) for the product areas they build, and code contributions
are under MIT ([`LICENSE-CODE`](../../../LICENSE-CODE)). That naming is pedagogical / product
equity, not research publication of a personal-data dataset. See
[`AUTORIA-LICENCIA-COHORTE-ES.md`](AUTORIA-LICENCIA-COHORTE-ES.md). Optional image use in
communications remains consent item **G**.

**Honest legal note:** under GDPR / LOPDGDD, pseudonymized process data can still constitute
personal data if re-identification is reasonably possible. The protocol therefore:

1. strips direct identifiers before research use;
2. keeps the research corpus confidential and access-restricted;
3. sets retention and destruction rules;
4. never treats the corpus as open anonymous data;
5. does **not** treat *README* authorship credit as a substitute for research consent (B) or
   image consent (G).

The pedagogical **grades and identifiable academic records** remain in ordinary teaching systems
and are **outside** the research corpus.

---

## 2. What may enter the research corpus (after consent + ethics clearance)

| Artifact | Transform before research use |
| -------- | ----------------------------- |
| Commit / PR narrative text | Replace handles/names with `P01…Pn`; redact emails/URLs that identify |
| AI-use declaration text | Same pseudonymization; keep pedagogical content |
| Automated check summaries | Aggregate or pseudonymize paths that encode usernames |
| Oral-defence structured notes | No audio/video unless separate C3 consent; notes without identifiers |
| Code excerpts for publication | Separate C4 diffusion consent; prefer non-identifying snippets |

## 3. What never enters the research corpus

- Student civil names, emails, phone numbers, national IDs
- Grade sheets, LMS gradebook exports
- Instructor private feedback tied to identity (unless fully redacted and consented)
- Non-consented peers’ artifacts
- Strand A philosophical materials framed as student evidence

## 4. Legal bases (to confirm with institutional DPO)

Suggested framing for consultation (not a legal opinion):

| Processing | Candidate basis |
| ---------- | --------------- |
| Ordinary teaching / assessment | Public-interest / contractual academic relationship (institutional) |
| Research secondary use of pseudonymized process artifacts | **Informed consent** (Art. 6 GDPR / LO 3/2018), with withdrawal rights as stated in the information sheet |

## 5. Retention

| Store | Retention (proposed) |
| ----- | -------------------- |
| Signed consent forms | Institutional rule (typically study end + ≥5 years or local equivalent) — private custody |
| Pseudonymized research corpus | Until thesis/article revision complete, then destroy or archive under institutional research-data policy |
| Public papers | Aggregated / non-identifying findings only |

## 6. Controllers and processors

Fill before submission:

| Role | Name / unit |
| ---- | ----------- |
| Principal investigator | Rubén Vega Balbás, PhD |
| Independent consent / data custodian (if designated) | _[to be named]_ |
| Data controller (institution) | UDIT — _[confirm with DPO]_ |
| Processors | None beyond institutional systems unless named |
