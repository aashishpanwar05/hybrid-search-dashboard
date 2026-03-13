function ResultCard({ result }) {

  return (
    <div
      style={{
        border: "1px solid #ddd",
        padding: "15px",
        marginBottom: "15px",
        borderRadius: "8px"
      }}
    >

      <h3>{result.title}</h3>

      <p><b>Document ID:</b> {result.doc_id}</p>

      <p>BM25 Score: {result.bm25_score}</p>
      <p>Vector Score: {result.vector_score}</p>
      <p>Hybrid Score: {result.hybrid_score}</p>

    </div>
  );
}

export default ResultCard;