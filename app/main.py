from fastapi import FastAPI

from app.api import router
from app.config import API_TITLE, API_VERSION

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "SHL Conversational Assessment Recommender API",
        "health": "/health",
        "chat": "/chat",
    }