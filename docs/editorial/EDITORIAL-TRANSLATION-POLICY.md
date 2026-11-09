# TTOD Spanish translation — editorial policy

**Policy ID:** `TTOD-ES-POLICY`
**Version:** `1.0.0-draft`
**Status:** approved for S5E1 gate (`EDITORIAL_POLICY_APPROVED` 2026-11-08); glossary still `0.0.0` empty
**Authority:** Rubén Vega Balbás, product owner / general editor
**Parent plan:** [`PHASE-S5-BILINGUAL-CORPUS-TRANSLATION-PLAN.md`](../DEV_PLAN/PHASE-S5-BILINGUAL-CORPUS-TRANSLATION-PLAN.md) §§4, 7–8, 11–12
**Companion:** [`TTOD-ES-GLOSSARY.yml`](TTOD-ES-GLOSSARY.yml) · [`EDITORIAL-DECISIONS.md`](EDITORIAL-DECISIONS.md) · [`EDITORIAL-REVIEW-LEDGER.schema.json`](EDITORIAL-REVIEW-LEDGER.schema.json)

This document freezes the rules reviewers apply before judging the canonical Spanish edition. A
model may draft or flag; it may not decide correctness, accept, dispose, or release.

---

## 1. Target variety

- Contemporary international Spanish.
- Spain usage is preferred only where it does not reduce wider intelligibility across Latin America
  and other Spanish-reading cohorts.
- Do not localize the corpus to a single regional slang register.

## 2. Address, voice, and register

- Preserve the source’s impersonal, imperative, or dialogical stance.
- Keep aphoristic force: concision over explanatory expansion.
- Preferences of style never masquerade as defects (see §12 Severity).

## 3. Intentional ambiguity (binding)

When two readings of the English source materially affect the Spanish wording, record an editorial
note in the private review ledger. Do not let a model choose invisibly. Do not flatten productive
ambiguity into a single “clearer” reading merely because ambiguity is hard.

**Binding precedent — `img-086` “Coda con sabiduría”.** Product owner decision
`EDITORIAL-DECISION-2026-11-08-CODA` (2026-11-08): the canonical Spanish wording is correct and
intentional. Future reviewers treat this as authorial intent, not an open lexical defect. Do not
silently normalize to “Codifica” / “Codea” or auto-promote an alternate proposal. Keep
`PHASE-S4-REPORT.md` unchanged as historical evidence of the earlier literal-translation assessment.
See [`EDITORIAL-DECISIONS.md`](EDITORIAL-DECISIONS.md).

## 4. Taoist language, koans, and haiku

- Preserve semantic tension and rhetorical economy.
- Taoist sources guide composition and metaphor; they do not substantiate software, education,
  Athanor, or WPL factual claims.
- Do not claim syllabic or formal equivalence unless a human reviewer has scanned and recorded it.
- Prefer non-invention over ornamental paraphrase.

## 5. Wordplay and humor

- Preserve the joke, double meaning, or sonic play when it carries pedagogical force.
- If wordplay cannot be preserved without inventing content, record the choice (retain / gloss /
  transpose) in the ledger and prefer fidelity of teaching effect over decorative cleverness.
- Never invent a Spanish pun the English does not earn.

## 6. Technical literals and protected tokens

Never translate:

- literal syntax, filenames, commands, URLs, IDs;
- CSS properties, library names, standards identifiers;
- code fences and quoted identifiers meant as tokens.

Loanwords: retain established technical English only when normal Spanish professional usage
warrants it; never leave ordinary prose untranslated. Glossary preferred/forbidden terms bind once
human-approved; models may consult the glossary and must not add preferred terms to it.

## 7. Lineation and form

- Preserve meaningful line breaks, parallelism, deliberate repetition, and stanza-like structure.
- Haiku and lineated forms are high-risk; lost lineation is a form error, not a preference.

## 8. Punctuation and typography

- Use Spanish punctuation and quotation conventions.
- Do not “fix” English-style punctuation when doing so erases intentional rhythm or lineation.
- Typographic preference without meaning change is `preference`, not `major`.

## 9. `text` versus `teaches`

- `text` is the aphorism; `teaches` is the pedagogical gloss.
- `teaches` must not contradict, exceed, or invent claims beyond what the aphorism supports.
- Align both fields under Pass A (fidelity); judge Spanish clarity of both under Pass B.
- Blank `text`/`teaches`, prompt labels, or fence leakage are governance/critical defects.

## 10. Translation rights and attributed material

- Default content license remains CC BY-NC-SA 4.0 unless a record’s `rights` block says otherwise.
- Do not translate or adapt quotations whose rights or attribution do not authorize adaptation
  without a separate recorded rights decision.
- Proper names and attributed citations stay under explicit choice; unresolved rights → `hold`.

## 11. Gender and inclusivity

- Prefer natural non-marked formulations.
- Avoid mechanically expanding concise aphorisms for inclusivity marking when that destroys form.

## 12. Severity

MQM-inspired taxonomy adapted to aphorisms. Severity enum:

| Severity | Meaning | Effect on acceptance |
| --- | --- | --- |
| `critical` | reversed prescription, corrupted protected token, invented claim, unmarked omission that changes teaching, wrong language/relation/rights | blocks |
| `major` | material mistranslation, harmful terminology, lost form that changes reading, `teaches` contradiction | blocks |
| `minor` | small linguistic issue that does not change meaning or pedagogy | may accept-after-edit |
| `preference` | alternate wording with no defect | never blocks; never relabeled as defect |

Categories: accuracy · terminology · linguistic quality · style/register · locale · form ·
pedagogy · governance.

## 13. Adjudication (two passes)

Every in-scope pair receives two conceptually separate passes (S5 plan §7):

### Pass A — bilingual fidelity

Compare source and target side by side: meaning, negation, agency, modality, technical literals,
omissions/additions, metaphor, ambiguity, lineation, and `teaches` alignment. Read the source
before any model rationale.

### Pass B — Spanish editorial

Read the Spanish independently for idiom, rhythm, punctuation, concision, register, consistency,
and pedagogical clarity.

Decision states: `accept` · `accept-after-edit` · `second-opinion` · `retranslate` · `hold` ·
`reject`.

High-risk items (poetry/haiku, wordplay, culturally specific metaphors, legal/ethical claims,
attributed material, any critical error) require a second human reading before acceptance where
feasible.

## 14. Reviewer independence

- One qualified person may perform both passes only if the edition statement discloses that
  limitation.
- Do not turn one person’s review into a claim of independent dual review.
- Cold audit (S5E5) samples accepted pairs; it does not replace Pass A/B.
- Models and scripts may flag candidates; they cannot write a human decision into the ledger.

## 15. Glossary authority

- Versioned file: `TTOD-ES-GLOSSARY.yml`.
- Only human-approved terms enter. Empty glossary is valid until terms are curated.
- A model may consult; it may not add preferred terms autonomously.

## 16. Private ledger

Item-level notes live only at the product-owner-approved private location (env
`TTOD_EDITORIAL_LEDGER` for gates). Public reports hold aggregate evidence and necessary
provenance only. Schema: [`EDITORIAL-REVIEW-LEDGER.schema.json`](EDITORIAL-REVIEW-LEDGER.schema.json).
Owner recorded path/access as `EDITORIAL-DECISION-2026-11-08-LEDGER-LOCATION`
(`_private/editorial/EDITORIAL-REVIEW-LEDGER.json`; absolute canonical
`/Users/ruvebal/src/ttod/_private/editorial/EDITORIAL-REVIEW-LEDGER.json`) and froze the
S5E1 gate with `EDITORIAL_POLICY_APPROVED` on 2026-11-08.
