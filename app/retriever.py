import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import FAISS_INDEX_PATH, DOCUMENTS_PATH, EMBEDDING_MODEL, TOP_K


class Retriever:
    def __init__(self):
        # Load embedding model
        self.model = SentenceTransformer(EMBEDDING_MODEL)

        # Load FAISS index
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))

        # Load documents (metadata for each vector)
        with open(DOCUMENTS_PATH, "rb") as f:
            self.documents = pickle.load(f)

    # ---------------------------
    # Embed text
    # ---------------------------
    def embed(self, text: str):
        vector = self.model.encode([text])[0]
        return np.array(vector).astype("float32")

    # ---------------------------
    # Search FAISS
    # ---------------------------
    def search(self, query: str, top_k: int = TOP_K):
        query_vector = self.embed(query).reshape(1, -1)

        scores, indices = self.index.search(query_vector, top_k)

        results = []

        for idx in indices[0]:
            if idx == -1:
                continue

            doc = self.documents[idx]

            results.append({
                "name": doc.get("name"),
                "url": doc.get("url"),
                "test_type": doc.get("test_type"),
                "description": doc.get("description", "")
            })

        return results


retriever = Retriever()