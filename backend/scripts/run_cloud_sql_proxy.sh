#!/usr/bin/env zsh
set -euo pipefail

# Runs Cloud SQL Auth Proxy locally using environment variables.
# Requirements:
# - cloud-sql-proxy binary in ../
# - INSTANCE_CONNECTION_NAME set (project:region:instance)
# - GOOGLE_APPLICATION_CREDENTIALS pointing to service account JSON
# - DB_LOCAL_PORT set or defaults to 3307

SCRIPT_DIR=${0:a:h}
BACKEND_DIR=${SCRIPT_DIR:h}
PROXY_BIN="${BACKEND_DIR}/cloud-sql-proxy"

: ${INSTANCE_CONNECTION_NAME:?"INSTANCE_CONNECTION_NAME is required (e.g. project:region:instance)"}
: ${GOOGLE_APPLICATION_CREDENTIALS:?"GOOGLE_APPLICATION_CREDENTIALS must point to a service account JSON key"}
DB_LOCAL_PORT=${DB_LOCAL_PORT:-3307}

if [[ ! -x "$PROXY_BIN" ]]; then
  echo "cloud-sql-proxy not found at $PROXY_BIN or not executable."
  echo "Download from GitHub releases and place it at: $PROXY_BIN"
  exit 1
fi

echo "Starting Cloud SQL Proxy on 127.0.0.1:${DB_LOCAL_PORT} for ${INSTANCE_CONNECTION_NAME}"
"$PROXY_BIN" \
  --address 127.0.0.1 \
  --port "$DB_LOCAL_PORT" \
  --credentials-file "$GOOGLE_APPLICATION_CREDENTIALS" \
  "$INSTANCE_CONNECTION_NAME"