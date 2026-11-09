#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
pack="docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT"
ledger="$pack/PROPOSAL-DISPOSITION-LEDGER.md"
test -f "$ledger"

while IFS= read -r proposal_id; do
  test -n "$proposal_id" || continue
  grep -Fq "$proposal_id" "$ledger" || {
    echo "Missing human disposition for open proposal $proposal_id" >&2
    exit 1
  }
done < <(jq -r 'select((.status == "proposed" or .status == "needs_revision") and
  ([.candidate_content.relation_edges[]? | select(.relation_type == "translation_of")] | length) > 0) |
  .proposal_id' proposals/*.json)

git diff --quiet HEAD -- ttod.yml
make check
/Users/ruvebal/src/ttod/.venv/bin/python \
  /Users/ruvebal/src/.cursor/skills/ttod-bridge/scripts/tests/test_ttod_bridge.py
git diff --check
echo 'S5E2 exit gate passed; all currently open translation proposals have a ledger disposition.'
