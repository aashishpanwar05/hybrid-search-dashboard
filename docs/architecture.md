# Architecture Documentation

## System Overview

The Hybrid Search + KPI Dashboard is a CPU-only, end-to-end search system combining lexical (BM25) and semantic (vector) retrieval with comprehensive observability and evaluation capabilities.

## Core Components

### 1. Data Pipeline

#### Ingestion (`backend/app/ingest/`)
- **Input**: .txt/.md files from `data/raw/`
- **Processing**: Extract text, generate metadata, create unique doc_ids
- **Output**: JSONL format in `data/processed/ingested.jsonl`
- **Key Features**:
  - Recursive directory traversal
  - File modification timestamp extraction
  - Unique ID generation from relative paths

#### Indexing (`backend/app/index/`)
- **BM25 Index** (`data/index/bm25/index.pkl`):
  - Uses rank-bm25 library
  - Tokenizes documents with simple whitespace splitting
  - Stores corpus and model for querying
- **Vector Index** (`data/index/vector/index.pkl`):
  - Uses sentence-transformers (all-MiniLM-L6-v2)
  - 384-dimensional embeddings
  - Cosine similarity for retrieval

### 2. Search Engine

#### BM25 Search (`backend/app/search/bm25.py`)
```python
class BM25Index:
    def build(self, documents):  # Tokenize and build index
    def query(self, query_text, top_k):  # Return ranked results
```

#### Vector Search (`backend/app/search/vector.py`)
```python
class VectorIndex:
    def build(self, documents):  # Generate embeddings
    def query(self, query_text, top_k):  # Cosine similarity search
```

#### Hybrid Ranking (`backend/app/search/hybrid.py`)
- **Normalization**: Min-max scaling for both score types
- **Combination**: `hybrid = alpha * norm_bm25 + (1-alpha) * norm_vector`
- **Ranking**: Sort by hybrid score descending

### 3. API Layer

#### FastAPI Application (`backend/app/main.py`)
- Router inclusion from `app.api.routes`
- Uvicorn startup configuration
- Health checks and error handling

#### Routes (`backend/app/api/routes.py`)
- `GET /health`: Service status
- `POST /search`: Hybrid search endpoint
- Pydantic models for request/response validation

#### Metrics (`backend/app/api/metrics.py`)
- Request counting and latency tracking
- Prometheus text format output
- Global metrics instance

### 4. Observability

#### Logging (`backend/app/logging_db.py`)
- SQLite database: `data/metrics/search_logs.db`
- Schema: id, query, latency_ms, result_count, created_at
- Structured logging for analysis

#### Evaluation (`backend/app/eval/eval.py`)
- Uses ranx library for IR metrics
- Computes nDCG@10, Recall@10, MRR@10
- Results logged to `data/metrics/experiments.csv`

### 5. Frontend Dashboard

#### React Application (`frontend/`)
- **Search Page**: Query interface with result display
- **KPI Page**: Charts for volume, latency, top queries
- **Tech**: React Router, Axios, Recharts

## Data Flow

```
Documents (.txt/.md)
    ↓
Ingestion → JSONL
    ↓
Indexing → BM25 + Vector Indexes
    ↓
Query → BM25 Scores + Vector Scores
    ↓
Hybrid Ranking → Ranked Results
    ↓
API Response + Logging
    ↓
Dashboard Display + Metrics
```

## Key Design Patterns

### 1. Modular Architecture
- Clear separation between ingestion, indexing, search, and API
- Each component independently testable
- Easy to modify or replace individual parts

### 2. CPU-First Design
- No GPU dependencies
- Memory-efficient processing
- Fast startup times

### 3. Observability by Default
- Structured logging for all operations
- Metrics collection for monitoring
- Evaluation framework for quality assessment

### 4. Configuration through Code
- Environment variables for runtime config
- Sensible defaults
- No external configuration files

## Performance Characteristics

### Indexing
- **BM25**: ~1000 docs/second
- **Vector**: ~500 docs/second (CPU)
- **Memory**: ~500MB for 10K documents

### Querying
- **BM25**: ~100 queries/second
- **Vector**: ~50 queries/second
- **Hybrid**: ~30 queries/second
- **Latency**: <100ms for typical queries

### Storage
- **Indexes**: Pickle files (~10MB for 10K docs)
- **Logs**: SQLite (~1MB for 100K queries)
- **Metrics**: CSV for experiments

## Error Handling

### Validation Layers
1. **Input Validation**: Pydantic models in API
2. **Index Validation**: Metadata checks on load
3. **Query Validation**: Sanitization and limits
4. **Response Validation**: Schema enforcement

### Recovery Strategies
- Automatic index rebuild on mismatch
- Graceful degradation for partial failures
- Clear error messages for debugging
- Transactional logging to prevent data loss

## Testing Strategy

### Unit Tests (`backend/tests/`)
- Core algorithms (BM25, vector, hybrid)
- Data processing functions
- API route contracts

### Integration Tests
- End-to-end search pipeline
- Index building and loading
- API response formats

### Evaluation Tests
- Metric computation accuracy
- Regression detection
- Performance benchmarking

## Deployment

### Local Development
```bash
./up.sh  # Sets up everything
```

### Production Considerations
- Gunicorn for multiple workers
- Nginx reverse proxy
- Log aggregation
- Index backup strategies
- Monitoring integration

## Security Considerations

- Input sanitization
- Rate limiting (basic)
- No secrets in codebase
- File system isolation
- Error message sanitization

## Future Extensions

- Query expansion
- Relevance feedback
- Multi-language support
- Index compression
- Distributed indexing
- Real-time updates