import pytest
import os
import tempfile
import json
from pathlib import Path

def test_bm25_index_creation():
    """Test BM25 index creation and basic functionality."""
    from backend.app.index.bm25 import BM25Index

    # Create sample documents
    documents = [
        {"id": "doc1", "title": "Machine Learning Basics", "content": "Machine learning is a subset of artificial intelligence"},
        {"id": "doc2", "title": "Deep Learning", "content": "Deep learning uses neural networks with multiple layers"},
        {"id": "doc3", "title": "Natural Language Processing", "content": "NLP deals with the interaction between computers and human language"}
    ]

    # Create temporary directory for index
    with tempfile.TemporaryDirectory() as temp_dir:
        index_path = Path(temp_dir) / "bm25_index.pkl"

        # Create and save index
        bm25_index = BM25Index()
        bm25_index.index_documents(documents)
        bm25_index.save(index_path)

        # Load and test search
        loaded_index = BM25Index.load(index_path)

        # Test search
        query = "machine learning"
        scores = loaded_index.search(query, top_k=5)

        assert len(scores) > 0
        assert "doc1" in [doc_id for doc_id, _ in scores]
        assert all(isinstance(score, (int, float)) for _, score in scores)

def test_bm25_preprocessing():
    """Test text preprocessing for BM25."""
    from backend.app.index.bm25 import preprocess_text

    # Test basic preprocessing
    text = "Hello, World! This is a TEST with 123 numbers."
    processed = preprocess_text(text)

    assert "hello" in processed
    assert "world" in processed
    assert "test" in processed
    assert "123" not in processed  # Numbers should be removed
    assert "!" not in processed    # Punctuation should be removed

    # Test empty input
    assert preprocess_text("") == []

    # Test None input
    assert preprocess_text(None) == []