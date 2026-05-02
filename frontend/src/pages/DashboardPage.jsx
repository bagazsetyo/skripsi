import { Col, Row, Statistic, Tag, Typography } from "antd";
import { PageSection } from "../components/ui/PageSection";

export function DashboardPage() {
  return (
    <div className="page-stack">
      <div>
        <Typography.Title level={2}>Dashboard</Typography.Title>
        <Typography.Paragraph type="secondary">
          Ringkasan sistem, model aktif, dan kondisi dataset akan ditampilkan di halaman ini.
        </Typography.Paragraph>
      </div>
      <Row gutter={[16, 16]}>
        <Col xs={24} md={12} xl={6}>
          <PageSection title="Model Aktif">
            <Statistic value="yolos" />
            <Tag color="success">Siap dipakai</Tag>
          </PageSection>
        </Col>
        <Col xs={24} md={12} xl={6}>
          <PageSection title="Total Kelas">
            <Statistic value={21} suffix="kelas" />
          </PageSection>
        </Col>
        <Col xs={24} md={12} xl={6}>
          <PageSection title="Dataset">
            <Statistic value={2100} suffix="gambar" />
          </PageSection>
        </Col>
        <Col xs={24} md={12} xl={6}>
          <PageSection title="Training Runs">
            <Statistic value={0} />
          </PageSection>
        </Col>
      </Row>
    </div>
  );
}
