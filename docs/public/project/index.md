---
title: Project
eyebrow: What TTOD is
description: Mission, governance, provenance, and licensing for 道 The Tao of Development (TTOD).
permalink: /project/
---

# Wisdom with a chain of custody

TTOD is a pedagogical knowledge base: short development aphorisms organized by subject and learning level, connected to what they teach and where they came from. The YAML collection is canonical; interfaces and exports are derived views.

The project is designed around a distinction that matters in education: a memorable statement can support teaching without becoming academic evidence. TTOD entries are cited by stable ID, carry language, origin, rights, and relationship metadata, and remain subject to human governance.

## Governance principles

- Canonical records change through validated transactions, not casual file edits.
- IDs are stable; superseded material is deprecated rather than erased.
- Human, studio, AI-proposed, and legacy origins remain distinguishable.
- AI-proposed material requires human validation before acceptance.
- Derived JSON and graph views never outrank the canonical source.
- Pedagogical aphorisms do not independently substantiate research claims.

<figure class="diagram-teaser">
  <a class="diagram-teaser-link" href="{{ '/assets/diagrams/ttod-wisdom-dataflow.html' | relative_url }}">
    <img src="{{ '/assets/diagrams/ttod-wisdom-dataflow.png' | relative_url }}" alt="Diagram of the governed write path: a citable work moves through agent distillation into a pending inbox, a human accept step, the canonical ttod.yml store, and a C14N export read by Web Atelier, DevIAC MCP, and fine-tuning." loading="lazy">
  </a>
  <figcaption><a href="{{ '/assets/diagrams/ttod-wisdom-dataflow.html' | relative_url }}">Open the interactive data-path diagram ↗</a> — the governed write path from a citable source to canonical acceptance, and the read-only exports every consumer shares.</figcaption>
</figure>

## What the platform adds

The application makes those governance choices observable through localized routes, individual quote views, related-content navigation, a graph island, a streaming Oracle island, documentation, and representative quality checks. The platform is currently a local teaching reference, not a public cloud service.

## Licensing

Code is licensed under MIT ([`LICENSE-CODE`](https://github.com/ruvebal/ttod/blob/main/LICENSE-CODE)):
copyright the steward and individual contributors listed in the repository README
(Development Team), except where a file states otherwise. Cohort code contributions use the
same MIT terms inbound and outbound; naming in the README is product authorship, not a research
personal-data corpus. Curated Tao knowledge content is licensed under CC BY-NC-SA 4.0
([`LICENSE-CONTENT`](https://github.com/ruvebal/ttod/blob/main/LICENSE-CONTENT)) unless a
record states otherwise. **These are not contradictory:** MIT covers software; CC BY-NC-SA
covers the wisdom corpus. A research or commercial partner must account for that
non-commercial, share-alike content boundary rather than infer unrestricted reuse of quotes.

## Stewardship

The project is stewarded through the research studio domain `@crea-comm.net`. Public documents deliberately omit workstation paths, internal infrastructure names, network coordinates, and private studio tooling.

## Where TTOD sits in the studio

TTOD is one project inside a small sovereign-AI development studio built on one non-negotiable
rule: every model call runs on locally-hosted infrastructure, never a cloud AI provider. TTOD's
own Oracle and any proposal-drafting assistance follow that rule the same way every other studio
project does.

Two sibling projects are worth naming so the boundary is explicit, not just asserted: **Athanor**,
the studio's own knowledge platform, may consume a read-only snapshot of TTOD's governed
collection and may surface candidate quotes back into TTOD's normal human-review inbox — it never
writes a canonical record directly, the same rule that governs every other path into TTOD's data.
**Ahmes**, the studio's general-purpose document-extraction engine, is unrelated to TTOD's own
pipeline; it feeds Athanor from other source material and has no direct connection to TTOD's
quote governance. Naming both here is about precision, not affiliation-by-proximity: TTOD's
governance rules apply regardless of which other studio tool is asking.
