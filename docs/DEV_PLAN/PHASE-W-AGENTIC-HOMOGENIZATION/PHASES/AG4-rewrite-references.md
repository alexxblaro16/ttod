# AG4 — Rewrite evergreen references (not historical reports)

**Status:** DONE (2026-09-18) — `AGENTS.md` rewritten with edit-home table, discovery map,
and the old `.cursor`-read instruction fixed; cold-reviewed PASS, zero findings. See
`../PHASE-AG4-REPORT.md` and `../PHASE-AG4-COLD-REVIEW.md`.  
**Depends on:** landings live; bodies under `agentic/` — both satisfied, see `../PHASE-AG3-REPORT.md`

## Goal

Update **evergreen** pointers so humans and agents edit under `agentic/`, while
landings remain the tool load path. Leave historical phase reports alone unless the
AG4 allowlist explicitly includes a path.

## Deliverables

1. `AGENTS.md` path table updated (edit-home vs load-path distinguished).
2. `scripts/generate-ts5-teaching-baseline.sh` and similar generators updated if they
   copy full `.cursor` bodies — they should copy landings + `agentic/` as needed for
   the student artifact policy AG0 froze.
3. Short allowlist/blocklist for `git grep` verification in the phase report.

## Scope

| In | Out |
| --- | --- |
| `AGENTS.md`, README agent sections, live scripts, CI comments | Rewriting old `PHASE-*-REPORT.md` path strings |
| Clarifying studio `ttod-bridge` still lives under studio skills until a studio cascade moves it | Claiming Phase W migrated all studio skills |

## Prompt (paste when executing)

```text
Execute AG4 only. Update evergreen references per allowlist. Do not rewrite
historical reports. Keep CI privacy watcher path working. Full suite green.
Stop at VERIFYING. Do not mark DONE; hand off for cold review.
```

## Acceptance

- [ ] `AGENTS.md` states `agentic/` as edit-home for TTOD rules/skills and names
      `.cursor`/`.claude` as landings.
- [ ] `AGENTS.md` contains a **discovery map** (or Integration rows) linking:
      (1) `agentic/` harness, (2) `services/mcp/` product FastMCP, (3) Astro/Oracle
      as MCP *client* path — without claiming Astro or `agentic/` contains the server.
- [ ] `agentic/README.md` links back to `../AGENTS.md` and one-lines the product MCP
      pointer (`services/mcp/`).
- [ ] `git grep -n 'Read \`.cursor/rules/ttod-editing'` AGENTS.md` returns 0 (or
      only a historical footnote AG4 allowlists).
- [ ] Privacy watcher still invoked as
      `agentic/report-steward/scripts/check_public_privacy.py` in
      `.github/workflows/public-docs-pages.yml` (path exists).
- [ ] Generator dry-run or documented copy list still produces a runnable student
      baseline per AG0 policy.
- [ ] Full suite green.
- [ ] Negative: `services/mcp` was **not** moved under `agentic/` (`test -d services/mcp`
      and `test ! -d agentic/mcp` or AG0-approved equivalent).

## Risks

- Updating generators to omit `agentic/` leaves students without privacy/report skills.
- Over-rewriting history destroys provenance of older reports.
