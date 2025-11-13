import os
import uvicorn

# Import the app from main
from .main import app

if __name__ == "__main__":
    # Allow overriding host/port via env without hardcoding secrets
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "3001"))
    uvicorn.run(app, host=host, port=port)
