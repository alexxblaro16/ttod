---
name: lao-tzu-tao-compose
purpose: Inference harness that composes Tao of Development aphorisms from the Lao Tzu bibliography; propose-only.
surfaces: [skills, rules, queries, prompts]
landings: []
mirrors: []
locks: []
external_readers: [A sibling repo skill (provenance-layer profiles) names queries/ as an output directory]
status: local-untracked
---

# Lao Tzu → Tao of Development Compose Pack

Inference harness for composing TTOD aphorisms grounded in the Lao Tzu
bibliography (`scholar-lao-tzu`), without treating DevIAC vector snippets as
citation authority.

| Surface | Purpose |
| --- | --- |
| `skills/tao-compose/SKILL.md` | compose workflow: discover → distill → propose |
| `rules/tao-compose.md` | hard gates (propose-only; cite by ID; no invented SAFE) |
| `queries/` | frozen discovery harvests (vectors · Athanor · graph) |
| `prompts/compose-system.md` | generative system prompt for local Ollama |

**Corpus:** Ahmes vaults under `~/ahmes-library/scholar/documents/` from
`~/projects/.../bibliographies/lao_tzu`. **Project slug:** `scholar-lao-tzu`.

**Authority ladder (non-negotiable):**

1. DevIAC vectors / graph — discovery only (`authority_level: derived`)
2. Athanor search — canonical pointers (`node_id`, coat)
3. `ahmes query --cite "$DB:$NODE"` — only cite-grade evidence
4. TTOD merge — human `proposal accept` only; never hand-edit `ttod.yml`
