<!--
PHASE-W — Agentic homogenization (tool-neutral agentic/ as source of truth;
.cursor / .claude as thin landings). AG0–AG6 all merged to main via PR #21 and #22.
Author: Rubén Vega Balbás PhD · 2026-09-18, closed 2026-09-19.
-->

# Phase W — Agentic Homogenization

**Status: COMPLETE.** AG0–AG5 merged to `main` via
[PR #21](https://github.com/ruvebal/ttod/pull/21); AG6 merged via
[PR #22](https://github.com/ruvebal/ttod/pull/22) (`main`@`1ca1e686`, 2026-09-19,
`--admin` merge — required `typecheck-and-build` check had not run against the branch, same
as PR #21). Every phase closed through its own VERIFYING → cold review → report cycle, seven
independent cold reviews total, zero unresolved findings. Student IDE MCP harness
(`.cursor/mcp.json` — Astro/Svelte/Playwright/`filesystem`) is live on `main`, verified at
every layer: offline config gate, live protocol handshake (4/4, independently reproduced by
cold review), **and** a complete human-run manual walkthrough with real per-server tool calls
(live Astro/Svelte docs content, a real Playwright navigation, a confirmed filesystem sandbox
boundary). The product's own Compose MCP (`services/mcp`) was separately sanity-checked live
(real `initialize` handshake + `tools/list` against the running container) — confirmed
working, untouched by this cascade, exactly as the discovery map says it should be.
([`PHASE-AG6-REPORT.md`](PHASE-AG6-REPORT.md)). **Next action: open a PR for AG6 whenever the
product owner is ready.**
**Author:** Rubén Vega Balbás PhD · 2026-09-18
**Readers:** product owner (rationale first); implementer (orchestrator second).

## How to read this pack

| Face | File | Question it answers |
| ---- | ---- | ------------------- |
| Product owner | [`RATIONALE.md`](RATIONALE.md) | Why leave proprietary agent trees as landings; what ships; what must not. |
| Technical director | [`PHASE-W-AGENTIC-HOMOGENIZATION-CASCADE.md`](PHASE-W-AGENTIC-HOMOGENIZATION-CASCADE.md) | Ordered phases, gates, branch naming, hard constraints, closing protocol. |
| Harness / MCP / validators | [`AGENTIC-HARNESS.md`](AGENTIC-HARNESS.md) | App vs IDE stacks; which validators are ready; where students put `mcp.json`. |
| Evidence | [`FINDINGS-2026-09-18.md`](FINDINGS-2026-09-18.md) | What was checked live this session against the real tree. |
| Pedagogy | Orchestrator § *Pedagogical merge* | How merging this branch teaches the same accept/merge discipline as quote proposals. |

Phase files (do not invert):
[AG0](PHASES/AG0-inventory-and-naming-freeze.md) ·
[AG1](PHASES/AG1-branch-and-target-layout.md) ·
[AG2](PHASES/AG2-migrate-bodies-into-agentic.md) ·
[AG3](PHASES/AG3-landing-stubs.md) ·
[AG4](PHASES/AG4-rewrite-references.md) ·
[AG5](PHASES/AG5-verify-and-merge-gate.md) ·
[AG6](PHASES/AG6-student-ide-harness.md).

Harness roles / validator readiness:
[`AGENTIC-HARNESS.md`](AGENTIC-HARNESS.md).

Closing: each phase → VERIFYING → `PHASE-AGn-COLD-REVIEW.md` → amend if needed →
`PHASE-AGn-REPORT.md` → DONE.

## One-sentence claims

- **Product:** TTOD’s agent-facing material lives under one visible, tool-neutral
  `agentic/` tree; Cursor and Claude Code keep only thin discovery landings.
- **Engineering:** Bodies move once; `.cursor/` and `.claude/` become redirect
  stubs with real frontmatter; CI and teaching generators keep working paths.
- **Discovery:** `AGENTS.md` links `agentic/` and names product MCP (`services/mcp`)
  + Astro/Oracle as siblings — harness does not swallow the MCP server.
- **Student IDE:** AG6 commits project-level MCP for official/vendor-maintained servers
  only (Astro, Svelte, Playwright, MCP-org reference `filesystem`/`git`/`fetch`) +
  `llms.txt` index; Docker MCP stays application-only; React gets **no entry, settled**
  (no official server exists); GitHub MCP is opt-in-only, never the committed default.

## Live snapshot (2026-09-18)

Checked against the live TTOD tree and studio home this session — not assumed
from older briefs.

| Fact | Value | Where checked |
| ---- | ----- | ------------- |
| Root contract | `AGENTS.md` (190 lines); `CLAUDE.md` is a 10-line redirect | `wc -l`, file read |
| Neutral pack already present | `agentic/report-steward/` (agent · rules · skills · scripts · `PACK.md`) | `find agentic -type f` |
| Cursor landing (project) | `.cursor/rules/ttod-editing.mdc`, `.cursor/skills/public-docs-i18n/SKILL.md` (2 files) | `find .cursor -type f` |
| Claude landing (project) | `.claude/agents/cascade-*.md` — already thin stubs → `~/src/.agents/agents/` | file headers |
| Studio canonical (partial) | `~/src/.agents/` — README + 2 cascade agents + `assignment-forger` skill skeleton | `find ~/src/.agents -type f` |
| Studio Cursor still fat | `~/src/.cursor/skills/` ≈ 18 skill dirs; agents are stubs | `ls ~/src/.cursor` |
| Prior agentic remote ref | `origin/agentic/gh-pack` (unrelated gh-pack work; do not reuse blindly) | `git branch -a \| grep agentic` |
| Programme letters Q–V taken | Next free programme letter **W** | `docs/DEV_PLAN/PHASE-*` inventory |
| Canonical data | Untouched by this session; plan authorizes no `ttod.yml` mutation | scope declaration |

## Related studio precedent (do not confuse)

| Precedent | Path | Relation to Phase W |
| --- | --- | --- |
| Studio `.agents/` plan | `~/src/.agents/README.md` (2026-09-11) | Same *problem* (body duplication); different *home name* (`.agents` vs `agentic`). AG0 freezes the map. |
| Report-steward pack | `ttod/agentic/report-steward/` | Already the target *shape* for a governed agent pack inside this repo. |
| Phase V proposal pipeline | `PHASE-V-FEII-…` §2.7 | Pedagogical analogue for how this cleanup branch merges. |
| Cascade-forge | `~/src/.cursor/skills/cascade-forge/SKILL.md` | Authoring shape for this pack. |
