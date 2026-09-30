"""Generate validated multiple-choice quizzes."""

import json
import re

from ai_client import generate_text


def _parse_json(text: str):
    cleaned = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text, flags=re.I)
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\[[\s\S]*\]", cleaned)
        if not match:
            raise ValueError("The model did not return valid quiz JSON. Please try again.")
        value = json.loads(match.group(0))
    if isinstance(value, dict):
        value = value.get("questions", [])
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError("The quiz response must contain exactly three questions.")
    normalized = []
    for index, item in enumerate(value, start=1):
        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        answer = str(item.get("answer", item.get("correct_answer", ""))).strip()
        if not question or not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"Question {index} must have text and exactly four options.")
        options = [str(option).strip() for option in options]
        if answer not in options and answer.upper() in {"A", "B", "C", "D"}:
            answer = options[ord(answer.upper()) - ord("A")]
        if answer not in options:
            raise ValueError(f"Question {index} has an answer that is not one of its options.")
        normalized.append({"question": question, "options": options, "answer": answer})
    return normalized


def generate_quiz(text: str):
    prompt = f"""Create exactly 3 distinct multiple-choice questions based only on the learning material below.
Each question must have exactly 4 concise options and one unambiguous correct answer.
Return only a JSON array. Every item must have this shape:
{{"question":"...","options":["...","...","...","..."],"answer":"exact text of correct option"}}

Learning material:
{text}
"""
    return _parse_json(generate_text(prompt, temperature=0.2))
