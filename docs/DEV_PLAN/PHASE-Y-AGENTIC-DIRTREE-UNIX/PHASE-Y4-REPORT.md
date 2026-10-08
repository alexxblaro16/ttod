# PHASE-Y4-REPORT.md

**Status:** DONE for the agent's work (2026-09-20) — cold review PASS, see [`PHASE-Y4-COLD-REVIEW.md`](PHASE-Y4-COLD-REVIEW.md). **The human gate is still closed**: nothing was accepted.
**Runbook:** [`PHASES/Y4-dear-tree-proposals.md`](PHASES/Y4-dear-tree-proposals.md)

## What the agent did (and only this)

1. Read the five staged proposals (`20260920T1656*`, ttod-bridge `pending/`): all
   `origin: blackbox`, `status: pending_human_review`, no `validated_by`; every section
   (`architecture`, `code-craft`, `devops`, `wisdom`) exists and every tag is in `tag_taxonomy`.
2. Dry-ran the whole import → accept → validate chain in a **disposable sandbox** (a copy of
   `cli.py`, `ttod_core/`, `schema/`, `ttod.yml` under `/tmp`, an empty proposal store), using the
   reviewer id `DRYRUN-NOT-A-HUMAN`, then deleted the sandbox. Result: 5 imported, 5 accepted, quotes
   460 → 465, `validate --strict` **valid**, `stats --check` **OK**, `subsection` and `teaches`
   preserved, each accepted record carries a `validation` block. The live `ttod.yml` SHA-256
   (`9503e81d…`) and `git status` on it and on `proposals/` are unchanged.

The agent did **not** run `proposal accept` against the live file, supplied no real reviewer id, and
did not touch `collections`.

## Surprises (amend-on-surprise — the plan assumed a working path)

| # | Finding | Consequence |
| --- | --- | --- |
| 1 | The staged files' own `acceptance.command` **cannot run**: `cli.py add` requires `--reviewer-id` ("no bypass") and has **no** `--subsection` / `--teaches` options; the note tells a human to "hand-add `validated_by: human`", a pre-v3 contract | Do not paste those commands. The bridge is a studio skill (cite-not-absorb); its emitted command is stale against the v3 CLI — owner action |
| 2 | Staged files are YAML; `proposal import` takes proposal **JSON** (`schema/proposal.schema.json`) | A conversion is needed. A verified converter is in the appendix; `subsection`/`teaches` survive because the schema carries them (`cli.py proposal create` and `add` cannot set them) |
| 3 | Runbook step 2 says to add a `collections.dear_tree` block. **No CLI verb edits `collections`**, and hand-editing `ttod.yml` is forbidden by the project contract | Left undone. **Owner decision:** skip the collection, accept a deliberate human hand-edit of `collections` only, or add a CLI verb (out of scope here) |
| 4 | Provenance strings say `lens:lao-tzu-tao-compose(scholar-lao-tzu)`, but Y3 showed only Athanor answers for that lens (vectors empty, cite `[BIBLIO-GAP]`) | Not a defect — no Lao Tzu cite is claimed — but the reviewer should know the lens grounding is Athanor-only |

## What the converter added that the staged files did not contain

Text, section, level, tags, `subsection` and `teaches` carry over unchanged. The converter also
**asserts**: `lang: en`; a `rights` block (CC-BY-NC-SA-4.0, holder `ruvebal@crea-comm.net`,
`permission_basis: rights-holder-relicense-2026-08-18` — identical on all 460 live quotes, so
defensible, but still a rights statement made by an agent); an `authorship_assertion` built from the
staged `source` string; and a `generation_method` label (which does not reach the accepted quote).
**The human should confirm the rights block and `lang` before accepting.**

## For the human reviewer (advisory, not a verdict)

- `cc-077`-candidate *"Name a folder as if you were baptising a star — then refuse a second name for
  the same sky"* sits next to existing `cc-033` (*"Before you baptise a star, grep the registry…"*):
  same motif. Keep as a deliberate companion (consider a `related` link) or reject as redundant.
- The IDs the sandbox assigned (`cc-077`, `arch-111`, `arch-112`, `wis-035`, `dop-015`) are
  **provisional** — real IDs depend on accept order. Cite by ID only after a real accept.

## Human steps (verified shape; ID and decisions are yours)

```bash
cd ~/src/ttod && . .venv/bin/activate
python <converter> /tmp/dear-tree-json        # appendix; writes one proposal JSON per staged file
python cli.py proposal import /tmp/dear-tree-json/<uuid>.json      # per file you keep
python cli.py proposal review <uuid> --action comment --reviewer-id <YOUR-ID> --comment "..."   # optional
python cli.py proposal accept <uuid> --reviewer-id <YOUR-ID>       # per file you accept
python cli.py validate --strict && python cli.py stats --check
```

Reject or amend freely — an unaccepted proposal costs nothing and never touched `ttod.yml`.

## Appendix — converter used in the dry run

```python
import yaml, json, uuid, glob, sys, pathlib
out=pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
RIGHTS={"access":"public","license":"CC-BY-NC-SA-4.0","holder":"ruvebal@crea-comm.net","permission_basis":"rights-holder-relicense-2026-08-18"}
for f in sorted(glob.glob(str(pathlib.Path.home()/"src/.cursor/skills/ttod-bridge/pending/20260920T1656*.yaml"))):
    y=yaml.safe_load(open(f)); q=y["quote"]; pid=str(uuid.uuid4())
    cc={"text":q["text"],"section":q["section"],"level":q["level"],"lang":"en","origin":"blackbox",
        "tags":q["tags"],"subsection":q["subsection"],"teaches":q["teaches"],
        "authorship_assertion":"proposed by ttod-bridge, provenance: "+q["source"]+" — human review required before acceptance",
        "rights":RIGHTS}
    p={"proposal_id":pid,"status":"proposed","candidate_content":cc,"proposer_kind":"model","proposer_id":y["proposal"]["proposed_by"],
       "generation_method":"ttod-bridge:studio-session/agentic-dirtree-coherence-2026-09-20","human_review_activities":[],
       "created_at":y["proposal"]["proposed_at"].replace("+00:00","Z")}
    (out/f"{pid}.json").write_text(json.dumps(p,indent=2,ensure_ascii=False)); print(pid, q["section"], "|", q["text"][:60])
```
