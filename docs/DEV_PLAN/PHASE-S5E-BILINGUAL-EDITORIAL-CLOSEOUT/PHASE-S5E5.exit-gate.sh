#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
test -f exports/bilingual-alignment.json
test -f exports/bilingual-coverage.json
test -f docs/editorial/EDITION-STATEMENT.md
test -f docs/editorial/KNOWN-LIMITATIONS.md
jq -e 'type == "array"' exports/bilingual-alignment.json >/dev/null
jq -e 'type == "object"' exports/bilingual-coverage.json >/dev/null
.venv/bin/python cli.py validate --strict --json
.venv/bin/python cli.py stats --check
make check
git diff --check
echo 'S5E5 exit gate passed; release evidence is assembled and canonical data validates.'
