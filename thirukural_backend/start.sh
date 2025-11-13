#!/usr/bin/env bash
set -euo pipefail

# This script intentionally does NOT source venv/bin/activate.
# It installs dependencies globally for the runtime environment if needed,
# then starts the FastAPI app using uvicorn as a module.

export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-3001}"

# Ensure script is executable (no-op safety)
chmod +x "$(realpath "$0")" >/dev/null 2>&1 || true

# Install dependencies if FastAPI is not available yet (idempotent and quick when cached)
if ! python -c "import fastapi" >/dev/null 2>&1; then
  echo "FastAPI not found. Installing dependencies from requirements.txt..."
  pip install --no-input --disable-pip-version-check -r "$(dirname "$0")/requirements.txt"
fi

# Start the app
exec python -m uvicorn src.api.main:app --host "${HOST}" --port "${PORT}"
