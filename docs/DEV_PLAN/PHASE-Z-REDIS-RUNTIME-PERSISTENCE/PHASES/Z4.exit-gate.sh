#!/usr/bin/env bash
# Gate for Z4: proposal/review tests green; no KEYS in backend app code.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
if rg -n '\.keys\(|KEYS |\bFLUSHALL\b|\bFLUSHDB\b' services/backend/app --glob '*.py'; then
  echo "Z4 exit-gate: forbidden Redis KEYS/FLUSH in app code" >&2
  exit 1
fi
python3 -m unittest \
  services.backend.tests.test_api \
  services.backend.tests.test_review_pipeline \
  -v
echo "Z4 exit-gate OK"