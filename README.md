# thirukural-explorer-223287-223304

## Backend (FastAPI)

Location: thirukural_backend/

Install dependencies (one of):
- pip install -r thirukural_backend/requirements.txt
- or: pip install .

Start (no venv activation required by script):
- bash thirukural_backend/start.sh
- or directly: uvicorn src.api.main:app --host 0.0.0.0 --port 3001

Health check:
- GET http://localhost:3001/api/health

Random Thirukural:
- GET http://localhost:3001/api/random