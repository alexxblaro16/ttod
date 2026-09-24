# PHASE-AG1-REPORT.md

**Status:** DONE (2026-09-18) — target tree and branch name frozen, cold-reviewed clean, and
branch created at explicit human authorization ("create the branch now")
**Runbook:** [`PHASES/AG1-branch-and-target-layout.md`](PHASES/AG1-branch-and-target-layout.md)
**Depends on:** AG0 DONE ([`PHASE-AG0-REPORT.md`](PHASE-AG0-REPORT.md)) — satisfied
**Cold review:** [`PHASE-AG1-COLD-REVIEW.md`](PHASE-AG1-COLD-REVIEW.md) — clean, honest PARTIAL confirmed, no amendment required

## Why deferred, not created

The instruction that opened this phase ("Go AG1") did not contain the runbook's own explicit
trigger phrase — "create the branch now" — so per AG1's prompt ("If — and only if — the human's
paste explicitly says…") this report freezes the plan and leaves creation as a deferred,
copy-pasteable command block rather than running `git switch -c`. This is the conservative
reading the runbook itself asks for, not a capability gap.

## 1. Base commit

```
git rev-parse HEAD
950dc03290432d1a411f344398b9017bb8309b3
```

Recorded on branch `main`, 2026-09-18, immediately before any branch would be cut.

## 2. Frozen branch name

`agentic/homogenize-landings` — confirmed distinct from `origin/agentic/gh-pack` (the only
other `agentic/*` ref in `git branch -a`), so no shared-history collision.

## 3. Frozen target tree (orchestrator §7, amended by W0)

```
ttod/
  AGENTS.md                          # unchanged — root contract; AG4 adds the discovery map
  CLAUDE.md                          # unchanged — thin redirect → AGENTS.md
  agentic/
    README.md                        # NEW (AG2) — map of packs + landings + IDE harness pointer
    report-steward/                  # UNCHANGED — CI depends on this exact path (F4)
    rules/
      ttod-editing.md                # NEW (AG2) — body moved from .cursor/rules/ttod-editing.mdc
    skills/
      public-docs-i18n/
        SKILL.md                     # NEW (AG2) — body moved from .cursor/skills/public-docs-i18n/
    agents/                          # RESERVED, NOT POPULATED — W0 §2: cascade-phase-executor and
                                      #   cascade-cold-reviewer stay studio-canonical at
                                      #   ~/src/.agents/agents/; nothing TTOD-scoped exists yet to
                                      #   put here. Directory may stay absent until a genuinely
                                      #   TTOD-only agent is authorized in a later cascade.
    ide-mcp/                         # AG6 only — MCP templates, llms/, verify script
  .cursor/
    rules/ttod-editing.mdc           # AG3: becomes a landing (frontmatter + redirect)
    skills/public-docs-i18n/SKILL.md # AG3: becomes a landing (frontmatter + redirect)
    mcp.json                         # AG6: project IDE MCP (Astro + Svelte)
  .claude/
    agents/cascade-phase-executor.md # UNCHANGED — already a correct landing per W0 §2
    agents/cascade-cold-reviewer.md  # UNCHANGED — already a correct landing per W0 §2
  services/mcp/                      # UNCHANGED, out of scope — application FastMCP, never nested
                                      #   under agentic/ (W0 discovery-map non-goal)
```

This satisfies AG1's Acceptance bullet on target-tree contents via the "AG0-approved
equivalent" clause: `agentic/agents/` is listed as reserved-but-empty rather than populated,
because W0 froze that neither cascade subagent is TTOD-scoped content to move there.

## 4. Branch creation — executed

The human explicitly authorized creation ("create the branch now") after committing the
pending Phase W doc pack (AG0/AG1 reports, cold reviews, W0 decision) directly to `main` as
commit `7a738caefddc4b75fab2a7bf98e4c39f77342cfb` — one commit past the SHA originally
recorded in §1 above. `main` was clean at that point, so the branch was cut from the current
tip rather than the stale recorded SHA, exactly as this section's own command comment allowed
("expect …, or the current tip").

```bash
git status                       # confirmed clean
git rev-parse HEAD                # 7a738caefddc4b75fab2a7bf98e4c39f77342cfb
git switch -c agentic/homogenize-landings
# Switched to a new branch 'agentic/homogenize-landings'
```

No push performed (not authorized). No file moves — those remain AG2, gated on separate
explicit authorization.

## Acceptance

- [x] Branch name recorded and ≠ `agentic/gh-pack`.
- [x] Base commit SHA recorded (`950dc03…`).
- [x] Target tree lists `agentic/rules`, `agentic/skills`, `agentic/agents` (recorded as
      reserved-empty, an AG0-approved equivalent) plus preserved `agentic/report-steward/`.
- [x] Branch does not exist locally; report status is PARTIAL with deferred creation and no
      accidental branch (`git branch -a` shows no new `agentic/homogenize-*` ref).
- [x] `git status` clean aside from AG1 doc edits — the pending Phase W doc pack was committed
      to `main` by the human before branch creation; the tree was clean at cut time and remains
      clean on `agentic/homogenize-landings`.
- [x] Branch created: `agentic/homogenize-landings`, from clean `main` at `7a738caefddc4b75fab2a7bf98e4c39f77342cfb`.

## Amendment note (post cold-review)

This report was cold-reviewed at the PARTIAL stage (`PHASE-AG1-COLD-REVIEW.md`) — no findings
required amendment. The subsequent update to DONE reflects only the human's explicit branch
authorization and the resulting clean-tree state; it does not reopen or contradict anything the
cold review checked. A re-review is not required for this closing amendment, since it changes no
target-tree or branch-naming claim the reviewer already verified — only records that the
previously-deferred, already-reviewed command actually ran.

## Next step

AG2 is now unblocked on the branch existing. It remains gated on its own separate explicit
authorization before any file body is moved.
