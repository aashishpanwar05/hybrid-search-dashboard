import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data

def test_search_endpoint():
    """Test the search endpoint."""
    search_request = {
        "query": "machine learning",
        "top_k": 5,
        "alpha": 0.5
    }

    response = client.post("/search", json=search_request)
    assert response.status_code == 200
    results = response.json()

    assert isinstance(results, list)
    if len(results) > 0:  # Only check structure if results exist
        result = results[0]
        assert "doc_id" in result
        assert "title" in result
        assert "bm25_score" in result
        assert "vector_score" in result
        assert "hybrid_score" in result

def test_metrics_endpoint():
    """Test the metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()

    # Check that expected metrics are present
    expected_keys = ["total_queries", "avg_latency_ms", "total_documents"]
    for key in expected_keys:
        assert key in data

def test_logs_endpoint():
    """Test the logs endpoint."""
    response = client.get("/logs?limit=10")
    assert response.status_code == 200
    logs = response.json()

    assert isinstance(logs, list)
    if len(logs) > 0:
        log_entry = logs[0]
        assert "query" in log_entry
        assert "latency_ms" in log_entry
        assert "result_count" in log_entry
        assert "created_at" in log_entry

def test_experiments_endpoint():
    """Test the experiments endpoint."""
    response = client.get("/experiments")
    assert response.status_code == 200
    experiments = response.json()

    assert isinstance(experiments, list)
    if len(experiments) > 0:
        exp = experiments[0]
        expected_keys = ["timestamp", "git_commit", "experiment_name", "alpha",
                        "ndcg_at_10", "recall_at_10", "mrr_at_10", "query_count"]
        for key in expected_keys:
            assert key in exp