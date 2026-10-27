#!/usr/bin/env bash
# Gate for Z6: hardening report exists; no from_url sprawl outside shared client.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
REPORT="$ROOT/docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASE-Z6-REPORT.md"
test -f "$REPORT"
grep -Eq '503|isolation|pool|client' "$REPORT"
# Allow from_url only in the shared client module (name flexible).
hits="$(rg -n 'Redis\.from_url|from_url\(' services/backend/app --glob '*.py' || true)"
if [ -n "$hits" ]; then
  bad="$(echo "$hits" | rg -v 'redis_client\.py|redis_pool\.py|client\.py' || true)"
  if [ -n "$bad" ]; then
    echo "Z6 exit-gate: Redis.from_url outside shared client:" >&2
    echo "$bad" >&2
    exit 1
  fi
fi
echo "Z6 exit-gate OK"