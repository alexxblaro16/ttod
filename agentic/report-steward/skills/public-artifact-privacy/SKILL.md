---
name: public-artifact-privacy
description: Audit exact public, partner, student, or research-facing artifact candidates for leaked local paths, private network coordinates, internal hostnames, private machinery names, non-studio email identities, internal roadmap language, and htmlproofer-breaking empty anchors. Use before publishing, distributing, synchronizing, or claiming an artifact is sanitized — especially when shipping Archify HTML under docs/public/assets/diagrams.
---

# Public Artifact Privacy

Audit the exact artifact to be released, not merely its source branch or a nearby working tree.

## Workflow

1. Resolve the candidate's file list, generated output, archive contents, and reachable Git objects
   where relevant. A safe build source does not prove its rendered or packaged artifact is safe.
2. Run `../../scripts/check_public_privacy.py` over those files. For repository-wide checks, omit
   paths so the watcher reads `git ls-files`. For public docs:
   `python3 agentic/report-steward/scripts/check_public_privacy.py docs/public _site-public`
   (when `_site-public` exists after `jekyll build`).
3. Supply private machinery terms through `TTOD_PRIVATE_TERMS_FILE`, pointing to a local untracked
   newline-delimited denylist. Never commit that denylist or repeat its values in a report.
4. Manually review findings. Replace local paths with repository-relative paths, private coordinates
   with role labels, personal identities with the approved `@crea-comm.net` studio domain, and
   internal phase identifiers with reader-facing capability or maturity language.
5. Rebuild or re-export, then rerun against the exact rendered or packaged candidate. Zero findings
   are required in source and output.
6. For Pages candidates, also run htmlproofer as CI does:
   `cd docs/public && bundle exec htmlproofer ../../_site-public --disable-external --allow-hash-href --swap-urls '^/ttod/:/'`

The tracked watcher covers common local home, mount, temporary and tilde paths; private IPv4 and
IPv6; internal hostname suffixes; disallowed email domains; public-surface phase shorthand; and
(on public `.html`/`.md`/`.astro`/`.svelte`) `<a>` tags missing `href` (the htmlproofer Links
failure). Bare machine or project names still depend on the untracked denylist. The watcher is a
deterministic gate, not proof that all sensitive information has been found. Pair it with secret
scanning, history inspection, rights review, and human cold reading appropriate to the release
risk. Do not suppress a real finding through broad exclusions.

Within `docs/public` and rendered `_site-public` output, the watcher also rejects internal
development phase names and shorthand. Public readers should see what exists, what remains open,
and why it matters—not the private indexing system used to orchestrate implementation.

## Defect catalog — do not reintroduce (2026-09-08 CI)

| Failure | Bad pattern | Public-safe fix |
| --- | --- | --- |
| Phase ID in Archify card / evidence | `R6`, `Q4 transport`, `Phase Q` | Entrega 1 / Unit 4 / “bridge transport” / maturity language |
| Internal hostname | `host.docker.internal`, `*.crea-comm.loc` | “Docker host gateway”, “Compose network”, “local Ollama” |
| Studio host in ethics/OTRI pack | Lilith, Tanit, LAN IP in budget/hosting prose | “hosting institucional UDIT”, “VPS”, service names only |
| Empty citation anchor | `<a id="ref-…"></a>` | `<span id="ref-…"></span>` |
| Archify passport shell | `<a id="focus-repository" …></a>` with no `href` | Same attrs plus `href="https://github.com/ruvebal/ttod"` |

## Archify → `docs/public/assets/diagrams/` checklist

1. Author Archify JSON under `docs/architecture/archify/` with **public-safe** labels (no phase IDs,
   no `*.internal` hostnames) even for internal copies — public delivery copies this text into HTML.
2. `deliver` the HTML; then copy/sync into `docs/public/assets/diagrams/` only after step 3–4.
3. Ensure `#focus-repository` has an `href` (patch after deliver if the renderer omits it).
4. Run the privacy watcher on `docs/public/assets/diagrams/` and the full `docs/public` tree.
5. Build `_site-public` and run htmlproofer with the CI flags above.
6. Keep PNG teasers in sync after label changes; privacy does not OCR images, but students see them.
