# Y5 — One-axis tree: every child of `agentic/` is a topic pack

**Depends on:** Y1–Y4 agent work done, and the owner checkbox ticked in the
[Y5 decision](../../DECISIONS/Y5-2026-09-21-ONE-AXIS-TREE.md). Without the tick this phase is
BLOCKED — an open slot is not a green light. **Tick given 2026-09-21; executed (see `PHASE-Y5-REPORT.md`).**

## Target

```text
agentic/
  README.md                    legend, with an annotated tree
  ttod-editing/                pack   PACK.md  rules/ttod-editing.md
  public-docs-i18n/            pack   PACK.md  skills/public-docs-i18n/SKILL.md
  report-steward/              pack   (path frozen: CI, Makefile, test)   agents/ rules/ scripts/ skills/
  ide-mcp/                     pack   (mcp.cursor.json mirrored to .cursor/mcp.json)
  lao-tzu-tao-compose/         pack   local-untracked (path frozen: read by a sibling repo)
```

## Do

1. **Census, fresh.** Re-run before touching anything and record the output in the report:
   `git grep -n -e 'agentic/rules' -e 'agentic/skills' -e 'report-steward/agent' -e 'agent/report-steward.md'` outside
   `docs/DEV_PLAN`, plus the same paths in the studio home's `.cursor` and `.agents` directories and in the sibling repositories (deviac, athanor, ahmes, profield, MSCA).
   Also list relative links **inside** the two moved files (`grep -n '](\.\./'`); a move changes
   their depth. Expected live readers, from the 2026-09-21 census: `.cursor/rules/ttod-editing.mdc`,
   `.cursor/skills/public-docs-i18n/SKILL.md`, `AGENTS.md` (lines 56, 57, 95, 232), `agentic/README.md`.
   Known relative link that breaks on the move: `agentic/rules/ttod-editing.md:9` links
   `../AGENTS.md`; at `agentic/ttod-editing/rules/` it must become `../../../AGENTS.md`.
   Anything else is a plan defect: amend this file first.
2. **Move with `git mv`** (history follows): the rule into `agentic/ttod-editing/rules/`, the skill
   into `agentic/public-docs-i18n/skills/`. Fix any relative links found in step 1. **Then `rmdir agentic/rules agentic/skills`** — `git mv` leaves them behind empty, and they would fail the tree test.
3. **Rename** `report-steward/agent/` → `report-steward/agents/`. The 2026-09-21 census found
   exactly two readers, both docs this phase already edits: `report-steward/PACK.md:7` and
   `agentic/README.md:48`. If the fresh census finds any other reader, keep the name and record
   why. Rename nothing else inside that pack.
4. **Add `PACK.md`** to the two new packs and **add the front-matter contract** (decision file) to
   `report-steward`, `ide-mcp`, and — locally — `lao-tzu-tao-compose` (`status: local-untracked`).
   Do not `git add` the `lao-tzu-tao-compose/` pack (Y-phase lesson: stage by explicit path, never
   `git add -A agentic`).
5. **Retarget** the two `.cursor` landings' canonical-path line, the four `AGENTS.md` path lines (56, 57, 95, 232) **and the `AGENTS.md` tree drawing (~lines 189–193)**, whose legend text
   "IDE agent harness (rules, skills, packs)" is stale and which omits the two new packs and `lao-tzu-tao-compose` (local). `test -f` every landing target.
6. **Add `tests/test_agentic_tree.py`** — a `unittest.TestCase` (no pytest in this repo), stdlib only, skipped when `agentic/` is absent — enforcing the seven invariant lines in the decision
   file with the tiny front-matter parser specified there. **Tree-test control:** run it once against a temporary `agentic/rules/` and record the failure, then remove the directory. The negative controls are also a permanent regression (`AgenticTreeNegativeControls`), so this step is not a one-off.
7. **Rewrite `agentic/README.md`** for a human reader: an annotated tree first, one paragraph on
   the single rule ("every folder here is a topic; `rules/`, `skills/`, `agents/`, `scripts/` only
   exist inside one"), then the frozen-path warnings. Keep the epigraphs, the "Harness honesty"
   section, and the cite `Raymond, Eric S. 2001, PDF p. 42` (re-verify with `ahmes query --cite`).
   **Rewrite the pack criterion** (it currently says "≥2 surfaces inside `agentic/`" and would contradict the new tree): a pack is a topic folder with a `PACK.md` and ≥1 surface. Remove the
   Leaf rows and the "Reserved `agents/`" row. (The Y1 supersession banner is already in `Y1-2026-09-20-AGENTIC-LAYOUT.md` and the INDEX; do not add it to the README.)

## Gates

| Gate | Command / evidence |
| --- | --- |
| Tests | `python3 -m unittest tests.test_agentic_tree tests.test_public_privacy_watcher` green, then `make test`; plus `verify-ide-mcp.py` (offline is its default; `--live` not required) |
| Privacy | **Delta gate, not absolute.** In step 1 run `check_public_privacy.py` on each file Y5 creates, edits or moves (`agentic/README.md`, every `PACK.md`, the two landings, `AGENTS.md`, the two moved bodies) and record per-file findings as the baseline, **keyed by (reason, line text), not by line number** (step 5 edits `AGENTS.md` above its existing findings and shifts them). After: **no new finding**. Known pre-existing baseline on 2026-09-21: `AGENTS.md` and the moved `public-docs-i18n` skill (a tilde path at line 22 and a deliberate "never ship `*.internal`" example at line 50) have findings; `agentic/README.md`, `report-steward/PACK.md`, `ide-mcp/PACK.md`, the rule and both landings are clean. A *moved* file keeps its pre-existing findings unless the owner asks for a sanitize; new files must be clean. The whole of `agentic/` is not gated (the watcher's own source and skill carry deliberate examples; the untracked pack has ten findings) |
| No stale readers | `git grep -n -e 'agentic/rules/' -e 'agentic/skills/' -e 'report-steward/agent/' -e 'agent/report-steward.md'` outside `docs/DEV_PLAN` returns nothing — with trailing slashes, so `report-steward/agents/` does not false-match |
| Landings resolve | `test -f` on each landing's canonical target |
| Frozen paths | CI file, `Makefile:134`, test line 13 unchanged and `make` target still finds the script |
| Tree-test control | The tree test fails on the temporary top-level `rules/` (recorded) |
| Skeleton | The generator reads a **branch**, so it cannot exercise this tree. Method: overlay `tests/test_agentic_tree.py` (and the stub landing) onto the generated skeleton and run its suite: it must pass or skip. Running the generator itself needs a clean tree (the untracked `lao-tzu-tao-compose/` alone makes it refuse) and no pre-existing local `skeleton/ts5-fresh-history` branch |
| **Human reader** | See below. **Only the owner can mark this passed**; until then the report says `VERIFYING (human gate open)` |
| Model reader | Secondary. A cold model given only the README and `find agentic -maxdepth 2`, same questions. A pass never substitutes for the owner. The pre-Y5 tree is **not** used as a control: Y0's cold review recorded a model passing that very layout, so it cannot discriminate |

### Human reader protocol

1. **Key first, anchored outside the agent.** Before the owner reads anything, write the answer key and put its sha256 **in a message to the owner and in the report** (the anchor is the owner's copy of that
   message). The key's questions are **hypotheticals the README does not answer verbatim** — e.g. "where does a new one-off workflow for translating slides go?", "where would a rule for commit messages
   go?", "what is the difference between `rules/` inside `report-steward/` and a top-level `rules/`?" (expected: there is no top-level one).
2. **Owner reads cold**: the README's annotated tree and `find agentic -maxdepth 2`, nothing else.
3. **Provenance.** The owner's answers arrive **in the owner's own message** and are quoted verbatim in the report. **The pass/fail line is written by the owner** (a message or an owner-authored commit); an
   agent transcribing "the owner answered X" or judging its own transcription does not count.
4. **Scoring**: answers match the key. A wrong answer, or the owner saying it is still confusing, is a **finding, not a failure to hide**: the phase returns to design with the owner's words as the brief.
5. **Lock discoverability** ("what must never be renamed and why") is **not** in the pass criteria — the README's frozen-path section states it verbatim by design. It is reported separately, as in DevIAC's Q3.
6. Because the README states the classification, this tests README + tree together, not the tree alone; the report says so.

## Do not

- Rename `report-steward/` or `lao-tzu-tao-compose/`. Touch `services/mcp/` or `ttod.yml`.
- Commit the untracked pack. Push. Merge. Self-certify DONE.

## Report

`PHASE-Y5-REPORT.md` then a cold review (`PHASE-Y5-COLD-REVIEW.md`) by the `cascade-cold-reviewer`
subagent, which also re-runs the census independently and reads the diff, not the report.
