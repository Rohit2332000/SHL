import os
from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

TOP_K = int(os.getenv("TOP_K", 10))


API_TITLE = "SHL Assessment Recommender"
API_VERSION = "1.0"