---
name: public-docs-i18n
description: >-
  Author and translate the mandatory English/Spanish TTOD public documentation
  site at docs/public. Use when adding, editing, or localizing Jekyll pages
  under docs/public or docs/public/es, when the public index flagship quote
  must be cited, or when a Spanish documentation lane is requested. Reuses
  Phase S4/S5 quote-translation discipline and local Ollama qwen3.8:27b; never
  hand-edits ttod.yml.
---

# Public documentation i18n

Mandatory bilingual publication source: `docs/public` (English, `lang: en`) and
`docs/public/es` (Spanish, `lang: es`). One Jekyll site, two language trees,
shared chrome and visual system.

## Skill stack (do not substitute)

| Need | Use | Do not use |
| --- | --- | --- |
| Quote read / propose | `~/src/.cursor/skills/ttod-bridge/SKILL.md` | parsing `ttod.yml` |
| Quote Spanish sister | `python cli.py translate-draft <id> --to es --model qwen3.8:27b` then human `proposal accept` | inventing locale-suffixed IDs |
| Editorial policy for Spanish | `docs/DEV_PLAN/PHASE-S5-BILINGUAL-CORPUS-TRANSLATION-PLAN.md` §4 | scholar-editor (essay voice) |
| Audience / structure | `documentation-forger` | dumping internal `docs/research` |
| Publication privacy | `agentic/report-steward/skills/public-artifact-privacy/SKILL.md` | skipping the watcher |
| Information-for-users | IEEE 1063 task structure already used in the English pages | expanding claims |

`qwen3.8:27b` is the proven S4/S5 baseline. Call Ollama through the Python/HTTP
API (`ttod_core.translation.call_ollama_generate` or `ollama.Client`), never
`ollama run`. Check `ollama ps` first. Model output is a draft; a named human
accepts quotes and cold-reads pages.

## Quote rules

- Cite accepted IDs only. The English public-index flagship is `wis-033`. The
  Spanish index cites its sister `wis-034` (`translation_of: wis-033`).
- Never invent `wis-033-es`. If a new flagship has no sister, draft with
  `translate-draft`; do not put ungoverned Spanish quote text in the site.
- IDs, commands, paths, Liquid, DOIs, license names, and code stay untranslated.

## Page rules

- English permalinks stay `/…/`. Spanish permalinks are `/es/…/`.
- Front matter: `lang`, `title`, `eyebrow`, `description`, `permalink`. Translate
  values, not keys.
- Preserve hedging. Do not promote planned work to implemented, or design
  rationale to learning-effect evidence.
- No internal phase shorthand in public prose (`R6`, `Q4`, `RC0`, …). Prefer Entrega / Unit /
  maturity language. Never ship `host.docker.internal` or other `*.internal` hostnames in public
  pages or Archify diagram HTML under `docs/public/assets/diagrams/`.
- Citation fragment targets: `<span id="ref-…"></span>` — never empty `<a id="ref-…"></a>`
  (htmlproofer: “a tag is missing a reference”).
- After edits: privacy watcher on source and rendered output; htmlproofer with
  `--swap-urls '^/ttod/:/'`. When publishing Archify HTML, follow
  `agentic/report-steward/skills/public-artifact-privacy/SKILL.md` § Archify checklist
  (including `#focus-repository` `href`).

## Drafting a Spanish page

1. Read the English sibling. Translate that artifact, not a nearby plan.
2. Call `scripts/translate_public_docs.py` (qwen3.8:27b, temperature 0.3).
3. Pass B: read the Spanish alone for idiom, rhythm, and pedagogy.
4. Set permalink under `/es/` and `lang: es`. Wire nav via `_data/navigation.yml`.
5. Rebuild and run the privacy watcher.
