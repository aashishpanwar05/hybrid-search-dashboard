from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import sqlite3
import csv
import os

from backend.app.search_service import HybridSearch
from backend.app.api.metrics import get_metrics

router = APIRouter()

search_engine = HybridSearch()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 10
    alpha: float = 0.5

class SearchResult(BaseModel):
    doc_id: str
    title: str
    bm25_score: float
    vector_score: float
    hybrid_score: float

@router.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}

@router.post("/search", response_model=List[SearchResult])
def search(request: SearchRequest):
    results = search_engine.search(
        request.query,
        request.top_k,
        request.alpha
    )
    return results

@router.get("/metrics")
def metrics():
    return get_metrics()

@router.get("/logs")
def get_logs(limit: int = 100):
    """Get recent search logs."""
    db_path = 'data/metrics/search_logs.db'
    if not os.path.exists(db_path):
        return []

    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT query, latency_ms, result_count, created_at
        FROM query_logs
        ORDER BY created_at DESC
        LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        logs = [
            {
                'query': row[0],
                'latency_ms': row[1],
                'result_count': row[2],
                'created_at': row[3]
            }
            for row in rows
        ]
        return logs
    finally:
        conn.close()

@router.get("/experiments")
def get_experiments():
    """Get experiment results."""
    csv_path = 'data/metrics/experiments.csv'
    if not os.path.exists(csv_path):
        return []

    experiments = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            experiments.append({
                'experiment': row['experiment'],
                'ndcg@10': float(row.get('ndcg@10', 0)),
                'recall@10': float(row.get('recall@10', 0)),
                'mrr@10': float(row.get('mrr@10', 0))
            })
    return experiments