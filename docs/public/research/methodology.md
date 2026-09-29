---
title: Method and safeguards
eyebrow: Research design boundary
description: A cautious methodology outline for a possible future TTOD educational study.
permalink: /research/methodology/
---

# Method before data

Strand B prepares and submits an educational case-study protocol: explicit questions, participant information, ethics and data-protection review, defined access and retention, and a clear separation between teaching, assessment, and voluntary research participation. Templates and the committee dossier live in the repository under `docs/research/ethics/`. **Analysis of student artifacts as research data does not begin** until the competent ethics body authorizes the protocol and valid consent is on file. Strand A (philosophical) remains parked and has no human subjects.

Teaching may proceed without treating coursework as research evidence.

## Methodological stance

The engineering work follows a design-enquiry logic: articulate a pedagogical problem, build a traceable intervention, expose its assumptions, and preserve evidence of iteration. That supports disciplined design decisions but does not convert product development into educational research.

A future study could use a bounded case-study design to examine the artifact in context. If the focus is how students negotiate AI support, a constructivist grounded-theory approach with constant comparison may be appropriate; [Liu, Fan, and Pan 2026](#ref-liu-fan-pan-2026) provide a recent programming-education example, not a protocol to copy unchanged. The researcher must state positionality, sampling, coding, negative-case treatment, and the boundary between inductive findings and prior sensitizing concepts.

Self-regulation under AI assistance is itself an empirical object. [López-Pernas et al. 2025](#ref-lopez-pernas-et-al-2025) coded thousands of undergraduate ChatGPT interactions in a web programming course to study collaboration, dependence, and delegation over time—evidence that process logs and interaction coding can be research instruments when authorized, not that TTOD’s logs already are.

## Possible empirical design

A bounded educational case could combine technical artifact audit with qualitative analysis of versioned decision records and a short oral explanation. Questions, inclusion criteria, codebook, and analysis plan should be registered or versioned before analysis. Any comparison should focus on observable reasoning and traceability unless the design supports stronger inference.

Potential artifacts include a student repository, decision notes, declared AI use, automated checks, and a defense of selected changes. Triangulation can compare what the product does, what the record says, and what the learner can explain; disagreement between those sources is evidence to analyze, not noise to erase. None should be collected for research without the required authorization and communication.

Assessment-facing designs in computing education already treat student-built web products as authentic evidence. [Garcia 2025](#ref-garcia-2025) studies self-coded digital portfolios in a web design and development course under a project-based frame, which motivates keeping technical ownership and reflection together—without claiming the same outcomes for TTOD. Brownfield process studies such as [Shihab et al. 2025](#ref-shihab-et-al-2025) motivate questions about how learners accept, reject, and debug AI suggestions inside an inherited codebase—the situation the teaching spine creates by design.

## Safeguards

- Course access and grading must not depend on research participation.
- Pedagogical participation in the cohort project and research consent for secondary use are distinct (see consent forms A vs B).
- The teaching repository and any research dataset must have different identities and access rules.
- Data minimization, retention, pseudonymization, withdrawal, and reviewer access must be settled in advance — special-category personal data are not collected; the research corpus, if authorized, holds pseudonymized process traces only.
- The rich instructor reference must be isolated from the student artifact by evidence, not assertion.
- Results must distinguish feasibility, teaching observation, assessment evidence, and research evidence.
- Negative, mixed, or inconclusive findings remain valid outcomes.
- Strand A philosophical claims must not be imported as empirical warrants for Strand B.

## Evidence anchors

The following sources motivate, but do not validate, the proposed design. In-text author–date forms link to the Chicago list below.

### Methods backbone (reporting, small-n, process-data ethics)

- [Runeson and Höst 2009](#ref-runeson-host-2009) on conducting and reporting software-engineering case studies (process + checklists).
- [Runeson, Höst, Rainer, and Regnell 2012](#ref-runeson-et-al-2012) — the extended Wiley handbook (*Case Study Research in Software Engineering*).
- [Wohlin et al. 2012](#ref-wohlin-et-al-2012) on empirical software-engineering strategies (survey, experiment, case study); used here to keep Strand B clearly **non-experimental**.
- [Heckman et al. 2022](#ref-heckman-et-al-2022) on empiricism and reporting norms in CER.
- [Brown and Guzdial 2024](#ref-brown-guzdial-2024) on rich versus big data — small-n insight without population inference.
- [McGill et al. 2023](#ref-mcgill-et-al-2023) on sound CER: transferability, consent reporting, null findings.
- [Fischer et al. 2024](#ref-fischer-et-al-2024) on consent architectures for programming-process data.

### Domain and phenomenon

- [Shihab et al. 2025](#ref-shihab-et-al-2025) on Copilot effects and processes in brownfield coding tasks.
- [Nikolić and Basta Nikolić 2026](#ref-nikolic-basta-nikolic-2026) on a four-pillar AI-resilient assessment framework (conceptual; no validation data reported).
- [Liu, Fan, and Pan 2026](#ref-liu-fan-pan-2026) on scaffolding versus cognitive offloading in AI-assisted programming education.
- [López-Pernas et al. 2025](#ref-lopez-pernas-et-al-2025) on self-regulation dynamics in student–AI programming problem solving.
- [Garcia 2025](#ref-garcia-2025) on self-coded portfolios as authentic assessment in web design and development.
- [Davalos and Zhang 2026](#ref-davalos-zhang-2026) on learning visibility when AI enters the assessment loop.
- [Prather et al. 2024](#ref-prather-et-al-2024) on benefits and harms of generative AI for novice programmers (performance versus learning).
- [*Computer Science Curricula 2023*](#ref-cs2023) on curriculum-wide generative AI, ethics, and professional responsibility.

These sources support studying process and assessment design. They do not establish effectiveness for this platform, course, or cohort. The AI-resilient assessment framework is explicitly conceptual; its indicators and instruments require empirical validation. The qualitative programming study is theory-building and context-bound. Those limits are carried into TTOD’s claim language. Method inheritance from the studio’s STEM-code Profield digests is documented internally under `docs/research/PROFIELD-STEM-CODE-INHERITANCE.md` (discovery map, not a substitute for the DOI list above).

## Analysis and quality controls

- Version the research questions, artifact definitions, interview or defense prompts, and analysis plan before examining outcomes.
- Keep engineering telemetry, assessed coursework, and consented research records as distinct datasets with distinct access rules.
- Use at least two evidence forms for claims about reasoning; do not infer understanding from repository activity alone. [Davalos and Zhang 2026](#ref-davalos-zhang-2026) argue that retaining final outputs while losing process visibility is a measurement failure mode—not a detection problem alone.
- Record disconfirming cases, coding changes, researcher memos, and unresolved interpretations.
- Report the learning setting, AI policy, tool access, prior experience, language context, and starter-code depth so readers can judge transferability.
- Treat accessibility, workload, and differential participation as research questions and possible harms—not merely implementation details.

<figure class="diagram-teaser">
  <a class="diagram-teaser-link" href="{{ '/assets/diagrams/ttod-research-safeguards.html' | relative_url }}">
    <img src="{{ '/assets/diagrams/ttod-research-safeguards.png' | relative_url }}" alt="Data-flow diagram showing candidate evidence — logs, grades, and defence — gated by consent and ethics/data review, authorized into distinct teaching and research datasets, and triangulated into either validated findings or equally valid negative/mixed findings." loading="lazy">
  </a>
  <figcaption><a href="{{ '/assets/diagrams/ttod-research-safeguards.html' | relative_url }}">Open the interactive safeguards diagram ↗</a> — how evidence would be gated, kept in distinct-access datasets, and triangulated once authorized.</figcaption>
</figure>

## Evidence still needed

The research preparation must deepen its evidence on worked-example fading, system tracing, cognitive load, studio learning, front-end conceptual transfer, student–AI self-regulation beyond single-course cases, and the dual teacher–researcher role. Primary classics on cognitive load while learning software and on cognitive apprenticeship are present incompletely or without verified bibliographic metadata for public citation; claim language therefore keeps them as open evidence needs rather than cited warrants. Current legal or institutional requirements must be verified against authoritative sources when a protocol is drafted.

## References

- <span id="ref-brown-guzdial-2024"></span>Brown, Neil C. C., and Mark Guzdial. 2024. “Confidence vs Insight: Big and Rich Data in Computing Education Research.” In *Proceedings of the 55th ACM Technical Symposium on Computer Science Education V. 1*, 158–64. [https://doi.org/10.1145/3626252.3630813](https://doi.org/10.1145/3626252.3630813).
- <span id="ref-cs2023"></span>*Computer Science Curricula 2023*. Association for Computing Machinery, IEEE Computer Society, and AAAI. [https://doi.org/10.1145/3664191](https://doi.org/10.1145/3664191).
- <span id="ref-davalos-zhang-2026"></span>Davalos, Eduardo, and Yike Zhang. 2026. “AI Misuse in Education Is a Measurement Problem: Toward a Learning Visibility Framework.” arXiv. [https://doi.org/10.48550/arxiv.2603.07834](https://doi.org/10.48550/arxiv.2603.07834).
- <span id="ref-fischer-et-al-2024"></span>Fischer, Björn, Berit Barthelmes, Sven Eric Panitz, Eva-Maria Iwer, and Ralf Dörner. 2024. “Seeking Consent for Programming Process Data Collection with Trustee-Based Encryption.” In *Proceedings of the 2024 ACM Conference on International Computing Education Research V.1*, 131–42. [https://doi.org/10.1145/3632620.3671125](https://doi.org/10.1145/3632620.3671125).
- <span id="ref-garcia-2025"></span>Garcia, Manuel B. 2025. “Self-Coded Digital Portfolios as an Authentic Project-Based Learning Assessment in Computing Education: Evidence from a Web Design and Development Course.” *Education Sciences* 15 (9): 1150. [https://doi.org/10.3390/educsci15091150](https://doi.org/10.3390/educsci15091150).
- <span id="ref-heckman-et-al-2022"></span>Heckman, Sarah, Jeffrey C. Carver, Mark Sherriff, and Ahmed Al-Zubidy. 2022. “A Systematic Literature Review of Empiricism and Norms of Reporting in Computing Education Research Literature.” *ACM Transactions on Computing Education* 22 (1): Article 3. [https://doi.org/10.1145/3470652](https://doi.org/10.1145/3470652).
- <span id="ref-liu-fan-pan-2026"></span>Liu, Dandan, Guangrui Fan, and Lihu Pan. 2026. “Tool, Tutor, or Crutch?: A Grounded Theory of Cognitive Scaffolding and Offloading in AI-Assisted Programming Education.” *International Journal of STEM Education* 13: 10. [https://doi.org/10.1186/s40594-025-00592-w](https://doi.org/10.1186/s40594-025-00592-w).
- <span id="ref-lopez-pernas-et-al-2025"></span>López-Pernas, Sonsoles, Kamila Misiejuk, Eduardo Oliveira, and Mohammed Saqr. 2025. “The Dynamics of the Self-Regulation Process in Student-AI Interactions: The Case of Problem-Solving in Programming Education.” In *Proceedings of the 25th Koli Calling International Conference on Computing Education Research*. [https://doi.org/10.1145/3769994.3770043](https://doi.org/10.1145/3769994.3770043).
- <span id="ref-mcgill-et-al-2023"></span>McGill, Monica M., Sarah Heckman, Christos Chytas, et al. 2023. “Conducting Sound, Equity-Enabling Computing Education Research.” In *Proceedings of the 2023 Working Group Reports on Innovation and Technology in Computer Science Education*, 30–56. [https://doi.org/10.1145/3623762.3633495](https://doi.org/10.1145/3623762.3633495).
- <span id="ref-nikolic-basta-nikolic-2026"></span>Nikolić, Dragan, and Marijana Basta Nikolić. 2026. “Designing AI-Resilient Assessment in Higher Education: A Four-Pillar Conceptual Framework.” *Frontiers in Artificial Intelligence* 9. [https://doi.org/10.3389/frai.2026.1841682](https://doi.org/10.3389/frai.2026.1841682).
- <span id="ref-prather-et-al-2024"></span>Prather, James, et al. 2024. “The Widening Gap: The Benefits and Harms of Generative AI for Novice Programmers.” In *Proceedings of the 2024 ACM Conference on International Computing Education Research V.1*. [https://doi.org/10.1145/3632620.3671116](https://doi.org/10.1145/3632620.3671116).
- <span id="ref-runeson-host-2009"></span>Runeson, Per, and Martin Höst. 2009. “Guidelines for Conducting and Reporting Case Study Research in Software Engineering.” *Empirical Software Engineering* 14 (2): 131–64. [https://doi.org/10.1007/s10664-008-9102-8](https://doi.org/10.1007/s10664-008-9102-8).
- <span id="ref-runeson-et-al-2012"></span>Runeson, Per, Martin Höst, Austen Rainer, and Björn Regnell. 2012. *Case Study Research in Software Engineering: Guidelines and Examples*. Hoboken, NJ: Wiley. [https://doi.org/10.1002/9781118181034](https://doi.org/10.1002/9781118181034).
- <span id="ref-shihab-et-al-2025"></span>Shihab, Md Istiak Hossain, Christopher Hundhausen, Ahsun Tariq, Summit Haque, Yunhan Qiao, and Brian Wise Mulanda. 2025. “The Effects of GitHub Copilot on Computing Students’ Programming Effectiveness, Efficiency, and Processes in Brownfield Coding Tasks.” In *Proceedings of the 2025 ACM Conference on International Computing Education Research V.1*. [https://doi.org/10.1145/3702652.3744219](https://doi.org/10.1145/3702652.3744219).
- <span id="ref-wohlin-et-al-2012"></span>Wohlin, Claes, Per Runeson, Martin Höst, Magnus C. Ohlsson, Björn Regnell, and Anders Wesslén. 2012. *Experimentation in Software Engineering*. Berlin: Springer. [https://doi.org/10.1007/978-3-642-29044-2](https://doi.org/10.1007/978-3-642-29044-2).
