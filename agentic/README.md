# `agentic/` — TTOD's tool-neutral agent harness

Canonical edit-home for TTOD-scoped agent rules, skills, and packs. `.cursor/` and `.claude/`
load these bodies through thin landings (real per-tool frontmatter, a redirect body) — they are
not a second copy. See [`../AGENTS.md`](../AGENTS.md) for the root contract and full discovery
map (agent harness · product MCP · Astro/Oracle · studio ttod-bridge), and
[`../docs/DEV_PLAN/DECISIONS/W0-2026-09-18-AGENTIC-HOME.md`](../docs/DEV_PLAN/DECISIONS/W0-2026-09-18-AGENTIC-HOME.md)
for why each item below lives where it does.

**Product MCP lives at [`../services/mcp/`](../services/mcp/)** — read-only FastMCP for the
Oracle/Astro stack. It is a runtime protocol, not a skill pack; it is never nested here.

## Contents

| Path | What it is | TTOD-scoped? |
| --- | --- | --- |
| `report-steward/` | Evidence-report workflow + public-artifact privacy watcher. CI (`public-docs-pages.yml`) depends on `report-steward/scripts/check_public_privacy.py` at this exact path — do not move it. | Yes — already correctly homed before Phase W |
| `rules/ttod-editing.md` | Strict TTOD YAML editing discipline (schema v3, IDs, `proposal`/`add` CLI path, bilingual `lang`/`translation_of` invariants). Landing: [`.cursor/rules/ttod-editing.mdc`](../.cursor/rules/ttod-editing.mdc). | Yes |
| `skills/public-docs-i18n/SKILL.md` | Authoring/translating the bilingual `docs/public` Jekyll site. Landing: [`.cursor/skills/public-docs-i18n/SKILL.md`](../.cursor/skills/public-docs-i18n/SKILL.md). | Yes |
| `agents/` | Reserved, currently empty. `cascade-phase-executor` and `cascade-cold-reviewer` are cross-repo cascade-forge infrastructure, not TTOD content — they stay canonical at `~/src/.agents/agents/` per W0 §2. Nothing moves here unless a genuinely TTOD-only agent is authorized later. | N/A |
| `ide-mcp/` | Not yet created — student IDE MCP harness (Astro + Svelte docs MCP, `llms.txt`, verify script) ships under AG6. | AG6 |

## What is deliberately absent

- No `.cursor`/`.claude` fork of the two cascade subagents (see `agents/` row above).
- No copy of studio-only skills (`ttod-bridge`, `cascade-forge`) — cited from `AGENTS.md` and
  this pack's own docs, never absorbed. See W0's cite-but-do-not-absorb list.
- No `services/mcp/` content — that is application infrastructure, discovered through the map
  above, not nested under this tree.
