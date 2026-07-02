# 🚀 SHL Conversational Assessment Recommender

An AI-powered conversational assistant that recommends **SHL Individual Test Solutions** through natural dialogue.

Instead of relying on keyword search or filters, this assistant understands hiring requirements conversationally, asks clarifying questions when needed, and recommends relevant SHL assessments grounded in the official SHL catalog.

Built as part of the **SHL AI Intern Take-Home Assignment**.

---

## ✨ Features

* 💬 Conversational assessment recommendation
* 🤖 Intelligent clarification before recommending
* 🔍 Semantic search using FAISS
* 🧠 Sentence Transformer embeddings
* ⚡ FastAPI REST API
* 🔒 Prompt injection protection
* 🚫 Off-topic request handling
* 📚 Recommendations strictly from the SHL catalog
* 🔄 Stateless conversation design
* 📦 SHL-compliant request/response schema

---

# Architecture

```
                User
                  │
                  ▼
           FastAPI (/chat)
                  │
                  ▼
          Conversation Parser
                  │
                  ▼
             Guardrails
                  │
                  ▼
          Requirement Checker
          (Role + Seniority)
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
 Clarification        Recommendation
                              │
                              ▼
                      FAISS Vector Search
                              │
                              ▼
                     SHL Assessment Catalog
                              │
                              ▼
                     Structured JSON Response
```

---

# Project Structure

```
SHL_FINAL/

│
├── app/
│   ├── main.py
│   ├── api.py
│   ├── agent.py
│   ├── retriever.py
│   ├── guardrails.py
│   ├── conversation.py
│   ├── prompts.py
│   ├── llm.py
│   ├── schemas.py
│   ├── config.py
│   └── intent.py
│
├── data/
│   ├── catalog.json
│   ├── faiss.index
│   ├── documents.pkl
│   └── build_index.py
│
├── .env
├── requirements.txt
├── run.py
└── README.md
```

---

# Tech Stack

* Python 3.11
* FastAPI
* FAISS
* Sentence Transformers
* Groq LLM
* HuggingFace Embeddings
* Pydantic
* Uvicorn

---

# Workflow

## 1. User starts conversation

Example:

> Hiring a Java developer.

---

## 2. Agent checks available information

If the role is missing:

```
What role are you hiring for?
```

If seniority is missing:

```
Sure. What is the seniority level for this role?
```

---

## 3. Enough information available

The assistant searches the SHL catalog using semantic retrieval.

---

## 4. Recommendations returned

Example response

```json
{
  "reply": "Got it. Here are 5 assessments that fit your requirements.",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/...",
      "test_type": "K"
    }
  ],
  "end_of_conversation": false
}
```

---

# API

## Health Check

```
GET /health
```

Response

```json
{
  "status": "ok"
}
```

---

## Chat

```
POST /chat
```

Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer"
    }
  ]
}
```

---

Response

```json
{
  "reply": "Sure. What is the seniority level for this role?",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

Second Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer"
    },
    {
      "role": "assistant",
      "content": "Sure. What is the seniority level for this role?"
    },
    {
      "role": "user",
      "content": "Mid-level with around 4 years experience"
    }
  ]
}
```

Response

```json
{
  "reply": "Got it. Here are 5 assessments that fit your requirements.",
  "recommendations": [
    {
      "name": "...",
      "url": "...",
      "test_type": "..."
    }
  ],
  "end_of_conversation": false
}
```

---

# Building the FAISS Index

```
python -m data.build_index
```

This command:

* Loads the SHL catalog
* Generates embeddings
* Builds the FAISS index
* Saves metadata for retrieval

---

# Running the Project

Install dependencies

```bash
pip install -r requirements.txt
```

Run the server

```bash
python run.py
```

or

```bash
uvicorn app.main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

# Design Decisions

### Stateless API

The server stores no conversation state.

Each `/chat` request contains the complete conversation history, making the application horizontally scalable and compliant with the assignment specification.

---

### Semantic Retrieval

Recommendations are generated using vector similarity search over the SHL catalog.

This enables retrieval based on meaning rather than exact keyword matching.

---

### Deterministic Conversation Flow

The assistant follows a simple and predictable workflow:

* Missing role → Ask for role
* Missing seniority → Ask for seniority
* Enough information → Recommend assessments

This avoids unnecessary ambiguity while keeping conversations efficient.

---

### Grounded Recommendations

Every recommendation returned by the API originates from the indexed SHL catalog.

The assistant never invents assessment names or URLs.

---

### Safety

The system includes guardrails to:

* reject prompt injection attempts
* refuse off-topic requests
* remain focused on SHL assessments

---

# Example Conversation

**User**

```
Hiring a Java developer
```

**Assistant**

```
Sure. What is the seniority level for this role?
```

**User**

```
Mid-level with 4 years experience
```

**Assistant**

```
Got it. Here are 5 assessments that fit your requirements.
```

---

# Future Improvements

* Hybrid retrieval (BM25 + FAISS)
* Metadata-aware ranking
* Better skill extraction
* Improved refinement handling
* Automatic evaluation using Recall@10
* Streaming responses
* Multi-language support

---

# Author

**Rohit Kumar Yadav**

AI Engineer | Machine Learning | Generative AI | FastAPI | RAG | LLM Applications

---

Built for the **SHL AI Intern Take-Home Assignment (2026)**.
