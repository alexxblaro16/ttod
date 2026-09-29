---
name: ttod-editing
purpose: The strict discipline for editing ttod.yml: schema v3, IDs, tags, collections, validation.
surfaces: [rules]
landings: [.cursor/rules/ttod-editing.mdc]
mirrors: []
locks: []
external_readers: [The TS5 skeleton generator copies the Cursor landing into student skeletons]
status: tracked
---

# TTOD Editing Pack

The always-on rule that keeps `ttod.yml` edits going through the CLI. One topic, one rule; Cursor
loads it through the landing named above (the landing is a redirect, never a second copy).

| Surface | Purpose |
| --- | --- |
| `rules/ttod-editing.md` | the complete editing discipline (edit-home) |
