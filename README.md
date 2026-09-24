# 道 THE TAO OF THE DEVELOPMENT (TTOD)

**by Rubén Vega Balbás, PhD** — `ruvebal@crea-comm.net`

```text
═══════════════════════════════════════════════════════════════════════════════
                              道
                    THE TAO OF THE DEVELOPMENT
                              道
         Ancestral Wisdom for the Age of Machine-Assisted Creation
═══════════════════════════════════════════════════════════════════════════════
```

> *"The Tao that can be prompted is not the eternal Tao. The code that can be generated without understanding is not true code."*  
> — Lao Tzu, if he had lived to see Stack Overflow

---

> In the ancient scrolls of the silicon age, there existed a sacred text known as [The Tao of Programming](https://www.mit.edu/~xela/tao.html) —a collection of paradoxical wisdom passed down through generations of code warriors. Inspired by its timeless teachings, this book of wisdom is dedicated to the art of machine-assisted creation, revealing the eternal truths of technological intelligence in the digital realm.

---

TTOD is a pedagogical wisdom database — aphorisms for developers walking the path, organized by
section and mastery level, and served outward as content-addressed, human-governed quotes. See
[`AGENTS.md`](AGENTS.md) for the agent contract, data model, and CLI.

**Development status, contract, and engineering runbooks** live in one place so they never drift
into two tellings: [`docs/DEV_PLAN/INDEX.md`](docs/DEV_PLAN/INDEX.md). That file is the canonical
source for programme state and links to the evidence reports. This README does not repeat it.

## Public guide map

The independent Jekyll publication is sourced only from [`docs/public`](docs/public). English
opens at `/`; Spanish at `/es/`. The indexes provide a complete menu across the developed and
planned teaching surfaces:

- [Project](docs/public/project/index.md) — mission, governance, provenance, and licensing
- [Product areas](docs/public/platform/index.md) — content, quotes, graph, Oracle, operations, and tests
- [Teaching model](docs/public/teaching/index.md) — FE II Units 1–7, Entrega 1, mid-term defence
- [Research](docs/public/research/index.md) — questions, maturity, method, and safeguards
- [Guides](docs/public/guides/index.md) — local setup, product use, and contribution
- [Students](docs/public/audiences/students.md) — Entrega 1 product and Units 1–7 mid-term
- [University partners](docs/public/audiences/partners.md) — academic value and release gates
- [Research and venture partners](docs/public/audiences/research-funders.md) — assets, risk, and diligence
- [Roadmap](docs/public/roadmap/index.md) — evidence-backed current and proposed states

The documentation site may be published while the application remains local. That does not by
itself authorize making the whole source repository public.

## Canonical surface

The live collection is schema **v3.1.0**. English originals and Spanish sisters are separate
records linked by `translation_of`; IDs never carry locale suffixes. The public-index flagship is
`wis-033`; its Spanish sister is `wis-034`. Canonical writes remain CLI/repository transactions
only. Derive counts with `python cli.py stats` — do not copy them into this file.

Public documentation is the Jekyll tree above. It is a documentation-only publication lane: it
may go online while the application stays local. GitHub Pages is configured from that tree; it
does not implement application hosting and does not authorize changing repository visibility.

Programme tables, engineering reports, and runbooks remain only in
[`docs/DEV_PLAN/INDEX.md`](docs/DEV_PLAN/INDEX.md).

## Verification

```bash
. .venv/bin/activate
python cli.py validate --strict --json   # must exit 0
python cli.py stats --check              # meta must match recomputed
python -m unittest discover -s tests -p 'test_*.py'   # full suite must pass
```

When `docs/public` changes, also run the publication privacy watcher over that tree (and over
rendered output after a Jekyll build). The full agent verification set, including the ttod-bridge
suite, is listed in [`AGENTS.md`](AGENTS.md).

## Development Team

**Rubén Vega Balbás, PhD. <ruben.vega@udit.es>**: Product owner, product manager  
**Rodrigo García Sánchez <rodrigo.garcia.sanchez@alumnos.udit.es>**: Developer, Oracle Terminal  
**Àvila Rodriguez Andrea <andrea.avila@alumnos.udit.es>**: Developer, Oracle Terminal  
**Alejandro Blanco Rodríguez (alexxblaro16) <alejandro.blanco@alum.udit.es>**: Developer, Front End II  
**Iván (@Gonsiii11)<ivan.herrera@alumnos.udit.es>**: Developer, Front End II  
**Pablo Novoa Rodríguez (@PRNovoa)<pablo.novoa@alumnos.udit.es>**: PWA Local Operations  
**Gonzalo Pérez Fernández-Corugedo (@gpfc-git)<gonzalo.perez.fernandezcorugedo@alumnos.udit.es>**: Knowledge Graph Developer  


## License

Code is MIT ([`LICENSE-CODE`](LICENSE-CODE)); content — `ttod.yml` quotes, `docs/`,
`sources/` — is CC BY-NC-SA 4.0 ([`LICENSE-CONTENT`](LICENSE-CONTENT)), per
[`docs/DEV_PLAN/DECISIONS/Q0-2026-08-18-RIGHTS-LICENSE-NC.md`](docs/DEV_PLAN/DECISIONS/Q0-2026-08-18-RIGHTS-LICENSE-NC.md).

## Agent contract

[`AGENTS.md`](AGENTS.md)
([agentsmd standard](https://github.com/agentsmd/agents.md)).

## Tarea en curso - Alejandro e Iván
