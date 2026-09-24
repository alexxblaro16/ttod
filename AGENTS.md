# AGENTS.md — 道 The Tao of Development (TTOD)

> _"Name your variables as if you were baptising stars."_

**Repository:** `/Users/ruvebal/src/ttod`
**Author:** Rubén Vega Balbás PhD — `ruvebal@crea-comm.net`
**Format:** [AGENTS.md open standard](https://github.com/agentsmd/agents.md) (Agentic AI Foundation / Linux Foundation)
**Licenses:** code MIT ([`LICENSE-CODE`](LICENSE-CODE)); content CC BY-NC-SA 4.0 ([`LICENSE-CONTENT`](LICENSE-CONTENT))

Read this file before editing quotes, running the CLI, or proposing new aphorisms. Phase Q contract:
[`docs/DEV_PLAN/INDEX.md`](docs/DEV_PLAN/INDEX.md).

---

## Mission

TTOD is the studio **pedagogical wisdom database** — aphorisms for developers walking the path,
organized by section (images, CSS, architecture, wisdom, …) and level (beginner → master). Never
embed a current quote count in prose; derive counts from the canonical snapshot with the CLI.

After every development iteration, distilled insights may flow back through the **ttod-bridge**
(`~/src/.cursor/skills/ttod-bridge/`) as **proposals**, not direct YAML edits.

---

## Dev environment

```bash
cd ~/src/ttod
make help                                        # root task surface (Compose · CLI · Jekyll · Astro)
make venv                                        # once — .venv + editable install
make validate                                    # or: .venv/bin/python cli.py validate
make stats
```

Legacy one-liner (same corpus tools without Make):

```bash
python3 -m venv .venv && . .venv/bin/activate   # once
pip install -e .                                 # if pyproject present; else: pip install typer pyyaml
. .venv/bin/activate && python cli.py validate
. .venv/bin/activate && python cli.py stats
```

**Running the stack (`make up`):** starts the full application, including its own Ollama
container — nothing to install first, no host dependency. This is the one supported path,
and what students use. Borrowing an Ollama you already run yourself (e.g. for Metal GPU
speed outside Docker on macOS) is a personal, manual override, not a `make` target — set
`OLLAMA_MODE=host` and `OLLAMA_BASE_URL` in your own `.env` if you want it. See the `ollama`
service in `docker-compose.yml` and the comments in `.env.example` for both paths.

| Path                                    | Role                                                                                         |
| --------------------------------------- | -------------------------------------------------------------------------------------------- |
| `ttod.yml`                              | Canonical quote database (human-governed)                                                    |
| `cli.py`                                | validate · stats · snapshot · export · migrate · proposal · bridge · add · deprecate · erase |
| `agentic/`                              | **Edit-home** for TTOD-scoped agent rules/skills (e.g. `agentic/rules/ttod-editing.md`); `.cursor`/`.claude` are load-path landings only, not a second copy — see `agentic/README.md` |
| `.cursor/rules/ttod-editing.mdc`        | Load-path landing (Cursor) → `agentic/rules/ttod-editing.md`; strict YAML editing checklist  |
| `schema/`                               | v3 schema surface (Phase Q complete)                                                         |
| `exports/`                              | Derived JSON/graph (gitignored)                                                              |
| `sources/tao-of-ai-development/`        | Parked chapter — **not merged**; read README before extracting IDs                           |
| `sources/tao-of-human-centered-design/` | Parked HCD chapter (hc-app-design) — **not merged**; read README before extracting IDs       |

**Do not** hand-append YAML to `ttod.yml`. Mutations go through `proposal accept`, `add`
(requires `--reviewer-id`), or `migrate apply --approve` (one-time v2→v3 only) via
`ttod_core/repository.py` atomic transactions. Use disposable copies (`--file`) for bridge
self-tests and experiments.

---

## Editing workflow

### Read or search (any agent)

```bash
~/src/ttod/.venv/bin/python -c "
import sys; sys.path.insert(0, '$HOME/src/.cursor/skills/ttod-bridge/scripts')
from ttod_cli_adapter import TTODCliAdapter
a = TTODCliAdapter()
print(a.read_quote('arch-001'))
print(a.search_quotes(section='wisdom', theme='simplicity', limit=3))
"
```

Use the **ttod-bridge** skill for propose/search/read — never parse `ttod.yml` ad hoc in forge skills.

### Propose a new quote (never merge)

1. Distill only from a **citable source** (lesson, grounded research, studio session).
2. Call `adapter.propose_quote(...)` — writes to `~/src/.cursor/skills/ttod-bridge/pending/`.
3. A **human** reviews, then `proposal import` → `proposal accept --reviewer-id …` (or ttod-bridge accept path when wired).
4. Every `origin: blackbox` entry needs `validated_by: human` before it counts as accepted.

### Edit existing quotes (human, post-Q3)

1. Read `agentic/rules/ttod-editing.md` — Cursor loads the same content via the
   `.cursor/rules/ttod-editing.mdc` landing.
2. Pick section + next free ID prefix (`meta.last_id_by_section`).
3. Tags only from `tag_taxonomy` (extend taxonomy first if needed).
4. Run `python cli.py validate` — **zero errors** before finishing.
5. Never hand-edit `meta.total_quotes`, section counts, or collection totals.

---

## Quote record (v3 shape)

```yaml
- id: arch-001
  schema_version: '3.1.0' # after Phase S S2′; fixtures may still show 3.0.0+lang during S1′
  content_digest: '<sha256 via TTOD-C14N-v1>'
  text: 'The aphorism itself.'
  section: architecture
  subsection: boundaries
  level: advanced # beginner | intermediate | advanced | master
  lang: en # ISO 639-1; required. Translations are separate IDs.
  tags: [boundaries, coupling] # from tag_taxonomy
  teaches: 'What the student learns'
  related: [arch-002, cc-001]
  relation_edges: # optional typed edges
   - { target: arch-060, relation_type: translation_of } # Spanish twin points here; never arch-001-es
  lesson: lesson-slug
  source: source-slug
  origin: human # human | studio | blackbox | legacy-unknown
  rights:
   access: public
   license: CC-BY-NC-SA-4.0
   holder: ruvebal@crea-comm.net
   permission_basis: rights-holder-relicense-2026-08-18
  created_at: '2025-12-06'
```

**ID / language policy (Phase S):** IDs stay `{section_prefix}-{number}` — never locale suffixes
(`arch-001-es` is invalid). A Spanish twin of `arch-001` is the next free `arch-NNN`, linked via
`relation_edges: [{target: arch-001, relation_type: translation_of}]` with `lang: es`.

**Origin contract**

| `origin`         | Meaning                                                       |
| ---------------- | ------------------------------------------------------------- |
| `human`          | Original authorship                                           |
| `studio`         | Distilled by the developer during work                        |
| `blackbox`       | Proposed by AI — requires validated human review block        |
| `legacy-unknown` | Pre-v3 records with no recorded origin (not human-by-default) |

---

## Verification before claiming done

```bash
make check                                                  # validate --strict + stats --check + unittest
# or without Make:
. .venv/bin/activate && python cli.py validate --strict --json  # must exit 0
. .venv/bin/activate && python cli.py stats --check             # meta must match recomputed
python -m unittest discover -s tests -p 'test_*.py'            # full suite must be green (count grows — do not hardcode it, this line itself went stale once already)
~/src/ttod/.venv/bin/python ~/src/.cursor/skills/ttod-bridge/scripts/tests/test_ttod_bridge.py
```

If you only staged a proposal, confirm `ttod.yml` hash unchanged and `pending/*.yaml` exists with
`origin: blackbox` and **no** `validated_by`.

---

## Non-negotiable rules

1. Never delete quotes — set `deprecated: true`.
2. IDs are immutable; prefix must match section (`arch-*` → `architecture`).
3. YAML is source of truth; JSON exports are derived.
4. NC content default: see [`docs/DEV_PLAN/DECISIONS/Q0-2026-08-18-RIGHTS-LICENSE-NC.md`](docs/DEV_PLAN/DECISIONS/Q0-2026-08-18-RIGHTS-LICENSE-NC.md). Do not silently relicense.
5. TTOD quotes are **pedagogical**, not independent evidence for Athanor/WPL claims.
6. Cite quotes in lessons **by ID** only — never cite a pending proposal's suggested id.

---

## Integration

| Consumer         | How                                       |
| ---------------- | ----------------------------------------- |
| Web Atelier      | Jekyll `site.data.ttod`                   |
| DevIAC MCP       | `exports/ttod.json` → pgvector ingest     |
| Fine-tuning      | `prepare_data.py` reads `ttod.yml`        |
| ttod-bridge      | Read/search/propose port for forge skills |
| Knowledge Engine | Future RAG + 3D graph visualization       |
| `services/mcp/`  | Product FastMCP — read-only corpus retrieval for the Oracle/Astro stack (`make up`). Not a skill pack; not nested under `agentic/`. |
| `services/frontend` (Astro) / `services/backend` | Astro UI + Oracle island; backend is the FastMCP **client** that talks to `services/mcp/` |

### Discovery map

`AGENTS.md` is the single discovery index for both agent-facing tooling and the running product:

```text
AGENTS.md                          ← root contract (read first)
  ├── agentic/                     ← IDE agent harness (rules, skills, packs)
  │     ├── report-steward/        ← evidence + privacy watcher (CI uses this)
  │     └── ide-mcp/                ← student IDE MCP configs, llms index, verify scripts
  ├── .cursor/ · .claude/          ← landings only (tool loaders); .cursor/mcp.json = IDE MCP client config
  ├── services/mcp/                ← product FastMCP (read-only corpus retrieval)
  ├── services/frontend/ (Astro)   ← UI; Oracle island talks to backend
  ├── services/backend/            ← FastMCP *client* → mcp-server
  └── studio ttod-bridge           ← propose/read (outside this repo's agentic/)
```

**Agent harness:** edit under [`agentic/`](agentic/); tools load via `.cursor` /
`.claude` landings. **Product MCP:** [`services/mcp/`](services/mcp/) — read-only FastMCP for
the Oracle/Astro stack (`make up`). Not a skill pack; do not relocate under `agentic/`.
**Studio MCP ingest:** `exports/ttod.json` → DevIAC (separate consumer, table above).

**IDE MCP ≠ Docker MCP — two different "MCP"s, do not conflate them.** `.cursor/mcp.json`
(edit-home: [`agentic/ide-mcp/`](agentic/ide-mcp/)) configures **development-time** MCP
servers your coding agent calls from inside the IDE (Astro/Svelte/Playwright docs, a
sandboxed filesystem tool) — official/vendor-maintained servers only, see
[`agentic/ide-mcp/README.md`](agentic/ide-mcp/README.md). `services/mcp/` is the
**running product's** own FastMCP server, consumed by the Oracle/Astro stack at runtime.
Same three letters, unrelated processes, unrelated audiences — an IDE MCP outage is not a
product bug, and a product MCP outage is not fixed by touching `.cursor/mcp.json`.

**Why this layout, in one classroom line:** `.cursor` and `.claude` are doorways. `agentic/`
is the room. Merging a homogenization branch like `agentic/homogenize-landings` is like
accepting a quote proposal: the PR is the review; the merge is the human act that makes the
new layout real. Same discipline as `proposal accept`, different write surface — this never
touches `ttod.yml`. See `docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/PHASE-W-AGENTIC-HOMOGENIZATION-CASCADE.md`
§6 for the full isomorphism.

---

## Related docs

| Doc                                                                                      | When                                    |
| ---------------------------------------------------------------------------------------- | --------------------------------------- |
| [`INDEX.md`](INDEX.md)                                                                   | Public readme + constitutional boundary |
| [`docs/DEV_PLAN/INDEX.md`](docs/DEV_PLAN/INDEX.md)                                       | Phase Q programme state                 |
| [`~/src/.cursor/skills/ttod-bridge/SKILL.md`](../../.cursor/skills/ttod-bridge/SKILL.md) | Propose/read contract (studio skill — cited, not absorbed into `agentic/`; see `docs/DEV_PLAN/DECISIONS/W0-2026-09-18-AGENTIC-HOME.md`) |
| [`agentic/README.md`](agentic/README.md)                                                | Map of TTOD's agent-facing tree: edit-home vs landings vs product MCP |
| [`agentic/rules/ttod-editing.md`](agentic/rules/ttod-editing.md)                         | YAML editing gate (edit-home; loaded via the `.cursor/rules/ttod-editing.mdc` landing) |
