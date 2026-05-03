import { Alert, Button, Result, Space, Spin, Typography } from "antd";
import { ReloadOutlined } from "@ant-design/icons";
import { ActiveModelCard } from "./components/ActiveModelCard";
import { ModelsTable } from "./components/ModelsTable";
import { TrainingRunForm } from "./components/TrainingRunForm";
import { TrainingRunsTable } from "./components/TrainingRunsTable";
import { useTrainingWorkspace } from "./hooks/useTrainingWorkspace";

export function TrainingPage() {
  const {
    config,
    runs,
    models,
    activeModel,
    isLoading,
    isError,
    errors,
    createRun,
    isCreatingRun,
    activateModel,
    isActivatingModel,
    refetchAll,
  } = useTrainingWorkspace();

  if (isLoading) {
    return (
      <div className="page-loading">
        <Spin size="large" />
        <Typography.Text type="secondary">Memuat workspace training...</Typography.Text>
      </div>
    );
  }

  if (isError) {
    return (
      <Result
        status="error"
        title="Gagal memuat halaman training"
        subTitle={errors[0]?.message || "Terjadi kesalahan saat mengambil data training."}
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
        <Typography.Title level={2}>Training & Model</Typography.Title>
        <Typography.Paragraph type="secondary">
          Halaman ini akan memuat form training subset kelas, daftar model, dan aktivasi model.
        </Typography.Paragraph>
      </div>

      <Space wrap>
        <Button icon={<ReloadOutlined />} onClick={refetchAll}>
          Refresh Workspace
        </Button>
      </Space>

      <ActiveModelCard activeModel={activeModel} onRefresh={refetchAll} />

      <TrainingRunForm
        config={config}
        isSubmitting={isCreatingRun}
        onSubmit={createRun}
      />

      <ModelsTable
        models={models}
        onActivate={activateModel}
        isActivating={isActivatingModel}
      />

      <TrainingRunsTable runs={runs} />

      <Alert
        type="info"
        showIcon
        message="Training workspace tersambung ke backend"
        description="Form training, daftar model, model aktif, dan riwayat training run sekarang menggunakan endpoint backend yang sudah dibuat."
      />
    </div>
  );
}
