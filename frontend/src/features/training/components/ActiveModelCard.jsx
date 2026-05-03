import { Button, Descriptions, Tag } from "antd";
import { ReloadOutlined } from "@ant-design/icons";
import { PageSection } from "../../../app/shared/PageSection";

export function ActiveModelCard({ activeModel, onRefresh }) {
  return (
    <PageSection
      title="Model Aktif"
      subtitle="Model ini yang saat ini dipakai backend untuk prediksi."
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
        <Descriptions.Item label="Model Name">
          {activeModel?.model_name ?? "-"}
        </Descriptions.Item>
        <Descriptions.Item label="Status">
          <Tag color={activeModel?.status === "ready" ? "success" : "default"}>
            {activeModel?.status ?? "-"}
          </Tag>
        </Descriptions.Item>
      </Descriptions>
    </PageSection>
  );
}
