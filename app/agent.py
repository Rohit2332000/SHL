import re
from typing import List, Dict

from app.guardrails import check_guardrails
from app.retriever import retriever


# =========================
# Helpers
# =========================

def has_role(text: str) -> bool:
    text = text.lower()

    role_keywords = [
        "developer", "engineer", "manager",
        "analyst", "scientist", "sales",
        "support", "consultant",
        "java", "python", "software"
    ]

    return any(r in text for r in role_keywords)


def has_seniority(text: str) -> bool:
    text = text.lower()

    seniority_keywords = [
        "intern", "junior", "entry",
        "mid", "mid-level", "senior",
        "lead", "principal", "architect",
        "associate"
    ]

    if any(s in text for s in seniority_keywords):
        return True

    if re.search(r"\b\d+\+?\s*(year|years|yrs|yr)\b", text):
        return True

    return False


def build_conversation_text(messages: List[Dict]) -> str:
    """
    Merge all user messages (stateless handling).
    """
    return " ".join(
        msg["content"]
        for msg in messages
        if msg["role"] == "user"
    )


# =========================
# Main Agent
# =========================

def process_chat(messages: List[Dict]) -> Dict:

    # -------------------------
    # Get full conversation text
    # -------------------------
    conversation_text = build_conversation_text(messages)

    latest_user_message = messages[-1]["content"]

    # -------------------------
    # 1. Guardrails
    # -------------------------
    allowed, reason = check_guardrails(latest_user_message)

    if not allowed:
        return {
            "reply": reason,
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------------
    # 2. Step 1: Need ROLE?
    # -------------------------
    if not has_role(conversation_text):
        return {
            "reply": "What role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------------
    # 3. Step 2: Need SENIORITY?
    # -------------------------
    if not has_seniority(conversation_text):
        return {
            "reply": "Sure. What is the seniority level for this role?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -------------------------
    # 4. Build retrieval query
    # -------------------------
    query = conversation_text

    retrieved = retriever.search(query, top_k=10)

    # -------------------------
    # 5. Build recommendations (STRICT SHL FORMAT)
    # -------------------------
    recommendations = []
    for item in retrieved[:5]:
        recommendations.append({
            "name": item.get("name", ""),
            "url": item.get("url", ""),
            "test_type": item.get("test_type", "")
        })

    # -------------------------
    # 6. Final response
    # -------------------------
    return {
        "reply": f"Got it. Here are {len(recommendations)} assessments that fit your requirements.",
        "recommendations": recommendations,
        "end_of_conversation": False
    }