import os
from pathlib import Path

from backend.app.search.bm25 import BM25Search
from backend.app.search.vector import VectorSearch

def build_indices():
    """
    Build and validate BM25 and vector indices.
    The new search classes handle loading and indexing internally.
    """
    print("Validating data availability...")

    # Check if processed data exists
    data_path = Path("data/processed/ingested.jsonl")
    if not data_path.exists():
        raise FileNotFoundError(f"Processed data not found at {data_path}. Run ingestion first.")

    print(f"Data file found: {data_path}")

    # Validate BM25 search can be initialized
    print("Validating BM25 search...")
    try:
        bm25_search = BM25Search()
        print("BM25 search initialized successfully")
    except Exception as e:
        raise RuntimeError(f"Failed to initialize BM25 search: {e}")

    # Validate vector search can be initialized
    print("Validating vector search...")
    try:
        vector_search = VectorSearch()
        print("Vector search initialized successfully")
    except Exception as e:
        raise RuntimeError(f"Failed to initialize vector search: {e}")

    print("All indices validated successfully!")

if __name__ == "__main__":
    build_indices()
