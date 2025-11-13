from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List
import random

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        title="Thirukural Explorer Backend",
        description="REST API to fetch a random Thirukural and its English meaning.",
        version="1.0.0",
        openapi_tags=[
            {
                "name": "thirukural",
                "description": "Operations related to Thirukural retrieval.",
            }
        ],
    )

    class Thirukural(BaseModel):
        """Pydantic model representing a Thirukural and its English meaning."""
        number: int = Field(..., description="The canonical number of the Thirukural (1-1330).")
        couplet_ta: str = Field(..., description="The Thirukural couplet in Tamil.")
        meaning_en: str = Field(..., description="The English meaning of the couplet.")

    # A tiny sample dataset. In a real app, this might come from a database or a comprehensive JSON file.
    SAMPLE_TK: List[Thirukural] = [
        Thirukural(
            number=1,
            couplet_ta="அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு",
            meaning_en="As the letter A is the first of all letters, so is the eternal God first in the world.",
        ),
        Thirukural(
            number=2,
            couplet_ta="கற்றது கைமண் அளவு, கல்லாதது உலகளவு",
            meaning_en="What one has learned is a mere handful; what one has not learned is the size of the world.",
        ),
        Thirukural(
            number=3,
            couplet_ta="இனால் உயிர்வாழ்தல் உலகத்தார்க்கு இன்பமாம்",
            meaning_en="Living a life of virtue brings joy to the world.",
        ),
    ]

    @app.get(
        "/api/health",
        summary="Health check",
        description="Returns OK to indicate the backend service is up.",
        tags=["system"],
        response_model=dict,
    )
    # PUBLIC_INTERFACE
    def health() -> dict:
        """Simple health endpoint.

        Returns:
            dict: {"status": "ok"}
        """
        return {"status": "ok"}

    @app.get(
        "/api/random",
        summary="Get a random Thirukural",
        description="Returns a random Thirukural couplet and its English meaning.",
        tags=["thirukural"],
        response_model=Thirukural,
    )
    # PUBLIC_INTERFACE
    def get_random_thirukural() -> Thirukural:
        """Return a random Thirukural entry from the sample dataset.

        Returns:
            Thirukural: A random Thirukural object containing number, couplet in Tamil, and English meaning.
        """
        return random.choice(SAMPLE_TK)

    # Add a help route describing WebSocket usage if present (none here), per docs requirements
    @app.get(
        "/api/docs/websocket",
        summary="WebSocket usage help",
        description="This backend currently does not expose WebSocket endpoints.",
        tags=["system"],
        response_model=dict,
    )
    # PUBLIC_INTERFACE
    def websocket_help() -> dict:
        """WebSocket usage doc stub for API completeness."""
        return {"websocket": "not_available"}

    return app


# Expose the FastAPI app for uvicorn
app = create_app()
