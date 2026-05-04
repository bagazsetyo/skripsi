import {
  LoginOutlined,
  DatabaseOutlined,
  DashboardOutlined,
  DeploymentUnitOutlined,
  LogoutOutlined,
  RadarChartOutlined,
  RocketOutlined,
  ReadOutlined,
} from "@ant-design/icons";
import { Layout, Menu, Typography } from "antd";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../features/auth/AuthProvider";

const { Sider } = Layout;

export function AppNavBar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated, logout } = useAuth();

  const menuItems = [
    { key: "/prediction", icon: <RadarChartOutlined />, label: "Prediksi" },
    { key: "/guide", icon: <ReadOutlined />, label: "User Guide" },
    { key: "/method", icon: <DeploymentUnitOutlined />, label: "Cara Kerja YOLOS" },
    ...(isAuthenticated
      ? [
          { type: "divider" },
          { key: "/dashboard", icon: <DashboardOutlined />, label: "Dashboard" },
          { key: "/dataset", icon: <DatabaseOutlined />, label: "Dataset" },
          { key: "/training", icon: <RocketOutlined />, label: "Training & Model" },
          { key: "__logout__", icon: <LogoutOutlined />, label: "Logout Admin" },
        ]
      : [{ type: "divider" }, { key: "/login", icon: <LoginOutlined />, label: "Login Admin" }]),
  ];

  return (
    <Sider
      width={280}
      breakpoint="lg"
      collapsedWidth="0"
      style={{
        background: "linear-gradient(180deg, #073b3a 0%, #0f766e 50%, #164e63 100%)",
        boxShadow: "12px 0 36px rgba(6, 78, 59, 0.18)",
      }}
    >
      <div className="brand-block">
        <Typography.Text className="brand-kicker">Vision Transformer</Typography.Text>
        <Typography.Title level={3} className="brand-title">
          Traffic Sign Lab
        </Typography.Title>
        <Typography.Paragraph className="brand-copy">
          Deteksi dan klasifikasi rambu lalu lintas Indonesia berbasis YOLOS.
        </Typography.Paragraph>
      </div>
      <Menu
        mode="inline"
        selectedKeys={[location.pathname === "/" ? "/prediction" : location.pathname]}
        items={menuItems}
        onClick={({ key }) => {
          if (key === "__logout__") {
            logout();
            navigate("/prediction");
            return;
          }
          navigate(key);
        }}
        theme="dark"
        style={{
          background: "transparent",
          borderInlineEnd: "none",
          paddingInline: 12,
        }}
      />
    </Sider>
  );
}
