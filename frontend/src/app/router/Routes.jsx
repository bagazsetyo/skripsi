import { createBrowserRouter } from "react-router-dom";
import App from "../layout/App";
import { DashboardPage } from "../../features/dashboard/DashboardPage";
import { DatasetPage } from "../../features/dataset/DatasetPage";
import { TrainingPage } from "../../features/training/TrainingPage";
import { PredictionPage } from "../../features/prediction/PredictionPage";
import { NotFoundPage } from "../../features/errors/NotFoundPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { path: "", element: <DashboardPage /> },
      { path: "dashboard", element: <DashboardPage /> },
      { path: "dataset", element: <DatasetPage /> },
      { path: "training", element: <TrainingPage /> },
      { path: "prediction", element: <PredictionPage /> },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
]);
