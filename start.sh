#!/usr/bin/env bash
set -euo pipefail

# Run migrations and start the app.
if command -v alembic >/dev/null 2>&1; then
  echo "Running Alembic migrations..."
  alembic upgrade head
else
  echo "Alembic not installed in image; skipping migrations"
fi

echo "Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
