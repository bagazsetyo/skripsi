import { Alert, Button, Col, Result, Row, Space, Spin, Typography } from "antd";
import { ReloadOutlined } from "@ant-design/icons";
import { DashboardActiveModelCard } from "./components/DashboardActiveModelCard";
import { DashboardDatasetCard } from "./components/DashboardDatasetCard";
import { DashboardRecentRunsTable } from "./components/DashboardRecentRunsTable";
import { DashboardSummaryCards } from "./components/DashboardSummaryCards";
import { useDashboardOverview } from "./hooks/useDashboardOverview";

export function DashboardPage() {
  const {
    datasetSummary,
    models,
    trainingRuns,
    activeModel,
    isLoading,
    isError,
    errors,
    refetchAll,
  } = useDashboardOverview();

  if (isLoading) {
    return (
      <div className="page-loading">
        <Spin size="large" />
        <Typography.Text type="secondary">Memuat ringkasan dashboard...</Typography.Text>
      </div>
    );
  }

  if (isError) {
    return (
      <Result
        status="error"
        title="Gagal memuat dashboard"
        subTitle={errors[0]?.message || "Terjadi kesalahan saat mengambil data dashboard."}
        extra={
          <Button type="primary" icon={<ReloadOutlined />} onClick={refetchAll}>
            Coba Lagi
          </Button>
        }
      />
    );
  }

  return (
    <div className="page-stack">
      <div>
        <Typography.Title level={2}>Dashboard</Typography.Title>
        <Typography.Paragraph type="secondary">
          Ringkasan sistem, model aktif, dan kondisi dataset akan ditampilkan di halaman ini.
        </Typography.Paragraph>
      </div>

      <Space wrap>
        <Button icon={<ReloadOutlined />} onClick={refetchAll}>
          Refresh Dashboard
        </Button>
      </Space>

      <DashboardSummaryCards
        datasetSummary={datasetSummary}
        models={models}
        trainingRuns={trainingRuns}
        activeModel={activeModel}
      />

      <Row gutter={[16, 16]}>
        <Col xs={24} xl={10}>
          <DashboardDatasetCard datasetSummary={datasetSummary} />
        </Col>
        <Col xs={24} xl={14}>
          <DashboardActiveModelCard activeModel={activeModel} />
        </Col>
      </Row>

      <DashboardRecentRunsTable trainingRuns={trainingRuns} />

      <Alert
        type="success"
        showIcon
        message="Dashboard sudah tersambung ke backend"
        description="Ringkasan dataset, model aktif, jumlah model, dan training terakhir sekarang diambil dari endpoint backend."
      />
    </div>
  );
}
