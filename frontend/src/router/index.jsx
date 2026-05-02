import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "../layouts/AppShell";
import { DashboardPage } from "../pages/DashboardPage";
import { DatasetPage } from "../pages/DatasetPage";
import { TrainingPage } from "../pages/TrainingPage";
import { PredictionPage } from "../pages/PredictionPage";
import { NotFoundPage } from "../pages/NotFoundPage";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/dataset" element={<DatasetPage />} />
          <Route path="/training" element={<TrainingPage />} />
          <Route path="/prediction" element={<PredictionPage />} />
        </Route>
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </BrowserRouter>
  );
}
