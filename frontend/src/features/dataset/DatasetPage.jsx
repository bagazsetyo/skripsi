import { Alert, Typography } from "antd";
import { PageSection } from "../../app/shared/PageSection";

export function DatasetPage() {
  return (
    <div className="page-stack">
      <div>
        <Typography.Title level={2}>Dataset</Typography.Title>
        <Typography.Paragraph type="secondary">
          Halaman ini akan menampilkan statistik dataset, daftar kelas, dan hasil validasi data.
        </Typography.Paragraph>
      </div>
      <PageSection
        title="Dataset Overview"
        subtitle="Endpoint backend untuk dataset sudah siap, tinggal dihubungkan ke React Query."
      >
        <Alert
          type="info"
          showIcon
          message="Scaffold dataset page sudah siap"
          description="Langkah berikutnya adalah menghubungkan /dataset/summary, /dataset/classes, dan /dataset/validation ke UI."
        />
      </PageSection>
    </div>
  );
}
