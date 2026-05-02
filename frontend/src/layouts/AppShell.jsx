import { DatabaseOutlined, DashboardOutlined, RadarChartOutlined, RocketOutlined } from "@ant-design/icons";
import { Layout, Typography } from "antd";
import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { SidebarNav } from "../components/navigation/SidebarNav";

const { Header, Sider, Content } = Layout;

const menuItems = [
  { key: "/dashboard", icon: <DashboardOutlined />, label: "Dashboard" },
  { key: "/dataset", icon: <DatabaseOutlined />, label: "Dataset" },
  { key: "/training", icon: <RocketOutlined />, label: "Training & Model" },
  { key: "/prediction", icon: <RadarChartOutlined />, label: "Prediksi" },
];

export function AppShell() {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <Layout style={{ minHeight: "100vh" }}>
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
        <SidebarNav
          items={menuItems}
          selectedKey={location.pathname}
          onSelect={(key) => navigate(key)}
        />
      </Sider>
      <Layout>
        <Header className="app-header">
          <div>
            <Typography.Text className="header-kicker">Prototype System</Typography.Text>
            <Typography.Title level={4} className="header-title">
              Implementasi Aplikasi Skripsi
            </Typography.Title>
          </div>
        </Header>
        <Content className="app-content">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
