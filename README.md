# EduGenie

EduGenie is a small learning assistant following the attached project brief. It includes question answering, simple explanations, three-question quizzes with answer feedback, passage summaries, and personalized learning paths. The web app uses FastAPI, Jinja2, and plain HTML/CSS/JavaScript.

## Requirements

- Python 3.10 or newer
- A Gemini API key for Q&A, quiz generation, summaries, and learning paths
- Optional: enough disk space and memory for LaMini-Flan-T5-783M, used by the local explanation mode

The brief names Gemini 1.5 Pro. Since that model reference is outdated, the app uses the configurable `GEMINI_MODEL` setting and defaults to `gemini-3.8-flash`. Confirm model availability for your Google AI Studio project; change the setting if needed.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env`, add your API key, then run:

```bash
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000>. The health endpoint is <http://127.0.0.1:8000/health> and the interactive API docs are at <http://127.0.0.1:8000/docs>.

## Explanation model

By default, `/explain` uses `MBZUAI/LaMini-Flan-T5-783M`, loaded on the first request. Install the optional CPU/local dependencies with `pip install -r requirements-local.txt`. The first request downloads model weights and may take several minutes; the model requires substantial memory and disk space.

To avoid the local model, set `EXPLANATION_BACKEND=gemini` in `.env`. This uses the configured Gemini model for explanations too and only requires the base dependencies.

## API routes

| Method | Route | Request JSON | Response |
|---|---|---|---|
| POST | `/qa` | `{"question":"Why is the sky blue?"}` | `{"answer":"..."}` |
| POST | `/explain` | `{"topic":"Photosynthesis","level":"beginner"}` | `{"explanation":"..."}` |
| POST | `/quiz` | `{"text":"Study passage..."}` | `{"questions":[...]}` |
| POST | `/summarize` | `{"text":"Long passage..."}` | `{"summary":"..."}` |
| POST | `/learn/recommendations` | `{"topic":"SQL","level":"beginner","weeks":4}` | `{"learning_path":"..."}` |

Text inputs are capped at 20,000 characters (5,000 for question/topic fields). Keep API keys in `.env`; never commit that file or expose the key in browser code.
