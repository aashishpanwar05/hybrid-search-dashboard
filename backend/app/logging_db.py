import sqlite3
import os

DB_PATH = 'data/metrics/search_logs.db'

def init_db():
    """
    Initialize the database and create tables if they don't exist.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
    CREATE TABLE IF NOT EXISTS query_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT,
        latency_ms REAL,
        result_count INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

def log_query(query, latency_ms, result_count):
    """
    Log a search query to the database.

    Args:
        query: The search query string
        latency_ms: Latency in milliseconds
        result_count: Number of results returned
    """
    # Ensure database is initialized
    init_db()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute('''
        INSERT INTO query_logs (query, latency_ms, result_count)
        VALUES (?, ?, ?)
        ''', (query, latency_ms, result_count))
        conn.commit()
    finally:
        conn.close()
