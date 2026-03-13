import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import KpiPage from "./pages/KpiPage";

function App() {
  return (
    <BrowserRouter>
      <div style={{ padding: "20px", fontFamily: "Arial" }}>

        <h1>Hybrid Search Dashboard</h1>

        <nav style={{ marginBottom: "20px" }}>
          <Link to="/">Search</Link> |{" "}
          <Link to="/kpi">KPI Dashboard</Link>
        </nav>

        <Routes>
          <Route path="/" element={<SearchPage />} />
          <Route path="/kpi" element={<KpiPage />} />
        </Routes>

      </div>
    </BrowserRouter>
  );
}

export default App;
