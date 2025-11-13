# thirukural-explorer-223287-223304

## Backend (FastAPI)

Location: thirukural_backend/

Install dependencies (one of):
- pip install -r thirukural_backend/requirements.txt
- or: pip install .
- Note: start.sh will auto-install requirements if FastAPI is not found.

Start (no venv activation required by script):
- Recommended: bash thirukural_backend/start.sh
  - This script ensures dependencies are installed and starts Uvicorn binding to 0.0.0.0:3001.
- Direct Uvicorn: python -m uvicorn src.api.main:app --host 0.0.0.0 --port 3001
- Module fallback (if preview runner ignores start.sh):
  - python -m src.api
  - or: python -m src

Notes:
- A no-op venv activation shim exists at thirukural_backend/venv/bin/activate to avoid failures in environments that attempt `source venv/bin/activate`.
- The app binds to HOST and PORT env vars (defaults HOST=0.0.0.0, PORT=3001).

Health checks:
- GET http://localhost:3001/api/health
- GET http://localhost:3001/health

Random Thirukural:
- GET http://localhost:3001/api/random