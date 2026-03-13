#!/bin/bash

set -e  # Exit on any error

echo "Setting up hybrid search dashboard..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Add project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Generate sample corpus if raw data is missing
if [ ! -d "data/raw" ] || [ $(ls data/raw/ | wc -l) -lt 300 ]; then
    echo "Generating sample corpus..."
    python generate_corpus.py
fi

# Run ingestion if processed data is missing
if [ ! -f "data/processed/ingested.jsonl" ]; then
    echo "Running data ingestion..."
    python -m backend.app.ingest.ingest --input data/raw --out data/processed
fi

# Run indexing if processed data exists (validate search classes can initialize)
if [ -f "data/processed/ingested.jsonl" ]; then
    echo "Running index validation..."
    python -m backend.app.index.index
fi

# Start FastAPI server
echo "Starting FastAPI server..."
echo "Press Ctrl+C to stop the server"
uvicorn backend.app.main:app --host 0.0.0.0 --port 8001 --reload