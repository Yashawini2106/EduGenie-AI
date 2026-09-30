from ai_client import generate_text


def summarize_text(text: str) -> str:
    return generate_text(
        "Summarize the educational passage below for quick revision. Preserve the central "
        "facts and important terms, remove repetition, and use clear concise language. "
        "Do not add unsupported facts.\n\nPassage:\n" + text,
        temperature=0.3,
    )
