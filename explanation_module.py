"""Concept explanations using local LaMini-Flan-T5 when enabled, Gemini otherwise."""

import os
from functools import lru_cache


@lru_cache(maxsize=1)
def _load_local_pipeline():
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation mode needs the optional 'local' dependencies. "
            "Install requirements-local.txt, or set EXPLANATION_BACKEND=gemini."
        ) from exc
    model_name = os.getenv("EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
    return pipeline("text2text-generation", model=model_name, device=-1)


def explain_concept(topic: str, level: str = "beginner") -> str:
    prompt = (
        f"Explain {topic} to a {level} learner. Use plain language, a concrete example, "
        "and a short recap. Keep it accurate and under 180 words."
    )
    backend = os.getenv("EXPLANATION_BACKEND", "local").lower()
    if backend == "gemini":
        from ai_client import generate_text

        return generate_text("You are a patient teacher. " + prompt)
    if backend != "local":
        raise RuntimeError("EXPLANATION_BACKEND must be either 'local' or 'gemini'.")
    result = _load_local_pipeline()(prompt, max_new_tokens=220, do_sample=False)
    return result[0]["generated_text"].strip()
