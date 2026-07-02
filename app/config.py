from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# =========================
# Project Paths
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

CATALOG_PATH = DATA_DIR / "catalog.json"
FAISS_INDEX_PATH = DATA_DIR / "faiss.index"
DOCUMENTS_PATH = DATA_DIR / "documents.pkl"

# =========================
# Groq
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "llama-3.3-70b-versatile"
)

# =========================
# Embeddings
# =========================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

# =========================
# Retrieval
# =========================

TOP_K = int(os.getenv("TOP_K", "10"))

# =========================
# FastAPI
# =========================

API_TITLE = "SHL Conversational Assessment Recommender"

API_VERSION = "1.0.0"
