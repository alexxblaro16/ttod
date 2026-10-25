---
title: Product areas
eyebrow: The implemented reference
description: The visible areas and front-end boundaries in the TTOD instructor reference.
permalink: /platform/
---

# One product, several teachable boundaries

The instructor reference runs end to end on a local machine. Its areas are not separate demonstrations: they share localization, content contracts, API boundaries, accessible browser states, and the same governed quote source.

| Area | User-visible purpose | Front-end idea made observable |
| --- | --- | --- |
| Welcome | enter in English or Spanish | localized routing and document language |
| Quote | inspect one governed entry | typed data, provenance, rights, and semantic presentation |
| Wisdom | browse the collection | information architecture, filters, and empty states |
| Documentation | learn the system in context | content collections and editorial navigation |
| Graph | explore related entries | a hydrated Svelte island with accessible textual state |
| Oracle | ask and receive a streamed response | a React island, streaming state, grounding, and recovery |
| Local operations | start and observe the stack | the browser/service boundary, not a DevOps syllabus |
| Account & library | log in, save quotes, propose new ones | server-verified sessions, a bearer-token API, and the reviewed path a proposal takes into the governed collection |
| Tests | locate evidence at useful layers | unit, component, contract, route, and accessibility reasoning |

## Architecture at teaching scale

```text
localized route
  → Astro document and content contract
  → bounded Svelte or React island
  → HTTP or streamed request
  → application and retrieval contracts
  → governed quote snapshot
  → accessible browser state
  → test at the cheapest useful layer
```

Astro owns the document and content-oriented routes. Interactive islands are used where local state or streaming warrants them. The backend is explained only far enough to trace the request and trust boundary; the teaching emphasis remains front-end architecture.

The personal library is deliberately outside the governed corpus: Redis stores a per-user hash of
`quoteId → savedAt`, while the backend re-validates each reference against the active public
snapshot before returning it. This keeps user preference data mutable without allowing it to
change `ttod.yml`.

<figure class="diagram-teaser">
  <a class="diagram-teaser-link" href="{{ '/assets/diagrams/ttod-system-overview.html' | relative_url }}">
    <img src="{{ '/assets/diagrams/ttod-system-overview.png' | relative_url }}" alt="System diagram showing IDE agents and ttod-bridge staging proposals, a human reviewer accepting into the canonical ttod.yml store, the read-only Astro, Oracle API, and MCP runtime inside the Docker Compose network, and Ollama shown twice: the app's own container (the make up default) and a personal Ollama borrowed manually from the host." loading="lazy">
  </a>
  <figcaption><a href="{{ '/assets/diagrams/ttod-system-overview.html' | relative_url }}">Open the interactive system-overview diagram ↗</a> — the same path above, as a full component map with trust boundaries and guided views.</figcaption>
</figure>

## Honest maturity

The rich reference demonstrates localized content, graph exploration, and a streamed Oracle. Browser operations, offline behavior, and the testing surface are not yet a complete student-ready implementation. A future teaching baseline will keep every major area present at hello-world depth; that reduction is planned, not complete.

In the [FE II course](https://ruvebal.github.io/web-atelier-udit/tracks/feii/), that baseline is **Entrega 1** and the product defended in the Units 1–7 mid-term. See the [teaching model]({{ '/teaching/' | relative_url }}).
