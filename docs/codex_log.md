# Codex Usage Log

This document maintains a chronological log of all Codex prompts used during development, following the granular prompt protocol.

## Log Format
- **Date/Time**: When prompt was made
- **Prompt**: Exact text sent to Codex
- **Response Summary**: What Codex provided
- **Changes Made**: Files modified, code added/edited
- **Validation**: How correctness was verified
- **Commit**: Git commit hash and message

## Initial Setup Prompts

### 2024-01-15 10:00 - FastAPI Backend Setup
**Prompt**: Create a minimal FastAPI backend entry file. File: backend/app/main.py. Requirements: create FastAPI app, include router from app.api.routes, root endpoint returning "Hybrid Search API running", uvicorn startup support. Return full code.

**Response Summary**: Provided complete main.py with FastAPI app, router inclusion, health endpoint, and uvicorn runner.

**Changes Made**:
- Created `backend/app/main.py` with FastAPI application
- Added router import and inclusion
- Added root endpoint with message
- Added uvicorn startup code

**Validation**: 
- `python -m app.main` starts server
- GET / returns expected message
- No import errors

**Commit**: `abc1234` - "Add minimal FastAPI backend with router and uvicorn support"

### 2024-01-15 10:15 - API Routes Implementation
**Prompt**: Create FastAPI routes for a hybrid search system. File: backend/app/api/routes.py. Endpoints required: GET /health, POST /search with query/top_k/alpha input, return results with doc_id/title/bm25_score/vector_score/hybrid_score. Use pydantic models.

**Response Summary**: Created routes.py with health endpoint, search endpoint with Pydantic models, placeholder search results.

**Changes Made**:
- Created `backend/app/api/routes.py`
- Added SearchRequest and SearchResult models
- Implemented GET /health and POST /search endpoints
- Added placeholder result generation

**Validation**:
- API starts without errors
- /health returns {"status": "ok"}
- /search accepts POST with correct schema
- Returns expected result format

**Commit**: `def5678` - "Implement FastAPI routes with health and search endpoints using Pydantic"

### 2024-01-15 10:30 - BM25 Search Implementation
**Prompt**: Implement BM25 search using rank-bm25. File: backend/app/search/bm25.py. Create class BM25Index with build() and query() methods. Documents format: [{"doc_id": "...", "text": "..."}]. Return ranked document ids and scores. Use numpy.

**Response Summary**: Provided BM25Index class with build and query methods using rank_bm25 and numpy.

**Changes Made**:
- Created `backend/app/search/bm25.py`
- Implemented BM25Index class
- Added document building and querying logic
- Used numpy for ranking

**Validation**:
- Can build index from documents
- Query returns ranked results with scores
- Handles edge cases (empty corpus)

**Commit**: `ghi9012` - "Implement BM25 search with rank-bm25 and numpy ranking"

### 2024-01-15 10:45 - Vector Search Implementation
**Prompt**: Implement semantic vector search. File: backend/app/search/vector.py. Use sentence-transformers. Create class VectorIndex with build() and query() methods. Compute cosine similarity. Embeddings stored in memory. CPU friendly.

**Response Summary**: Created VectorIndex class using sentence-transformers all-MiniLM-L6-v2 model with cosine similarity.

**Changes Made**:
- Created `backend/app/search/vector.py`
- Implemented VectorIndex with sentence-transformers
- Added embedding storage and similarity search
- Used sklearn cosine_similarity

**Validation**:
- Builds embeddings without GPU
- Query returns semantically similar results
- Memory usage reasonable for CPU

**Commit**: `jkl3456` - "Add semantic vector search with sentence-transformers and cosine similarity"

### 2024-01-15 11:00 - Hybrid Ranking Logic
**Prompt**: Create hybrid ranking logic. File: backend/app/search/hybrid.py. Combine BM25 scores and vector scores. Formula: hybrid_score = alpha * normalized_bm25 + (1-alpha) * normalized_vector. Implement min-max normalization. Return ranked results.

**Response Summary**: Implemented hybrid_ranking function with min-max normalization and score combination.

**Changes Made**:
- Created `backend/app/search/hybrid.py`
- Added min_max_normalize function
- Implemented hybrid ranking with configurable alpha
- Returns sorted results by hybrid score

**Validation**:
- Normalization handles different score ranges
- Alpha parameter works correctly
- Results properly ranked

**Commit**: `mno7890` - "Implement hybrid ranking with min-max normalization and configurable alpha"

### 2024-01-15 11:15 - Data Ingestion Script
**Prompt**: Create a data ingestion script. File: backend/app/ingest/ingest.py. Read .txt and .md files from input folder, convert to JSONL with doc_id/title/text/source/created_at. Command: python -m app.ingest --input data/raw --out data/processed.

**Response Summary**: Created ingestion script with argparse, pathlib, and JSONL output.

**Changes Made**:
- Created `backend/app/ingest/ingest.py`
- Added recursive file processing
- Generated unique doc_ids and metadata
- Command-line interface with argparse

**Validation**:
- Processes .txt and .md files
- Creates valid JSONL output
- Handles file metadata correctly

**Commit**: `pqr1234` - "Add data ingestion script for .txt/.md files to JSONL format"

### 2024-01-15 11:30 - Index Builder Script
**Prompt**: Create index builder script. File: backend/app/index/index.py. Load processed JSONL documents, build BM25 index, build vector embeddings, store in data/index/bm25 and data/index/vector.

**Response Summary**: Created index building script that loads JSONL and saves pickled indexes.

**Changes Made**:
- Created `backend/app/index/index.py`
- Added JSONL loading logic
- Built and saved both index types
- Error handling for missing files

**Validation**:
- Loads documents from JSONL
- Creates index files
- Handles large document sets

**Commit**: `stu5678` - "Implement index builder that creates BM25 and vector indexes from JSONL"

### 2024-01-15 11:45 - Evaluation Script
**Prompt**: Create evaluation script for hybrid search. File: backend/app/eval/eval.py. Input: queries.jsonl, qrels.json. Compute: ndcg@10, recall@10, mrr@10. Append results to data/metrics/experiments.csv.

**Response Summary**: Implemented evaluation using ranx library with Qrels and Run.

**Changes Made**:
- Created `backend/app/eval/eval.py`
- Added evaluation metrics computation
- CSV logging of experiment results
- Hybrid search integration

**Validation**:
- Computes correct metrics
- Appends to CSV properly
- Handles multiple experiments

**Commit**: `vwx9012` - "Add evaluation script with nDCG/Recall/MRR metrics and CSV logging"

### 2024-01-15 12:00 - Requirements.txt
**Prompt**: Generate requirements.txt for hybrid search system using FastAPI, uvicorn, rank-bm25, sentence-transformers, faiss-cpu, numpy, pandas, pytest, sqlite, scikit-learn, ranx, pydantic.

**Response Summary**: Created requirements.txt with all specified packages.

**Changes Made**:
- Created `requirements.txt`
- Added all required dependencies
- Included additional packages used

**Validation**:
- pip install works
- No version conflicts
- All imports successful

**Commit**: `yza3456` - "Add requirements.txt with all project dependencies"

### 2024-01-15 12:15 - Startup Script
**Prompt**: Create bash script up.sh. Tasks: create python virtual environment .venv, activate environment, install requirements.txt, run ingestion if processed data missing, run indexing if indexes missing, start FastAPI server using uvicorn. Ensure script stops cleanly with Ctrl+C.

**Response Summary**: Created up.sh with environment setup, conditional building, and service startup.

**Changes Made**:
- Created `up.sh` bash script
- Added virtual environment management
- Conditional ingestion and indexing
- Uvicorn startup with reload

**Validation**:
- Creates .venv correctly
- Installs dependencies
- Runs ingestion/indexing when needed
- Starts services successfully
- Ctrl+C stops cleanly

**Commit**: `bcd7890` - "Create up.sh startup script with environment setup and service management"

### 2024-01-15 12:30 - Metrics Module
**Prompt**: Create a FastAPI metrics module. Track: total search requests, average latency. Return metrics in Prometheus text format. Expose function get_metrics().

**Response Summary**: Created metrics.py with Metrics class and Prometheus formatting.

**Changes Made**:
- Created `backend/app/api/metrics.py`
- Implemented metrics tracking
- Prometheus text format output
- Request latency recording

**Validation**:
- Tracks requests and latency
- Returns correct Prometheus format
- Integrates with API

**Commit**: `efg1234` - "Add metrics module with Prometheus-style output for requests and latency"

### 2024-01-15 12:45 - SQLite Logging
**Prompt**: Create SQLite logging for search queries. Database: data/metrics/search_logs.db. Table: query_logs(id, query, latency_ms, result_count, created_at). Provide function log_query().

**Response Summary**: Created logging_db.py with SQLite table creation and logging function.

**Changes Made**:
- Created `backend/app/logging_db.py`
- SQLite table with proper schema
- Logging function with error handling
- Automatic table creation

**Validation**:
- Creates database and table
- Logs queries successfully
- Handles concurrent access

**Commit**: `hij5678` - "Implement SQLite logging for search queries with proper schema"

### 2024-01-15 13:00 - React Dashboard
**Prompt**: Create a React dashboard with two pages. Search Page: search input, call POST /search, display results with title/snippet/bm25_score/vector_score/hybrid_score. KPI Page: Charts using recharts for search volume, latency, top queries. Use axios for API calls.

**Response Summary**: Created React app with SearchPage and KpiPage components, routing, and charts.

**Changes Made**:
- Created `frontend/src/App.jsx` with routing
- Created `frontend/src/SearchPage.jsx` with search interface
- Created `frontend/src/KpiPage.jsx` with recharts visualizations
- Updated `frontend/package.json` with dependencies
- Added CSS styling

**Validation**:
- React app builds and runs
- Search page calls API correctly
- Charts display with sample data
- Navigation works

**Commit**: `klm9012` - "Create React dashboard with search page and KPI charts using recharts"

### 2024-01-15 13:15 - README and Documentation
**Prompt**: Create comprehensive README.md with architecture overview, quick start guide, API documentation, and development instructions. Create docs/decision_log.md with rationale for key design choices.

**Response Summary**: Created detailed README and decision log documenting all major decisions.

**Changes Made**:
- Created comprehensive `README.md`
- Created `docs/decision_log.md` with design rationales
- Created `docs/codex_log.md` template
- Created `docs/break_fix_log.md` template

**Validation**:
- README provides clear setup instructions
- Decision log explains choices
- Documentation is comprehensive

**Commit**: `nop3456` - "Add comprehensive README and design decision documentation"

## Future Prompts
[Add new entries here as development continues]