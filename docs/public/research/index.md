---
title: Research
eyebrow: Evidence before effect claims
description: TTOD's research questions, current maturity, safeguards, and evidence boundaries.
permalink: /research/
---

# A research programme with two strands

TTOD currently supports a technical and pedagogical design enquiry: how can a complete but deliberately shallow front-end system make architectural boundaries, process evidence, and student design responsibility easier to examine in an AI-assisted learning environment?

**Strand B (pedagogical)** asks whether participation as a developer in that real, agentic-assisted product — inside a cohort — can be a learning activity with pedagogical outcomes (*learning by doing*). Department pedagogical framing and participant information/consent templates are in place; **ethics-committee review is in progress**. Student work becomes research data only under that protocol, with pseudonymization and clear separation from grading.

**Strand A (philosophical)** — relating classical ontological, gnoseological, epistemological, and transcendental traditions to cybernetics and technical practice — is **parked** and does not use student participants or coursework as evidence.

No claim is made that TTOD improves learning. Coursework alone does not authorize research use.

## Four artifacts that must not be confused

1. **Rich instructor reference:** feasibility evidence that the architecture can run end to end.
2. **Teaching baseline:** a future hello-world product used for explanation and tracing.
3. **Student products:** independently expanded, assessed work demonstrating learner decisions.
4. **Research records:** only material collected under a separately approved and communicated protocol.

## Candidate questions (Strand B)

- Can developer participation in a real agentic-assisted cohort product function as learning by doing with observable pedagogical outcomes?
- Which traces help a learner correctly locate rendering, state, trust, data, and test ownership?
- How much starter implementation supports system understanding without collapsing authentic design work?
- Which process artifacts make AI-assisted contributions explainable and reviewable?
- How can oral explanation, repository evidence, accessibility checks, and product behavior complement one another in assessment?

## What existing literature can and cannot do

Research on AI-assisted programming, authentic assessment, process documentation, and explanation motivates the design. [Liu, Fan, and Pan 2026](#ref-liu-fan-pan-2026) describe a tension between domain mastery and tool mastery and distinguish scaffolding from cognitive offloading; their grounded-theory study does not adjudicate efficacy or predict outcomes in this course. [Nikolić and Basta Nikolić 2026](#ref-nikolic-basta-nikolic-2026) propose process documentation, oral defense, authentic tasks, and transparent AI-use policies, while explicitly reporting no validation data.

Complementary STEM and computing-education work sharpens the same boundary without proving a TTOD effect. [Shihab et al. 2025](#ref-shihab-et-al-2025) study how Copilot changes effectiveness, efficiency, and process in brownfield programming tasks—useful for questions about integrating suggestions into an existing codebase, not as a transfer claim for this scaffold. [López-Pernas et al. 2025](#ref-lopez-pernas-et-al-2025) examine self-regulation in student–AI interactions during web-programming problem solving, which motivates attention to dependence, delegation, and regulation over time. [Garcia 2025](#ref-garcia-2025) reports on self-coded digital portfolios as authentic project-based assessment in a web design and development course, supporting product-plus-process assessment designs. [Davalos and Zhang 2026](#ref-davalos-zhang-2026) reframe “AI misuse” as a learning-visibility and measurement problem when educators retain products but lose process insight—an analogy for why TTOD treats traces and oral defence as design requirements rather than detection theatre.

Curriculum guidance in [*Computer Science Curricula 2023*](#ref-cs2023) treats generative AI, society, ethics, and professional responsibility as curriculum-wide concerns rather than a detached tool lesson; that is a standards-facing warrant for scope, not classroom evidence.

These sources justify questions and safeguards, not a TTOD effect. More longitudinal classroom evidence is needed, and local implementation observations are engineering evidence rather than educational outcomes. Classic instructional-design primaries on cognitive load and cognitive apprenticeship remain on the evidence-needed list until their bibliographic metadata can be verified for public citation.

## Critical perspective

The central risk is confusing a polished product with learning. Faster completion can coexist with weaker explanation, debugging, or independent problem decomposition. TTOD therefore treats generated code as an object for critique: learners must locate its assumptions, test it, modify it, and explain responsibility for the result. The intended contrast is not “AI or no AI,” but support that is deliberately faded versus dependency that remains invisible.

That critical lens also applies to the platform itself. A governed corpus can still encode omissions; a graph can make editorial relations appear natural; an Oracle can project authority; process logs can be staged; and an oral defense can create workload or equity costs. Research must examine those power and validity questions rather than using traceability as a synonym for truth.

Read the [method and safeguards]({{ '/research/methodology/' | relative_url }}) or the [teaching model]({{ '/teaching/' | relative_url }}).

## Current status

| Layer | Status | Next gate |
| --- | --- | --- |
| Engineering feasibility | locally observed; independent verification open | close the evidence report |
| Teaching skeleton | in cohort use / Phase U–V | keep subtraction and assignment contracts frozen |
| Curriculum alignment | ongoing | bilingual semantic-parity review |
| Strand A (philosophical) | parked | reopen only with its own design doc |
| Strand B (pedagogical case) | protocol drafted; consent templates in repo; **ethics review in progress** | committee decision; then consented pseudonymized analysis after grades |

Internal design and ethics package (not all published on this site): `docs/research/INDEX.md` and `docs/research/ethics/` in the project repository.

<figure class="diagram-teaser">
  <a class="diagram-teaser-link" href="{{ '/assets/diagrams/ttod-research-maturity.html' | relative_url }}">
    <img src="{{ '/assets/diagrams/ttod-research-maturity.png' | relative_url }}" alt="Lifecycle diagram of the research pathway: design enquiry, protocol drafting, and an ethics and data review gate, with the current position parked before that gate, leading to authorized collection and analysis that converges on validated findings or diverges to equally valid negative or mixed findings." loading="lazy">
  </a>
  <figcaption><a href="{{ '/assets/diagrams/ttod-research-maturity.html' | relative_url }}">Open the interactive maturity diagram ↗</a> — where empirical research sits today, the gate it must clear next, and why negative or mixed findings count as valid outcomes, not failures.</figcaption>
</figure>

## References

- <span id="ref-cs2023"></span>*Computer Science Curricula 2023*. Association for Computing Machinery, IEEE Computer Society, and AAAI. [https://doi.org/10.1145/3664191](https://doi.org/10.1145/3664191).
- <span id="ref-davalos-zhang-2026"></span>Davalos, Eduardo, and Yike Zhang. 2026. “AI Misuse in Education Is a Measurement Problem: Toward a Learning Visibility Framework.” arXiv. [https://doi.org/10.48550/arxiv.2603.07834](https://doi.org/10.48550/arxiv.2603.07834).
- <span id="ref-garcia-2025"></span>Garcia, Manuel B. 2025. “Self-Coded Digital Portfolios as an Authentic Project-Based Learning Assessment in Computing Education: Evidence from a Web Design and Development Course.” *Education Sciences* 15 (9): 1150. [https://doi.org/10.3390/educsci15091150](https://doi.org/10.3390/educsci15091150).
- <span id="ref-liu-fan-pan-2026"></span>Liu, Dandan, Guangrui Fan, and Lihu Pan. 2026. “Tool, Tutor, or Crutch?: A Grounded Theory of Cognitive Scaffolding and Offloading in AI-Assisted Programming Education.” *International Journal of STEM Education* 13: 10. [https://doi.org/10.1186/s40594-025-00592-w](https://doi.org/10.1186/s40594-025-00592-w).
- <span id="ref-lopez-pernas-et-al-2025"></span>López-Pernas, Sonsoles, Kamila Misiejuk, Eduardo Oliveira, and Mohammed Saqr. 2025. “The Dynamics of the Self-Regulation Process in Student-AI Interactions: The Case of Problem-Solving in Programming Education.” In *Proceedings of the 25th Koli Calling International Conference on Computing Education Research*. [https://doi.org/10.1145/3769994.3770043](https://doi.org/10.1145/3769994.3770043).
- <span id="ref-nikolic-basta-nikolic-2026"></span>Nikolić, Dragan, and Marijana Basta Nikolić. 2026. “Designing AI-Resilient Assessment in Higher Education: A Four-Pillar Conceptual Framework.” *Frontiers in Artificial Intelligence* 9. [https://doi.org/10.3389/frai.2026.1841682](https://doi.org/10.3389/frai.2026.1841682).
- <span id="ref-shihab-et-al-2025"></span>Shihab, Md Istiak Hossain, Christopher Hundhausen, Ahsun Tariq, Summit Haque, Yunhan Qiao, and Brian Wise Mulanda. 2025. “The Effects of GitHub Copilot on Computing Students’ Programming Effectiveness, Efficiency, and Processes in Brownfield Coding Tasks.” In *Proceedings of the 2025 ACM Conference on International Computing Education Research V.1*. [https://doi.org/10.1145/3702652.3744219](https://doi.org/10.1145/3702652.3744219).
