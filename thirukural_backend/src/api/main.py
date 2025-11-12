from __future__ import annotations

import json
import os
import random
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.models import ThirukuralOut, AnalyzeKuralIn, AnalyzeKuralOut
from src.api.ai_service import analyze_kural_for_user

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
    """Load the thirukural dataset from JSON, normalizing to the stable API shape.

    Supports both:
    - Old shape: { "number", "kural", "translation", "section"?, "chapter"? }
    - New shape: { "Number", "Line1", "Line2", "Translation", "explanation"?, "couplet"?, ... }

    Mapping rules:
    - number  <- Number (int) OR number (int)
    - kural   <- (Line1 + "\n" + Line2) OR kural
    - translation <- Translation OR couplet OR explanation
    - section, chapter are optional passthrough if present
    """
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

    def _get_number(obj: Dict[str, Any]) -> Any:
        # Prefer new schema "Number", fallback to old "number"
        num = obj.get("Number", obj.get("number"))
        # Try convert numeric strings safely
        if isinstance(num, str):
            if num.isdigit():
                return int(num)
            try:
                return int(float(num))
            except Exception:
                return None
        return num

    def _get_kural(obj: Dict[str, Any]) -> str | None:
        # Prefer composed Tamil lines if present
        line1 = obj.get("Line1")
        line2 = obj.get("Line2")
        if isinstance(line1, str) and isinstance(line2, str):
            composed = f"{line1.strip()}\n{line2.strip()}"
            if composed.strip():
                return composed
        # Fallback to existing "kural" if present
        k = obj.get("kural")
        return k if isinstance(k, str) and k.strip() else None

    def _get_translation(obj: Dict[str, Any]) -> str | None:
        # Priority: Translation -> couplet -> explanation
        for key in ("Translation", "couplet", "explanation", "translation"):
            val = obj.get(key)
            if isinstance(val, str) and val.strip():
                return val.strip()
        return None

    for item in data:
        if not isinstance(item, dict):
            continue

        number = _get_number(item)
        kural = _get_kural(item)
        translation = _get_translation(item)

        # Validate required fields
        if not isinstance(number, int) or not isinstance(kural, str) or not isinstance(translation, str):
            continue

        # Optional metadata if present
        section = item.get("section")
        chapter = item.get("chapter")
        # Coerce non-strings to None for optional fields
        section = section if isinstance(section, str) else None
        chapter = chapter if isinstance(chapter, str) else None

        normalized.append(
            {
                "number": number,
                "kural": kural,
                "translation": translation,
                "section": section,
                "chapter": chapter,
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


# PUBLIC_INTERFACE
@app.post(
    "/api/v1/thirukural/analyze",
    response_model=AnalyzeKuralOut,
    tags=["Thirukural"],
    summary="Analyze a Thirukural (AI placeholder)",
    description=(
        "Accepts a Thirukural (number, Tamil text, and English translation) and returns a mock, "
        "deterministic explanation tailored for “Al Ayman” unless OpenAI is configured and external calls are enabled. "
        "Environment variables: OPENAI_API_KEY, OPENAI_MODEL (default 'gpt-5-nano'), DISABLE_EXTERNAL_CALLS (default 'true')."
    ),
)
def analyze_thirukural(payload: AnalyzeKuralIn) -> AnalyzeKuralOut:
    """
    Analyze a specific Thirukural and return an explanation.

    Parameters:
        payload (AnalyzeKuralIn): Contains number, kural (Tamil), and translation (English).

    Returns:
        AnalyzeKuralOut: Explanation tailored for “Al Ayman”, indicating whether an external AI call was made.

    Notes:
        The actual external OpenAI call is gated behind environment variables.
        If OPENAI_API_KEY is not provided or DISABLE_EXTERNAL_CALLS is true, a deterministic placeholder is returned.
    """
    try:
        result = analyze_kural_for_user(payload.dict(), user_name="Al Ayman")
        return AnalyzeKuralOut(**result)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve)) from ve
    except Exception:
        # Avoid leaking internal details
        raise HTTPException(status_code=500, detail="Unable to analyze the Kural at this time.")
