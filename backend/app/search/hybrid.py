from backend.app.search.bm25 import BM25Search
from backend.app.search.vector import VectorSearch


class HybridSearch:

    def __init__(self, alpha=0.5):

        self.alpha = alpha
        self.bm25 = BM25Search()
        self.vector = VectorSearch()

    def search(self, query, top_k=5):

        bm25_results = self.bm25.search(query, top_k)
        vector_results = self.vector.search(query, top_k)

        results = []

        for i in range(len(bm25_results)):

            bm25_doc = bm25_results[i]
            vector_doc = vector_results[i]

            hybrid_score = (
                self.alpha * bm25_doc["score"]
                + (1 - self.alpha) * vector_doc["score"]
            )

            results.append({
                "doc_id": bm25_doc["doc_id"],
                "title": bm25_doc["title"],
                "bm25_score": bm25_doc["score"],
                "vector_score": vector_doc["score"],
                "hybrid_score": hybrid_score
            })

        return results