import { Navigate, createBrowserRouter } from "react-router-dom";
import App from "../layout/App";
import { DashboardPage } from "../../features/dashboard/DashboardPage";
import { DatasetPage } from "../../features/dataset/DatasetPage";
import { TrainingPage } from "../../features/training/TrainingPage";
import { PredictionPage } from "../../features/prediction/PredictionPage";
import { UserGuidePage } from "../../features/guide/UserGuidePage";
import { MethodPage } from "../../features/method/MethodPage";
import { AdminRoute } from "../../features/auth/AdminRoute";
import { LoginPage } from "../../features/auth/LoginPage";
import { NotFoundPage } from "../../features/errors/NotFoundPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { path: "", element: <Navigate to="/prediction" replace /> },
      { path: "prediction", element: <PredictionPage /> },
      { path: "guide", element: <UserGuidePage /> },
      { path: "method", element: <MethodPage /> },
      { path: "login", element: <LoginPage /> },
      {
        element: <AdminRoute />,
        children: [
          { path: "dashboard", element: <DashboardPage /> },
          { path: "dataset", element: <DatasetPage /> },
          { path: "training", element: <TrainingPage /> },
        ],
      },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
]);
