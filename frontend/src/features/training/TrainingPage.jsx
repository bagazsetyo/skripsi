import { Alert, Typography } from "antd";
import { PageSection } from "../../app/shared/PageSection";

export function TrainingPage() {
  return (
    <div className="page-stack">
      <div>
        <Typography.Title level={2}>Training & Model</Typography.Title>
        <Typography.Paragraph type="secondary">
          Halaman ini akan memuat form training subset kelas, daftar model, dan aktivasi model.
        </Typography.Paragraph>
      </div>
      <PageSection
        title="Training Workspace"
        subtitle="Kontrak API training sudah siap. UI tinggal dibangun di atas struktur ini."
      >
        <Alert
          type="warning"
          showIcon
          message="Form training belum diimplementasikan"
          description="Struktur folder dan route sudah disiapkan agar implementasi fitur bisa langsung masuk tanpa mengubah fondasi."
        />
      </PageSection>
    </div>
  );
}
