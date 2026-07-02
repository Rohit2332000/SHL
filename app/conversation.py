from typing import Dict, List
from app.llm import llm
from app.prompts import CONTEXT_EXTRACTION_PROMPT


def format_conversation(messages: List[Dict]) -> str:
    """
    Convert chat history into readable text for LLM
    """

    formatted = []

    for msg in messages:
        role = msg["role"].upper()
        content = msg["content"]
        formatted.append(f"{role}: {content}")

    return "\n".join(formatted)


def extract_context(messages: List[Dict]) -> Dict:
    """
    Uses LLM to extract structured hiring requirements
    """

    conversation_text = format_conversation(messages)

    prompt = CONTEXT_EXTRACTION_PROMPT.format(
        conversation=conversation_text
    )

    response = llm.generate_json(
        system_prompt="You are a strict JSON extractor.",
        user_prompt=prompt
    )

    # ---------------------------
    # Safety fallback (important for SHL eval)
    # ---------------------------

    if not isinstance(response, dict):
        response = {}

    return {
        "role": response.get("role"),
        "seniority": response.get("seniority"),
        "skills": response.get("skills", []),
        "must_have": response.get("must_have", []),
        "nice_to_have": response.get("nice_to_have", []),
        "assessment_preference": response.get("assessment_preference")
    }