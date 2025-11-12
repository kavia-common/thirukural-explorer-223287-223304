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
