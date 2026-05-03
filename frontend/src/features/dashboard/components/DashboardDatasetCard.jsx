import { Descriptions, Progress } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

export function DashboardDatasetCard({ datasetSummary }) {
  const totals = datasetSummary?.totals;
  const trainImages = datasetSummary?.splits?.train?.image_count ?? 0;
  const testImages = datasetSummary?.splits?.test?.image_count ?? 0;
  const totalImages = totals?.image_count ?? 0;
  const trainRatio = totalImages > 0 ? Math.round((trainImages / totalImages) * 100) : 0;

  return (
    <PageSection
      title="Kondisi Dataset"
      subtitle="Ringkasan distribusi dataset train dan test yang sedang dipakai backend."
    >
      <Descriptions column={1} size="small">
        <Descriptions.Item label="Root Dataset">
          {datasetSummary?.root_dir ?? "-"}
        </Descriptions.Item>
        <Descriptions.Item label="Total Gambar">
          {totals?.image_count ?? 0}
        </Descriptions.Item>
        <Descriptions.Item label="Total Label File">
          {totals?.label_file_count ?? 0}
        </Descriptions.Item>
        <Descriptions.Item label="Total Anotasi">
          {totals?.annotation_count ?? 0}
        </Descriptions.Item>
      </Descriptions>
      <Progress
        percent={trainRatio}
        success={{ percent: 100 - trainRatio }}
        format={() => `Train ${trainImages} | Test ${testImages}`}
      />
    </PageSection>
  );
}
