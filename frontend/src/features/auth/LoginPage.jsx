import { Button, Card, Col, Form, Input, Row, Typography, message } from "antd";
import { LockOutlined, UserOutlined } from "@ant-design/icons";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "./AuthProvider";

export function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  const handleFinish = async (values) => {
    try {
      await login(values);
      const nextPath = location.state?.from?.pathname || "/dashboard";
      navigate(nextPath, { replace: true });
    } catch (error) {
      message.error(error?.response?.data?.detail || "Login admin gagal");
    }
  };

  return (
    <div className="page-stack">
      <div>
        <Typography.Title level={2}>Login Admin</Typography.Title>
        <Typography.Paragraph type="secondary">
          Halaman ini digunakan untuk mengakses menu administrasi seperti dashboard,
          dataset, dan training model.
        </Typography.Paragraph>
      </div>

      <Row gutter={[20, 20]}>
        <Col xs={24} xl={10}>
          <Card className="page-card auth-login-card">
            <Typography.Title level={4}>Akses Admin</Typography.Title>
            <Typography.Paragraph type="secondary">
              Gunakan akun admin untuk mengelola dataset, menjalankan training, dan
              memilih model aktif.
            </Typography.Paragraph>
            <Form layout="vertical" onFinish={handleFinish}>
              <Form.Item
                label="Username"
                name="username"
                rules={[{ required: true, message: "Username wajib diisi" }]}
              >
                <Input prefix={<UserOutlined />} placeholder="Masukkan username admin" />
              </Form.Item>
              <Form.Item
                label="Password"
                name="password"
                rules={[{ required: true, message: "Password wajib diisi" }]}
              >
                <Input.Password
                  prefix={<LockOutlined />}
                  placeholder="Masukkan password admin"
                />
              </Form.Item>
              <Button type="primary" htmlType="submit" block>
                Login
              </Button>
            </Form>
          </Card>
        </Col>
        <Col xs={24} xl={14}>
          <Card className="page-card auth-login-hint-card">
            <Typography.Title level={4}>Menu yang Dilindungi</Typography.Title>
            <Typography.Paragraph>
              Setelah login berhasil, admin dapat mengakses:
            </Typography.Paragraph>
            <ul className="guide-inline-list">
              <li>Dashboard</li>
              <li>Dataset</li>
              <li>Training & Model</li>
            </ul>
            <Typography.Paragraph style={{ marginTop: 16 }}>
              Halaman publik tetap dapat diakses tanpa login:
            </Typography.Paragraph>
            <ul className="guide-inline-list">
              <li>Prediksi</li>
              <li>User Guide</li>
              <li>Cara Kerja YOLOS</li>
            </ul>
          </Card>
        </Col>
      </Row>
    </div>
  );
}
