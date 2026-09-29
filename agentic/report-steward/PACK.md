---
name: report-steward
purpose: Evidence-state reporting workflow and the public-privacy watcher that CI runs.
surfaces: [agents, skills, rules, scripts]
landings: [.cursor/rules/public-privacy.mdc, .cursor/rules/spanish-research-prose.mdc]
mirrors: []
locks: [.github/workflows/public-docs-pages.yml, Makefile, tests/test_public_privacy_watcher.py]
external_readers: [The studio cascade-forge skill mentions this pack by name]
status: tracked
---

# Evidence-State Reporting Pack

Maintained by `@crea-comm.net` for reusable, agent-oriented engineering reports.

| Surface | Purpose |
| --- | --- |
| `agents/report-steward.md` | bounded role and operating contract |
| `skills/evidence-state-report/SKILL.md` | reusable report workflow |
| `skills/public-artifact-privacy/SKILL.md` | public/student artifact privacy gate |
| `skills/evidence-state-report/references/report-contract.md` | report schema and claim tests |
| `rules/evidence-reporting.md` | concise repository rule |
| `rules/public-privacy.md` | public-output privacy boundary |
| `rules/spanish-research-prose.md` | Spanish ethics/institutional prose (columna metodológica; italics for loanwords) |
| `scripts/check_public_privacy.py` | deterministic tracked-text watcher (paths, hosts, phases, empty `<a>`) |

The pack is source material, not an automatic installation. A host studio may map the agent,
skill, and rules into its own discovery directories. Keep the files together so the privacy
watcher and reporting contract evolve as one governed method.

CI (`public-docs-pages.yml`) runs the same watcher on `_site-public` before htmlproofer. Agents
must clear the watcher locally on `docs/public` (and diagram assets) before pushing — see
`skills/public-artifact-privacy/SKILL.md` defect catalog.
