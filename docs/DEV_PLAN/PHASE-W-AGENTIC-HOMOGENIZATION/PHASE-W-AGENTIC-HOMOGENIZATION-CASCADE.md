# Phase W — Technical Director Cascade (Agentic Homogenization)

**Status:** COMPLETE — AG0–AG6 all merged to `main` (PR #21, PR #22; 2026-09-18/19).  
**Does not authorize:** creating the branch, moving files, rewriting landings, merging to
`main`, mutating `ttod.yml`, or renaming `~/src/.agents/` without an AG0 decision.  
**Depends on:** Phase Q governance; existing `agentic/report-steward/` pack; studio
`.agents/` README as precedent (not as automatic authority over TTOD naming).  
**Step labels:** `AG0`–`AG6` (“Agentic Governance”), under programme letter **W**.

## 0. Mission

Make TTOD’s agent-facing material **homogenized under `agentic/`**, with proprietary
tool directories (`.cursor/`, `.claude/`) reduced to **landings** that load the same
bodies. Record how the cleanup **branch** is opened and how its **merge** teaches the
same human-accept discipline students already use for quote proposals. Add a
**student IDE harness** (project-level Astro/Svelte MCP + `llms.txt` index + existence
probes) without conflating it with Docker application MCP.

**Workload honesty:** AG0–AG5 are layout/governance. They are **not** yet a wired
“frontier orchestrator + local Ollama validator fleet.” Closing protocol uses the
ready subagents `cascade-phase-executor` and `cascade-cold-reviewer` (+ report-steward
privacy). Dual-model / extra MCP validators are specified in
[`AGENTIC-HARNESS.md`](AGENTIC-HARNESS.md) and delivered under **AG6**.

## 1. Programme (do not invert)

| Step | File | Deliverable | Gate |
| ---- | ---- | ----------- | ---- |
| AG0 | [PHASES/AG0-inventory-and-naming-freeze.md](PHASES/AG0-inventory-and-naming-freeze.md) | Decision record: canonical home map (`agentic/` vs `~/src/.agents/`); inventory table frozen; IDE vs Docker MCP ontology | **DONE** (2026-09-18) — `DECISIONS/W0-2026-09-18-AGENTIC-HOME.md` frozen, FINDINGS F1/F3 closed, cold-reviewed PASS ([`PHASE-AG0-REPORT.md`](PHASE-AG0-REPORT.md)) |
| AG1 | [PHASES/AG1-branch-and-target-layout.md](PHASES/AG1-branch-and-target-layout.md) | Target tree sketch + **branch name frozen**; branch creation commands in report (executed only when authorized) | **DONE** (2026-09-18) — tree + name frozen, cold-reviewed clean; branch `agentic/homogenize-landings` created from `main`@`7a738cae` at explicit human authorization ([`PHASE-AG1-REPORT.md`](PHASE-AG1-REPORT.md)) |
| AG2 | [PHASES/AG2-migrate-bodies-into-agentic.md](PHASES/AG2-migrate-bodies-into-agentic.md) | Bodies of TTOD-scoped rules/skills/agents live under `agentic/`; `report-steward` undisturbed; seed `agentic/README.md` pointing at harness annex | **DONE** (2026-09-18) — byte-identical moves confirmed (SHA-256), 219 tests + strict validate green, cold-reviewed PASS ([`PHASE-AG2-REPORT.md`](PHASE-AG2-REPORT.md)) |
| AG3 | [PHASES/AG3-landing-stubs.md](PHASES/AG3-landing-stubs.md) | `.cursor/` and `.claude/` stubs with real frontmatter + redirect only (`.cursor/mcp.json` is AG6 tooling, not a skill body) | **DONE** (2026-09-18) — 3-line redirect stubs, `.claude` correctly left untouched per W0 §2, cold-reviewed PASS ([`PHASE-AG3-REPORT.md`](PHASE-AG3-REPORT.md)) |
| AG4 | [PHASES/AG4-rewrite-references.md](PHASES/AG4-rewrite-references.md) | Evergreen docs, generators, CI path comments updated; discovery map includes IDE harness pointer | **DONE** (2026-09-18) — `AGENTS.md` discovery map + edit-home table live, cold-reviewed PASS ([`PHASE-AG4-REPORT.md`](PHASE-AG4-REPORT.md)) |
| AG5 | [PHASES/AG5-verify-and-merge-gate.md](PHASES/AG5-verify-and-merge-gate.md) | Full verification + pedagogical merge note + PR checklist; merge only by named human | **DONE, merged** — PR [#21](https://github.com/ruvebal/ttod/pull/21), cold-reviewed PASS, merged by the product owner (`--admin`, required check hadn't run) ([`PHASE-AG5-REPORT.md`](PHASE-AG5-REPORT.md)) |
| AG6 | [PHASES/AG6-student-ide-harness.md](PHASES/AG6-student-ide-harness.md) | Project-level IDE MCP (Astro+Svelte+Playwright+MCP-org reference), `llms.txt` index, verify script, harness roles in `AGENTS.md` / `agentic/ide-mcp` | **DONE, merged** — offline + live (real MCP handshake) verification pass, cold-reviewed with independent reproduction, **and** the human-run manual walkthrough completed with real per-server tool calls; merged to `main` via [PR #22](https://github.com/ruvebal/ttod/pull/22) ([`PHASE-AG6-REPORT.md`](PHASE-AG6-REPORT.md)) |

**Harness note:** Gate column first word is the harness status token
(`READY|BLOCKED|IN_PROGRESS|VERIFYING|COLD_REVIEW|DONE`); prose after it is human-facing.

## 2. Master paste (start / resume — when execution is authorized)

```text
Implement Phase W per
docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/PHASE-W-AGENTIC-HOMOGENIZATION-CASCADE.md.

## Context
- Evidence: docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/FINDINGS-2026-09-18.md
- Product why: …/RATIONALE.md
- Skill shape: ~/src/.cursor/skills/cascade-forge/SKILL.md (until AG2 moves it — do not
  migrate cascade-forge in this cascade unless AG0 explicitly scopes it in)

## Out of scope
- ttod.yml mutation, proposal accept, ID allocation
- Renaming or deleting ~/src/.cursor/skills/* studio skills wholesale
- Deleting historical DEV_PLAN reports that mention .cursor paths
- Merging to main without a named human
- Creating the branch before AG0 DONE and AG1 Acceptance
- Adding @modelcontextprotocol/* to services/frontend just to consume docs MCPs
- Treating Docker services/mcp as an IDE MCP server
- Shipping any third-party/community MCP server as cohort-default — official/vendor-maintained
  or `modelcontextprotocol`-org reference servers only (React gets no entry at all: no official
  server exists, and a third-party substitute is never acceptable regardless of convenience)
- Shipping GitHub MCP (or any credentialed server) in the committed default config — opt-in
  example only, per its own OAuth/PAT credential-in-git rule

## Programme
Execute the next incomplete phase only, in order AG0 → AG6.
After each phase: VERIFYING → cold subprocess review → PHASE-AGn-COLD-REVIEW.md →
triage/amend → PHASE-AGn-REPORT.md.
Implementer must not self-certify DONE.
Read docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/AGENTIC-HARNESS.md for roles and
validator readiness before claiming a dual-model or MCP-validator fleet.

## Hard constraints
- AGENTS.md wins over CLAUDE.md and over any landing stub
- Preserve agentic/report-steward paths used by CI (public-docs-pages.yml)
- Landings keep real per-tool frontmatter; bodies are not duplicated
- No cloud AI SDKs; no force-push; do not commit unless the human asks
- Branch name must not reuse origin/agentic/gh-pack
```

## 3. Resume rule

Report status enum: `BLOCKED` | `READY` | `IN_PROGRESS` | `VERIFYING` | `COLD_REVIEW` |
`DONE` | `PARTIAL`.

| Report status | Resume action |
| --- | --- |
| `DONE` | Skip; open next phase only if its dependencies are DONE |
| `PARTIAL` | Finish remaining Acceptance items in that phase; do not start the next |
| `IN_PROGRESS` | Continue the same phase; do not open a second AG lane |
| `VERIFYING` | Do not edit product files; run/fix verification; then hand to cold review |
| `COLD_REVIEW` | Wait for `PHASE-AGn-COLD-REVIEW.md`; triage findings; amend cascade if needed |
| `BLOCKED` | Read Blockers; do not improvise authority; stop |
| `READY` | Paste the phase runbook and start |

## 4. Closing protocol

```
BLOCKED → READY → IN_PROGRESS → VERIFYING → COLD_REVIEW → DONE
```

Implementer never promotes to DONE. Prefer
[`cascade-phase-executor`](../../../.claude/agents/cascade-phase-executor.md) and
[`cascade-cold-reviewer`](../../../.claude/agents/cascade-cold-reviewer.md) (stubs →
studio canonical until AG0 remaps them).

Amend-on-surprise: if AG2 discovers a body that is studio-scoped (not TTOD), do not move
it into `ttod/agentic/`; amend AG0/AG2 scope in the same commit as the phase report.

## 5. Branch plan (do not create in the planning session)

| Item | Planned value | Notes |
| --- | --- | --- |
| Base | `main` at the commit recorded in AG1’s report | Capture `git rev-parse HEAD` before branching |
| Branch name (proposed) | `agentic/homogenize-landings` | Avoids collision with `origin/agentic/gh-pack` |
| Creation (AG1, when authorized) | `git switch -c agentic/homogenize-landings` from clean `main` | Optional: worktree via `cascade-harness.sh` if harness is used |
| Push | Only when human asks | `git push -u origin HEAD` |
| PR title (proposed) | `agentic: homogenize rules/skills/agents; .cursor/.claude as landings` | Links Phase W INDEX |
| PR creation (AG5, agent may run) | `gh pr create --base main --head agentic/homogenize-landings --title "agentic: homogenize rules/skills/agents; .cursor/.claude as landings" --body-file <PHASE-AG5-REPORT.md PR-body section>` | Agent opens the PR; this is not a merge |
| Merge authority | Named human (product owner) after AG5 | Agent opens PR; agent does not merge |
| Merge (human-only, after cold review + `MERGE_APPROVED`) | `gh pr merge --merge --delete-branch` (or `--squash` if the human prefers a single commit) | **Never run by the agent.** Requires the human to have read `PHASE-AG5-COLD-REVIEW.md` and recorded `MERGE_APPROVED` in `PHASE-AG5-REPORT.md` first |
| Rollback if merged in error | `git revert -m 1 <merge-sha>` on `main` | Prefer revert over `reset --hard`; this branch only touches docs/agent-tree paths, not `ttod.yml` |

AG1 may amend the branch string if `agentic/homogenize-landings` is taken; record the
final string in `PHASE-AG1-REPORT.md` before any commits land on it.

## 6. Pedagogical merge — how this is the TTOD process in miniature

Students already practice a **two-touchpoint** path for governed quotes (Phase V §2.7):

```text
propose (JSON under proposals/)
    → PR review (human comments / requests changes)
    → approval triggers cli.py proposal accept  (computes ttod.yml diff)
    → second human approval + merge            (lands the canonical write)
```

Phase W’s cleanup uses the **same mental model**, with different write authority:

```text
AG0 freeze (decision record)                 ≈ schema / rights freeze before propose
branch agentic/homogenize-landings           ≈ proposal branch
AG2–AG4 commits on that branch               ≈ proposal payload + computed diff
PR + cold review (AG5)                       ≈ human review of the exact diff
product-owner merge to main                  ≈ second touch: land the accepted layout
```

| Quote pipeline | Agentic homogenization | Teaching point |
| --- | --- | --- |
| `proposal create` | Open `agentic/homogenize-landings` | Work happens off `main` |
| Reviewer comments on PR | Cold review + PR review | Another mind reads the diff |
| `proposal accept --reviewer-id` | N/A (no `ttod.yml` write) | Accept is for *canonical data*; layout changes use ordinary merge |
| Human merge of the accept diff | Human merge of the homogenization PR | The living tree changes only when a named human merges |
| Never hand-edit `ttod.yml` | Never leave full bodies in `.cursor` after AG3 | Source of truth is named and singular |

**Classroom phrasing (for AG5’s short note in `AGENTS.md` or teaching docs):**

> “`.cursor` and `.claude` are doorways. `agentic/` is the room. Merging the
> homogenization branch is like accepting a proposal: the PR is the review; the merge
> is the human act that makes the new layout real.”

This isomorphism is **pedagogy**, not a claim that layout PRs run
`cli.py proposal accept`. Canonical quote writes remain on the proposal pipeline only.

## 7. Target layout (sketch — AG1 freezes paths)

```
ttod/
  AGENTS.md                          # unchanged role: root contract + discovery map
  CLAUDE.md                          # stays thin redirect → AGENTS.md
  agentic/
    README.md                        # NEW: map of packs + landings + IDE harness
    report-steward/                  # KEEP pack shape (CI depends on it)
    rules/                           # e.g. ttod-editing.md (body)
    skills/                          # e.g. public-docs-i18n/SKILL.md (body)
    agents/                          # TTOD-scoped agents if any after AG0 map
    ide-mcp/                         # AG6: MCP templates, llms/, verify script
  .cursor/
    rules/ttod-editing.mdc           # LANDING: frontmatter + redirect
    skills/public-docs-i18n/SKILL.md # LANDING: frontmatter + redirect
    mcp.json                         # AG6: project IDE MCP (Astro + Svelte)
  .claude/
    agents/*.md                      # LANDING: frontmatter + redirect (remap per AG0)
  services/mcp/                      # APPLICATION FastMCP — not under agentic/
```

Studio `~/src/.agents/` remains outside this repository’s git object graph; AG0 decides
whether TTOD landings point into `ttod/agentic/`, into `~/src/.agents/`, or both with an
explicit table.

## 8. Layer map

| Layer | Read | Write (when authorized) | Downstream |
| --- | --- | --- | --- |
| `AGENTS.md` | All agents | AG4 (evergreen path table + discovery map: `agentic/` + product MCP + Astro/Oracle) | Humans, all tools |
| `agentic/**` | All agents | AG2+ (harness bodies + `README.md` back-link to `AGENTS.md`) | Skills, CI privacy watcher, teaching generators |
| `.cursor/**` | Cursor loader | AG3 stubs | Cursor IDE only |
| `.claude/**` | Claude Code Agent tool | AG3 stubs | Claude Code only |
| `services/mcp/**` | Oracle backend, Compose, agents (read) | **out of scope** — document only | Astro/Oracle retrieval |
| `services/frontend` · `services/backend` | — | **out of scope** — named in AGENTS.md map only | Product UI / FastMCP client |
| `ttod.yml` | — | **never in this cascade** | — |

**Ontology freeze (AG0 must restate):** `agentic/` = IDE harness. `services/mcp/` =
product FastMCP. Agents discover MCP **through `AGENTS.md` (and `agentic/README.md`
pointer)**, not by nesting the server under `agentic/`.

## 9. Hard constraints (non-negotiable)

1. Phase Q: no hand-edit of `ttod.yml`; no silent relicense.
2. Preserve `agentic/report-steward/scripts/check_public_privacy.py` path for CI.
3. Do not delete `.cursor` or `.claude` directories — empty landings are failures; stubs required.
4. Do not create the branch during planning; AG1 owns creation when authorized.
5. Do not commit unless the human asks.
6. Full existing test suite green before VERIFYING→COLD_REVIEW on AG2–AG5.
7. Historical `docs/DEV_PLAN/PHASE-*-REPORT.md` path mentions of `.cursor` are evidence, not bugs — leave them unless AG4’s allowlist says otherwise.
8. Do not relocate `services/mcp/` under `agentic/`; discovery is via `AGENTS.md` map + `agentic/README.md` pointer only.
9. IDE MCP configs are project-level (`.cursor/mcp.json`); Docker MCP remains application-level only.
10. Do not add TypeScript MCP SDK packages to the Oracle frontend solely for docs MCP consumption.
