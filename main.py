"""EduGenie: a small educational assistant built with FastAPI."""

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(title="EduGenie", version="1.0.0", description="A Gemini-powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000)


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: str = Field(default="beginner", max_length=40)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=5000)
    level: str = Field(default="beginner", max_length=40)
    weeks: int = Field(default=4, ge=1, le=52)


def service_error(exc: Exception) -> HTTPException:
    return HTTPException(status_code=503, detail=str(exc))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QuestionRequest):
    try:
        return {"answer": answer_question(payload.question)}
    except Exception as exc:
        raise service_error(exc) from exc


@app.post("/explain")
async def explain(payload: ExplainRequest):
    try:
        return {"explanation": explain_concept(payload.topic, payload.level)}
    except Exception as exc:
        raise service_error(exc) from exc


@app.post("/quiz")
async def quiz(payload: TextRequest):
    try:
        return {"questions": generate_quiz(payload.text)}
    except Exception as exc:
        raise service_error(exc) from exc


@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        return {"summary": summarize_text(payload.text)}
    except Exception as exc:
        raise service_error(exc) from exc


@app.post("/learn/recommendations")
async def recommendations(payload: LearningPathRequest):
    try:
        return {"learning_path": get_learning_recommendations(payload.topic, payload.level, payload.weeks)}
    except Exception as exc:
        raise service_error(exc) from exc
