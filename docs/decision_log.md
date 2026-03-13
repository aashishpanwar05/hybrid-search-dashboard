# Design Decision Log

This document records key architectural and implementation decisions made during development, with rationale and alternatives considered.

## 1. Hybrid Scoring Normalization

**Decision**: Min-max normalization for BM25 and vector scores before combining.

**Rationale**:
- BM25 and vector similarity scores have different ranges (BM25: 0+, cosine: -1 to 1)
- Min-max ensures both contribute equally to hybrid score
- Simple and interpretable, avoids complex statistical normalization

**Alternatives Considered**:
- Z-score normalization: Requires mean/std calculation, more complex
- No normalization: Leads to one score dominating (usually BM25)
- L2 normalization: Not suitable for score combination

**Implementation**: `hybrid_ranking()` in `backend/app/search/hybrid.py`

## 2. Embedding Model Selection

**Decision**: sentence-transformers `all-MiniLM-L6-v2`

**Rationale**:
- CPU-friendly (no GPU required)
- Good balance of quality and speed (384 dimensions)
- Well-established model with strong performance
- Compatible with sklearn cosine_similarity

**Alternatives Considered**:
- Larger models (e.g., all-mpnet-base-v2): Better quality but slower, higher memory
- Smaller models (e.g., all-MiniLM-L12-v2): Faster but potentially lower quality
- OpenAI embeddings: Requires API key, not local

## 3. Storage Strategy

**Decision**: SQLite for logs/metrics, pickle for indexes, JSONL for processed data

**Rationale**:
- SQLite: ACID transactions, SQL queries, no external services
- Pickle: Fast Python serialization for ML objects
- JSONL: Human-readable, streaming-friendly for large datasets

**Alternatives Considered**:
- PostgreSQL: Overkill for local development, requires server
- CSV for logs: No transactions, harder to query
- HDF5 for indexes: More complex, less portable

## 4. API Design

**Decision**: RESTful FastAPI with Pydantic models

**Rationale**:
- Type safety with Pydantic validation
- Automatic OpenAPI documentation
- Async support for future scalability
- Easy testing with TestClient

**Alternatives Considered**:
- Flask: Less structured, manual validation
- GraphQL: Overkill for simple search API
- gRPC: Binary protocol, more complex for web clients

## 5. Frontend Framework

**Decision**: React + Vite

**Rationale**:
- Modern development experience with hot reload
- Component-based architecture for maintainability
- Rich ecosystem (React Router, Recharts)
- Fast build times with Vite

**Alternatives Considered**:
- Streamlit: Simpler but less flexible for complex UIs
- Vue.js: Similar to React, team preference for React
- Vanilla JS: Too low-level for dashboard complexity

## 6. Error Handling Strategy

**Decision**: Structured logging with error context, graceful degradation

**Rationale**:
- JSON logs enable better debugging and monitoring
- Graceful degradation prevents full system failure
- Request IDs for tracing across components

**Alternatives Considered**:
- Exception propagation: Can crash services
- Silent failures: Hides issues from users
- Email alerts: Not suitable for local development

## 7. Testing Approach

**Decision**: pytest with unit tests for core logic, integration tests for API

**Rationale**:
- pytest is Python standard with good fixtures
- Unit tests for algorithmic correctness
- Integration tests for end-to-end validation

**Alternatives Considered**:
- unittest: Built-in but more verbose
- No tests: Increases bug risk
- Only integration tests: Slower feedback

## 8. Configuration Management

**Decision**: Environment variables with sensible defaults

**Rationale**:
- No config files to manage
- Easy to override for different environments
- Secure (no secrets in code)

**Alternatives Considered**:
- Config files (YAML/JSON): Adds complexity
- Hardcoded values: Not flexible
- Database config: Overkill

## 9. Observability Stack

**Decision**: SQLite logs + Prometheus-style metrics endpoint

**Rationale**:
- Local development friendly
- Standard Prometheus format for future monitoring
- SQL queries for log analysis

**Alternatives Considered**:
- ELK stack: Heavy for local development
- Cloud logging: Not local
- No metrics: Poor operational visibility

## 10. Data Pipeline Design

**Decision**: Modular pipeline with clear separation of concerns

**Rationale**:
- Each step (ingest, index, search) is independently testable
- Easy to modify or replace components
- Clear data flow and dependencies

**Alternatives Considered**:
- Monolithic script: Harder to maintain
- Over-engineered pipeline framework: Adds complexity
- Manual process: Error-prone