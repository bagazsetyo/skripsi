import { Descriptions, Tag } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

export function DashboardActiveModelCard({ activeModel }) {
  const metrics = activeModel?.metrics;

  return (
    <PageSection
      title="Ringkasan Model Aktif"
      subtitle="Snapshot model yang sedang dipakai untuk prediksi."
    >
      <Descriptions column={1} size="small">
        <Descriptions.Item label="Display Name">
          {activeModel?.display_name ?? "-"}
        </Descriptions.Item>
        <Descriptions.Item label="Version">
          {activeModel?.version ?? "-"}
        </Descriptions.Item>
        <Descriptions.Item label="Status">
          <Tag color={activeModel?.status === "ready" ? "success" : "default"}>
            {activeModel?.status ?? "-"}
          </Tag>
        </Descriptions.Item>
        <Descriptions.Item label="Jumlah Kelas">
          {activeModel?.class_names?.length ?? 0}
        </Descriptions.Item>
        <Descriptions.Item label="mAP@0.5">
          {metrics?.mAP_50 != null ? metrics.mAP_50.toFixed(4) : "-"}
        </Descriptions.Item>
        <Descriptions.Item label="Precision">
          {metrics?.precision != null ? metrics.precision.toFixed(4) : "-"}
        </Descriptions.Item>
        <Descriptions.Item label="Recall">
          {metrics?.recall != null ? metrics.recall.toFixed(4) : "-"}
        </Descriptions.Item>
      </Descriptions>
    </PageSection>
  );
}
