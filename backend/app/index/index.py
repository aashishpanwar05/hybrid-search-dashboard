import json
import pickle
import os
from pathlib import Path

from backend.app.search.bm25 import BM25Index
from backend.app.search.vector import VectorIndex

def load_documents(jsonl_path):
    """
    Load documents from JSONL file.

    Args:
        jsonl_path: Path to the JSONL file

    Returns:
        List of document dictionaries
    """
    documents = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                documents.append(json.loads(line))
    return documents

def build_indices(jsonl_path, bm25_dir, vector_dir):
    """
    Build and save BM25 and vector indices.

    Args:
        jsonl_path: Path to processed JSONL documents
        bm25_dir: Directory to save BM25 index
        vector_dir: Directory to save vector index
    """
    # Load documents
    documents = load_documents(jsonl_path)
    print(f"Loaded {len(documents)} documents")

    # Build BM25 index
    print("Building BM25 index...")
    bm25_index = BM25Index()
    bm25_index.build(documents)

    # Save BM25 index
    Path(bm25_dir).mkdir(parents=True, exist_ok=True)
    bm25_path = Path(bm25_dir) / 'index.pkl'
    with open(bm25_path, 'wb') as f:
        pickle.dump(bm25_index, f)
    print(f"BM25 index saved to {bm25_path}")

    # Build vector index
    print("Building vector index...")
    vector_index = VectorIndex()
    vector_index.build(documents)

    # Save vector index
    Path(vector_dir).mkdir(parents=True, exist_ok=True)
    vector_path = Path(vector_dir) / 'index.pkl'
    with open(vector_path, 'wb') as f:
        pickle.dump(vector_index, f)
    print(f"Vector index saved to {vector_path}")

    print("Index building complete!")

if __name__ == "__main__":
    # Default paths
    jsonl_path = 'data/processed/ingested.jsonl'
    bm25_dir = 'data/index/bm25'
    vector_dir = 'data/index/vector'

    build_indices(jsonl_path, bm25_dir, vector_dir)
