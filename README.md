# thirukural-explorer-223287-223304

## Backend: AI Analyzer Endpoint (Placeholder)

A new endpoint is available in the FastAPI backend:

- POST /api/v1/thirukural/analyze
  - Body (JSON):
    - number: integer
    - kural: string (Tamil)
    - translation: string (English)
  - Response: JSON containing number, kural, translation, explanation, model, external_call_used

Behavior:
- By default, the service returns a deterministic placeholder explanation tailored for “Al Ayman”.
- To enable real LLM calls, set environment variables:
  - OPENAI_API_KEY=<your key>
  - OPENAI_MODEL=<model name, default 'gpt-5-nano'>
  - DISABLE_EXTERNAL_CALLS=false
- If OPENAI_API_KEY is missing or DISABLE_EXTERNAL_CALLS=true, no external request is made.

OpenAPI docs are available at /docs when the backend is running.

Example request:
```json
{
  "number": 1,
  "kural": "அகர முதல எழுத்தெல்லாம்\nஆதி பகவன் முதற்றே உலகு",
  "translation": "As the letter A is the first of all letters, so is the Eternal God first in the world."
}
```