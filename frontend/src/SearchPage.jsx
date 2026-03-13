import { useState } from 'react';
import axios from 'axios';

function SearchPage() {
  const [query, setQuery] = useState('');
  const [topK, setTopK] = useState(10);
  const [alpha, setAlpha] = useState(0.5);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8001/search', {
        query,
        top_k: topK,
        alpha: alpha
      });
      setResults(response.data);
    } catch (error) {
      console.error('Search error:', error);
      alert('Search failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-page">
      <h1>Hybrid Search</h1>
      <div className="search-form">
        <input
          type="text"
          placeholder="Enter search query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <input
          type="number"
          placeholder="Top K"
          value={topK}
          onChange={(e) => setTopK(parseInt(e.target.value))}
          min="1"
          max="100"
        />
        <input
          type="number"
          step="0.1"
          placeholder="Alpha"
          value={alpha}
          onChange={(e) => setAlpha(parseFloat(e.target.value))}
          min="0"
          max="1"
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      <div className="results">
        {results.map((result, index) => (
          <div key={index} className="result-item">
            <h3>{result.title}</h3>
            <p><strong>Document ID:</strong> {result.doc_id}</p>
            <div className="scores">
              <span>BM25: {result.bm25_score.toFixed(3)}</span>
              <span>Vector: {result.vector_score.toFixed(3)}</span>
              <span>Hybrid: {result.hybrid_score.toFixed(3)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchPage;