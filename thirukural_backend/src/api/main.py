from __future__ import annotations

import json
import os
import random
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.models import ThirukuralOut

# Configure FastAPI app with metadata and tags for OpenAPI
app = FastAPI(
    title="Thirukural Backend API",
    description="API to serve random Thirukural couplets with English translations.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Health",
            "description": "Basic service health endpoints.",
        },
        {
            "name": "Thirukural",
            "description": "Endpoints related to Thirukural data.",
        },
    ],
)

# CORS configuration - permissive for demo; tighten in production as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load dataset once at module import (startup)
_DATASET: List[Dict[str, Any]] = []
_DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "thirukural.json")


def _load_dataset() -> List[Dict[str, Any]]:
    """Load the thirukural dataset from JSON with minimal validation and UTF-8 handling."""
    try:
        with open(_DATA_FILE_PATH, "r", encoding="utf-8") as f:
            data: Any = json.load(f)
    except FileNotFoundError as e:
        raise RuntimeError(f"Dataset file not found at {_DATA_FILE_PATH}") from e
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in dataset file: {_DATA_FILE_PATH}") from e

    if not isinstance(data, list):
        raise RuntimeError("Dataset must be a JSON array of objects")

    normalized: List[Dict[str, Any]] = []
    for idx, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            # Skip invalid entries but continue
            continue

        # Minimal shape validation
        number = item.get("number")
        kural = item.get("kural")
        translation = item.get("translation")

        if not isinstance(number, int) or not isinstance(kural, str) or not isinstance(translation, str):
            # Skip if required fields are missing or wrong types
            continue

        normalized.append(
            {
                "number": number,
                "kural": kural,
                "translation": translation,
                "section": item.get("section"),
                "chapter": item.get("chapter"),
            }
        )

    if not normalized:
        raise RuntimeError("No valid entries found in dataset after validation")

    return normalized


# Initialize dataset at import
_DATASET = _load_dataset()


@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Simple health check endpoint to verify service is running."""
    return {"message": "Healthy"}


# PUBLIC_INTERFACE
@app.get(
    "/api/v1/thirukural/random",
    response_model=ThirukuralOut,
    tags=["Thirukural"],
    summary="Get a random Thirukural",
    description="Returns a randomly selected Thirukural couplet with its English translation.",
)
def get_random_thirukural() -> ThirukuralOut:
    """
    Return a random Thirukural item from the embedded dataset.

    Returns:
        ThirukuralOut: A randomly selected Thirukural with Tamil text and English translation.

    Raises:
        HTTPException: 503 if the dataset is unavailable.
    """
    if not _DATASET:
        # Should not happen if startup load succeeded, but guard anyway
        raise HTTPException(status_code=503, detail="Dataset unavailable")

    item = random.choice(_DATASET)
    # Pydantic model will enforce the schema and types
    return ThirukuralOut(**item)
