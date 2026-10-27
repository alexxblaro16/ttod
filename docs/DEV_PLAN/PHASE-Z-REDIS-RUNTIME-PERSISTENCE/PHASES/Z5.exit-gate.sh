#!/usr/bin/env bash
# Gate for Z5: visual sync clean; docs mention Redis shore; #87 disposition in report.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
python3 scripts/sync_visual_system.py --check
grep -Eq 'Redis|REDIS' docs/public/guides/local-setup.md
grep -Eq 'ttod\.yml|corpus|temple|shore' docs/public/guides/local-setup.md || \
  grep -Eq 'ttod\.yml|corpus' docs/public/platform/index.md
REPORT="$ROOT/docs/DEV_PLAN/PHASE-Z-REDIS-RUNTIME-PERSISTENCE/PHASE-Z5-REPORT.md"
test -f "$REPORT"
grep -Eq '87|superseded|merged' "$REPORT"
echo "Z5 exit-gate OK"