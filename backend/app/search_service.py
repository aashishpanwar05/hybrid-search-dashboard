import time
from typing import List

from backend.app.search.bm25 import BM25Search
from backend.app.search.vector import VectorSearch
from backend.app.api.metrics import record_request
from backend.app.logging_db import log_query

class HybridSearch:
    def __init__(self):
        self.bm25_search = BM25Search()
        self.vector_search = VectorSearch()

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
        start_time = time.time()

        # Get BM25 results
        bm25_results = self.bm25_search.search(query, top_k=top_k)
        
        # Get vector results  
        vector_results = self.vector_search.search(query, top_k=top_k)

        # Create score dictionaries for hybrid ranking
        bm25_scores = {}
        vector_scores = {}
        
        # Collect all unique doc_ids
        all_doc_ids = set()
        for result in bm25_results + vector_results:
            all_doc_ids.add(result['doc_id'])
        
        # Initialize scores for all docs
        for doc_id in all_doc_ids:
            bm25_scores[doc_id] = 0.0
            vector_scores[doc_id] = 0.0
        
        # Fill in actual scores
        for result in bm25_results:
            bm25_scores[result['doc_id']] = result['score']
        for result in vector_results:
            vector_scores[result['doc_id']] = result['score']

        # Min-max normalization and hybrid ranking
        doc_ids = list(all_doc_ids)
        bm25_score_list = [bm25_scores[doc_id] for doc_id in doc_ids]
        vector_score_list = [vector_scores[doc_id] for doc_id in doc_ids]
        
        # Min-max normalize scores
        if bm25_score_list:
            bm25_min, bm25_max = min(bm25_score_list), max(bm25_score_list)
            bm25_range = bm25_max - bm25_min if bm25_max != bm25_min else 1
            bm25_normalized = [(s - bm25_min) / bm25_range for s in bm25_score_list]
        else:
            bm25_normalized = bm25_score_list
            
        if vector_score_list:
            vector_min, vector_max = min(vector_score_list), max(vector_score_list)
            vector_range = vector_max - vector_min if vector_max != vector_min else 1
            vector_normalized = [(s - vector_min) / vector_range for s in vector_score_list]
        else:
            vector_normalized = vector_score_list

        # Calculate hybrid scores and rank
        hybrid_results = []
        for i, doc_id in enumerate(doc_ids):
            hybrid_score = alpha * bm25_normalized[i] + (1 - alpha) * vector_normalized[i]
            hybrid_results.append((doc_id, hybrid_score))
        
        # Sort by hybrid score descending
        hybrid_results.sort(key=lambda x: x[1], reverse=True)
        top_results = hybrid_results[:top_k]

        # Format results
        results = []
        for doc_id, hybrid_score in top_results:
            # Find the doc details from BM25 results (assuming all docs are there)
            doc_details = next((r for r in bm25_results if r['doc_id'] == doc_id), 
                             next((r for r in vector_results if r['doc_id'] == doc_id), None))
            if doc_details:
                results.append({
                    'doc_id': doc_id,
                    'title': doc_details['title'],
                    'bm25_score': bm25_scores[doc_id],
                    'vector_score': vector_scores[doc_id],
                    'hybrid_score': hybrid_score
                })

        # Record metrics
        latency_ms = (time.time() - start_time) * 1000
        record_request(latency_ms)
        log_query(query, latency_ms, len(results))

        return results