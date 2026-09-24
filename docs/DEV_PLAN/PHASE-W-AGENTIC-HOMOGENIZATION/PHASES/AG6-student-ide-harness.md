# AG6 — Student IDE harness (MCP configs, llms index, existence probes)

**Status:** DONE, MERGED (2026-09-19) — `.cursor/mcp.json` (Astro/Svelte/Playwright/
filesystem), `verify-ide-mcp.py`, and `simulate-student-check.py` all built and live-verified
(real MCP handshakes, 4/4 pass, independently reproduced by cold review); deliverable 9b's
manual walkthrough completed in full by the product owner, including real per-server tool
calls (live Astro/Svelte docs content, a real Playwright navigation, a confirmed filesystem
sandbox boundary). Merged to `main` via [PR #22](https://github.com/ruvebal/ttod/pull/22)
(`--admin`, required check hadn't run). See `../PHASE-AG6-REPORT.md` and
`../PHASE-AG6-COLD-REVIEW.md`.  
**Depends on:** AG0 discovery-map freeze — satisfied, see `../PHASE-AG0-REPORT.md` and
`../PHASE-AG4-REPORT.md`

## Goal

Give co-developer students a **project-level** IDE agent harness: committed MCP
client config for **official, vendor-maintained servers only** (Astro docs,
Svelte official, Playwright official, plus the general-purpose
`modelcontextprotocol`-org reference servers where useful), an indexed
`llms.txt` tree agents can read, a short “role of each piece” section (from
[`AGENTIC-HARNESS.md`](../AGENTIC-HARNESS.md)), and a **verification** script that
proves the config exists and (when network is allowed) that servers respond.
Keep **Docker / `services/mcp`** strictly application-level and out of this file set
except as a named sibling in the discovery map.

**Official-only policy (hard rule, not a preference):** a server qualifies for the
cohort default only if it is published and maintained by the framework/tool vendor
itself (e.g. Astro's own `mcp.docs.astro.build`, Svelte's own `@sveltejs/mcp`,
Microsoft's own `@playwright/mcp`) or by the `modelcontextprotocol` reference-server
org itself (`@modelcontextprotocol/server-*`). Third-party/community/marketplace
listings (Smithery, unaudited npm packages claiming to wrap a framework's docs) are
never cohort-default, regardless of how convenient the install looks. This is not
specific to React — it is the general rule React's case exposed: **React has no
official MCP server (Meta does not publish one)**, so React gets no IDE MCP entry
at all, not a third-party substitute.

## Deliverables

1. `agentic/ide-mcp/README.md` — student setup; HTTP vs stdio; single-folder Cursor warning;
   states the official-only policy above and why (untrusted-server attack surface on every
   student machine, not just a taste preference).
2. `agentic/ide-mcp/mcp.cursor.json` + committed landing `.cursor/mcp.json` (same content
   or generated copy — AG6 picks one mechanism and documents it).
3. Optional `agentic/ide-mcp/mcp.claude-code.json` / `examples/*.json` for Desktop etc.
4. `agentic/ide-mcp/llms/` — vendored Svelte prompts `llms.txt` (+ README); optional Astro
   index if a stable URL is frozen in AG0.
5. `agentic/ide-mcp/scripts/verify-ide-mcp.sh` (or Python) + a unittest or Makefile target
   that runs the **offline** subset in CI. The script also asserts that every server key in
   `.cursor/mcp.json` is on the named official-servers allowlist (§ below) — a config drift
   toward an unaudited server fails CI, not just a human review.
6. **React MCP: settled, not deferred for reconsideration.** No entry ships. Document in
   `README.md` that this is permanent pending Meta ever publishing an official server, not a
   "revisit later" TODO — react.dev context stays file/docs-based (existing course materials,
   `context7`-style copy-paste, or a future *studio-hosted* option is explicitly out of reach
   for students off the LAN; see rejected-alternatives note in `AGENTIC-HARNESS.md` §4).
7. **Official studio dev-tools MCP pack** — beyond the two framework-doc servers, add to the
   committed cohort config (or document as an easy opt-in block in the README, instructor's
   call which are default-on vs opt-in):
   - `@playwright/mcp` (Microsoft, official) — browser automation via accessibility snapshots;
     directly useful for students testing the Astro/Svelte frontend they are building, and
     framework-agnostic so it is the closest thing to a "React-shaped" capability available
     without a React-specific server.
   - `@modelcontextprotocol/server-filesystem` (MCP-org reference), scoped to the repo root
     only (never the student's home directory) — safe, sandboxed file access for agents.
   - `@modelcontextprotocol/server-git` (MCP-org reference) — repo history/search tools.
   - `@modelcontextprotocol/server-fetch` (MCP-org reference) — general web-content fetch,
     useful when a framework has no dedicated docs MCP (covers gaps like React's).
   - GitHub's official `github-mcp-server` (`github/github-mcp-server`) is **explicitly not
     cohort-default** — not only because of the credential, but because a `github` entry in the
     committed `.cursor/mcp.json` would show disconnected/red for every student who hasn't set
     one up, failing the fresh-clone "nothing red by default" bar (deliverable 9). Ship it as an
     **opt-in pair**: `agentic/ide-mcp/examples/github.json` (server block referencing
     `${env:GITHUB_PERSONAL_ACCESS_TOKEN}`, or Cursor's `envFile` pointing at `.env`) plus a
     committed `.env.example` (variable name only, no value) with `.env` gitignored. No SSH-key
     option exists for this server — it only supports OAuth, PAT, or GitHub App auth, and does
     not read an existing `gh auth login` session; a student's SSH-based git access does not
     help with this setup step. Opting in is: merge the block, copy `.env.example` → `.env`,
     add your own token — never paste a secret into a file the repo tracks.
   - No official standalone TypeScript-language-server MCP was found as of this phase's
     authoring; do not fabricate one into the pack. Re-check when AG6 executes, not before.
8. Explicit non-install: no `@modelcontextprotocol/server|client` in frontend
   `package.json` unless a separate optional lab is authorized. (Running reference servers via
   `npx` at IDE-config time does not add them to `package.json` — that distinction stays intact.)
9. **Student-simulation smoke test — "am I actually wired," not just "does the JSON parse."**
   `verify-ide-mcp` (deliverable 5) checks config shape and the allowlist; it does not prove a
   server actually speaks MCP or that a fresh co-developer, not the instructor's already-tuned
   machine, would see it work. Two parts, both required, because neither alone is trustworthy:

   a. **Automated protocol-level probe** —
      `agentic/ide-mcp/scripts/simulate-student-check.sh` (or `.py`), runnable standalone
      without Cursor or Claude Code open. For each **stdio** server in the committed
      `.cursor/mcp.json` (`svelte`, `playwright`, `filesystem`, `git`, `fetch` if enabled), it
      spawns the exact committed command (`npx -y @sveltejs/mcp`, etc.), sends a real MCP
      `initialize` JSON-RPC request over stdin, and asserts a well-formed `initialize` response
      comes back on stdout within a timeout — proof the server actually starts and speaks MCP,
      not just that `npx --help` exits 0. For the **HTTP** Astro server, it performs the same
      `initialize` handshake as an HTTP POST against `https://mcp.docs.astro.build/mcp`
      (skippable offline, matching the existing offline/live split in deliverable 5). Exit
      nonzero and name the failing server if any handshake fails or times out — this is a
      *live* check (network + `npx` fetch required), documented as such, never folded into the
      offline CI gate deliverable 5 already owns.
   b. **"Confirm it like a new co-developer would" — README walkthrough, run from a clean
      checkout, not the instructor's tuned environment.** A short, numbered section in
      `agentic/ide-mcp/README.md`:
      1. `git worktree add --detach /tmp/ttod-student-sim <branch-under-test>` — detached,
         not a second checkout of the branch by name, since the primary clone may already
         have that branch checked out (a worktree can't share a branch across two working
         directories). Point `<branch-under-test>` at whichever branch actually holds the
         harness — simulating against `main` proves nothing while AG6 lives on its own
         branch. Sanity-check before opening the IDE: `.cursor/mcp.json` and
         `agentic/ide-mcp/` should both exist in the new worktree. Throwaway, no
         pre-existing global Cursor state assumed — closest reproduction of "student just
         cloned the repo" available without a second machine.
      2. Open **that folder** (single-root, per the multi-root caveat in
         `AGENTIC-HARNESS.md` §4) as a fresh Cursor window.
      3. Enable each server in Cursor's MCP panel — a required one-time trust step for any
         project-committed MCP config (servers start **disabled**, not connected, until
         flipped on; this is Cursor's own security gate, not a sign the config is broken) —
         then confirm each shows connected/green. Nothing to install beforehand; the one
         click per server is the only manual step. **Confirmed by direct testing during this
         phase, not assumed:** the four TTOD servers do start disabled in a fresh worktree,
         while a pre-existing personal/global server the tester had already trusted showed
         connected — exactly the asymmetry this step exists to explain, not paper over.
      4. Ask the agent one *real*, verifiable question per server whose answer only a working
         MCP call (not model memory) could get right — e.g. "use the Svelte MCP to fetch the
         current `$state` rune docs and quote one exact sentence," "use the Playwright MCP to
         take an accessibility snapshot of `http://localhost:4321`" (with `make up` running).
         A plausible-sounding but unverifiable answer is a **fail**, not a pass — model memory
         can fake a docs summary; only a real tool call returns something checkable against the
         live source.
      5. `git worktree remove /tmp/ttod-student-sim` when done — this is a one-off simulation,
         not a standing worktree to maintain (same pattern as the review-worktree escape hatch
         in `docs/public/guides/reviewing-cohort-prs.md`).
      Record the outcome (which servers passed the live question, which didn't) in the AG6
      phase report as evidence — "I ran the walkthrough, here's what each server actually
      returned" — not a checkbox ticked from memory.

## Scope

| In | Out |
| --- | --- |
| Project-level IDE MCP for Astro + Svelte + Playwright + MCP-org reference servers | Moving `services/mcp` into `agentic/` |
| llms.txt vendor + offline verify | Requiring cloud frontier API keys in git |
| Existence probes (config + optional live) | Replacing product Ollama with cloud LLM |
| Harness role section linked from `AGENTS.md` | Mandating Claude Desktop for all students |
| Official-servers allowlist, enforced by `verify-ide-mcp` | Third-party/community MCP servers (Smithery or any unaudited marketplace listing) as cohort-default |
| GitHub MCP as a documented, individually opt-in example | GitHub MCP (or any credentialed server) in the committed default config |

## Prompt (paste when executing)

```text
Execute AG6 only per
docs/DEV_PLAN/PHASE-W-AGENTIC-HOMOGENIZATION/PHASES/AG6-student-ide-harness.md.
Read ../AGENTIC-HARNESS.md first. Commit project-level MCP config for Astro,
Svelte, and Playwright (all official/vendor-maintained) plus needed
modelcontextprotocol-org reference servers (filesystem scoped to repo root,
git, fetch); vendor svelte llms.txt; add verify script (offline CI + optional
live) that also enforces the official-servers allowlist. Do not add
@modelcontextprotocol/* to services/frontend unless a separate lab is
explicitly authorized. Do not treat Docker MCP as IDE MCP. React MCP: no
entry — no official server exists; do not substitute a third-party one.
GitHub MCP: opt-in example only, never in the committed default (credential
handling). Build simulate-student-check (real MCP initialize handshakes, not
process-spawn checks) and actually run the README walkthrough from a
throwaway git worktree — record what each server returned in the phase
report, not a checkbox from memory. Full suite + offline verify green. Stop
at VERIFYING. Do not mark DONE; hand off for cold review.
```

## Acceptance

- [ ] `.cursor/mcp.json` exists in git and lists `astro-docs` (or AG0 name), `svelte`,
      and `playwright`.
- [ ] Astro entry uses HTTP URL **or** documented `mcp-remote` stdio fallback — both
      documented; one marked default.
- [ ] Svelte entry is `npx -y @sveltejs/mcp` (or AG0-pinned version).
- [ ] Playwright entry is `npx @playwright/mcp@latest` (or AG0-pinned version).
- [ ] Every server key in the committed `.cursor/mcp.json` is on a documented
      official-servers allowlist in `agentic/ide-mcp/README.md`; `verify-ide-mcp` fails
      if an unlisted server key appears (proves the policy is load-bearing, not prose).
- [ ] `agentic/ide-mcp/llms/` contains Svelte prompts index; README tells agents when to
      use file vs MCP `get-documentation`.
- [ ] `verify-ide-mcp` offline mode exits 0 in CI; live mode documented for students.
- [ ] `AGENTS.md` discovery map links this harness and states Docker MCP ≠ IDE MCP.
- [ ] React MCP: no server key present anywhere in the committed default config;
      `README.md` states the "no official server exists" reason, not "deferred."
- [ ] GitHub MCP, if documented at all, exists only under `agentic/ide-mcp/examples/`
      and is absent from the committed `.cursor/mcp.json`.
- [ ] `git grep -n '@modelcontextprotocol/server' services/frontend/package.json`
      returns 0 (unless lab authorized).
- [ ] Full existing suite still green.
- [ ] Negative: removing `.cursor/mcp.json` makes offline verify fail (proves the check
      is load-bearing).
- [ ] Negative: injecting an unlisted server key into a scratch copy of `.cursor/mcp.json`
      makes `verify-ide-mcp` fail (proves the allowlist check is load-bearing, not decorative).
- [ ] `simulate-student-check` performs a real MCP `initialize` handshake (not just process
      spawn / `--help`) against every stdio server in the committed config, and the HTTP
      handshake against Astro's endpoint when network is allowed; documented as a live check,
      separate from `verify-ide-mcp`'s offline CI gate.
- [ ] The README's "confirm it like a new co-developer would" walkthrough was actually run
      from a throwaway `git worktree`, not just written — the AG6 phase report names which
      server(s) answered a real, checkable question correctly and quotes what each returned
      (a plausible-sounding but unverifiable answer counts as a fail, not a pass).

## Risks

- npx-on-first-agent-call surprises air-gapped students — document Node/npm prerequisite.
- HTTP Astro MCP blocked on campus networks — document stdio fallback.
- Treating IDE MCP outages as product bugs — keep checklists separate.
- A future contributor re-adds a third-party "convenience" server (React or otherwise)
  without reading the official-only policy — the CI allowlist check, not just this
  document, is what actually prevents that.
- `@modelcontextprotocol/server-filesystem` misconfigured with too broad a root would
  hand an agent read/write over the student's whole home directory — must be pinned to
  the repo root in the committed config, never left as a default/unset argument.
- "It works on the instructor's machine" is not evidence: global user-level Cursor config,
  a warm `npx` cache, or an already-authenticated tool can mask a project-config bug that
  a genuinely fresh student clone would hit. The student-simulation deliverable exists
  specifically to catch that gap — running it from the instructor's normal, already-tuned
  working copy instead of the throwaway worktree defeats its purpose.
- A tool call that returns a fluent but fabricated-sounding answer can look like a pass at a
  glance — the walkthrough's questions must have a checkable, specific answer (an exact
  quoted sentence, a real accessibility-tree snapshot) precisely so a model-memory guess is
  distinguishable from a real MCP round-trip.
