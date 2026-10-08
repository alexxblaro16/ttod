# Y4 — Dear Tree proposals (human gate)

**Amended 2026-09-20 after a dry run** — the plan's accept path did not exist as written; see
[`PHASE-Y4-REPORT.md`](../PHASE-Y4-REPORT.md) for what was measured and the verified recipe.

## Already staged (2026-09-20) — review these first

Under `~/src/.cursor/skills/ttod-bridge/pending/`:

| File stem | Theme |
| --- | --- |
| `…-architecture-a-dirtree-is-a-cathedral-of-names-and-a-` | cathedral/bazaar dirtree |
| `…-code-craft-name-a-folder-as-if-you-were-baptising-a` | naming / one star |
| `…-architecture-when-packs-and-leaves-share-a-parent-wit` | deer lost in forest |
| `…-wisdom-wu-wei-in-a-repository-remove-the-wrong-` | non-forcing layout |
| `…-devops-release-early-the-layout-you-can-defend-` | ESR release-early → README |

All `origin: blackbox`, no `validated_by`.

## What the agent may do here — and only this

- Read the five staged files; confirm each is well-formed and still `origin: blackbox` with no
  `validated_by`.
- Dry-run the import → accept chain in a **disposable sandbox** (never the live file or the live
  `proposals/`), with a reviewer id that cannot be mistaken for a person (`DRYRUN-NOT-A-HUMAN`), delete
  the sandbox, and show the live hash unchanged.
- Write `PHASE-Y4-REPORT.md` and leave the exact accept commands for the named human.

The agent does **not** run `proposal accept`, does not supply a `--reviewer-id`, and does not
edit `collections`. Accepting is the human act; the collection edit is only valid after it.

## Human steps

1. Convert the staged YAML to proposal JSON (the staged `acceptance.command` lines are stale and will
   not run), then `proposal import` → review → `proposal accept --reviewer-id <your id>`.
2. **Collection — owner decision, not an agent step.** No CLI verb edits `collections`, and a hand-edit of
   `ttod.yml` breaks the project contract. Skip it, accept a deliberate human hand-edit, or add a CLI
   verb first. If (and only if) the owner chooses the hand-edit, after IDs exist:

```yaml
dear_tree:
  name: The Tao of the Dear Tree
  description: >-
    Quotes on dirtree coherence — naming homes, packs vs leaves,
    non-forcing structure (cathedral of names, bazaar of packs).
  ids: [cc-XXX, arch-XXX]   # replace with the real accepted IDs; YAML comments here change the
                            # snapshot's collection-policy digest, so keep this block bare
```

3. `python cli.py validate --strict` + `stats --check`.
