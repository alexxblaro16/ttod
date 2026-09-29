# Legibility-test transcripts (Haiku, no tools, README + listings only)

Reader instructions: classify each top-level `agentic/` entry (pack / leaf rule / leaf skill /
other); classify each `.cursor`/`.claude` file; say where to add a new rule / skill / harness; say
what must never be renamed; report anything confusing. Prompts were built from the README under
test plus `find agentic -maxdepth 2` and the landing listing.

## Run 1 — Y0 README (commit `a6cb144a`) — PASS

```
1. ide-mcp/ - pack - Byte-mirrored multifile MCP student IDE harness
2. lao-tzu-tao-compose/ - pack - Generated pipeline pack untracked local repository
3. report-steward/ - pack - Locked CI privacy watcher evidence harness
4. rules/ - other - Directory container for leaf editing rules
5. skills/ - other - Directory container for leaf workflow skills

2. .claude/agents/cascade-cold-reviewer.md - landing (redirect)
   .claude/agents/cascade-phase-executor.md - landing (redirect)
   .cursor/mcp.json - byte-copy exception
   .cursor/rules/ttod-editing.mdc - landing (redirect)
   .cursor/skills/public-docs-i18n/SKILL.md - landing (redirect)

3. (a) agentic/rules/<name>.md
   (b) agentic/skills/<name>/SKILL.md
   (c) agentic/<name>/ with PACK.md at its root

4. Never rename report-steward/ — CI (public-docs-pages.yml) runs
   report-steward/scripts/check_public_privacy.py at that exact path.

5. Nothing.
```

## Run 2 — negative control: `main`'s pre-Y0 README, same listings — FAIL (contradictions found)

```
1. ide-mcp: pack — PACK.md, multi-subdir harness
   lao-tzu-tao-compose: pack — PACK.md, multi-subdir harness
   report-steward: pack — PACK.md, multi-subdir harness
   rules: leaf rule — single YAML file container
   skills: leaf skill — single skill subdir container

2. .claude/agents/cascade-cold-reviewer.md: landing (redirect)
   .claude/agents/cascade-phase-executor.md: landing (redirect)
   .cursor/mcp.json: other
   .cursor/rules/ttod-editing.mdc: landing (redirect)
   .cursor/skills/public-docs-i18n/SKILL.md: landing (redirect)

3. (a) Always-on YAML rule: agentic/rules/<rule-name>.md
   (b) One-off workflow skill: agentic/skills/<skill-name>/SKILL.md
   (c) Multi-file harness with script: agentic/<harness-name>/PACK.md + agentic/<harness-name>/scripts/

4. Never rename agentic/report-steward/scripts/check_public_privacy.py — CI depends on it.

5. Contradictions found: (1) README says ide-mcp/ is "Not yet created" but it exists with PACK.md,
   README.md, examples/, llms/, scripts/, mcp.cursor.json. (2) README's "deliberately absent"
   section claims cascade subagents are absent, but .claude/agents/cascade-*.md exist in the file
   listing — they appear to be landings but the absence claim is misleading. (3) README references
   agentic/agents/ as "Reserved, currently empty" but no such directory exists.
```

## Run 3 — final tree (README at Y2, commit `00349309`) — PASS

```
1. ide-mcp: pack - student IDE MCP harness multi-file pack
   lao-tzu-tao-compose: pack - generated bibliography pack local and untracked
   report-steward: pack - CI-locked evidence reports public privacy watcher
   rules: other - container for leaf rules never packs
   skills: other - container for leaf skills never packs
2. .claude/agents/cascade-{cold-reviewer,phase-executor}.md: landing (redirect)
   .cursor/mcp.json: byte-copy exception (JSON cannot redirect)
   .cursor/rules/ttod-editing.mdc, .cursor/skills/public-docs-i18n/SKILL.md: landing (redirect)
3. (a) agentic/rules/<name>.md  (b) agentic/skills/<name>/SKILL.md  (c) agentic/<name>/PACK.md
4. Never rename report-steward/ — CI runs report-steward/scripts/check_public_privacy.py there.
5. Nothing.
```

Caveat, stated plainly: the readers are a single small-model sample each, and the listing given
to Run 2 already contained `ide-mcp/PACK.md` (added in Y0). The control shows the test can fail on
the old README; it is not a statistical claim.
