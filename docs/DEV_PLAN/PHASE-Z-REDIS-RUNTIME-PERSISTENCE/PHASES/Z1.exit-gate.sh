#!/usr/bin/env bash
# Gate for Z1: Compose validates and redis uses a host bind mount under data/redis.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
CFG="$(mktemp)"
trap 'rm -f "$CFG"' EXIT
docker compose config >"$CFG"
grep -q '^  redis:' "$CFG"
# Reject host port publish on redis (teaching stack stays internal-network only).
if awk '
  $0 ~ /^  redis:/ {in_redis=1; next}
  in_redis && $0 ~ /^  [a-z]/ {in_redis=0}
  in_redis && $0 ~ /^    ports:/ {found=1}
  END {exit found ? 0 : 1}
' "$CFG"; then
  echo "Z1 exit-gate: redis must not publish host ports" >&2
  exit 1
fi
# docker compose config expands binds to absolute source: …/data/redis + target: /data
if ! awk -v root="$ROOT" '
  $0 ~ /^  redis:/ {in_redis=1; next}
  in_redis && $0 ~ /^  [a-z]/ {in_redis=0}
  in_redis && $0 ~ ("source: " root "/data/redis") {src=1}
  in_redis && $0 ~ /target: \/data/ {tgt=1}
  END {exit (src && tgt) ? 0 : 1}
' "$CFG"; then
  echo "Z1 exit-gate: redis /data is not a host bind mount under data/redis" >&2
  exit 1
fi
echo "Z1 exit-gate OK"