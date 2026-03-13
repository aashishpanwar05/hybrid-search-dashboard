from rank_bm25 import BM25L
import json


class BM25Search:

    def __init__(self):

        with open("data/processed/ingested.jsonl") as f:
            docs = [json.loads(line) for line in f]

        self.docs = docs
        # Convert to lowercase for case-insensitive matching
        self.corpus = [doc["text"].lower().split() for doc in docs]

        self.bm25 = BM25L(self.corpus)

    def search(self, query, top_k=5):

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            list(zip(self.docs, scores)),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        results = []

        for doc, score in ranked:

            results.append({
                "doc_id": doc["doc_id"],
                "title": doc["title"],
                "score": float(score)
            })

        return results