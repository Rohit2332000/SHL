import re
from typing import Dict


COMPARE_KEYWORDS = [
    "compare",
    "difference",
    "vs",
    "versus",
    "better than"
]

REFINE_KEYWORDS = [
    "actually",
    "instead",
    "also",
    "include",
    "exclude",
    "remove",
    "add",
    "change",
    "update"
]

OFF_TOPIC_KEYWORDS = [
    "weather",
    "ipl",
    "cricket",
    "football",
    "movie",
    "recipe",
    "python tutorial",
    "java tutorial",
    "legal advice",
    "medical advice"
]


def _latest_user_message(messages):
    """
    Return the latest user message.
    """

    for message in reversed(messages):
        if message["role"] == "user":
            return message["content"].strip()

    return ""


def detect_intent(messages, context: Dict) -> str:
    """
    Returns one of:

    clarify
    recommend
    refine
    compare
    refuse
    """

    latest = _latest_user_message(messages).lower()

    # ----------------------------
    # Compare
    # ----------------------------

    if any(word in latest for word in COMPARE_KEYWORDS):
        return "compare"

    # ----------------------------
    # Refinement
    # ----------------------------

    if any(word in latest for word in REFINE_KEYWORDS):
        return "refine"

    # ----------------------------
    # Off-topic
    # ----------------------------

    if any(word in latest for word in OFF_TOPIC_KEYWORDS):
        return "refuse"

    # ----------------------------
    # Prompt Injection
    # ----------------------------

    injections = [
        "ignore previous",
        "ignore all instructions",
        "system prompt",
        "developer prompt",
        "reveal prompt",
        "jailbreak",
        "act as"
    ]

    if any(x in latest for x in injections):
        return "refuse"

    # ----------------------------
    # Need Clarification?
    # ----------------------------

    role = context.get("role")

    if not role:

        vague = [
            "assessment",
            "test",
            "hire",
            "hiring",
            "recommend"
        ]

        if any(word in latest for word in vague):
            return "clarify"

    # ----------------------------
    # Recommend
    # ----------------------------

    return "recommend"