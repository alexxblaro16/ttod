---
name: public-docs-i18n
purpose: Authoring and translating the bilingual public documentation site; its step 2 calls the standalone CLI scripts/translate_public_docs.py, which lives outside this pack.
surfaces: [skills]
landings: [.cursor/skills/public-docs-i18n/SKILL.md]
mirrors: []
locks: []
external_readers: []
status: tracked
---

# Public Docs i18n Pack

The English/Spanish public-docs workflow. The skill is inside this pack; the translation CLI it calls
is a standalone repo-level script (`scripts/translate_public_docs.py`) and stays there — `--help`
works without the skill. Cursor loads the skill through the landing named above.

| Surface | Purpose |
| --- | --- |
| `skills/public-docs-i18n/SKILL.md` | bilingual public-docs authoring workflow (edit-home) |
