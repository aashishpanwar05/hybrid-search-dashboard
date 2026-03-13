# Hybrid Search + KPI Dashboard System

A fully working, end-to-end hybrid search system with KPI dashboard, designed to run on CPU-only machines. Implements BM25 + semantic vector search with configurable hybrid scoring, evaluation harness, and observability features.

## Architecture Overview

### Components

- **Data Ingestion** (`backend/app/ingest/`): Processes .txt/.md files into JSONL format with metadata
- **Indexing** (`backend/app/index/`): Builds BM25 and vector indexes using rank-bm25 and sentence-transformers
- **Search API** (`backend/app/api/`): FastAPI service with hybrid search, metrics, and logging
- **Evaluation** (`backend/app/eval/`): Computes nDCG@10, Recall@10, MRR@10 on labeled queries
- **Frontend** (`frontend/`): React dashboard with search interface and KPI visualizations
- **Observability**: SQLite logging, Prometheus-style metrics, structured error handling

### Tech Stack

- **Backend**: Python 3.11+, FastAPI, Uvicorn
- **Search**: rank-bm25, sentence-transformers (all-MiniLM-L6-v2), scikit-learn
- **Storage**: SQLite for logs/metrics, local filesystem for indexes
- **Frontend**: React 19, Vite, React Router, Recharts, Axios
- **Testing**: pytest
- **Packaging**: requirements.txt, up.sh startup script

### Data Flow

1. Documents → Ingestion → JSONL
2. JSONL → Indexing → BM25 + Vector indexes
3. Query → Hybrid scoring → Ranked results
4. Results + metrics → Dashboard visualization
5. Evaluation queries → Metrics computation → Experiment tracking

## Quick Start (1 minute)

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- macOS/Linux (CPU-only)

### Run Everything
```bash
# Clone and enter repo
git clone <repo-url>
cd hybrid-search-dashboard

# Run setup and start services
./up.sh
```

This will:
- Create Python virtual environment
- Install dependencies
- Generate sample data (300 documents)
- Build indexes
- Start backend API (http://localhost:8000)
- Start frontend dashboard (http://localhost:5173)

### Manual Steps (if needed)

#### Backend Only
```bash
source .venv/bin/activate
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Only
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `GET /health` - Service health and version info
- `POST /search` - Hybrid search with configurable alpha
- `GET /metrics` - Prometheus-style metrics
- `POST /feedback` - Relevance feedback logging (bonus)

## Testing

```bash
# Backend tests
source .venv/bin/activate
pytest backend/tests/

# Evaluation
python -m app.eval --queries data/eval/queries.jsonl --qrels data/eval/qrels.json
```

## Development

### Adding New Features
1. Create granular prompts for Codex
2. Implement in small, testable units
3. Add tests and documentation
4. Update docs/codex_log.md and docs/decision_log.md

### Key Design Decisions
- Min-max normalization for hybrid scoring (handles varying score ranges)
- SQLite for observability (simple, no external deps)
- React + Vite for fast frontend development
- CPU-only sentence-transformers model (all-MiniLM-L6-v2)

## Repository Structure

```
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # Routes, metrics, logging
│   │   ├── search/         # BM25, vector, hybrid logic
│   │   ├── ingest/         # Data processing
│   │   ├── index/          # Index building
│   │   ├── eval/           # Evaluation harness
│   │   └── main.py         # FastAPI app entry
│   └── tests/              # Unit tests
├── frontend/                # React dashboard
│   └── src/
│       ├── SearchPage.jsx  # Search interface
│       ├── KpiPage.jsx     # KPI visualizations
│       └── App.jsx         # Router setup
├── data/                    # Data and artifacts
│   ├── raw/                # Input documents
│   ├── processed/          # JSONL output
│   ├── index/              # BM25/vector indexes
│   ├── eval/               # Queries and qrels
│   └── metrics/            # Logs and experiments
├── docs/                    # Documentation
│   ├── architecture.md
│   ├── codex_log.md        # Prompt history
│   ├── decision_log.md     # Design rationale
│   └── break_fix_log.md    # Error induction/fixes
├── up.sh                   # Startup script
├── requirements.txt        # Python dependencies
└── README.md
```

## Evaluation Metrics

The system tracks:
- nDCG@10, Recall@10, MRR@10
- Request latency and volume
- Top queries and zero-result queries
- Experiment trends across parameter variations

## Troubleshooting

### Common Issues
- **Index mismatch**: Run `python -m app.index` to rebuild
- **Port conflicts**: Check if 8000/5173 are available
- **Memory issues**: Reduce top_k or use smaller embedding model

### Logs
- Application logs: `data/metrics/search_logs.db`
- Experiment results: `data/metrics/experiments.csv`

## Contributing

1. Follow granular Codex usage protocol
2. Update docs/codex_log.md for each prompt
3. Add tests for new functionality
4. Document design decisions in docs/decision_log.md
5. Test end-to-end with `./up.sh`

## License

[Add appropriate license - public domain sample data]
