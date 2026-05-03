import { Button, Descriptions, Tag } from "antd";
import { ReloadOutlined } from "@ant-design/icons";
import { PageSection } from "../../../app/shared/PageSection";

export function ActivePredictionModelCard({ activeModel, onRefresh }) {
  return (
    <PageSection
      title="Model Aktif Untuk Prediksi"
      subtitle="Model ini dipakai backend saat tombol prediksi dijalankan."
      extra={
        <Button icon={<ReloadOutlined />} onClick={onRefresh}>
          Refresh
        </Button>
      }
    >
      <Descriptions column={1} size="small">
        <Descriptions.Item label="Display Name">
          {activeModel?.display_name ?? "-"}
        </Descriptions.Item>
        <Descriptions.Item label="Version">
          {activeModel?.version ?? "-"}
        </Descriptions.Item>
        <Descriptions.Item label="Status">
          <Tag color={activeModel?.is_active ? "success" : "default"}>
            {activeModel?.is_active ? "Active" : activeModel?.status ?? "-"}
          </Tag>
        </Descriptions.Item>
        <Descriptions.Item label="Classes">
          {activeModel?.class_names?.length ?? 0} kelas
        </Descriptions.Item>
      </Descriptions>
    </PageSection>
  );
}
