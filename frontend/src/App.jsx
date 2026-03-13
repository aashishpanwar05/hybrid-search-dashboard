import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import SearchPage from "./pages/SearchPage";
import KpiPage from "./pages/KpiPage";
import EvaluationPage from "./pages/EvaluationPage";
import DebugPage from "./pages/DebugPage";

function App() {
  return (
    <BrowserRouter>
      <div style={{ padding: "20px", fontFamily: "Arial" }}>

        <h1>Hybrid Search Dashboard</h1>

        <nav style={{ marginBottom: "20px" }}>
          <Link to="/">Search</Link> |{" "}
          <Link to="/kpi">KPI Dashboard</Link> |{" "}
          <Link to="/evaluation">Evaluation</Link> |{" "}
          <Link to="/debug">Debug</Link>
        </nav>

        <Routes>
          <Route path="/" element={<SearchPage />} />
          <Route path="/kpi" element={<KpiPage />} />
          <Route path="/evaluation" element={<EvaluationPage />} />
          <Route path="/debug" element={<DebugPage />} />
        </Routes>

      </div>
    </BrowserRouter>
  );
}

export default App;
