import time
import pickle
from typing import List

from app.search.bm25 import BM25Index
from app.search.vector import VectorIndex
from app.search.hybrid import hybrid_ranking
from app.api.metrics import record_request
from app.logging_db import log_query

class HybridSearch:
    def __init__(self):
        self.bm25_index = None
        self.vector_index = None
        self.doc_ids = None
        self._load_indexes()

    def _load_indexes(self):
        """Load BM25 and vector indexes from disk."""
        try:
            with open('data/index/bm25/index.pkl', 'rb') as f:
                self.bm25_index = pickle.load(f)
            with open('data/index/vector/index.pkl', 'rb') as f:
                self.vector_index = pickle.load(f)
            self.doc_ids = self.vector_index.doc_ids
            print("Indexes loaded successfully")
        except FileNotFoundError:
            print("Warning: Indexes not found. Run indexing first.")
        except Exception as e:
            print(f"Error loading indexes: {e}")

    def search(self, query: str, top_k: int = 10, alpha: float = 0.5) -> List[dict]:
        """
        Perform hybrid search.

        Args:
            query: Search query
            top_k: Number of results to return
            alpha: Weight for BM25 (0-1)

        Returns:
            List of search results with scores
        """
        if not self.bm25_index or not self.vector_index:
            return []

        start_time = time.time()

        # Get BM25 scores for all documents
        bm25_tokenized = query.split()
        bm25_scores = self.bm25_index.bm25.get_scores(bm25_tokenized)

        # Get vector scores for all documents
        query_embedding = self.vector_index.model.encode([query])[0]
        from sklearn.metrics.pairwise import cosine_similarity
        vector_scores = cosine_similarity([query_embedding], self.vector_index.embeddings)[0]

        # Hybrid ranking
        ranked_results = hybrid_ranking(self.doc_ids, bm25_scores, vector_scores, alpha)

        # Take top_k
        top_results = ranked_results[:top_k]

        # Record metrics
        latency_ms = (time.time() - start_time) * 1000
        record_request(latency_ms)
        log_query(query, latency_ms, len(top_results))

        # Format results
        results = []
        for doc_id, hybrid_score in top_results:
            # Find original BM25 and vector scores for this doc
            idx = self.doc_ids.index(doc_id)
            bm25_score = float(bm25_scores[idx])
            vector_score = float(vector_scores[idx])

            results.append({
                'doc_id': doc_id,
                'title': doc_id.replace('_', '/').replace('.txt', '').replace('.md', ''),  # Simple title
                'bm25_score': bm25_score,
                'vector_score': vector_score,
                'hybrid_score': hybrid_score
            })

        return results