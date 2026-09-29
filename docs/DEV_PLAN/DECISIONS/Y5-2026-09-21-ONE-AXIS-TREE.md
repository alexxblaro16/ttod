# Y5 decision — one axis: every child of `agentic/` is a topic pack

**Status:** ACCEPTED by the owner 2026-09-21 (after two plan-stage cold reviews); executed as Y5, human gate open — supersedes **Y1 row 2 only** (`public-docs-i18n` stays a leaf) once the owner accepts. Y1 row 1 (packs flat, not under `agentic/packs/`) **stands** and is re-used here; rows 3–4 stand.
**Owner:** `ruvebal@crea-comm.net` — may overturn any row.
**Implementation authority:** Y5 only; no file is moved by this record.

## Why Y1 was not enough

Y1 kept two organising axes side by side: *by topic* (`report-steward/`, `ide-mcp/`,
`lao-tzu-tao-compose/`) and *by kind* (`rules/`, `skills/`). The Y0 legibility test passed with a
small model reading the README, yet the human owner still found the tree confusing. The model was
the wrong reader, and the tree had three concrete defects a legend cannot remove:

| # | Defect | Evidence |
| --- | --- | --- |
| 1 | Two axes at one depth: `agentic/rules/` (a kind) sits beside `agentic/report-steward/` (a topic) | `find agentic -maxdepth 2` |
| 2 | The words `rules`, `skills` mean two things: a top-level container of leaves, and a pack's own folder | `rules` ×3, `skills` ×3 at depth ≤3 |
| 3 | A pack's agent folder is `agent/` (singular) while its siblings are `rules/`, `skills/` (plural), and the README reserves a third, top-level `agents/` | `report-steward/agent/` vs README "Reserved" row |

## Decisions

| # | Question | Decision | Basis |
| --- | --- | --- | --- |
| 1 | Keep leaves? | **No. Every child of `agentic/` is a topic pack** with a `PACK.md`. `agentic/rules/` and `agentic/skills/` stop existing. A pack needs **≥1 surface** (the old "≥2 surfaces" criterion is withdrawn: it existed only to separate packs from leaves) | One axis. Removes defects 1 and 2 |
| 2 | Kind folders | Inside a pack only, and always plural: `rules/`, `skills/`, `agents/`, `scripts/` | Removes defect 3. `report-steward/agent/` → `agents/` (census in Y5 step 1 must show no live reader) |
| 3 | What the two leaves become | `agentic/ttod-editing/rules/ttod-editing.md`; `agentic/public-docs-i18n/skills/public-docs-i18n/SKILL.md` | Pack name = the subject; the kind folder says what it is |
| 4 | `report-steward/` path | **Frozen** | CI, `Makefile:134`, `tests/test_public_privacy_watcher.py:13` |
| 5 | `lao-tzu-tao-compose/` path | **Frozen** | Read by a sibling: `deviac/.cursor/skills/provenance-layer/profiles.md:190` (`out_dir`) |
| 6 | Status marker | In `PACK.md` front matter (`status: tracked` or `local-untracked`), never in the directory name | A rename to mark status would break the two frozen paths' readers |
| 7 | Checkable, not just documented | A stdlib `unittest` (`tests/test_agentic_tree.py`) enforces the seven-line invariant | The project's own research page says a declared layout is not a verified one |
| 8 | Reader for the legibility gate | The **human owner** reads the annotated tree and answers the placement questions (protocol in the Y5 runbook, with provenance rules); the small-model test stays as a secondary check | The model passed while the human was confused |

## `PACK.md` contract

`PACK.md` **begins** with a `---`-fenced block (the three existing `PACK.md` files start with a `# Title`, so the block is prepended). The parser is hand-written and deliberately tiny:
one `key: value` per line; a list is an inline `[a, b]`; `[]` is the **empty list** (parse it to `[]`, never to `['']`); **no comments anywhere in the block**; no nesting. All keys required.

```yaml
---
name: ttod-editing
purpose: One sentence naming the topic.
surfaces: [rules]
landings: [.cursor/rules/ttod-editing.mdc]
mirrors: []
locks: []
external_readers: []
status: tracked
---
```

| Key | Meaning | Path base | Checked? |
| --- | --- | --- | --- |
| `name` | equals the directory name | — | yes |
| `purpose` | one sentence | — | present |
| `surfaces` | what the pack contains, ≥1 item: `rules`, `skills`, `agents`, `scripts`, or a file/folder name | **pack-relative** | each item must exist inside the pack |
| `landings` | redirect-stub files outside `agentic/` that point at this pack | **repo-root-relative** | see invariant 3 |
| `mirrors` | identical-copy files a tool must parse itself, as `src>dst` (e.g. `mcp.cursor.json>.cursor/mcp.json`) | `src` pack-relative, **`dst` repo-root-relative** | both exist; parsed JSON equal |
| `locks` | in-repo files that hard-wire this pack's path (CI, Makefile, tests) | **repo-root-relative** | exist, and their text contains the pack's directory name |
| `external_readers` | readers in sibling repos, in words, no home-directory paths | — | no (documentation) |
| `status` | `tracked` or `local-untracked` | — | value only |

## The invariant the test enforces

The test is a `unittest.TestCase` (this repo has no pytest; `make test` runs `python3 -m unittest discover`), **skipped when `agentic/` does not exist** because
`scripts/generate-ts5-teaching-baseline.sh` builds the student skeleton from the `skeleton/ts5-hello-world` **branch** (`git archive`), not from the working tree; that skeleton has no `agentic/`, so the guard matters once the branch is rebased onto a tree that carries this test. Prototyped in a scratch copy by the second cold review: all five packs describable, tree-test control fails, skeleton skips.

1. Every direct child directory of `agentic/` that is present has a `PACK.md` with every required key, and `name` equals the directory.
2. No direct child is named `rules`, `skills`, `agents`, or `scripts`.
3. Every `landings` path exists and its body matches the **exact marker** `Canonical:\s*`([^`]+)`` at least once; **every** captured path must exist **and lie inside the pack that declares the landing**. (A weaker
   "any backticked path exists" reading passes a stale landing — the reviewer demonstrated it — so the marker is mandatory.)
4. Every `mirrors` pair exists and the two files **parse to equal JSON** (the test does this itself; `verify-ide-mcp.py` stays `ide-mcp`'s own stricter gate — allowlist and digest — and is not called).
5. Every `locks` file exists and its text contains the pack's directory name (existence alone would pass a `Makefile` that no longer mentions the pack).
6. `surfaces` is non-empty and every item exists inside the pack (this is the "≥1 surface" criterion, made checkable).
7. A pack with `status: local-untracked` is validated exactly like any other **when present**; its being untracked is not an error, and a fresh clone simply does not have it.

`external_readers` is documentation, not a checked path: a sibling repo's file cannot be required to exist on every machine, and a home-directory path would trip the privacy watcher.

## What was considered and rejected

| Option | Why not |
| --- | --- |
| Keep leaves, improve the legend (Y1 status quo) | The defect is the layout, not the prose; the legend already passed a model and failed the human |
| Nest packs under `agentic/packs/` | Fixes nothing about defects 1–3; adds a level |
| Group by kind at top level (`agentic/rules/<topic>/…`) | Splits one topic across three trees; the opposite of "things that move together live together" |
| Rename `report-steward/` to fit a scheme | Breaks CI for cosmetics |
| Y1's option B — "a pack whose `PACK.md` indexes an external script" (rejected in Y1 as "contradicts what a pack is") | **Re-adopted for `public-docs-i18n`, knowingly.** Under one axis a pack is a *topic folder*, not a bundle of co-moving files, so the Y1 objection no longer applies: the script stays at `scripts/translate_public_docs.py` (a standalone CLI, `--help` works without the skill) and the `PACK.md` names it in `purpose`. The cost: the executable half of the topic lives outside the pack, as before |

## Cost, stated plainly

A one-file topic (`ttod-editing`) now needs a directory and a `PACK.md`. That is the price of a
single axis. It is small but not two lines: two moves, two new `PACK.md`, front matter on three existing `PACK.md`, two landing retargets, the `AGENTS.md` path lines and tree drawing, one
rename, one new test. The skill path gains a stutter (`public-docs-i18n/skills/public-docs-i18n/`); it
matches the existing `report-steward/skills/evidence-state-report/` shape, so it is the convention,
not an accident.

## Owner checkbox

- [x] Owner accepts the one-axis tree and authorises Y5 execution — **ACCEPTED 2026-09-21**, the owner's message quoted verbatim in [`PHASE-Y5-REPORT.md`](../PHASE-Y-AGENTIC-DIRTREE-UNIX/PHASE-Y5-REPORT.md) § Authorization. **Valid only if the tick is in a commit authored by the owner, or the owner's message is quoted in the Y5 report.** An agent editing this line does not count.

## Non-authorization

No move, no `ttod.yml` change, no `proposal accept`, no rename of `report-steward/` or
`lao-tzu-tao-compose/`, no push.
