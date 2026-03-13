import json
import pickle
import csv
from datetime import datetime
from pathlib import Path

import numpy as np
from ranx import Qrels, Run, evaluate
from sentence_transformers import SentenceTransformer

from backend.app.search.hybrid import hybrid_ranking

def load_queries(queries_path):
    """
    Load queries from JSONL file.

    Args:
        queries_path: Path to queries.jsonl

    Returns:
        Dict of {query_id: query_text}
    """
    queries = {}
    with open(queries_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                queries[data['query_id']] = data['query']
    return queries

def load_qrels(qrels_path):
    """
    Load qrels from JSON file.

    Args:
        qrels_path: Path to qrels.json

    Returns:
        Qrels object
    """
    return Qrels.from_file(qrels_path)

def load_indices(bm25_path, vector_path):
    """
    Load BM25 and vector indices.

    Args:
        bm25_path: Path to BM25 index pickle
        vector_path: Path to vector index pickle

    Returns:
        bm25_index, vector_index
    """
    with open(bm25_path, 'rb') as f:
        bm25_index = pickle.load(f)
    with open(vector_path, 'rb') as f:
        vector_index = pickle.load(f)
    return bm25_index, vector_index

def run_hybrid_search(query_text, bm25_index, vector_index, alpha=0.5, top_k=10):
    """
    Run hybrid search for a query.

    Args:
        query_text: The query string
        bm25_index: BM25Index instance
        vector_index: VectorIndex instance
        alpha: Weight for BM25
        top_k: Number of results to return

    Returns:
        List of (doc_id, score) tuples
    """
    # Get BM25 scores for all documents
    tokenized_query = query_text.split()
    bm25_scores = bm25_index.bm25.get_scores(tokenized_query)

    # Get vector scores for all documents
    query_embedding = vector_index.model.encode([query_text])[0]
    from sklearn.metrics.pairwise import cosine_similarity
    vector_scores = cosine_similarity([query_embedding], vector_index.embeddings)[0]

    # Hybrid ranking
    results = hybrid_ranking(vector_index.doc_ids, bm25_scores, vector_scores, alpha)
    return results[:top_k]

def evaluate_hybrid_search(queries_path, qrels_path, bm25_index_path, vector_index_path, output_csv, alpha=0.5):
    """
    Evaluate hybrid search and append results to CSV.

    Args:
        queries_path: Path to queries.jsonl
        qrels_path: Path to qrels.json
        bm25_index_path: Path to BM25 index
        vector_index_path: Path to vector index
        output_csv: Path to output CSV
        alpha: Hybrid search alpha parameter
    """
    # Load data
    queries = load_queries(queries_path)
    qrels = load_qrels(qrels_path)
    bm25_index, vector_index = load_indices(bm25_index_path, vector_index_path)

    # Create run
    run_dict = {}
    for query_id, query_text in queries.items():
        results = run_hybrid_search(query_text, bm25_index, vector_index, alpha)
        run_dict[query_id] = {doc_id: score for doc_id, score in results}

    run = Run(run_dict)

    # Evaluate
    results = evaluate(qrels, run, ["ndcg@10", "recall@10", "mrr@10"])

    # Prepare CSV row
    experiment_name = f"hybrid_alpha_{alpha}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    row = {
        'experiment': experiment_name,
        'ndcg@10': results['ndcg@10'],
        'recall@10': results['recall@10'],
        'mrr@10': results['mrr@10']
    }

    # Append to CSV
    file_exists = Path(output_csv).exists()
    with open(output_csv, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['experiment', 'ndcg@10', 'recall@10', 'mrr@10'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(f"Evaluation complete. Results appended to {output_csv}")
    print(f"NDCG@10: {results['ndcg@10']:.4f}")
    print(f"Recall@10: {results['recall@10']:.4f}")
    print(f"MRR@10: {results['mrr@10']:.4f}")

if __name__ == "__main__":
    # Default paths
    queries_path = 'data/eval/queries.jsonl'
    qrels_path = 'data/eval/qrels.json'
    bm25_index_path = 'data/index/bm25/index.pkl'
    vector_index_path = 'data/index/vector/index.pkl'
    output_csv = 'data/metrics/experiments.csv'
    alpha = 0.5

    evaluate_hybrid_search(queries_path, qrels_path, bm25_index_path, vector_index_path, output_csv, alpha)
