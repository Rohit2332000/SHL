# =========================
# 1. Conversation Extraction Prompt
# =========================

CONTEXT_EXTRACTION_PROMPT = """
You are an expert HR assessment assistant.

Extract structured hiring requirements from the conversation.

Return ONLY valid JSON.

Fields:
- role (string or null)
- seniority (string or null)
- skills (list of strings)
- must_have (list of strings)
- nice_to_have (list of strings)
- assessment_preference (string or null)

Conversation:
{conversation}

Rules:
- Do NOT guess missing information.
- If not mentioned, use null or empty list.
- Keep output strictly JSON.
"""


# =========================
# 2. Recommendation Prompt
# =========================

RECOMMENDATION_PROMPT = """
You are an SHL assessment expert.

You will be given:
1. Job role context
2. Retrieved SHL assessments

Your task:
- Select best matching assessments
- Explain briefly why each fits

IMPORTANT RULES:
- Only use provided assessments
- Do NOT invent new tests
- Do NOT hallucinate URLs

Context:
{context}

Assessments:
{docs}

Return a structured explanation.
"""


# =========================
# 3. Comparison Prompt
# =========================

COMPARISON_PROMPT = """
You are comparing SHL assessments.

You will be given two or more assessments from the catalog.

Rules:
- Only use provided data
- Be factual
- Focus on differences

Assessments:
{docs}

User Query:
{query}

Return:
- differences
- use cases
- recommendation if applicable
"""


# =========================
# 4. Clarification Prompt
# =========================

CLARIFY_PROMPT = """
You are an HR assistant helping choose SHL assessments.

The user request is incomplete.

Ask ONE short clarifying question.

User message:
{message}

Rules:
- Be concise
- Ask only one question
- Focus on missing hiring details
"""