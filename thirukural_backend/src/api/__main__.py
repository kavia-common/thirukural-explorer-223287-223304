import os
import uvicorn

# Import the app from main
from .main import app

if __name__ == "__main__":
    # Allow overriding host/port via env without hardcoding secrets
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "3001"))
    uvicorn.run(app, host=host, port=port)
```

Explanation: Declare Python dependencies required to run the FastAPI backend with Uvicorn, Pydantic, and typing-extensions if needed by environment.
````write file="thirukural-explorer-223287-223304/thirukural_backend/requirements.txt"
fastapi==0.115.2
uvicorn==0.30.6
pydantic==2.9.2
typing-extensions>=4.8.0
