---
title: Agentic development as a governed practice
eyebrow: Why this project verifies before it declares
description: What building this project's own IDE/MCP harness under cold review shows about teaching agentic development — and what it does not yet show.
permalink: /research/agentic-development/
lang: en
alt_lang_missing: true
---

# Evidence before declaration

A config file that parses is not a server that answers. That distinction — something this
project's own [IDE/MCP guide]({{ '/guides/connect-ide-mcp/' | relative_url }}) states as a
practical instruction — is also, unhedged, the whole argument of this page: agentic
development practice is teachable, and worth teaching deliberately, to the extent it makes the
gap between *declared* and *verified* visible, checkable, and someone else's job to confirm.
This page is a reflection on a design pattern this repository actually runs, not a report of a
completed study — [Method and safeguards]({{ '/research/methodology/' | relative_url }})
remains the page that governs whether and how a future study of this platform could be
authorized. Nothing here claims that gate has been passed.

## The pattern, stated plainly

Every non-trivial change to this repository's own agent-facing tooling — including the harness
described in the [IDE/MCP guide]({{ '/guides/connect-ide-mcp/' | relative_url }}) — moves
through the same four states before anyone calls it finished: an implementer builds it and
stops short of certifying it done; a second, independent reader with no memory of the
implementation session audits the actual artifact against a written acceptance list; findings
get triaged and fixed, not argued away; and a named human, not either automated reader, decides
whether it merges. No step is allowed to skip ahead on the strength of a plausible-sounding
report. When one recent build's own live-verification step returned a result that read as
success, a second, independent pass re-ran the same live check itself — network calls and all —
rather than accepting the first pass's transcript, and only then treated the claim as settled.

That habit is not incidental process overhead. It is the entire epistemic content of what
"governed agentic development" means in practice here: not that an AI agent is present, but
that its claims are structurally required to survive a reader who was not in the room when the
claim was made.

## A studio parallel, not a borrowed rationale

A sibling project in this studio, Athanor, states its own version of the same discipline as a
named law: *"Plans, decisions, commands, exit codes, raw test/evaluation artifacts, hashes, and
review verdicts are repository-local or stored under an indexed artifact path. Chat history is
not the system of record."* A unit of work is not considered finished, in Athanor's own
formulation, until another agent — one who was not party to the original decision — can
reproduce the acceptance verdict from the files alone. Athanor does not state this as a
pedagogical claim — it is a governance
rule for provenance of AI-produced engineering artifacts, nothing more, and this page does not
stretch it into something it isn't. What's worth noting is only that two independently governed
projects in the same studio converged on the same structural answer to the same problem
(evidence that outlives one agent's turn) from two different starting points (this project's
own quote-proposal review pipeline; Athanor's provenance law) — a pattern worth naming, not a
citation of shared authorship.

## What the corpus already says about this, unprompted

This project's own pedagogical quote database — governed the same way its code is, by the same
proposal-and-accept discipline described in [Contributing]({{ '/guides/contributing/' |
relative_url }}) — already contains entries that describe exactly this failure mode, written
before this particular guide existed:

> "the enricher writes ten thousand mentions — yet relations: zero" (`arch-058`)

A system can register that something was *mentioned* — a config key present, a server listed,
a connection attempted — without ever confirming a *relation* actually holds: that the
mention resolved to something real. `arch-058`'s own teaching note, written about a different
system entirely (a knowledge-extraction pipeline, not an IDE), names the exact shape of the bug
this project's own MCP verification scripts exist to catch: a server can appear in a config file
(a mention) without ever answering a real protocol handshake (the relation). The metaphor
transferred without being forced to.

Two more entries, cited by ID rather than paraphrased, describe the surrounding practice:

> "Ahmes extracts. Arkadia curates. DevIAC serves. A student who understands this triangle
> understands that knowledge flows — it is never static, never finished, never owned by one
> system alone." (`arch-049`)

> "Each PHASE-n.md is a self-contained prompt with all context embedded. A local 72B model
> following it will produce nearly identical output to a cloud model, because the prompt does
> the heavy lifting. The intelligence is in the specification, not the parameter count."
> (`arch-050`)

`arch-050`'s claim is directly testable, and was tested in the course of writing this guide's
companion page: a locally-run, open-weight coding model, given the same source material and
acceptance criteria a larger cloud model would receive, produced a faithful, unhallucinated
first draft of the [IDE/MCP guide]({{ '/guides/connect-ide-mcp/' | relative_url }}) — correct
on every checkable fact, incorrect only on register and on one rationale it under-specified.
That is one observation, not a benchmark; it is offered here as exactly the kind of concrete,
falsifiable claim §"Evidence still needed" in [Method and
safeguards]({{ '/research/methodology/' | relative_url }}) calls for, not as proof of anything
beyond itself.

## What the wider literature says — motivating, not validating

Consistent with the hedge [Method and safeguards]({{ '/research/methodology/' | relative_url }})
already applies to its own citations, the following sources motivate attention to this design
space; none of them evaluates this platform, and none is treated as validating it.

Large-scale classroom deployments of AI programming assistants already generate real,
studyable process data. [Kazemitabaar et al. 2024](#ref-kazemitabaar-et-al-2024) deployed an
LLM-based programming assistant to 700 students over a 12-week semester specifically designed
to avoid revealing direct code answers, then triangulated a thematic analysis of 8,000 usage
events with student interviews and educator interviews — a scale and method this project's own
practice does not yet approach, and does not claim to.

The governance question this project answers for its own IDE tooling — which MCP servers are
trustworthy enough to commit as a default, and why an official-source allowlist rather than
convenience — turns out to have an independent, contemporaneous answer in the security
literature. [Errico, Ngiam, and Sojan 2025](#ref-errico-ngiam-sojan-2025) name content-injection,
supply-chain compromise, and privilege-escalating "unintentional adversary" agents as the three
live threat classes MCP's flexibility introduces, and recommend exactly the controls this
project already applies to its own default configuration — per-scope authorization, provenance
tracking, and centralized governance via allowlists or gateway layers — arrived at independently
of this project, not cited by it in the design decision that predates this paper's own
publication.

Curriculum-wide treatments of generative AI already frame evaluating when an AI approach is
appropriate, not just how to invoke one, as a core competency
([*Computer Science Curricula 2023*](#ref-cs2023)) — the same framing this page applies to
verifying an MCP connection rather than assuming one.

## What this page does not claim

This is a design reflection on one project's own governed practice, read against literature
that predates and postdates it independently. It is not a completed study, it does not report
outcomes for any student cohort, and it does not authorize collecting evidence from students for
research purposes — that authorization, if it is ever sought, remains entirely
[Method and safeguards]({{ '/research/methodology/' | relative_url }})'s to grant, on its own
terms, not this page's to assume.

## References

- <span id="ref-cs2023"></span>*Computer Science Curricula 2023*. Association for Computing Machinery, IEEE Computer Society, and AAAI. [https://doi.org/10.1145/3664191](https://doi.org/10.1145/3664191).
- <span id="ref-errico-ngiam-sojan-2025"></span>Errico, Herman, Jiquan Ngiam, and Shanita Sojan. 2025. "Securing the Model Context Protocol (MCP): Risks, Controls, and Governance." arXiv. [https://doi.org/10.48550/arxiv.2511.20920](https://doi.org/10.48550/arxiv.2511.20920).
- <span id="ref-kazemitabaar-et-al-2024"></span>Kazemitabaar, Majeed, Runlong Ye, Xiaoning Wang, Austin Z. Henley, Paul Denny, Michelle Craig, and Tovi Grossman. 2024. "CodeAid: Evaluating a Classroom Deployment of an LLM-Based Programming Assistant that Balances Student and Educator Needs." In *Proceedings of the CHI Conference on Human Factors in Computing Systems (CHI '24)*. [https://doi.org/10.1145/3613904.3642773](https://doi.org/10.1145/3613904.3642773).
