import { useState, useEffect } from "react";
import axios from "axios";

function DebugPage() {
  const [logs, setLogs] = useState([]);
  const [filteredLogs, setFilteredLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [severityFilter, setSeverityFilter] = useState('all');
  const [timeFilter, setTimeFilter] = useState('24h');

  useEffect(() => {
    fetchLogs();
  }, []);

  useEffect(() => {
    filterLogs();
  }, [logs, severityFilter, timeFilter]);

  const fetchLogs = async () => {
    try {
      const response = await axios.get('http://localhost:8001/logs?limit=500');
      setLogs(response.data);
    } catch (error) {
      console.error('Error fetching logs:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterLogs = () => {
    let filtered = [...logs];

    // Time filter
    const now = new Date();
    let hoursBack = 24;
    if (timeFilter === '1h') hoursBack = 1;
    else if (timeFilter === '6h') hoursBack = 6;
    else if (timeFilter === '24h') hoursBack = 24;

    const cutoffTime = new Date(now.getTime() - (hoursBack * 60 * 60 * 1000));
    filtered = filtered.filter(log => new Date(log.created_at) > cutoffTime);

    // Severity filter (we'll simulate this with latency thresholds)
    if (severityFilter === 'error') {
      filtered = filtered.filter(log => log.latency_ms > 1000); // Slow queries as "errors"
    } else if (severityFilter === 'warning') {
      filtered = filtered.filter(log => log.latency_ms > 500 && log.latency_ms <= 1000);
    } else if (severityFilter === 'info') {
      filtered = filtered.filter(log => log.latency_ms <= 500);
    }

    setFilteredLogs(filtered);
  };

  const getSeverityColor = (latency) => {
    if (latency > 1000) return '#ff4444'; // error - red
    if (latency > 500) return '#ffaa00'; // warning - orange
    return '#44aa44'; // info - green
  };

  const getSeverityLabel = (latency) => {
    if (latency > 1000) return 'ERROR';
    if (latency > 500) return 'WARNING';
    return 'INFO';
  };

  if (loading) {
    return <div>Loading debug logs...</div>;
  }

  return (
    <div>
      <h2>Debug Dashboard</h2>

      <div style={{ marginBottom: "20px", display: "flex", gap: "20px" }}>
        <div>
          <label>Time Range: </label>
          <select value={timeFilter} onChange={(e) => setTimeFilter(e.target.value)}>
            <option value="1h">Last Hour</option>
            <option value="6h">Last 6 Hours</option>
            <option value="24h">Last 24 Hours</option>
          </select>
        </div>

        <div>
          <label>Severity: </label>
          <select value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}>
            <option value="all">All</option>
            <option value="error">Errors</option>
            <option value="warning">Warnings</option>
            <option value="info">Info</option>
          </select>
        </div>

        <button onClick={fetchLogs} style={{ padding: "5px 10px" }}>
          Refresh Logs
        </button>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <strong>Total Logs:</strong> {filteredLogs.length} (filtered from {logs.length})
      </div>

      <div style={{ maxHeight: "600px", overflowY: "auto", border: "1px solid #ddd" }}>
        {filteredLogs.map((log, index) => (
          <div
            key={index}
            style={{
              padding: "10px",
              borderBottom: "1px solid #eee",
              backgroundColor: index % 2 === 0 ? '#f9f9f9' : 'white'
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <strong>Query:</strong> "{log.query}"
              </div>
              <div style={{
                color: getSeverityColor(log.latency_ms),
                fontWeight: "bold"
              }}>
                {getSeverityLabel(log.latency_ms)}
              </div>
            </div>
            <div style={{ marginTop: "5px", fontSize: "0.9em", color: "#666" }}>
              <span><strong>Latency:</strong> {log.latency_ms.toFixed(2)}ms</span> |
              <span><strong>Results:</strong> {log.result_count}</span> |
              <span><strong>Time:</strong> {new Date(log.created_at).toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>

      {filteredLogs.length === 0 && (
        <div style={{ textAlign: "center", padding: "20px", color: "#666" }}>
          No logs match the current filters.
        </div>
      )}
    </div>
  );
}

export default DebugPage;