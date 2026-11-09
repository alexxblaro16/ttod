#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
index='docs/DEV_PLAN/INDEX.md'
statement='docs/editorial/EDITION-STATEMENT.md'
test -f "$statement"
grep -Fq 'PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT' "$index"
if rg -n 'Proposed corpus-completion continuation:.*PHASE-S5-BILINGUAL-CORPUS-TRANSLATION-PLAN' "$index"; then
  echo 'Programme index still describes S5 as only proposed.' >&2
  exit 1
fi
if rg -n 'img-086.*(FAIL|defect|unresolved)' "$index" docs/editorial/EDITORIAL-DECISIONS.md; then
  echo 'Current documentation contradicts the approved img-086 decision.' >&2
  exit 1
fi
make check
make docs-privacy
/Users/ruvebal/src/ttod/.venv/bin/python \
  /Users/ruvebal/src/.cursor/skills/ttod-bridge/scripts/tests/test_ttod_bridge.py
git diff --check
echo 'S5E6 exit gate passed; programme status is reconciled and privacy checks are clean.'
