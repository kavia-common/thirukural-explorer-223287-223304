# thirukural-explorer-223287-223304

## Backend (FastAPI)

Location: thirukural_backend/

Install dependencies (one of):
- pip install -r thirukural_backend/requirements.txt
- or: pip install .
- Note: start.sh will auto-install requirements if FastAPI is not found.

Start (no venv activation required by script):
- bash thirukural_backend/start.sh
- or directly: python -m uvicorn src.api.main:app --host 0.0.0.0 --port 3001

Health checks:
- GET http://localhost:3001/api/health
- GET http://localhost:3001/health

Random Thirukural:
- GET http://localhost:3001/api/random