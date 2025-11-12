import os
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class AIConfig(BaseModel):
    """Configuration for AI integration derived from environment variables."""
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key from OPENAI_API_KEY env var.")
    openai_model: str = Field(default="gpt-5-nano", description="OpenAI model name from OPENAI_MODEL env var.")
    disable_external_calls: bool = Field(default=False, description="If true, skip calling external AI APIs.")

    @classmethod
    def from_env(cls) -> "AIConfig":
        """Build configuration from environment variables safely."""
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY") or None,
            openai_model=os.getenv("OPENAI_MODEL") or "gpt-5-nano",
            disable_external_calls=(os.getenv("DISABLE_EXTERNAL_CALLS", "true").lower() == "true"),
        )


# PUBLIC_INTERFACE
def analyze_kural_for_user(payload: Dict[str, Any], user_name: str = "Al Ayman") -> Dict[str, Any]:
    """
    Analyze a Thirukural for a given user and provide an explanation.

    This function is structured to optionally call an external LLM provider (OpenAI) if enabled.
    By default, or when OPENAI_API_KEY is missing or DISABLE_EXTERNAL_CALLS=true, it returns
    a deterministic placeholder response that is stable for tests and local development.

    Args:
        payload: Dictionary containing 'number' (int), 'kural' (str), 'translation' (str).
        user_name: Name of the intended audience to tailor the response, default "Al Ayman".

    Returns:
        A dictionary containing:
            - number: int
            - kural: str
            - translation: str
            - explanation: str
            - model: str (model used or 'placeholder')
            - external_call_used: bool
    """
    cfg = AIConfig.from_env()

    number = payload.get("number")
    kural = payload.get("kural", "").strip()
    translation = payload.get("translation", "").strip()

    # Guard/validation (lightweight - main validation is at the API layer)
    if not isinstance(number, int) or not kural or not translation:
        raise ValueError("Invalid payload. Expecting {number:int, kural:str, translation:str}.")

    # Gate external calls
    use_external = bool(cfg.openai_api_key) and not cfg.disable_external_calls

    if not use_external:
        # Deterministic placeholder response for local/testing
        explanation = (
            f"Hi {user_name}, here is a concise reflection tailored for you.\n\n"
            f"Kural #{number} highlights a timeless principle. In simple terms: {translation}\n\n"
            f"Why it matters for you: Focus on the core value behind these lines—"
            f"consistency, humility, and purpose. Consider one small, practical step today "
            f"that aligns with this insight.\n\n"
            f"Summary: The Kural encourages living by foundational virtues. Even a small action "
            f"done consistently will compound meaningfully over time."
        )
        return {
            "number": number,
            "kural": kural,
            "translation": translation,
            "explanation": explanation,
            "model": "placeholder",
            "external_call_used": False,
        }

    # Placeholder structure for a future OpenAI call (not executed in CI by default).
    # The actual call is intentionally omitted to avoid external dependency during tests.
    # Example structure (commented):
    # from openai import OpenAI
    # client = OpenAI(api_key=cfg.openai_api_key)
    # prompt = f"Explain Thirukural #{number} to {user_name}.\nTamil:\n{kural}\nMeaning:\n{translation}\nProvide a concise, practical explanation."
    # resp = client.chat.completions.create(
    #     model=cfg.openai_model,
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.2,
    #     max_tokens=250,
    # )
    # ai_text = resp.choices[0].message.content.strip()

    ai_text = (
        f"(Simulated) Explanation for {user_name} via {cfg.openai_model}: "
        f"{translation} — Focus on practical application in daily habits."
    )
    return {
        "number": number,
        "kural": kural,
        "translation": translation,
        "explanation": ai_text,
        "model": cfg.openai_model,
        "external_call_used": True,
    }
