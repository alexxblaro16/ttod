#!/usr/bin/env bash
# Gate for Z3: auth module imports; auth tests pass without live Redis.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
python3 -c "from services.backend.app.auth import AuthService, RequireSession, RequireAccessToken"
python3 -m unittest services.backend.tests.test_auth -v
echo "Z3 exit-gate OK"