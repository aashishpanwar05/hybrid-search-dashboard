import { useState } from "react";
import axios from "axios";
import ResultCard from "../components/ResultCard";

function SearchPage() {

  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const runSearch = async () => {

    const response = await axios.post(
      "http://localhost:8000/search",
      {
        query: query,
        top_k: 5,
        alpha: 0.5
      }
    );

    setResults(response.data);
  };

  return (
    <div>

      <h2>Search</h2>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter search query"
        style={{ padding: "8px", width: "300px" }}
      />

      <button
        onClick={runSearch}
        style={{ marginLeft: "10px", padding: "8px" }}
      >
        Search
      </button>

      <div style={{ marginTop: "20px" }}>

        {results.map((r, i) => (
          <ResultCard key={i} result={r} />
        ))}

      </div>

    </div>
  );
}

export default SearchPage;