# `agentic/` — the legend

> "The module that knows its boundaries serves the whole. The module that knows no boundaries
> becomes the whole—and collapses under its own weight." — TTOD `arch-001`
>
> "A template is not a constraint. It is a garden where a thousand flowers can bloom in
> harmony." — TTOD `arch-014`
>
> "Linus's open development policy was the very opposite of cathedral-building." — Raymond,
> Eric S. 2001. *The Cathedral and the Bazaar: Musings on Linux and Open Source by an
> Accidental Revolutionary*. Rev. ed. O'Reilly, PDF p. 42.
> (A metaphor for how this tree grows — planned names, emergent packs — not evidence for it.)

## The one rule

**Every folder directly inside `agentic/` is a topic.** Each topic is a *pack*: a folder with a
`PACK.md` saying what it is for. The words `rules`, `skills`, `agents` and `scripts` appear only
*inside* a pack, never beside one — so when you see `rules/`, you always know whose it is.

```text
agentic/
├── README.md                     you are here
├── ttod-editing/                 pack — how ttod.yml may be edited
│   ├── PACK.md
│   └── rules/ttod-editing.md          the rule itself (edit here)
├── public-docs-i18n/             pack — the bilingual public-docs workflow
│   ├── PACK.md
│   └── skills/public-docs-i18n/SKILL.md   the skill itself (edit here)
├── report-steward/               pack — evidence reports + the public-privacy watcher
│   ├── PACK.md                        (path is locked: CI, Makefile and a test read it)
│   └── agents/  rules/  skills/  scripts/
├── ide-mcp/                      pack — student IDE MCP harness
│   ├── PACK.md  README.md             (README = the student-facing setup)
│   └── mcp.cursor.json  examples/  llms/  scripts/
└── lao-tzu-tao-compose/          pack — local and untracked; not committed by the layout phases
    └── PACK.md  skills/  rules/  queries/  prompts/   (path is locked: a sibling repo reads it)
```

Nothing inside a pack is loaded by a tool on its own: a rule or skill reaches Cursor only through a
doorway (below), and `report-steward/agents/report-steward.md` has none — it is source material.

The top of every `PACK.md` is a small fenced block, no comments, no nesting. This is a complete one:

```text
---
name: ttod-editing
purpose: The strict discipline for editing ttod.yml.
surfaces: [rules]
landings: [.cursor/rules/ttod-editing.mdc]
mirrors: []
locks: []
external_readers: []
status: tracked
---
```

`surfaces` are names inside the pack (each must exist and be non-empty, and every folder in the pack
must be listed); `landings` and `locks` are paths from the repository root; `mirrors` are
`file-in-pack>path-in-repo` pairs; `status` is `tracked` or `local-untracked`. The full grammar is in
the [Y5 decision](../docs/DEV_PLAN/DECISIONS/Y5-2026-09-21-ONE-AXIS-TREE.md). `tests/test_agentic_tree.py`
checks all of it — **locally**, through `make test`; the CI workflow runs no Python tests.

## Doorways (landings)

`.cursor/` and `.claude/` are doorways that let a tool find these packs. A doorway is a few lines
of redirect, never a second copy of the content — with one exception, the JSON file in the table below,
because JSON cannot redirect.

| Doorway | Points at |
| --- | --- |
| `.cursor/rules/ttod-editing.mdc` | `ttod-editing/rules/ttod-editing.md` |
| `.cursor/rules/public-privacy.mdc` | `report-steward/rules/public-privacy.md` |
| `.cursor/rules/spanish-research-prose.mdc` | `report-steward/rules/spanish-research-prose.md` |
| `.cursor/skills/public-docs-i18n/SKILL.md` | `public-docs-i18n/skills/public-docs-i18n/SKILL.md` |
| `.cursor/mcp.json` | **the exception:** an identical copy of `ide-mcp/mcp.cursor.json`; the tree test compares the parsed JSON, and `ide-mcp/scripts/verify-ide-mcp.py` is the stricter gate (allowlist and digest) |
| `.claude/agents/cascade-*.md` | the studio's shared agents, outside this repository |

## Adding something

A new topic gets **a new pack**: make `agentic/<topic>/`, give it a `PACK.md`, and put its rule,
skill, agent or script in the matching folder *inside* it. Add to an existing pack only when the
new thing is about **what that pack's `purpose` line says** — `ttod-editing` is about editing
`ttod.yml`, so a rule about CSS class naming is not its topic and starts its own pack. A tool that
must find the file gets a doorway that redirects to it.

**Never rename `report-steward/` or `lao-tzu-tao-compose/`.** The first is hard-wired in
`public-docs-pages.yml`, the `Makefile` and `tests/test_public_privacy_watcher.py`; the second
is read by a sibling repository. Their `PACK.md` lists say so under `locks` and `external_readers`.

## Beside this tree, not in it

- The running app's own MCP server is [`../services/mcp/`](../services/mcp/): a runtime protocol,
  not an agent pack.
- Studio skills (`ttod-bridge`, `cascade-forge`) and the two cascade subagents live outside this
  repository and stay there; TTOD points at them and never forks them.
- Root contract and map: [`../AGENTS.md`](../AGENTS.md). Why things live where they do:
  [W0](../docs/DEV_PLAN/DECISIONS/W0-2026-09-18-AGENTIC-HOME.md) and the
  [Phase Y plan](../docs/DEV_PLAN/PHASE-Y-AGENTIC-DIRTREE-UNIX/INDEX.md).

## Harness honesty

Cascades over this tree are orchestrated with the studio's `cascade-forge` skill and its
`cascade-*` subagents, kept outside this repository. There is no `agentic/` directory in the
sibling DevIAC repository; do not assume one. Layout changes are proposed through a branch and a
pull request, and merged only by a named human — the same two-touchpoint discipline as a quote
proposal, on a different write surface. Nothing here mutates `ttod.yml`.
