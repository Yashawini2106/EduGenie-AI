"""Shared, lazily-created Gemini client and text-generation helper."""

import os
from functools import lru_cache

from google import genai


@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Copy .env.example to .env and add your key.")
    return genai.Client(api_key=api_key)


def generate_text(prompt: str, *, temperature: float = 0.4) -> str:
    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    response = get_client().models.generate_content(
        model=model,
        contents=prompt,
        config={"temperature": temperature},
    )
    result = (response.text or "").strip()
    if not result:
        raise RuntimeError("Gemini returned an empty response. Please try again.")
    return result
