from typing import Tuple

# ---------------------------
# Off-topic keywords
# ---------------------------

OFF_TOPIC_KEYWORDS = {
    "weather",
    "ipl",
    "cricket",
    "football",
    "movie",
    "netflix",
    "recipe",
    "bitcoin",
    "stock market",
    "python tutorial",
    "java tutorial",
    "travel",
    "hotel",
    "restaurant",
    "music",
    "song"
}

# ---------------------------
# Restricted domains
# ---------------------------

RESTRICTED_TOPICS = {
    "legal",
    "medical",
    "diagnosis",
    "disease",
    "lawyer",
    "court",
    "medicine",
    "treatment"
}

# ---------------------------
# Prompt Injection Patterns
# ---------------------------

PROMPT_INJECTIONS = [
    "ignore previous instructions",
    "ignore all instructions",
    "forget previous instructions",
    "system prompt",
    "developer prompt",
    "hidden prompt",
    "reveal prompt",
    "show your instructions",
    "act as",
    "jailbreak",
    "bypass",
    "override",
    "pretend to be",
]

# ---------------------------
# Allowed SHL keywords
# ---------------------------

SHL_KEYWORDS = [
    "assessment",
    "test",
    "hiring",
    "candidate",
    "job",
    "developer",
    "engineer",
    "manager",
    "sales",
    "java",
    "python",
    "leadership",
    "personality",
    "cognitive",
    "opq",
    "verify",
    "gsa",
    "assessment recommendation"
]


def _contains(text: str, keywords) -> bool:
    """
    Case-insensitive keyword matching.
    """
    text = text.lower()

    return any(keyword.lower() in text for keyword in keywords)


def check_guardrails(message: str) -> Tuple[bool, str]:
    """
    Returns:
        (allowed, reason)
    """

    text = message.lower().strip()

    # ---------------------------
    # Prompt Injection
    # ---------------------------

    if _contains(text, PROMPT_INJECTIONS):
        return (
            False,
            (
                "I can only assist with recommending and comparing "
                "SHL assessments. I can't reveal or ignore my instructions."
            ),
        )

    # ---------------------------
    # Restricted Topics
    # ---------------------------

    if _contains(text, RESTRICTED_TOPICS):
        return (
            False,
            (
                "I can only assist with SHL assessment recommendations "
                "and comparisons."
            ),
        )

    # ---------------------------
    # Clearly Off-topic
    # ---------------------------

    if _contains(text, OFF_TOPIC_KEYWORDS):
        return (
            False,
            (
                "I'm designed to help only with SHL assessment selection "
                "and comparison."
            ),
        )

    # ---------------------------
    # Otherwise allow
    # ---------------------------

    return True, ""