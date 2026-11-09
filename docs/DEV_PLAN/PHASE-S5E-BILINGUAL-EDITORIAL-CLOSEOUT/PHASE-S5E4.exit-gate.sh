#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
decision="docs/editorial/CANONICAL-CORRECTION-DECISIONS.md"
test -f "$decision"

if grep -Fq 'outcome: NOT_NEEDED' "$decision"; then
  git diff --quiet HEAD -- ttod.yml ttod_core/repository.py tests
  echo 'S5E4 outcome is NOT_NEEDED; no canonical transaction was introduced.'
else
  grep -Fq 'CANONICAL_CORRECTIONS_APPROVED' "$decision"
  .venv/bin/python cli.py validate --strict --json
  .venv/bin/python cli.py stats --check
  make check
  /Users/ruvebal/src/ttod/.venv/bin/python \
    /Users/ruvebal/src/.cursor/skills/ttod-bridge/scripts/tests/test_ttod_bridge.py
fi
git diff --check
echo 'S5E4 exit gate passed.'
