from ai_client import generate_text


def get_learning_recommendations(topic: str, level: str = "beginner", weeks: int = 4) -> str:
    prompt = f"""Create a practical {weeks}-week learning path for: {topic}
Learner's current level: {level}.
Organize it from foundations toward more advanced material. For each week, give:
- goals and topics
- a short practice task
- suggested resource types (documentation, article, video, or book) and reputable named resources when known
Finish with a small project and a way to check understanding. Do not invent specific URLs.
Use readable Markdown and keep the plan focused."""
    return generate_text(prompt, temperature=0.5)
