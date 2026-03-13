import { useState, useEffect } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function EvaluationPage() {
  const [experiments, setExperiments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchExperiments();
  }, []);

  const fetchExperiments = async () => {
    try {
      const response = await axios.get('http://localhost:8001/experiments');
      setExperiments(response.data);
    } catch (error) {
      console.error('Error fetching experiments:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading evaluation data...</div>;
  }

  return (
    <div>
      <h2>Evaluation Dashboard</h2>

      <div style={{ marginBottom: "30px" }}>
        <h3>NDCG@10 Trend Over Time</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={experiments}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis domain={[0.8, 1.0]} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="ndcg_score" stroke="#8884d8" name="NDCG@10" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ marginBottom: "30px" }}>
        <h3>Query Performance Trends</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={experiments}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="timestamp" tickFormatter={(value) => new Date(value).toLocaleDateString()} />
            <YAxis />
            <Tooltip labelFormatter={(value) => new Date(value).toLocaleString()} />
            <Legend />
            <Line type="monotone" dataKey="ndcg_at_10" stroke="#8884d8" name="NDCG@10" />
            <Line type="monotone" dataKey="recall_at_10" stroke="#82ca9d" name="Recall@10" />
            <Line type="monotone" dataKey="mrr_at_10" stroke="#ff7300" name="MRR@10" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div>
        <h3>Experiment History</h3>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ backgroundColor: "#f5f5f5" }}>
              <th style={{ padding: "10px", border: "1px solid #ddd" }}>Timestamp</th>
              <th style={{ padding: "10px", border: "1px solid #ddd" }}>Experiment</th>
              <th style={{ padding: "10px", border: "1px solid #ddd" }}>Alpha</th>
              <th style={{ padding: "10px", border: "1px solid #ddd" }}>NDCG@10</th>
              <th style={{ padding: "10px", border: "1px solid #ddd" }}>Recall@10</th>
              <th style={{ padding: "10px", border: "1px solid #ddd" }}>MRR@10</th>
              <th style={{ padding: "10px", border: "1px solid #ddd" }}>Queries</th>
            </tr>
          </thead>
          <tbody>
            {experiments.map((exp, index) => (
              <tr key={index}>
                <td style={{ padding: "10px", border: "1px solid #ddd" }}>{new Date(exp.timestamp).toLocaleString()}</td>
                <td style={{ padding: "10px", border: "1px solid #ddd" }}>{exp.experiment_name}</td>
                <td style={{ padding: "10px", border: "1px solid #ddd" }}>{exp.alpha}</td>
                <td style={{ padding: "10px", border: "1px solid #ddd" }}>{exp.ndcg_at_10.toFixed(3)}</td>
                <td style={{ padding: "10px", border: "1px solid #ddd" }}>{exp.recall_at_10.toFixed(3)}</td>
                <td style={{ padding: "10px", border: "1px solid #ddd" }}>{exp.mrr_at_10.toFixed(3)}</td>
                <td style={{ padding: "10px", border: "1px solid #ddd" }}>{exp.query_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default EvaluationPage;