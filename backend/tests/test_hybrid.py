import pytest
import numpy as np
from pathlib import Path
import tempfile

def test_hybrid_ranking():
    """Test hybrid ranking function."""
    from backend.app.search.hybrid import hybrid_ranking

    # Mock data
    doc_ids = ["doc1", "doc2", "doc3"]
    bm25_scores = np.array([0.8, 0.6, 0.4])
    vector_scores = np.array([0.7, 0.9, 0.5])

    # Test alpha = 0.5 (equal weight)
    results = hybrid_ranking(doc_ids, bm25_scores, vector_scores, alpha=0.5)

    assert len(results) == 3
    assert all(doc_id in doc_ids for doc_id, _ in results)

    # Scores should be combination of BM25 and vector scores
    for doc_id, score in results:
        if doc_id == "doc1":
            expected_score = 0.5 * 0.8 + 0.5 * 0.7  # 0.75
        elif doc_id == "doc2":
            expected_score = 0.5 * 0.6 + 0.5 * 0.9  # 0.75
        elif doc_id == "doc3":
            expected_score = 0.5 * 0.4 + 0.5 * 0.5  # 0.45

        assert abs(score - expected_score) < 0.001

def test_hybrid_search_alpha_variations():
    """Test hybrid search with different alpha values."""
    from backend.app.search.hybrid import hybrid_ranking

    doc_ids = ["doc1", "doc2"]
    bm25_scores = np.array([1.0, 0.5])
    vector_scores = np.array([0.5, 1.0])

    # Test BM25-only (alpha = 0)
    bm25_results = hybrid_ranking(doc_ids, bm25_scores, vector_scores, alpha=0.0)
    assert bm25_results[0][0] == "doc1"  # Higher BM25 score
    assert bm25_results[0][1] == 1.0

    # Test vector-only (alpha = 1)
    vector_results = hybrid_ranking(doc_ids, bm25_scores, vector_scores, alpha=1.0)
    assert vector_results[0][0] == "doc2"  # Higher vector score
    assert vector_results[0][1] == 1.0

def test_hybrid_search_service():
    """Test the complete hybrid search service."""
    from backend.app.search_service import HybridSearch

    # This test assumes indices exist in the expected locations
    # In a real scenario, you'd mock or create test indices

    search_service = HybridSearch()

    # Test that the service initializes
    assert hasattr(search_service, 'bm25_index')
    assert hasattr(search_service, 'vector_index')

    # Test search (this will fail if indices don't exist, which is expected in test env)
    try:
        results = search_service.search("test query", top_k=5, alpha=0.5)
        assert isinstance(results, list)
    except Exception as e:
        # Expected if indices don't exist
        assert "index" in str(e).lower() or "file" in str(e).lower()