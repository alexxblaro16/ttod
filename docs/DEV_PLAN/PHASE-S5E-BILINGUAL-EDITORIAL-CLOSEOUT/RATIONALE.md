# Why the S5E closeout exists

## The decision

TTOD's bilingual model and translation pipeline are implemented, and canonical English–Spanish
coverage is complete. A successful schema check proves that records satisfy structural rules. An
accepted proposal proves that a named reviewer used the acceptance transaction. Neither fact alone
documents an exhaustive literary review or establishes that a scholarly edition is ready to publish.

S5E closes that evidence gap. It reconciles current data with older planning prose, records
authorial decisions, resolves alternate proposals without erasing history, reviews every translation
under a frozen policy, applies only approved corrections, and produces a cold audit and edition
statement.

The work is sequential: policy precedes review, review precedes correction, and correction precedes
the release audit. Each phase ends with a runnable gate and an independent cold review.

## Why Lao Tzu sources are in Ahmes and Athanor

The source works are supporting material for TTOD's local composition lens, not TTOD quote records.
The intended flow is:

```text
Lao Tzu bibliography
    ↓ extraction, page anchors, semantic enrichment
Ahmes scholar vault
    ↓ manifest injection and searchable project pointers
Athanor project: scholar-lao-tzu
    ↓ scoped search and source-page verification
TTOD compose lens
    ↓ local model drafts a developer-pedagogy proposal
ttod-bridge pending proposal
    ↓ human review and repository acceptance
TTOD canonical database
```

Ahmes retains extracted source text, page context, and bibliographic metadata. Athanor indexes
source pointers for scoped search and downstream discovery. This gives a TTOD author a way to
explore themes such as naming, emptiness, softness, and non-forcing action while composing a
development aphorism.

The source is a compositional lens. A Taoist text does not establish a factual claim about software
architecture, developer learning, or TTOD policy. TTOD quotes remain pedagogical material, not
independent evidence for Athanor or WPL claims. When a teaching note needs a scholarly citation, the
author reads the source page and passes Ahmes's citation resolver. If it returns `[BIBLIO-GAP]`, no
clean author-date citation is claimed.

The Lao Tzu compose skill says to discover, draft with local Ollama, and submit through ttod-bridge.
It prohibits direct canonical writes. Only a named human acceptance transaction may add the
proposal to `ttod.yml`.

## What is in progress now

Repository evidence distinguishes two pipeline runs:

- An earlier pipeline completed on 2026-09-19. Its `INJECT_DONE` marker records successful smoke
  command exits for Athanor search and vector search. Those codes do not prove that the vector
  search returned a nonempty Lao Tzu result.
- A fresh pipeline was running on 2026-11-08 in the Ahmes batch stage. The three previously
  processed works were skipped. The log shows extraction of `PIPELINE-README.md` and a Jwing Ming
  Yang *Dao de Jing* EPUB, with repeated local Ollama timeouts and semantic-vocabulary warnings.
  The later Athanor readiness, vector ingest, injection, and smoke stages had not been reached in
  the observed state.

The prior Y3 audit measured the vector gateway reading the `deviac` database while the Lao Tzu
ingest wrote to the `athanor` database. Athanor CLI search returned hits, but the vector API returned
zero scoped results for `scholar-lao-tzu`. The same audit found the Blakney source's Ahmes metadata
unsafe for Chicago citation: the extracted title was a reading-list heading and the ISBN was a
low-confidence LLM guess. The design therefore treats vectors as discovery, Athanor as a searchable
pointer, and the full Ahmes page plus citation resolver as the evidence boundary.

See [FINDINGS-2026-11-08.md](FINDINGS-2026-11-08.md). Do not stop, restart, or alter the running
source pipeline during S5E. Any rerun or live vault injection is a separate operation requiring
explicit authorization under the grounding skill.

## Product outcome

At completion, TTOD should be able to answer four questions with evidence:

1. Does every in-scope English original have one active Spanish sister?
2. Which editorial rules and human decisions govern the Spanish texts?
3. What review occurred, and what remains outside its claims?
4. Can another editor reproduce the source-to-translation alignment and release decision?

The closeout does not promise perfect translations. It records what was reviewed, which decisions
shaped the text, the remaining limitations, and who takes responsibility for the edition.
