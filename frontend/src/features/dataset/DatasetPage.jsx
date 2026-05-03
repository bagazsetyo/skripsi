import { Alert, Button, Result, Space, Spin, Typography } from "antd";
import { ReloadOutlined } from "@ant-design/icons";
import { DatasetClassTable } from "./components/DatasetClassTable";
import { DatasetSplitTable } from "./components/DatasetSplitTable";
import { DatasetSummaryCards } from "./components/DatasetSummaryCards";
import { DatasetValidationPanel } from "./components/DatasetValidationPanel";
import { useDatasetOverview } from "./hooks/useDatasetOverview";

export function DatasetPage() {
  const { classes, summary, validation, isLoading, isError, errors, refetchAll } =
    useDatasetOverview();

  if (isLoading) {
    return (
      <div className="page-loading">
        <Spin size="large" />
        <Typography.Text type="secondary">
          Memuat informasi dataset...
        </Typography.Text>
      </div>
    );
  }

  if (isError) {
    return (
      <Result
        status="error"
        title="Gagal memuat halaman dataset"
        subTitle={errors[0]?.message || "Terjadi kesalahan saat mengambil data dataset."}
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
        <Typography.Title level={2}>Dataset</Typography.Title>
        <Typography.Paragraph type="secondary">
          Halaman ini akan menampilkan statistik dataset, daftar kelas, dan hasil validasi data.
        </Typography.Paragraph>
      </div>

      <Space wrap>
        <Button icon={<ReloadOutlined />} onClick={refetchAll}>
          Refresh Dataset
        </Button>
      </Space>

      <DatasetSummaryCards summary={summary} validation={validation} />

      <Alert
        type="info"
        showIcon
        message="Sumber data backend"
        description={`Root dataset: ${summary?.root_dir ?? "-"}`}
      />

      <DatasetSplitTable summary={summary} />

      <DatasetClassTable summary={summary} classes={classes} />

      <DatasetValidationPanel validation={validation} />

      <Alert
        type="success"
        showIcon
        message="Halaman dataset sudah tersambung ke backend"
        description="Data kelas, ringkasan split, dan hasil validasi sekarang diambil langsung dari endpoint backend."
      />
    </div>
  );
}
