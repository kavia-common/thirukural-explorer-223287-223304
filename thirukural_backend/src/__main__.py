import os
import uvicorn

# Import the FastAPI app from the API package
from api.main import app

if __name__ == "__main__":
    # PUBLIC_INTERFACE
    def run() -> None:
        """Entrypoint to start the FastAPI app via `python -m src`.

        Binds to HOST:PORT (defaults HOST=0.0.0.0, PORT=3001).
        """
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "3001"))
        # Start the Uvicorn server with the imported app instance
        uvicorn.run(app, host=host, port=port)

    run()
