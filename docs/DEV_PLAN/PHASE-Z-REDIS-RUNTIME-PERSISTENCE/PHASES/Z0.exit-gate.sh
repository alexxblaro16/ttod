#!/usr/bin/env bash
# Gate for Z0: report freezes shore domains + dual-write + bind path.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
REPORT="$ROOT/docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASE-Z0-REPORT.md"
MAP="$ROOT/docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/REDIS-SHORE-MAP.md"
test -f "$MAP"
test -f "$REPORT"
grep -Eq 'data/redis|/data' "$REPORT"
grep -Eq 'dual-write|dual write|ProposalStore' "$REPORT"
grep -Eq 'ttod:user:|user profile|sessions' "$REPORT"
grep -Eq 'appendonly|appendfsync|noeviction|redis\.conf' "$REPORT"
echo "Z0 exit-gate OK"