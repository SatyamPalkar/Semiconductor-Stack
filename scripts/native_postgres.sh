#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
pg_bin="${PG_BIN:-/opt/homebrew/opt/postgresql@17/bin}"
cluster="$PWD/data/native-postgres"
if [[ "${1:-}" == "stop" ]]; then
  "$pg_bin/pg_ctl" -D "$cluster" stop -m fast
  exit 0
fi
if [[ ! -f "$pg_bin/../share/postgresql@17/extension/vector.control" && ! -f /opt/homebrew/share/postgresql@17/extension/vector.control ]]; then
  echo 'Install pgvector for the selected PostgreSQL version first (see README).'
  exit 1
fi
if [[ ! -f "$cluster/PG_VERSION" ]]; then
  mkdir -p data
  "$pg_bin/initdb" -D "$cluster" -U semi_local --auth-local=trust --auth-host=scram-sha-256 --encoding=UTF8 --locale=C
fi
if ! "$pg_bin/pg_ctl" -D "$cluster" status >/dev/null 2>&1; then
  "$pg_bin/pg_ctl" -D "$cluster" -l "$cluster/server.log" -o '-p 55432 -h 127.0.0.1 -k /tmp -c shared_buffers=32MB -c max_connections=20' start
fi
if ! "$pg_bin/psql" -h /tmp -p 55432 -U semi_local -d postgres -Atc "SELECT 1 FROM pg_database WHERE datname='semiconductor'" | grep -q 1; then
  "$pg_bin/createdb" -h /tmp -p 55432 -U semi_local semiconductor
fi
echo 'Local-only database ready. Set DATABASE_URL=postgresql+psycopg://semi_local@/semiconductor?host=/tmp&port=55432 in the ignored .env.'
