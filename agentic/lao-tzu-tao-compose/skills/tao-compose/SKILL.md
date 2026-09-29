---
name: tao-compose
description: >-
  Compose TTOD aphorisms guided by the Lao Tzu bibliography (scholar-lao-tzu)
  via vectors → Athanor → Ahmes cite → ttod-bridge propose. Use when drafting
  Tao of Development quotes that need Daoist structural voice without claiming
  Lao Tzu as independent scholarly evidence for studio claims.
---

# Tao compose (Lao Tzu harness)

**Pack root:** `~/src/ttod/agentic/lao-tzu-tao-compose/`
**Project slug:** `scholar-lao-tzu` · **library:** `scholar`

## Preflight

```bash
curl -sf http://localhost:11434/api/tags >/dev/null
curl -sf http://localhost:8100/health >/dev/null
test -f ~/projects/ruvebal/scholar/bibliographies/lao_tzu/.ahmes/pipeline/INJECT_DONE
```

## Workflow

1. **Discover (DERIVED)** — query vectors scoped to `scholar-lao-tzu`:

```bash
curl -s -X POST http://localhost:8100/vectors/search \
  -H "Content-Type: application/json" \
  -d '{"query":"<theme>","project_slug":"scholar-lao-tzu","knowledge_scope":"field_prospection","n_results":5}'
```

2. **Point (canonical)** — Athanor:

```bash
cd ~/src/athanor && source .venv/bin/activate && set -a && source .env && set +a
athanor search "<theme>" --project-slug scholar-lao-tzu --library scholar
```

3. **Ground (optional, for teaching notes)** — Ahmes cite only if needed for
   Surface A; TTOD quotes themselves are pedagogical, not evidence.

```bash
ahmes query --cite "$DB:<node_id>" --style chicago-author-date
```

4. **Draft** — feed `prompts/compose-system.md` + theme + 2–3 discovery
   snippets (labeled DERIVED) to local Ollama. Prefer short aphoristic form.

5. **Propose** — ttod-bridge only:

```bash
# via adapter.propose_quote(...); origin=blackbox; human accepts later
```

6. **Never** merge into `ttod.yml` from this skill.

## Voice lenses (from corpus themes)

| Lens | Compose toward |
| --- | --- |
| Naming / emptiness | Names that constrain systems; leave room for change |
| Wu wei | Non-forcing architecture; remove friction before adding power |
| Softness | Interfaces that yield without breaking contracts |
| Way vs spoken way | Spec vs runtime; the map is not the deployment |

Reuse frozen harvests under `queries/` when re-running the same themes.
