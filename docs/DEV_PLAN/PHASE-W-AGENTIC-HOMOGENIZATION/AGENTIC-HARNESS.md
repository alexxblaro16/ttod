# Agentic harness — roles (planning annex for Phase W)

**Status:** planning annex · 2026-09-18 · becomes living `agentic/README.md` prose in AG2/AG6  
**Audience:** instructors, co-developer students, cascade implementers

This page answers: what each piece is for, what runs where, and what is **not**
ready yet. It is not authorization to install packages or open the branch.

## 1. Two stacks (do not conflate)

| Stack | Where it lives | Who it serves | LLM |
| --- | --- | --- | --- |
| **Application (product)** | `docker-compose` · `services/mcp` · `services/backend` · `services/frontend` (Astro) | End users / Oracle / graph | **Local Ollama only** (`make up` / `make ollama-pull`) |
| **Development (IDE agents)** | `AGENTS.md` · `agentic/` · `.cursor` / `.claude` landings · **IDE MCP client configs** | Students & instructors coding the product | Often a **frontier** model in Cursor/Claude as orchestrator; may also call local Ollama for bounded jobs |

Docker MCP (`services/mcp`) is **application-level retrieval** for the Oracle.
It is **not** the development MCP harness students add for Astro/Svelte docs.

## 2. Role of each piece

| Piece | Role | Ready today? |
| --- | --- | --- |
| `AGENTS.md` | Root contract + discovery index | Yes (needs AG4 map) |
| `agentic/` | Tool-neutral **edit-home** for rules, skills, packs | Partial (`report-steward` only) |
| `agentic/report-steward/` | Evidence reports + public-privacy watcher (CI) | Yes |
| `.cursor/` · `.claude/` | **Landings** (tool discovery); after AG3, stubs only | Partial (bodies still fat in `.cursor`) |
| `cascade-phase-executor` | Implements one cascade phase; stops at VERIFYING | Yes (stub → `~/src/.agents/`) |
| `cascade-cold-reviewer` | Independent Acceptance audit; never self-DONE | Yes (stub → `~/src/.agents/`) |
| `services/mcp` (Compose) | Product FastMCP read-only corpus retrieval | Yes (Phase R2) |
| Astro frontend | Document shell + islands; **client** of Oracle/backend | Yes (reference) |
| IDE MCP: Astro docs | Official docs tools for agents writing Astro | Config **not** in repo yet → AG6 |
| IDE MCP: Svelte (`@sveltejs/mcp`) | Official Svelte docs/tools/autofixer | Config **not** in repo yet → AG6 |
| IDE MCP: Playwright (`@playwright/mcp`) | Official (Microsoft) browser automation via accessibility snapshots; framework-agnostic testing | Config **not** in repo yet → AG6 |
| IDE MCP: MCP-org reference servers (`server-filesystem` scoped to repo root, `server-git`, `server-fetch`) | Official, general-purpose — sandboxed file access, repo tools, web fetch for frameworks with no dedicated docs MCP | Config **not** in repo yet → AG6 |
| IDE MCP: React | **No official server exists (Meta publishes none).** Settled: no IDE MCP entry, not a third-party substitute, not a "revisit later" | Settled in AG6 — see official-only policy |
| IDE MCP: GitHub (`github/github-mcp-server`) | Official, but requires OAuth/PAT | **Opt-in example only** (`agentic/ide-mcp/examples/`), never the committed default — credential-in-git rule |
| `llms.txt` / Svelte prompts index | Agent-readable prompt/docs index | Vendor + verify in AG6 |
| Dual-model cascade (frontier orchestrator + Ollama validators) | Optional execution mode for Phase W itself | **Not wired** — see §3 |

## 3. Is Phase W orchestrated as “local Ollama workload + frontier orchestrator”?

**No — not as written in AG0–AG5.** Those steps are a **layout/governance** cascade
(homogenize `agentic/`, landings, docs). Closing protocol already names
`cascade-phase-executor` → VERIFYING → `cascade-cold-reviewer`; it does **not**
yet prescribe:

- which model runs the implementer vs the cold reviewer,
- an Ollama-only validator fleet,
- or automated MCP-existence probes as subagents.

| Role | Recommended when executing Phase W / FE II labs | Ready? |
| --- | --- | --- |
| Orchestrator / integrator | Frontier IDE agent (Cursor/Claude) pasting the master prompt | Human + IDE — ready as process |
| Phase implementer | `cascade-phase-executor` (same or separate session) | Ready |
| Cold validator | `cascade-cold-reviewer` in a **fresh** session | Ready |
| Privacy / evidence validator | `report-steward` + `check_public_privacy.py` | Ready |
| Local Ollama workload | Product stack (`llama3.2:1b`, `nomic-embed-text`); optional local coder for draft/translate | Ready for **app**; not required for AG0–AG5 file moves |
| Extra MCP “existence” validators | Scripted probes (`npx`/`curl` to Astro/Svelte/Playwright MCP + official-servers allowlist check) | **To build in AG6** — not ready |
| React MCP validator | **N/A — settled, no server ships** (no official server exists); nothing to validate | Not applicable |

**Honesty rule:** do not claim a multi-validator Ollama fleet exists until AG6’s
probe script and a short runbook are DONE. Cascade-forge already warns against
self-certified DONE; that is the validator bar we actually have.

## 4. Project level vs studio level

| Asset | Install / commit where | Why |
| --- | --- | --- |
| TTOD rules/skills bodies | **Project** `ttod/agentic/` | Students clone one repo and benefit |
| Cursor landings | **Project** `ttod/.cursor/rules|skills` (stubs) | Cursor loads them |
| Cursor IDE MCP servers (Astro, Svelte, Playwright, MCP-org reference) | **Project** `ttod/.cursor/mcp.json` (committed) | Shared cohort config; overrides global same-name; every entry vendor-official or MCP-org reference |
| GitHub MCP (official, but credentialed) | **User home / opt-in example** under `agentic/ide-mcp/examples/github.json` | Never committed default — OAuth/PAT can't go in git |
| Canonical MCP template + notes | **Project** `ttod/agentic/ide-mcp/` | Edit-home; landings may symlink/copy |
| Claude Code project MCP | **Project** `.mcp.json` (if used) — mirror of the same server list | Tool-specific landing |
| Claude Desktop / user-global clients | **User home** only — provide **example** under `agentic/ide-mcp/examples/` | Cannot commit into classmates’ Application Support |
| Studio skills (`ttod-bridge`, `cascade-forge`) | **Studio** `~/src/.cursor/skills` or `~/src/.agents` until studio migration | Not in student cohort artifact unless generator copies a subset |
| Product MCP server | **Project** `services/mcp` via Compose | Application, not IDE |

**Yes — go project-level** for Astro + Svelte + Playwright + MCP-org reference IDE
MCPs and the harness README so every co-developer student gets them on clone.
Keep studio-only skills studio-side, keep credentialed servers (GitHub) out of
the committed config entirely, and keep React without any IDE MCP entry since
none is official.

**Multi-root caveat:** Cursor may fail to load project `.cursor/mcp.json` from a
multi-root `.code-workspace`. Teaching baseline: open the **ttod folder** (or the
student skeleton folder) as a single root.

## 5. Where students save MCP JSON

| Client | Path students use | Source of truth in git |
| --- | --- | --- |
| Cursor | `.cursor/mcp.json` (project) | Same file committed; template also under `agentic/ide-mcp/mcp.cursor.json` |
| Claude Code | project `.mcp.json` (when applicable) | `agentic/ide-mcp/mcp.claude-code.json` → copy/landing |
| Claude Desktop / Codex / Zed / etc. | Vendor-specific **user** config | `agentic/ide-mcp/examples/<client>.json` — copy manually |
| Streamable HTTP vs stdio | Prefer **one** documented default per server in AG6 | Astro: prefer official HTTP URL if client supports `type: http`; else `npx mcp-remote`. Svelte: official stdio `npx -y @sveltejs/mcp` |

**Proposed default cohort block (AG6 freezes exact JSON):**

```json
{
  "mcpServers": {
    "astro-docs": {
      "type": "http",
      "url": "https://mcp.docs.astro.build/mcp"
    },
    "svelte": {
      "command": "npx",
      "args": ["-y", "@sveltejs/mcp"]
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

Fallback for clients without HTTP MCP: Astro via
`npx -y mcp-remote https://mcp.docs.astro.build/mcp`.

`git` and `fetch` reference servers (`@modelcontextprotocol/server-git`,
`@modelcontextprotocol/server-fetch`) are documented as an easy opt-in block in
`agentic/ide-mcp/README.md` rather than committed by default — AG6's call on
default-on vs opt-in, but either way they are on the official allowlist.

**Official-only policy:** every server key above is either vendor-official
(Astro, Svelte, Playwright/Microsoft) or MCP-org reference
(`@modelcontextprotocol/server-*`). No third-party/marketplace server is
cohort-default, ever — this is a standing rule, not a per-framework judgment
call. `verify-ide-mcp` enforces it mechanically (§8).

**React MCP: settled, not deferred.** No entry ships, because no official
server exists (Meta publishes none) — not because the Smithery OneDrive-path
sample specifically was unacceptable. Do not substitute any other third-party
React MCP later without first checking whether a vendor-official one has
shipped. React context stays file/docs-based for students.

**GitHub MCP: opt-in only.** `github/github-mcp-server` is official but
requires OAuth or a personal access token; this project's no-credentials-in-git
rule keeps it out of the committed default. Document it only under
`agentic/ide-mcp/examples/github.json` for students/instructors who want it
individually.

**Why opt-in, pedagogically — this is not just a security footnote:** the other
cohort-default servers (Astro, Svelte, Playwright, the MCP-org reference set)
are safe to commit *because they carry no secret* — anyone who clones the repo
can run them with zero setup, and that zero-setup property is exactly what
"every co-developer gets it on clone" means in practice. A GitHub PAT or OAuth
token is a **personal credential tied to one student's account**; committing
one to `.cursor/mcp.json` would mean either (a) every student silently shares
one instructor's token — a single point of failure and an attribution mess the
moment someone's automated PR looks like it came from the instructor, or (b)
each student is expected to overwrite the committed file with their own
secret, which trains them to treat "put a token in a file that `git status`
shows as clean" as a normal, then a required, habit. Both outcomes are the
opposite of what the course should teach about credential hygiene. Keeping it
as a **named, opt-in example file** instead does three pedagogical things at
once: it still tells students the tool exists and exactly how wire it up if
they want it; it makes the commit-vs-don't-commit boundary a visible, teachable
line rather than an invisible default; and it means the cohort-default config
— the one every student actually runs on Day 0 — never depends on anyone
having set up a credential first, so setup friction stays at zero for the
servers that don't need one.

**Refinement — `.env` changes *how* opt-in works, not *whether* it's opt-in.**
Cursor's `.cursor/mcp.json` supports an `envFile` field (stdio servers) plus
`${env:NAME}` interpolation, and Claude Code's `.mcp.json` supports `${VAR}` /
`${VAR:-default}` expansion (from the shell environment, not from a `.env`
file directly — the two clients differ here). Both mean the *config* — which
server, which env-var name it expects — can be committed with zero secret
material in it; only the value has to stay out of git. That is a genuinely
better mechanism than asking a student to paste a token straight into a JSON
file, and the opt-in example should use it: `agentic/ide-mcp/examples/github.json`
carries the server block referencing `${env:GITHUB_PERSONAL_ACCESS_TOKEN}` (or
Cursor's `envFile` pointing at `.env`), shipped alongside a committed
`.env.example` (variable name only, no value) with `.env` itself gitignored.
Opting in becomes: merge the block, copy `.env.example` → `.env`, drop in your
own token — never "paste your secret into a file the repo already tracks."

This does **not** move the `github` entry into the committed cohort default,
though. Even with the secret safely externalized, the *entry itself* sitting
in every student's `.cursor/mcp.json` means every student who hasn't done that
opt-in setup sees a disconnected/red server in their MCP panel from the moment
they open the folder — which fails the same "fresh clone just works, nothing
red by default" bar the student-simulation smoke test (deliverable 9) is built
to enforce. Presence, not just secrecy, is what makes a server cohort-default;
GitHub MCP fails that bar regardless of how well the credential is handled.

**SSH is not a substitute — it authenticates a different thing.** An SSH key
lets a student `git clone`/`push` over `git@github.com:...`; it authenticates
git's own transport protocol. `github-mcp-server` calls GitHub's REST/GraphQL
API, which is a different credential surface entirely — its own documentation
lists exactly three supported auth modes (OAuth browser login, Personal Access
Token via `GITHUB_PERSONAL_ACCESS_TOKEN`, GitHub App auth) and none of them is
an SSH key; it also does not read an existing `gh auth login` session/token
automatically. Every student already having SSH access configured for normal
git operations is good practice on its own merits, but it does not unlock or
simplify this MCP server's setup — the PAT/OAuth step is separate and
unavoidable if a student wants it.

**Rejected alternative — studio-hosted MCP gateway for students:** DevIAC's
own `mcp.crea-comm.loc` gateway is LAN-only by permanent architectural
constraint (`deviac/docs/DEV_PLAN/DEVIAC-STUDIO-READINESS/RATIONALE.md`:
"No WAN exposure, public SaaS, or automatic credential distribution"), so it
is unreachable to students off the studio's physical network (university,
home). This is not a timing gap that resolves once DevIAC's own React-catalogue
work (`DEVIAC-STUDIO-READINESS` DR3) ships — it is permanent. AG6's IDE MCP
choices must always be either vendor-hosted-public or run locally per student,
never dependent on the studio gateway.

## 6. Do students need `@modelcontextprotocol/server` / `client` / `node`?

| Need | Install? |
| --- | --- |
| Use Astro/Svelte **docs** MCP from the IDE | **No** — `npx -y …` is enough; no app `package.json` change |
| Author a **custom** MCP server as optional coursework | Yes — then add SDK deps in a **lab package**, not in the Oracle frontend by default |
| Run the **product** MCP | Already Python FastMCP under `services/mcp` — not the TS SDK |

Do **not** add `@modelcontextprotocol/*` to `services/frontend/package.json` just
to consume docs MCPs. That confuses application dependencies with IDE tooling.

## 7. `llms.txt` indexing

AG6 vendors (or pin-fetches) agent indexes under e.g.:

```text
agentic/ide-mcp/llms/
  README.md                 # how agents should use these files
  svelte-prompts-llms.txt   # from https://svelte.dev/docs/ai/prompts/llms.txt
  (optional) astro-*.txt    # if Astro publishes a stable llms index
```

Verification: script checks URL reachability **or** on-disk digest match; CI may
run the offline digest check only (no network flakiness in required gates).

## 8. Verification of existence (student / CI)

AG6 delivers `agentic/ide-mcp/scripts/verify-ide-mcp.sh` (or `.py`) that:

1. Asserts `.cursor/mcp.json` parses and lists required server keys.
2. Optionally dry-runs `npx -y @sveltejs/mcp --help` (or equivalent) when network
   allowed.
3. Optionally `curl -I` / MCP initialize against Astro HTTP endpoint when network
   allowed.
4. Prints a student-facing PASS/FAIL checklist for Week-0 setup.

Product Docker MCP health remains `make up` + existing MCP tests — separate check.

## 9. Student-simulation smoke test — "wired and ready," not just "config parses"

`verify-ide-mcp` (§8) is a config-shape and allowlist gate — it does not prove a server
actually speaks MCP, and it runs from the instructor's own already-tuned machine, which can
mask a bug a genuinely fresh student clone would hit. AG6 additionally delivers
`agentic/ide-mcp/scripts/simulate-student-check.sh`, which sends a real MCP `initialize`
JSON-RPC request to every committed stdio server and an HTTP `initialize` to Astro's endpoint,
asserting a well-formed response — not just that the process starts or `--help` exits 0. This
is a **live** check (network + `npx` fetch required), kept separate from the offline CI gate.

Alongside it, `agentic/ide-mcp/README.md` carries a short "confirm it like a new co-developer
would" walkthrough: open a throwaway `git worktree` of the branch under test (no pre-existing
global Cursor state assumed), confirm each server shows connected in Cursor's MCP panel, and
ask one real, checkable question per server (an exact quoted doc sentence, a live
accessibility-tree snapshot) — a fluent but unverifiable answer is a fail, since model memory
can fake a docs summary but only a real MCP round-trip returns something checkable. The AG6
phase report records what was actually asked and returned, not a checkbox from memory.
