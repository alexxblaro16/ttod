#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"
pack="docs/DEV_PLAN/PHASE-S5E-BILINGUAL-EDITORIAL-CLOSEOUT"
summary="$pack/PHASE-S5E3-REVIEW-SUMMARY.md"
ledger_path="${TTOD_EDITORIAL_LEDGER:-}"
test -f "$summary"
test -n "$ledger_path" && test -r "$ledger_path" || {
  echo 'Set TTOD_EDITORIAL_LEDGER to the owner-approved private ledger path.' >&2
  exit 2
}

export_path="$(mktemp /tmp/ttod-s5e3-export.XXXXXX)"
expected_ids="$(mktemp /tmp/ttod-s5e3-expected.XXXXXX)"
reviewed_ids="$(mktemp /tmp/ttod-s5e3-reviewed.XXXXXX)"
trap 'rm -f "$export_path" "$expected_ids" "$reviewed_ids"' EXIT

.venv/bin/python cli.py export --format json --output "$export_path"
jq -e '.entries | type == "array"' "$ledger_path" >/dev/null
jq -r '.quotes[] | select(.lang == "es") |
  select(any(.relation_edges[]?; .relation_type == "translation_of")) | .id' \
  "$export_path" | sort -u > "$expected_ids"
jq -r '.entries[] | select(.fidelity_pass.decision != null and .spanish_pass.decision != null) |
  .translation_id' "$ledger_path" | sort -u > "$reviewed_ids"
if ! diff -u "$expected_ids" "$reviewed_ids"; then
  echo 'Private ledger does not contain both review decisions for every current Spanish translation.' >&2
  exit 1
fi
git diff --quiet HEAD -- ttod.yml proposals
make check
git diff --check
echo 'S5E3 exit gate passed; every Spanish translation has both human review decisions.'
