import pytest
import numpy as np
from pathlib import Path
import tempfile

def test_vector_index_creation():
    """Test vector index creation and search."""
    from backend.app.index.vector import VectorIndex

    # Create sample documents
    documents = [
        {"id": "doc1", "title": "Machine Learning", "content": "Machine learning algorithms learn from data"},
        {"id": "doc2", "title": "Deep Learning", "content": "Deep learning uses neural networks"},
        {"id": "doc3", "title": "AI Ethics", "content": "Artificial intelligence ethics and responsible AI"}
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        index_path = Path(temp_dir) / "vector_index.pkl"

        # Create and save index
        vector_index = VectorIndex()
        vector_index.index_documents(documents)
        vector_index.save(index_path)

        # Load and test search
        loaded_index = VectorIndex.load(index_path)

        # Test search
        query = "artificial intelligence"
        results = loaded_index.search(query, top_k=3)

        assert len(results) <= 3
        assert all(isinstance(score, (int, float)) for _, score in results)

        # Test that results are sorted by score (descending)
        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True)

def test_sentence_transformer_model():
    """Test that the sentence transformer model loads correctly."""
    from sentence_transformers import SentenceTransformer

    # This should not raise an exception
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Test encoding
    texts = ["Hello world", "Machine learning is awesome"]
    embeddings = model.encode(texts)

    assert embeddings.shape[0] == 2
    assert embeddings.shape[1] == 384  # Dimension for all-MiniLM-L6-v2

    # Test that embeddings are normalized (approximately)
    norms = np.linalg.norm(embeddings, axis=1)
    assert all(abs(norm - 1.0) < 0.1 for norm in norms)  # Should be close to 1