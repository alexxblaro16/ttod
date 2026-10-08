<!--
PHASE-X — Public docs: two guides on connecting IDE agents to MCP servers,
sourced from Phase W's real, merged AG6 work. Planning pack only — no branch,
no publish. Author: Claude (orchestrator, at product-owner request) · 2026-09-19
-->

# Phase X — Public Docs: Agentic IDE/MCP Guides (dev + research editions)

**Status:** PROPOSED · planning only. No branch, no file published.
**Depends on:** Phase W AG0–AG6, merged to `main` (PR #21, #22) — the only source of technical
claims either guide is allowed to make.
**Programme letter:** X (Q, R, S, T, U, V, W already taken).

## 0. Mission

Two public pages, not one — different readers need different depth and register, and forcing
one document to serve both dilutes it for both:

1. **Developer/collaborator guide** — "how do I connect my IDE to TTOD's MCP servers, and how
   do I know it's actually working." Practical, step-by-step, same register as
   [`guides/contributing.md`](../public/guides/contributing.md) and
   [`guides/reviewing-cohort-prs.md`](../public/guides/reviewing-cohort-prs.md).
2. **Research/pedagogy guide** — why this cascade governs agentic development the way it does
   (real verification over declared verification, evidence that outlives the chat turn, a named
   human at every merge), and what that has to do with teaching. Same register as
   [`research/methodology.md`](../public/research/methodology.md): hedged, citation-backed,
   never overclaiming validated pedagogy from a single cascade's own evidence.

## 1. Sources — locked, not invented

| Claim type | Source | Constraint |
| --- | --- | --- |
| Technical (what AG6 built, how it verifies) | [`PHASE-W-AGENTIC-HOMOGENIZATION/INDEX.md`](PHASE-W-AGENTIC-HOMOGENIZATION/INDEX.md), `PHASE-AG6-REPORT.md`, `PHASE-AG6-COLD-REVIEW.md`, `agentic/ide-mcp/README.md` | Every command/claim must be checkable against the actual merged code on `main` — no aspirational or planned-but-unbuilt feature described as shipped |
| Governance parallel | `~/src/athanor/docs/DEV_PLAN/ATHANOR-PROVENANCE-LAW.md`, Law L8: *"Plans, decisions, commands, exit codes, raw test/evaluation artifacts, hashes, and review verdicts are repository-local or stored under an indexed artifact path. Chat history is not the system of record. A phase is not DONE until another agent can reproduce its acceptance decision from files."* | Cited as a **parallel governance philosophy**, not as "Athanor's rationale for teaching agentic dev" — no such document exists there, confirmed by direct search, and none is fabricated here |
| TTOD quotes (cite by ID only, per `AGENTS.md`'s own rule) | `arch-049` (*"Ahmes extracts. Arkadia curates. DevIAC serves. A student who understands this triangle understands that knowledge flows — it is never static, never finished, never owned by one system alone."*), `arch-050` (*"Each PHASE-n.md is a self-contained prompt with all context embedded. A local 72B model following it will produce nearly identical output to a cloud model, because the prompt does the heavy lifting. The intelligence is in the specification, not the parameter count."*), `arch-058` (*"the enricher writes ten thousand mentions — yet relations: zero"*) | All three verified directly in `ttod.yml`: `rights.access: public`, `license: CC-BY-NC-SA-4.0`, not deprecated. `arch-058` is `related: [arch-049, arch-055]` — a real thematic cluster, not three quotes forced together |
| Academic citations (research guide only) | Queried directly from the **studio knowledge engine** — not a generic web search. Deviac runs a pgvector store (`deviac-postgres`) with a `knowledge` collection (166,916 chunks, real ingested academic papers under `~/ahmes-library/scholar/documents/`), exposed over HTTP by the `tanit-mcp-gateway` container at `http://localhost:8100/vectors/search` (bypasses the broken Cursor-configured stdio MCP venv entirely — confirmed live, see § 1a). Two strong, independently verified candidates found this way: **Kazemitabaar, M., & Henley, A. Z. (2024). "CodeAid: Evaluating a Classroom Deployment of an LLM-based Programming Assistant that Balances Student and Educator Needs." CHI 2024** (700-student, 12-week real classroom deployment); **Errico Vanta, H., & Ngiam, J. (2025). "Securing the Model Context Protocol (MCP): Risks, Controls, and Governance." arXiv:2511.20920** (MCP-specific security governance literature — directly backs AG6's own official-servers-allowlist design, found independently of it) | Every candidate confirmed by reading its actual extracted source text (`~/ahmes-library/.../extract/index.md`), not just the retrieved chunk — title, authors, venue, year cross-checked before citing, same as any other literature check. `authority_level: derived` chunks in this corpus are leads, not pre-verified citations, until read at source. |

### 1a. How the studio knowledge-engine query actually works (verified live, 2026-09-19)

```bash
curl -s -X POST http://localhost:8100/vectors/search \
  -H "Content-Type: application/json" \
  -d '{"query":"<search terms>","n_results":5,"collection":"knowledge"}'
```

No MCP client, no fixed venv needed — the same server code the broken Cursor MCP entries
(`deviac-vectors`, `deviac-knowledge`) were configured to run is already running inside the
`tanit-mcp-gateway` Docker container and exposed over plain HTTP. This is a studio-infra fact
worth fixing separately (the Cursor-side venv path is stale), tracked as a follow-up, not part
of this cascade's own scope.

**What this cascade does not do:** authorize a research study (that gate is `methodology.md`'s,
untouched here), claim Athanor has a stated teaching rationale it doesn't, translate to Spanish
in this pass (`alt_lang_missing: true`, same accepted pattern as `reviewing-cohort-prs.md` —
ES is a real follow-on, not blocking), or restyle the site beyond the two new pages + one
diagram + nav entries.

## 2. Steps

| Step | What | Who drafts | Output |
| --- | --- | --- | --- |
| X0 | Freeze scope + citations (this document) | Orchestrator | This file |
| X1 | Developer guide draft | **Local Ollama `qwen2.5-coder:32b`**, first pass — fed Phase W's INDEX/AG6 report, `agentic/ide-mcp/README.md`, and `contributing.md` as a style exemplar; orchestrator fact-checks every command against the actual merged code and rewrites as needed before it ships | `docs/public/guides/connect-ide-mcp.md` |
| X2 | Research guide draft | Orchestrator, directly — citation accuracy and hedged academic register need tighter control than a first-pass coder model reliably gives; academic grounding already found via the studio knowledge engine (§ 1a), each candidate read at source before citing | `docs/public/research/agentic-development.md` |
| X3 | One diagram — the three-layer MCP model (IDE MCP / product MCP / studio ingest), reusing `AGENTS.md`'s own discovery-map tree, styled to match the site's existing diagram-teaser pattern | Orchestrator (inline SVG or Archify, whichever is cleaner in practice) | Asset under `docs/public/assets/diagrams/`, embedded in the dev guide |
| X4 | Wire up: `navigation.yml` (EN) entries under Docs + Research; run `check_public_privacy.py`; `jekyll build`; `htmlproofer` | Orchestrator | Clean build, zero privacy findings |
| X5 | Cold review (fresh subagent, zero prior context) + PR on branch `docs/agentic-dev-mcp-guides` + stop before merge | `cascade-cold-reviewer` + orchestrator | PR, awaiting product-owner merge decision |

Same closing discipline as Phase W: VERIFYING → cold review → report, never self-certified
DONE, merge stays a named-human act.

## 3. Branch plan

| Item | Value |
| --- | --- |
| Branch | `docs/agentic-dev-mcp-guides`, cut from `main` at the commit this plan is authorized |
| Push | Only when the human asks |
| PR title (proposed) | `docs: agentic dev/MCP guides for collaborators and research partners` |
| Merge authority | Named human, after X5's cold review |

## 4. Honesty checkpoints (carried from this cascade's own discipline, not decorative)

- Every command shown in the developer guide must be one that actually works against the
  merged `main` tree — re-run, not assumed, before publishing (same bar `PHASE-AG6-REPORT.md`
  held itself to).
- The research guide inherits `methodology.md`'s own hedges verbatim in spirit: Phase W's seven
  cold reviews are evidence of *a governed process working as designed*, not proof of a
  pedagogical outcome — the difference `methodology.md` already draws between "artifact audit"
  and "educational research finding."
- No quote gets bent to fit a narrative it doesn't support — `arch-049`/`050`/`058` were chosen
  because they were already, unforced, about exactly this (knowledge flow between systems,
  local-model delegation, and the gap between "looks connected" and "actually wired").

## 5. Awaiting authorization

This plan is ready to execute. Say the word (and whether X1's local-Ollama draft should be
literal — I'll actually spawn `qwen2.5-coder:32b` as a subprocess for that step, not simulate
it) and I'll open the branch and start X1.
