#!/usr/bin/env bash
set -euo pipefail

# This script intentionally does NOT source venv/bin/activate.
# The environment running this script must have Python and the required packages installed.
export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-3001}"

chmod +x "$(realpath "$0")" >/dev/null 2>&1 || true

# Run uvicorn as a module per preview system expectation (foreground, no backgrounding)
python -m uvicorn src.api.main:app --host "${HOST}" --port "${PORT}"
