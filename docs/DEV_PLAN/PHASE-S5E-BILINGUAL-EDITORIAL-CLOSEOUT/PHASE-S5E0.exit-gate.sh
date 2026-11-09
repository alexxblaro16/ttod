#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
pack="docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT"

test -f "$pack/FINDINGS-2026-11-08.md"
test -f "$pack/EDITORIAL-DECISIONS.md"
grep -Fq 'EDITORIAL-DECISION-2026-11-08-CODA' "$pack/EDITORIAL-DECISIONS.md"
grep -Fq 'Coda con sabiduría' "$pack/EDITORIAL-DECISIONS.md"
git diff --quiet HEAD -- ttod.yml proposals

.venv/bin/python cli.py validate --strict --json
.venv/bin/python cli.py stats --check
make check
/Users/ruvebal/src/ttod/.venv/bin/python \
  /Users/ruvebal/src/.cursor/skills/ttod-bridge/scripts/tests/test_ttod_bridge.py
git diff --check
echo 'S5E0 exit gate passed; canonical and proposal stores unchanged.'
