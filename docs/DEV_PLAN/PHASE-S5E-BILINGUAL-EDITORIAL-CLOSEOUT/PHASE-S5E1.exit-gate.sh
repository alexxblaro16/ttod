#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
pack="docs/editorial"
decisions="$pack/EDITORIAL-DECISIONS.md"

test -f "$pack/EDITORIAL-TRANSLATION-POLICY.md"
test -f "$pack/TTOD-ES-GLOSSARY.yml"
test -f "$pack/EDITORIAL-REVIEW-LEDGER.schema.json"
test -f "$decisions"
.venv/bin/python -m json.tool "$pack/EDITORIAL-REVIEW-LEDGER.schema.json" >/dev/null
.venv/bin/python -c 'import yaml,sys; yaml.safe_load(open(sys.argv[1], encoding="utf-8"))' "$pack/TTOD-ES-GLOSSARY.yml"
grep -Fq 'EDITORIAL_POLICY_APPROVED' "$decisions"
grep -Fq 'EDITORIAL-DECISION-2026-11-08-CODA' "$decisions"
git diff --quiet HEAD -- ttod.yml proposals
git diff --check
echo 'S5E1 exit gate passed; policy approval and ledger contract are present.'
