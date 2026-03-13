import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar } from 'recharts';
import axios from 'axios';

function KpiPage() {
  const [volumeData, setVolumeData] = useState([]);
  const [latencyData, setLatencyData] = useState([]);
  const [topQueriesData, setTopQueriesData] = useState([]);
  const [experimentsData, setExperimentsData] = useState([]);

  useEffect(() => {
    fetchKPIData();
  }, []);

  const fetchKPIData = async () => {
    try {
      // Fetch logs for volume and latency
      const logsResponse = await axios.get('http://localhost:8000/logs?limit=1000');
      const logs = logsResponse.data;

      // Process volume data (requests per day)
      const volumeMap = {};
      logs.forEach(log => {
        const date = new Date(log.created_at).toISOString().split('T')[0];
        volumeMap[date] = (volumeMap[date] || 0) + 1;
      });
      const volume = Object.entries(volumeMap).map(([date, requests]) => ({
        date,
        requests
      })).sort((a, b) => a.date.localeCompare(b.date));
      setVolumeData(volume);

      // Process latency data (average per hour)
      const latencyMap = {};
      logs.forEach(log => {
        const hour = new Date(log.created_at).getHours();
        if (!latencyMap[hour]) latencyMap[hour] = [];
        latencyMap[hour].push(log.latency_ms);
      });
      const latency = Object.entries(latencyMap).map(([hour, latencies]) => ({
        time: `${hour}:00`,
        latency: latencies.reduce((a, b) => a + b, 0) / latencies.length
      })).sort((a, b) => parseInt(a.time) - parseInt(b.time));
      setLatencyData(latency);

      // Process top queries
      const queryCount = {};
      logs.forEach(log => {
        queryCount[log.query] = (queryCount[log.query] || 0) + 1;
      });
      const topQueries = Object.entries(queryCount)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 10)
        .map(([query, count]) => ({ query, count }));
      setTopQueriesData(topQueries);

      // Fetch experiments
      const experimentsResponse = await axios.get('http://localhost:8000/experiments');
      setExperimentsData(experimentsResponse.data);

    } catch (error) {
      console.error('Error fetching KPI data:', error);
      // Fallback to sample data
      setVolumeData([
        { date: '2024-01-01', requests: 120 },
        { date: '2024-01-02', requests: 150 },
        { date: '2024-01-03', requests: 180 },
      ]);
      setLatencyData([
        { time: '00:00', latency: 0.5 },
        { time: '06:00', latency: 0.4 },
        { time: '12:00', latency: 0.6 },
      ]);
      setTopQueriesData([
        { query: 'machine learning', count: 50 },
        { query: 'AI', count: 40 },
        { query: 'neural networks', count: 30 },
      ]);
    }
  };

  return (
    <div className="kpi-page">
      <h1>KPIs Dashboard</h1>

      <div className="chart-container">
        <h2>Search Volume</h2>
        <LineChart width={600} height={300} data={volumeData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="requests" stroke="#8884d8" />
        </LineChart>
      </div>

      <div className="chart-container">
        <h2>Average Latency (ms)</h2>
        <LineChart width={600} height={300} data={latencyData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="latency" stroke="#82ca9d" />
        </LineChart>
      </div>

      <div className="chart-container">
        <h2>Top Queries</h2>
        <BarChart width={600} height={300} data={topQueriesData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="query" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#ffc658" />
        </BarChart>
      </div>

      <div className="chart-container">
        <h2>Experiment Results (nDCG@10)</h2>
        <LineChart width={600} height={300} data={experimentsData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="experiment" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="ndcg@10" stroke="#ff7300" />
        </LineChart>
      </div>
    </div>
  );
}

export default KpiPage;
          <Line type="monotone" dataKey="latency" stroke="#82ca9d" />
        </LineChart>
      </div>

      <div className="chart-container">
        <h2>Top Queries</h2>
        <BarChart width={600} height={300} data={topQueriesData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="query" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#ffc658" />
        </BarChart>
      </div>
    </div>
  );
}

export default KpiPage;