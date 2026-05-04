import { Layout, Typography } from "antd";
import { Outlet, useLocation } from "react-router-dom";
import { AppNavBar } from "./NavBar";
import "./styles.css";

const { Header, Content } = Layout;

function App() {
  const location = useLocation();

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <AppNavBar />
      <Layout>
        <Header className="app-header">
          <div>
            <Typography.Text className="header-kicker">Prototype System</Typography.Text>
            <Typography.Title level={4} className="header-title">
              {location.pathname === "/dataset"
                ? "Dataset Workspace"
                : location.pathname === "/training"
                  ? "Training & Model Workspace"
                  : location.pathname === "/prediction"
                    ? "Prediction Workspace"
                    : location.pathname === "/guide"
                      ? "Panduan Penggunaan Aplikasi"
                    : "Implementasi Aplikasi Skripsi"}
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

export default App;
