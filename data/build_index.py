import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import (
    CATALOG_PATH,
    DOCUMENTS_PATH,
    EMBEDDING_MODEL,
    FAISS_INDEX_PATH,
)


def build_search_text(item: dict) -> str:
    """
    Convert one catalog entry into searchable text.
    """

    sections = [
        item.get("name", ""),
        item.get("description", ""),
        " ".join(item.get("job_levels", [])),
        " ".join(item.get("languages", [])),
        " ".join(item.get("keys", [])),
        f"Duration: {item.get('duration', '')}",
        f"Remote: {item.get('remote', '')}",
        f"Adaptive: {item.get('adaptive', '')}",
    ]

    return "\n".join(filter(None, sections))


def main():

    print("Loading SHL catalog...")

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"Loaded {len(catalog)} assessments.")

    model = SentenceTransformer(EMBEDDING_MODEL)

    documents = []
    texts = []

    for assessment in catalog:

        search_text = build_search_text(assessment)

        texts.append(search_text)

        documents.append(
            {
                "name": assessment["name"],
                "url": assessment["link"],
                "test_type": ", ".join(assessment.get("keys", [])),
                "description": assessment.get("description", ""),
                "search_text": search_text,
                "metadata": assessment,
            }
        )

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    embeddings = embeddings.astype(np.float32)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    print("Saving FAISS index...")

    faiss.write_index(index, str(FAISS_INDEX_PATH))

    print("Saving documents...")

    with open(DOCUMENTS_PATH, "wb") as f:
        pickle.dump(documents, f)

    print("Done!")

    print(f"Index size : {index.ntotal}")
    print(f"Saved to    : {FAISS_INDEX_PATH}")
    print(f"Documents   : {DOCUMENTS_PATH}")


if __name__ == "__main__":
    main()