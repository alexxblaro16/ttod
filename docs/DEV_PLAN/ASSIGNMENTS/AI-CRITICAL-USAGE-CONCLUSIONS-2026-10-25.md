# Instructor conclusions — AI-critical usage + Evaluación TTOD (2026-10-25)

**Audience:** instructor only · **Not** for `docs/public/`  
**Companion web report:** [`ai-critical-usage-2026-10-25/index.html`](./ai-critical-usage-2026-10-25/index.html)  
**Rubric axis:** [AI Use Declaration & Oral Defence Rubric](https://ruvebal.github.io/web-atelier-udit/evaluation/shared/ai-declaration-oral-defence-rubric/) · Unit 6 · AI Practical Guide  
**Evidence:** merged tip PRs + AI Review Logs · `docs/uso-ia-team-4.md` · Moodle “Evaluación TTOD” free-text (8 submissions) · cohort PR scorecard Means Σ

> Draft for **human** qualification. Numbers below are provisional instructor aids, not Campus final marks until you confirm.

---

## 1. What this evaluation measures

Not “how much AI was used,” but **whether students can control assistance**: disclose, verify, reject, and own the diff (Unit 6 claim: *AI review is a second opinion; human review is the learning evidence*).

Four scored axes (same names as the shared rubric):

| Axis | Question in this cohort |
| --- | --- |
| **Defer** | Did they plan / constrain before prompting? |
| **Narrate** | Is the AI Review Log honest and specific? |
| **Critique** | Is there at least one defended REJECT (or equivalent non-acceptance)? |
| **Verify** | Can they name what *they* checked vs what the model ran? |

Eight observable **signs** (0–2 each → max 16) are defined in the HTML report. Cohort draft = signs → 0–10 band for AI-critical usage.

---

## 2. Cohort rollup (anonymized)

| Cohort | Seam | Tip Mean Σ | AI signs /16 | Draft AI-critical 0–10 | Standout control evidence |
| --- | --- | ---: | ---: | ---: | --- |
| **E1 Content** | Content | 96 | **15** | **9.0** | Mutation tests; plan-before-code; deliberate non-padding of tests; design-decision #68 |
| **E2 Graph** | Graph | 96 | **9** | **6.5** | Logs filled; verification commands named; thin REJECT trail; M2 admits struggle to use AI as primary tool |
| **E3 Oracle** | Oracle | 94 | **8** | **6.0** | Structured log on #42; M2 thin (“less IA… agents.md”); product strong, metacognition thin |
| **E4 PWA** | PWA | 96 | **14** | **9.0** | Cohort memo #74; rejected `tsc` drop; honest “AI ran checks, I did not claim them” |
| **E5 Accounts** | Accounts | 92 | **12** | **8.0** | Cookie vs PAT reject reasoning in M2; filled logs; plans-before-implement |

**Reading:** High tip Mean Σ ≠ automatic AI-critical excellence. Graph/Oracle shipped product well; their **control narrative** is thinner than Content/PWA.

---

## 3. Signs inventory (cohort counts)

| Sign | E1 | E2 | E3 | E4 | E5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| S1 AI Review Log present on tip PRs | 2 | 2 | 2 | 2 | 2 |
| S2 Verification named (test/cmd/browser) | 2 | 2 | 1 | 2 | 2 |
| S3 Explicit REJECT / non-accept + reason | 2 | 1 | 1 | 2 | 2 |
| S4 AI-run vs human-run distinguished | 1 | 1 | 1 | 2 | 1 |
| S5 Plan / defer before code | 2 | 1 | 1 | 1 | 1 |
| S6 Mutation / adversarial self-check | 2 | 0 | 0 | 1 | 0 |
| S7 M2 reflection cites concrete control | 2 | 1 | 0 | 1 | 2 |
| S8 Extended artifact (memo / decision doc) | 2 | 0 | 0 | 2 | 0 |
| **Total** | **15** | **9** | **8** | **14** | **12** |

---

## 4. Moodle “Evaluación TTOD” — draft grades (0–10)

Activity is free-text **M1** (Git) · **M2** (AI ritual) · **M3** (proposal). All marked *Necesita calificación* at export.  
**Map student → cohort for your eyes only** (do not paste into the public HTML).

### Scoring bands (same 0–10 geometry as the shared rubric)

| Score | M1 — Git | M2 — AI ritual | M3 — Proposal |
| ---: | --- | --- | --- |
| 9–10 | Names practices + concrete redesign (conflict ownership, amend, rename trap, checklist) | Names a control ritual + REJECT / verify example + what to keep | Engaged critique of the pedagogy (not only “liked / disliked”) |
| 7–8 | Clear learning + one usable improvement | Uses named (plan / log / verify) but thin REJECT | Interest with at least one substantive caveat |
| 5–6 | Short or mostly restates the prompt | Preference / struggle without Critique detail | Thin impression |
| 0–4 | Empty / off-prompt | Empty / off-prompt | Empty / dismissive without substance |

**Campus note (equal weights):**  
`Avg = (M1 + M2 + M3) / 3`, rounded to 1 decimal.  
**Optional AI-emphasis weight** (if you want Critique louder): `(M1 + 1.5×M2 + M3) / 3.5` — shown only in the last column as a check; **enter Avg unless you decide otherwise**.

| Cohort | Respondent (private) | M1 Git | M2 AI | M3 Proposal | **Avg** | Wtd (opt.) | Notes (one line each axis) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| E5 | Alejandro Blanco | **9.5** | **9.5** | **8.5** | **9.2** | 9.3 | M1: Ready for re-review, student-owned conflicts, rename trap, stacked branches. M2: AI Log as learning; cookie vs PAT reject. M3: recommends; time + Git absorbed by professor. |
| E1 | Gabriel Calvo | **9.0** | **9.0** | **8.5** | **8.8** | 8.9 | M1: checklist fetch→merge→check; grade branch sync; peer conflict review. M2: mutation tests; Bugbot = AI reviewing AI. M3: industry-like; stale sheets; early Git practice. *(PDF attachment)* |
| E1 | Gonzalo Sánchez | **7.0** | **9.5** | **8.5** | **8.3** | 8.6 | M1: wants README / Git lab (shorter). M2: plan-before-code vs stale facet sheets; keep agents rules; shorten tiny-PR log. M3: real-repo value; don’t trust docs/AI without code. |
| E4 | Pablo Novoa | **7.5** | **7.0** | **8.5** | **7.7** | 7.6 | M1: professional branches; asks CONTRIBUTING. M2: guide/debug/PR-review uses; “careful with free rein” but little REJECT. M3: reticent→fan; polish + feedback. *(Deeper Critique lives in memo #74, not this text.)* |
| E5 | Iván Herrera | **7.0** | **7.0** | **7.0** | **7.0** | 7.0 | M1: branches/PRs/cohort; bot review confusing. M2: plans + verify; keep shared project; Astro architecture hard. M3: learned despite cost; project not personal interest. |
| E1 | Rodrigo García | **6.0** | **5.5** | **7.0** | **6.2** | 6.0 | M1: issues+labels only (thin vs prompt). M2: vague “changed planning”; “task deps = paperwork”. M3: interesting but wants more / greenfield tasks. |
| E2 | Gonzalo Pérez | **7.0** | **5.0** | **6.0** | **6.0** | 5.7 | M1: bot workarounds + issues idea. M2: one line — hard to use AI as main tool. M3: one line — interesting group app. |
| E3 | Andrea Ávila | **4.0** | **5.5** | **3.5** | **4.3** | 4.6 | M1: clarity / redundant review only. M2: wants less AI; agents.md. M3: low interest, no substance. |

**Cohort means of Avg (informational):** E1 ≈ 7.8 · E2 = 6.0 · E3 = 4.3 · E4 = 7.7 · E5 ≈ 8.1.

### How this relates to §2 cohort AI-critical drafts

§2 scores **seam process evidence** (PR logs / memos). §4 scores **this Moodle reflection**. They should usually agree in direction (E5/E1 high, E3 low) but need not match exactly — e.g. E4’s #74 memo is stronger than Pablo’s M2 prose.

---

## 5. Conclusions for human qualification

1. **The protocol worked where students treated the AI Review Log as a decision surface, not paperwork.** E1 and E5 say so in their own words; E4 proved it with a rejected suggestion that would have weakened CI.
2. **Honesty about AI-run checks is a positive control signal**, not a penalty. E4’s “assistant ran the checks; I do not claim them as mine” matches the Practical Guide’s verification boundary better than vague “I verified everything.”
3. **Product excellence can coexist with thin metacognition.** E2/E3 mean Σ ≥ 94 with fewer critique signs — grade the *axes separately* so a strong Graph island does not auto-inflate AI-critical marks.
4. **Git hygiene was instructor-absorbed.** Multiple M1 answers ask for student-owned conflict practice. That is a course redesign note, not an AI-failure.
5. **Optional Tip 10 design memos** (Graph/Oracle/PWA/Accounts) never filed as PRs; only Content #68 and PWA #74 give extended process artifacts. Do not treat missing T10 as AI-log failure — it is a separate process tip.

### Recommended human next steps

- [ ] Confirm or adjust draft AI-critical 0–10 per cohort after oral notes (if any).
- [ ] Enter Moodle grades from §4 (or your override).
- [ ] Optionally ask E2/E3 for one written REJECT example retroactively (formative, not punitive).
- [ ] Keep `gradebook-import/` local-only (gitignored) — contains emails.

---

## 6. Sources used

- Unit 6 lesson · AI Practical Guide · AI Declaration / Oral Defence Rubric (Web Atelier)
- TTOD PR template AI Review Log · merged tip PRs (Content #61–#68, Graph #48–#78, Oracle #42, PWA #46–#74, Accounts #53–#59)
- `docs/uso-ia-team-4.md` (PR #74)
- `COHORT-PR-SCORECARD-2026-10-07.md` rollup
- Moodle export folder (2026-10-25) — local gitignored copy

_Generated 2026-10-25 as instructor base; not a published research claim._
