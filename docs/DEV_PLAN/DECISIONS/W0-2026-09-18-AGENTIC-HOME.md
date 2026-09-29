# W0 decision — agentic homogenization: canonical homes, discovery map, MCP ontology

**Status:** FROZEN by product-owner direction, 2026-09-18

**Owner:** `ruvebal@crea-comm.net`

**Implementation authority:** none by this record; AG1–AG6 gate implementation. No branch
created, no file moved, no commit beyond this record.

## Decision

1. **TTOD-scoped canonical bodies** (rules and skills whose content is specific to *this*
   repository) live under `ttod/agentic/{rules,skills}/`. `agentic/report-steward/` keeps its
   existing pack shape unchanged — it is already correctly homed.
2. **Cross-repo cascade subagents are not TTOD-scoped and are not absorbed.**
   `cascade-phase-executor` and `cascade-cold-reviewer` stay canonical at
   `~/src/.agents/agents/` (studio-wide, reused by `deviac`, `athanor`, and others via the
   cascade-forge pattern). `ttod/.claude/agents/cascade-*.md` remain thin stubs pointing there,
   exactly as they do today — this closes F3 without forking a studio asset into TTOD. Nothing
   is created under `ttod/agentic/agents/` in this cascade; that directory stays reserved for a
   future genuinely TTOD-only agent, if one is ever needed.
3. **`.cursor/` and `.claude/` remain landings only** — real per-tool frontmatter, thin
   redirect body, no duplicated procedure text, per the existing
   `ttod/.claude/agents/cascade-*.md` pattern.
4. **Studio `~/src/.agents/` is not renamed by this cascade.** Phase W does not decide the
   studio's own future naming (`.agents` vs `agentic`); it only records, for TTOD's stubs,
   which home is authoritative today (studio, for the two cascade subagents named above).

## Findings closure (FINDINGS-2026-09-18.md)

| ID | Finding | Disposition |
| --- | --- | --- |
| F1 | Two "canonical" homes exist with no written map | **Closed by this record** — TTOD-scoped bodies → `ttod/agentic/`; cross-repo cascade subagents → `~/src/.agents/`; no third home introduced |
| F3 | `.claude/agents/*` redirect to studio, not `ttod/agentic/` | **Closed by this record** — that redirect is correct and stays; the two cascade subagents are studio content, not TTOD content, so re-pointing them would be the split-brain, not fixing one |
| F2, F4–F10 | Fat landings, CI paths, branch collision, discovery map, MCP ontology, IDE MCP, validator honesty | Deferred to their named phases (AG2/AG3 → F2; AG4 → F4/F6; AG1 → F5; AG0+AG4 → F7 (frozen below); AG2+AG4 → F8; AG6 → F9; documented, not closed, in `AGENTIC-HARNESS.md` → F10 |

## Inventory (post-freeze home vs landing)

| File / body | Today | Post-freeze home (edit) | Landing (load path) |
| --- | --- | --- | --- |
| `AGENTS.md` | Root contract | Unchanged — root contract, becomes the discovery index (AG4 adds the map) | n/a — read by all tools directly |
| `CLAUDE.md` | Thin redirect → `AGENTS.md` | Unchanged | n/a |
| `.cursor/rules/ttod-editing.mdc` | Full body | `agentic/rules/ttod-editing.md` (AG2) | `.cursor/rules/ttod-editing.mdc` stub (AG3) |
| `.cursor/skills/public-docs-i18n/SKILL.md` | Full body | `agentic/skills/public-docs-i18n/SKILL.md` (AG2) | `.cursor/skills/public-docs-i18n/SKILL.md` stub (AG3) |
| `agentic/report-steward/**` | Canonical pack (agent/rules/skills/scripts/PACK.md) | Unchanged — already correct | n/a — CI reads this path directly, must not move |
| `.claude/agents/cascade-phase-executor.md` | Stub → `~/src/.agents/agents/cascade-phase-executor.md` | Unchanged (studio-canonical per Decision §2) | Stub stays as-is |
| `.claude/agents/cascade-cold-reviewer.md` | Stub → `~/src/.agents/agents/cascade-cold-reviewer.md` | Unchanged (studio-canonical per Decision §2) | Stub stays as-is |
| `agentic/README.md` | Does not exist | **New** — map of packs + landings + IDE harness pointer, back-linking `AGENTS.md` (AG2) | n/a |
| `agentic/ide-mcp/**` | Does not exist | **New** — AG6 only | `.cursor/mcp.json` (AG6) |

**Explicit cite-but-do-not-absorb list** (studio assets TTOD's docs may reference but this
cascade must not fork into `ttod/agentic/`):

- `~/src/.cursor/skills/ttod-bridge/SKILL.md` — studio propose/read contract, consumed by
  sibling repos; forking it here breaks that sharing.
- `~/src/.cursor/skills/cascade-forge/SKILL.md` — authoring shape reference for this pack
  itself; stays studio-side unless a separate studio cascade migrates it.
- `~/src/.agents/agents/cascade-phase-executor.md` and `cascade-cold-reviewer.md` — see
  Decision §2.

## Discovery map freeze

`AGENTS.md` becomes the single discovery index (AG4 wires the actual prose; the frozen
content, per `RATIONALE.md` § Discovery map, is):

```text
AGENTS.md                          ← root contract (read first)
  ├── agentic/                     ← IDE agent harness (rules, skills, packs)
  │     └── report-steward/        ← evidence + privacy watcher (CI uses this)
  ├── .cursor/ · .claude/          ← landings only (tool loaders)
  ├── services/mcp/                ← product FastMCP (read-only corpus retrieval)
  ├── services/frontend/ (Astro)   ← UI; Oracle island talks to backend
  ├── services/backend/            ← FastMCP *client* → mcp-server
  └── studio ttod-bridge           ← propose/read (outside this repo's agentic/)
```

**Bidirectional link required (AG4):** `AGENTS.md` links `agentic/`; `agentic/README.md`
links back to `../AGENTS.md` and one-lines the product MCP pointer.

**Explicit non-goal:** `services/mcp/` is never relocated under `agentic/`. Agents discover
the product MCP through the `AGENTS.md` map and the `agentic/README.md` pointer, not by
nesting the server inside the harness tree. This closes F7 as "documented", not "moved."

## IDE vs application MCP freeze

| Concern | Home | Scope |
| --- | --- | --- |
| Coding-agent rules/skills/packs (process) | `agentic/` + `.cursor`/`.claude` landings | AG0–AG5 |
| Project-level docs MCP for Astro + Svelte (IDE tooling) | `.cursor/mcp.json` (committed) + `agentic/ide-mcp/` (edit-home/templates) | AG6 only |
| Product FastMCP (runtime protocol) | `services/mcp/` via Compose | Out of scope — application, unchanged |
| React MCP (Smithery) | Not cohort-default; portable `npx` install or `DEFERRED` | AG6 decides, not this record |

This closes F9 as "scoped to AG6", not "solved today."

## Validator readiness (per `AGENTIC-HARNESS.md` §2–§3)

- **Ready today:** `cascade-phase-executor`, `cascade-cold-reviewer` (studio-canonical, stub
  wired), `agentic/report-steward/scripts/check_public_privacy.py` (CI-wired).
- **Not wired, not claimed:** a dual-model (frontier orchestrator + local-Ollama validator)
  execution mode for AG0–AG5 itself; MCP-existence probe scripts (AG6 builds these); a
  tool-using local-Ollama cold-reviewer (evaluated separately this session — see chat history
  2026-09-18 — and correctly not folded into this cascade's closing protocol until it has its
  own trust evaluation).
- This record does not upgrade any of the above readiness; it only restates it so AG1–AG6 do
  not silently assume more automation exists than does. Closes F10 as "documented", not
  "built."

No git branch was created and no file other than this record was written or moved in
producing this decision.

## Rationale

The repository already runs a correct, working split for the two cascade subagents
(studio-canonical, TTOD-side stub) — the risk this cascade exists to avoid is *re-breaking*
that by assuming "homogenize under `agentic/`" means "move everything agent-shaped into
`ttod/agentic/`." It doesn't: only content whose substance is TTOD-specific (the YAML editing
checklist, the public-docs i18n skill) is TTOD-scoped. Generic cascade-execution behavior is
studio infrastructure reused across repos, and duplicating it here would immediately recreate
the split-brain Phase W is named to end, just one level down.

## Non-authorization

This decision does not itself permit branch creation, file moves, landing rewrites, `AGENTS.md`
edits, or any commit beyond this record. Those actions remain gated behind AG1 through AG6 as
written in `PHASE-W-AGENTIC-HOMOGENIZATION-CASCADE.md`, each closing through its own
VERIFYING → cold review → report cycle.
