from typing import List, Literal, Optional
from pydantic import BaseModel


# =========================
# Input Schema (/chat)
# =========================

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# =========================
# Output Schema (/chat)
# =========================

class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str


class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool