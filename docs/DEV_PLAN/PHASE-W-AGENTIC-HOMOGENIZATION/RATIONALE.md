# Phase W — Rationale (product / pedagogy face)

**Status:** planning only · 2026-09-18  
**Audience:** product owner, teaching lead, anyone deciding whether to authorize AG0+.

## The problem in one paragraph

TTOD already has a tool-agnostic root contract (`AGENTS.md`, with `CLAUDE.md` as a
redirect). Below that layer the repository still speaks several proprietary dialects
at once: `.cursor/` (Cursor rules/skills), `.claude/` (Claude Code agents), a
studio-level `~/src/.agents/` skeleton started 2026-09-11, and a promising but
incomplete in-repo `agentic/` tree that today holds only `report-steward`. Agents
and humans must know *which tree is source of truth*. That is the same failure mode
the studio already named for duplicated root contracts — now at the rules/skills/
subagent layer.

## Why “agentic/” wins as the name

| Criterion | `.cursor` / `.claude` | `.agents` (studio) | `agentic/` (this repo) |
| --- | --- | --- | --- |
| Tool-neutral | No | Mostly | Yes |
| Visible to students in a clone | Hidden by convention | Hidden | Visible — pedagogically useful |
| Already used in TTOD | Yes (landings) | No (studio only) | Yes (`report-steward`) |
| Matches AGENTS.md open standard spirit | Indirect | Adjacent naming | Explicit *agentic method* |

**Proposed freeze (to be confirmed in AG0, not assumed):**

1. **Canonical bodies** for TTOD-scoped agent material live under `agentic/`.
2. **`.cursor/` and `.claude/`** remain as **landings only** — real tool frontmatter
   plus a one-paragraph redirect to the canonical path (same pattern already used by
   `ttod/.claude/agents/cascade-*.md` → `~/src/.agents/agents/`).
3. **Studio-wide** assets may stay under `~/src/.agents/` *or* be renamed later to
   `~/src/agentic/`; Phase W does not silently rename the studio home. AG0 records
   the chosen map so TTOD stubs do not point at two different “canonical” homes.

## What this cascade ships

- One readable layout: `agentic/{rules,skills,agents,scripts}/…` (packs like
  `report-steward/` keep their pack-internal subfolders).
- Thin landings under `.cursor/` and `.claude/` so Cursor and Claude Code still
  discover work.
- Rewritten evergreen pointers in `AGENTS.md`, generators, and CI path lists that
  still name the old trees as *load paths*, not as *edit homes*.
- An explicit **`AGENTS.md` ↔ `agentic/` link** (root contract points at the harness;
  `agentic/README.md` points back at `AGENTS.md`).
- A **discovery map** in `AGENTS.md` that lists the product MCP and Astro/Oracle
  path as *siblings* of the harness — so agents find MCP without mistaking it for
  skill/rule content (see § Discovery map below).
- A **named branch** and a **merge ritual** that students can recognize from the
  quote-proposal pipeline (see orchestrator § Pedagogical merge).

## Discovery map — link `agentic/` and MCP, without merging them

**Yes — link `agentic/` from `AGENTS.md`.** Today `AGENTS.md` § Integration /
Related docs still teach `.cursor/rules` and ttod-bridge paths, and never names
`agentic/`. After Phase W, `AGENTS.md` is the single discovery index:

```text
AGENTS.md                          ← root contract (read first)
  ├── agentic/                     ← IDE agent harness (rules, skills, packs)
  │     └── report-steward/        ← evidence + privacy watcher (CI uses this)
  ├── .cursor/ · .claude/          ← landings only (tool loaders)
  ├── services/mcp/                ← product FastMCP (read-only corpus retrieval)
  ├── services/frontend/ (Astro)   ← UI; Oracle island talks to backend
  ├── services/backend/            ← FastMCP *client* → mcp-server
  └── studio ttod-bridge           ← propose/read (outside this repo’s agentic/)
```

**Shall we put MCP “inside” `agentic/`?** **No.** That would teach the wrong
ontology:

| Concern | Home | What it is |
| --- | --- | --- |
| How coding agents behave | `agentic/` (+ landings) | Rules, skills, report packs — *process* |
| How the running product retrieves quotes | `services/mcp/` | FastMCP server — *runtime protocol* |
| How Astro/Oracle uses that protocol | `services/frontend` + `services/backend` | UI + HTTP/stream client of MCP |
| How DevIAC ingests TTOD | export → studio MCP | *Different* MCP consumer (already in § Integration) |

Astro does not “contain” MCP; the Compose stack wires **Astro → Oracle API →
FastMCP client → `mcp-server:3001`**. Making that path **official in `AGENTS.md`**
(and mirrored in `agentic/README.md` as a one-line “product MCP lives here →”)
is exactly how agents discover it — without pretending the harness *is* the
server.

**Proposed AG4 prose (freeze wording in AG0 if desired):**

> **Agent harness:** edit under [`agentic/`](agentic/); tools load via `.cursor` /
> `.claude` landings.  
> **Product MCP:** [`services/mcp/`](services/mcp/) — read-only FastMCP for the
> Oracle/Astro stack (`make up`). Not a skill pack; do not relocate under
> `agentic/`.  
> **Studio MCP ingest:** `exports/ttod.json` → DevIAC (separate consumer).

## What this cascade deliberately does not ship

- No `ttod.yml` mutation, proposal accept, or ID allocation.
- No deletion of historical cascade reports that mention `.cursor` paths.
- No claim that a single file format serves Cursor skills and Claude Code agents —
  frontmatter stays per-tool on the landing; only the **body** homogenizes
  (`~/src/AGENTS.md` already states this honesty requirement).
- No forced migration of every studio skill in `~/src/.cursor/skills/` in one pass
  (that remains a later studio cascade; TTOD-scoped first).
- No authorization to merge to `main` without AG5 gates and a named human.
- **No move of `services/mcp/` into `agentic/`** — discovery by map, not by nesting.
- No claim that AG0–AG5 already run a frontier orchestrator with a full Ollama
  validator fleet — see [`AGENTIC-HARNESS.md`](AGENTIC-HARNESS.md) §3; AG6 adds
  student IDE MCP + existence probes only.

## Student IDE harness (AG6) — summary answer

| Question | Plan answer |
| --- | --- |
| Project-level so students benefit? | **Yes** — commit `.cursor/mcp.json` + `agentic/ide-mcp/` |
| Where save MCP JSON? | Project `.cursor/mcp.json`; examples for Desktop/opt-in servers under `agentic/ide-mcp/examples/` |
| HTTP vs stdio Astro? | Prefer HTTP; document `mcp-remote` fallback |
| Svelte official? | `npx -y @sveltejs/mcp` + vendor `llms.txt` |
| Playwright official? | `npx @playwright/mcp@latest` (Microsoft) — browser automation, framework-agnostic |
| MCP-org reference servers? | `filesystem` (scoped to repo root only), `git`, `fetch` — default-on or documented opt-in, instructor's call |
| React MCP? | **Settled, no entry — not a "revisit later" TODO.** No official server exists (Meta does not publish one); a third-party substitute is never cohort-default regardless of convenience |
| GitHub MCP? | Official but credentialed (OAuth/PAT) — individually opt-in example only (`agentic/ide-mcp/examples/github.json`), never the committed default |
| `@modelcontextprotocol/*` in frontend? | **No** for docs MCP consumption (running reference servers via `npx` at IDE-config time does not add them to `package.json`) |
| Docker MCP? | Application only — sibling discovery, not IDE config |

## Pedagogical stake

Students already learn: *propose → review → accept → merge the diff*. Phase W uses
the same mental model for *agent-contract cleanup*: the branch is the proposal; the
PR is the review surface; merging is the human act that makes `agentic/` the living
source of truth. Teaching that isomorphism is an explicit deliverable of AG5’s
documentation note — not an afterthought.
