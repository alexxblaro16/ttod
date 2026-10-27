#!/usr/bin/env bash
# Gate for Z2: shared client + favorites import/tests without live Redis.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
PY="${ROOT}/.venv/bin/python"
test -x "$PY" || PY=python3
"$PY" -c "from services.backend.app.favorites import MemoryFavoriteStore, RedisFavoriteStore"
"$PY" -m unittest services.backend.tests.test_favorites services.backend.tests.test_library -v
echo "Z2 exit-gate OK"