import { Navigate, Outlet, useLocation } from "react-router-dom";
import { Spin, Typography } from "antd";
import { useAuth } from "./AuthProvider";

export function AdminRoute() {
  const { isAuthenticated, isHydrating } = useAuth();
  const location = useLocation();

  if (isHydrating) {
    return (
      <div className="page-loading">
        <Spin size="large" />
        <Typography.Text type="secondary">Memeriksa sesi admin...</Typography.Text>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  return <Outlet />;
}
