import { Alert, Typography } from "antd";
import { PageSection } from "../../app/shared/PageSection";

export function PredictionPage() {
  return (
    <div className="page-stack">
      <div>
        <Typography.Title level={2}>Prediksi</Typography.Title>
        <Typography.Paragraph type="secondary">
          Halaman ini akan menjadi area upload gambar, preview, dan hasil deteksi bounding box.
        </Typography.Paragraph>
      </div>
      <PageSection
        title="Prediction Workspace"
        subtitle="Endpoint prediksi dan model aktif sudah ada di backend."
      >
        <Alert
          type="success"
          showIcon
          message="Fondasi halaman prediksi siap"
          description="UI detail untuk upload, preview, dan visualisasi hasil akan ditambahkan pada step berikutnya."
        />
      </PageSection>
    </div>
  );
}
