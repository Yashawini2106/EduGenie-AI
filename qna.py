from ai_client import generate_text


def answer_question(question: str) -> str:
    return generate_text(
        "You are EduGenie, a careful educational tutor. Answer the learner's question "
        "accurately and concisely. Use clear language, define technical terms, and say "
        "when you are uncertain.\n\nQuestion: " + question
    )
