---
description: Strict TTOD YAML editing — schema v3, IDs, tags, collections, validation. Agent contract AGENTS.md.
globs: ttod.yml
alwaysApply: false
---

# TTOD Editing Discipline

Read [`AGENTS.md`](../AGENTS.md) first. **Do not hand-edit `ttod.yml`.** All writes go through the CLI
and `ttod_core/repository.py` atomic transactions (`proposal accept`, `add`, `deprecate`, `erase`).

```bash
. .venv/bin/activate && python cli.py validate --strict
```

## Quote identity

- **Never delete quotes** — set `status: deprecated` (or `erase` with institutional authority).
- **IDs are immutable** once published. Format: `{section_prefix}-{NNN}` (e.g. `arch-014`, `a11y-001`).
- **ID prefix must match section** — `arch-*` → `architecture`, `a11y-*` → `accessibility`, etc.
- When renaming an ID (rare), update **every** `related` reference and any `collections.*.ids` entry.

## v3 required fields (mechanically enforced)

Every quote must include: `schema_version`, `text`, `section`, `level`, `origin`, `content_digest`.
Pre-v3 records without origin were migrated to `legacy-unknown` — do not silently change them to `human`.

`blackbox` origin requires a validated `validation` block with `reviewer_id` and `status: validated`.

Default `rights` for studio content: see Q0 decision (`CC-BY-NC-SA-4.0`, holder `ruvebal@crea-comm.net`).

## Adding quotes (CLI only)

1. `python cli.py proposal create …` then `proposal accept --reviewer-id …`, **or**
   `python cli.py add --reviewer-id …` (same transaction path).
2. Pick section; CLI allocates the next ID under lock from `meta.last_id_by_section`.
3. Tags must exist in `tag_taxonomy` (extend taxonomy first if needed).
4. Never hand-edit `meta.total_quotes`, `last_id_by_section`, or collection counts — the repository
   recomputes them atomically on accept.

## Collections & graph

- `collections.*.ids` must reference live quote IDs only.
- All `related` targets must exist.

## Bilingual quotes — choosing `lang` and adding a `translation_of` edge

Post-Phase S (S1′/S2′), every quote record carries a required `lang` field and the live
`ttod.yml` is fully migrated: `schema_version: '3.1.0'` on every quote, `meta.version: 3.1.0`,
`meta.languages: [en]` (today — the corpus is still 100% English; this grows as Spanish quotes
are added). The examples below are the current live shape, not a pre-migration hypothetical.

### Checklist: authoring a brand-new quote (not a translation)

1. Decide the quote's language and set `lang` to its ISO 639-1 code (`en`, `es`, …) — a bare
   two-letter pattern in the schema, not a closed enum, so a third language needs no schema
   change.
2. Pick section + next free ID exactly as always (`meta.last_id_by_section`) — `lang` does not
   change ID allocation.
3. Everything else in "Adding quotes (CLI only)" above applies unchanged.

### Checklist: authoring a translation of an existing quote

1. Read the source quote (`python cli.py` read/search, or the ttod-bridge adapter) and confirm its
   `id`, `lang`, and `status: active`. A translation must target an **active** record — translating
   a deprecated/erased quote is a data-quality question for a human, not something the tooling
   should quietly permit.
2. **ID policy — no locale suffixes (S0 decision 6).** The translation is a **separate canonical
   record** with its own next-free section-number ID, allocated the normal way via
   `meta.last_id_by_section` at `proposal accept` / `add` time. A Spanish twin of `arch-001` is
   the next free `arch-NNN` (e.g. `arch-060`) — **never** `arch-001-es` or any other
   locale-suffixed scheme. `lang` and the `translation_of` edge already carry the
   language/lineage information; the ID stays a plain identity, exactly like every other quote.
3. Set the translation's own `lang` to the target language — it **must differ** from the source
   quote's `lang` (`TRANSLATION_SAME_LANGUAGE` rejects a same-language edge).
4. Add a `relation_edges` entry pointing at the source:
   ```yaml
   relation_edges:
     - target: arch-001
       relation_type: translation_of
   ```
5. **Star, not chain.** The `target` must itself carry no outgoing `translation_of` edge — point
   at the original, not at another translation (`TRANSLATION_CHAIN` rejects a translation-of-a-
   translation). "What is the canonical source" must stay a one-hop question.
6. **At most one active translation per `(target, lang)` pair** — if an active Spanish translation
   of `arch-001` already exists, a second one publishing to `status: active` trips
   `TRANSLATION_DUPLICATE_ACTIVE`. A second draft/candidate is fine to compare before accepting
   either; only one may be `active` at a time.
7. `section` should normally match the source's `section` — a mismatch is only a warning
   (`TRANSLATION_SECTION_MISMATCH`) non-strict, but an error under `--strict`, so resolve it
   deliberately rather than leaving it as an accident.
8. Full example — an English original and its Spanish translation as separate, complete records:
   ```yaml
   - id: arch-001
     schema_version: '3.1.0'
     text: 'The module that knows its boundaries serves the whole.'
     section: architecture
     level: master
     lang: en
     tags: [architecture, boundaries]
     teaches: 'Clear interfaces prevent modules from absorbing responsibilities that do not belong.'
     origin: human
     status: active
     rights:
       access: public
       license: CC-BY-NC-SA-4.0
       holder: ruvebal@crea-comm.net
       permission_basis: rights-holder-relicense-2026-08-18
     content_digest: '<sha256 via TTOD-C14N-v1>'
     created_at: '2025-12-06'

   - id: arch-060
     schema_version: '3.1.0'
     text: 'El módulo que conoce sus límites sirve al todo.'
     section: architecture
     level: master
     lang: es
     tags: [architecture, boundaries]
     teaches: 'Las interfaces claras evitan que los módulos absorban responsabilidades que no les corresponden.'
     origin: human
     status: active
     relation_edges:
       - target: arch-001
         relation_type: translation_of
     rights:
       access: public
       license: CC-BY-NC-SA-4.0
       holder: ruvebal@crea-comm.net
       permission_basis: rights-holder-relicense-2026-08-18
     content_digest: '<sha256 via TTOD-C14N-v1>'
     created_at: '2026-09-06'
   ```
9. Run `python cli.py validate --strict` — zero errors before finishing, same as any other edit.

See `docs/DEV_PLAN/DECISIONS/S0-2026-09-04-BILINGUAL-CONTENT-MODEL.md` decisions 5–6 for the full
invariant rationale, and `docs/DEV_PLAN/PHASE-S-TTOD-BILINGUAL-CONTENT-MODEL.md` §S1′ for the
frozen diagnostic-code table.

## Migration-backup convention

A future live-database migration of the Q6/S2′ kind (one that rewrites every record in
`ttod.yml` — a schema-version bump, a field backfill, etc.) takes its pre-migration backup as a
**byte-identical copy tracked inside the repo under `private/`** (e.g.
`private/ttod.yml.pre-<phase>-backup`), matching Q6's own precedent
(`private/ttod.yml.pre-q6-backup`, confirmed tracked via `git ls-files private/` — `.gitignore`
excludes `_private/`, not `private/`). This keeps the backup part of the same auditable git
history as everything else the project reports, rather than living only in a session-specific
scratchpad outside the repo. Compute and record the pre-migration byte digest before writing the
backup, exactly as every prior TTOD migration report has done.

## YAML formatting

Follow the indentation rules in the file header (2-space increments; quote list items at 1 space under `quotes:`).
