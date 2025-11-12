from typing import Optional
from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
class ThirukuralOut(BaseModel):
    """Pydantic model representing a Thirukural item for API responses."""
    number: int = Field(..., description="The unique number of the Thirukural couplet (1..1330).")
    kural: str = Field(..., description="The original Thirukural text in Tamil.")
    translation: str = Field(..., description="The English meaning/translation of the Thirukural.")
    section: Optional[str] = Field(None, description="High-level section (e.g., அறத்துப்பால், பொருட்பால், காமத்துப்பால்).")
    chapter: Optional[str] = Field(None, description="Chapter name within the section (optional).")


# PUBLIC_INTERFACE
class AnalyzeKuralIn(BaseModel):
    """Input payload for analyzing a specific Thirukural."""
    number: int = Field(..., description="Thirukural number being analyzed.")
    kural: str = Field(..., description="Original Tamil text of the Kural (can be two lines).")
    translation: str = Field(..., description="English meaning/translation of the Kural.")


# PUBLIC_INTERFACE
class AnalyzeKuralOut(BaseModel):
    """Output for AI analysis of a Thirukural."""
    number: int = Field(..., description="Thirukural number analyzed.")
    kural: str = Field(..., description="Original Tamil text of the Kural.")
    translation: str = Field(..., description="English meaning/translation of the Kural.")
    explanation: str = Field(..., description="AI-generated or placeholder explanation tailored for the user.")
    model: str = Field(..., description="Model used for generation or 'placeholder'.")
    external_call_used: bool = Field(..., description="Whether an external AI API call was made.")
