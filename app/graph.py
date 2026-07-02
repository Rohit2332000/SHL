from typing import TypedDict, List, Dict

from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    messages: List[Dict]
    intent: str
    requirements: dict
    retrieved_docs: list
    reply: str
    recommendations: list
    end_of_conversation: bool


# ---------------------------
# Node 1 : Analyze Conversation
# ---------------------------

def analyze_node(state: AgentState):

    messages = state["messages"]

    latest_user = ""

    for msg in reversed(messages):
        if msg["role"] == "user":
            latest_user = msg["content"]
            break

    state["latest_user"] = latest_user

    return state


# ---------------------------
# Node 2 : Intent Detection
# ---------------------------

def detect_intent_node(state: AgentState):

    text = state["latest_user"].lower()

    if "compare" in text:
        state["intent"] = "compare"

    elif "actually" in text or "instead" in text:
        state["intent"] = "refine"

    elif (
        "assessment" in text
        and len(text.split()) < 5
    ):
        state["intent"] = "clarify"

    else:
        state["intent"] = "recommend"

    return state


# ---------------------------
# Router
# ---------------------------

def router(state: AgentState):

    return state["intent"]


# ---------------------------
# Clarify
# ---------------------------

def clarify_node(state: AgentState):

    state["reply"] = "What role are you hiring for?"

    state["recommendations"] = []

    state["end_of_conversation"] = False

    return state


# ---------------------------
# Recommend Placeholder
# ---------------------------

def recommend_node(state: AgentState):

    # We'll connect FAISS here later

    state["reply"] = "Recommendation node executed."

    state["recommendations"] = []

    state["end_of_conversation"] = True

    return state


# ---------------------------
# Compare Placeholder
# ---------------------------

def compare_node(state: AgentState):

    state["reply"] = "Comparison node executed."

    state["recommendations"] = []

    state["end_of_conversation"] = False

    return state


# ---------------------------
# Build Graph
# ---------------------------

builder = StateGraph(AgentState)

builder.add_node("analyze", analyze_node)
builder.add_node("detect", detect_intent_node)
builder.add_node("clarify", clarify_node)
builder.add_node("recommend", recommend_node)
builder.add_node("compare", compare_node)

builder.set_entry_point("analyze")

builder.add_edge("analyze", "detect")

builder.add_conditional_edges(
    "detect",
    router,
    {
        "clarify": "clarify",
        "recommend": "recommend",
        "refine": "recommend",
        "compare": "compare",
    },
)

builder.add_edge("clarify", END)
builder.add_edge("recommend", END)
builder.add_edge("compare", END)

graph = builder.compile()