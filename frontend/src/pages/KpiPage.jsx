import { LineChart, Line, XAxis, YAxis, Tooltip, BarChart, Bar } from "recharts";

const data = [
  { time: "1", volume: 4, latency: 120 },
  { time: "2", volume: 6, latency: 110 },
  { time: "3", volume: 3, latency: 140 }
];

function KpiPage() {

  return (
    <div>

      <h2>KPI Dashboard</h2>

      <h3>Search Volume</h3>

      <LineChart width={500} height={300} data={data}>
        <XAxis dataKey="time"/>
        <YAxis/>
        <Tooltip/>
        <Line type="monotone" dataKey="volume"/>
      </LineChart>

      <h3>Latency</h3>

      <LineChart width={500} height={300} data={data}>
        <XAxis dataKey="time"/>
        <YAxis/>
        <Tooltip/>
        <Line type="monotone" dataKey="latency"/>
      </LineChart>

      <h3>Top Queries</h3>

      <BarChart width={500} height={300} data={data}>
        <XAxis dataKey="time"/>
        <YAxis/>
        <Tooltip/>
        <Bar dataKey="volume"/>
      </BarChart>

    </div>
  );
}

export default KpiPage;