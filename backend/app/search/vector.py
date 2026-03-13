import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss


class VectorSearch:

    def __init__(self):

        with open("data/processed/ingested.jsonl") as f:
            docs = [json.loads(line) for line in f]

        self.docs = docs
        texts = [doc["text"] for doc in docs]

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        embeddings = self.model.encode(texts)

        self.index = faiss.IndexFlatL2(len(embeddings[0]))
        self.index.add(np.array(embeddings).astype("float32"))

    def search(self, query, top_k=5):

        query_embedding = self.model.encode([query]).astype("float32")

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for i, idx in enumerate(indices[0]):

            doc = self.docs[idx]

            results.append({
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "score": float(scores[0][i])
            })

        return results