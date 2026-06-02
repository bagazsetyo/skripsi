import { Button, Descriptions, Divider, Space, Table, Tag, Typography } from "antd";
import { CheckCircleOutlined } from "@ant-design/icons";
import { PageSection } from "../../../app/shared/PageSection";

function getLastLoss(metrics) {
  const history = metrics?.loss_history;
  if (!Array.isArray(history) || history.length === 0) {
    return "-";
  }

  const value = history[history.length - 1]?.loss;
  return typeof value === "number" ? value.toFixed(3) : "-";
}

const columns = (onActivate, loading) => [
  { title: "ID", dataIndex: "id", key: "id", width: 80 },
  { title: "Display Name", dataIndex: "display_name", key: "display_name", width: 220 },
  { title: "Version", dataIndex: "version", key: "version", width: 160 },
  { title: "Model Name", dataIndex: "model_name", key: "model_name", width: 180 },
  {
    title: "Status",
    dataIndex: "status",
    key: "status",
    width: 120,
    render: (value) => <Tag color={value === "ready" ? "success" : "default"}>{value}</Tag>,
  },
  {
    title: "Active",
    dataIndex: "is_active",
    key: "is_active",
    width: 100,
    render: (value) =>
      value ? <Tag color="success">Active</Tag> : <Tag color="default">Idle</Tag>,
  },
  {
    title: "Classes",
    dataIndex: "class_names",
    key: "class_names",
    width: 120,
    render: (value) => `${value?.length ?? 0} kelas`,
  },
  {
    title: "Loss Akhir",
    dataIndex: "metrics",
    key: "loss_final",
    width: 110,
    render: (metrics) => getLastLoss(metrics),
  },
  {
    title: "Action",
    key: "action",
    width: 140,
    render: (_, record) => (
      <Space>
        <Button
          type={record.is_active ? "default" : "primary"}
          size="small"
          icon={<CheckCircleOutlined />}
          loading={loading}
          disabled={record.is_active}
          onClick={() => onActivate(record.id)}
        >
          Aktifkan
        </Button>
      </Space>
    ),
  },
];

export function ModelsTable({ models, onActivate, isActivating }) {
  return (
    <PageSection
      title="Daftar Model"
      subtitle="Model hasil training yang tersimpan dan bisa dipilih sebagai model aktif."
    >
      <Table
        rowKey="id"
        columns={columns(onActivate, isActivating)}
        dataSource={models}
        pagination={{ pageSize: 5, showSizeChanger: false }}
        size="middle"
        scroll={{ x: 1200 }}
        expandable={{
          expandedRowRender: (record) => (
            <Space direction="vertical" size="middle" style={{ width: "100%" }}>
              <Descriptions size="small" column={2} bordered>
                <Descriptions.Item label="Path Model">{record.path}</Descriptions.Item>
                <Descriptions.Item label="Dibuat">{record.created_at || "-"}</Descriptions.Item>
                <Descriptions.Item label="Jumlah Kelas">
                  {record.class_names?.length ?? 0}
                </Descriptions.Item>
                <Descriptions.Item label="Source">
                  {record.config?.source || "-"}
                </Descriptions.Item>
              </Descriptions>

              <div>
                <Typography.Text strong>Daftar Kelas</Typography.Text>
                <div style={{ marginTop: 8 }}>
                  <Space size={[8, 8]} wrap>
                    {(record.class_names || []).map((className) => (
                      <Tag key={className}>{className}</Tag>
                    ))}
                  </Space>
                </div>
              </div>

              {record.metrics ? (
                <>
                  <Divider style={{ margin: "8px 0" }} />
                  <Descriptions size="small" column={4} bordered>
                    <Descriptions.Item label="Precision">
                      {typeof record.metrics?.precision === "number"
                        ? record.metrics.precision.toFixed(3)
                        : "-"}
                    </Descriptions.Item>
                    <Descriptions.Item label="Recall">
                      {typeof record.metrics?.recall === "number"
                        ? record.metrics.recall.toFixed(3)
                        : "-"}
                    </Descriptions.Item>
                    <Descriptions.Item label="mAP@0.5">
                      {typeof record.metrics?.mAP_50 === "number"
                        ? record.metrics.mAP_50.toFixed(3)
                        : "-"}
                    </Descriptions.Item>
                    <Descriptions.Item label="Mean IoU">
                      {typeof record.metrics?.mean_iou === "number"
                        ? record.metrics.mean_iou.toFixed(3)
                        : "-"}
                    </Descriptions.Item>
                  </Descriptions>
                </>
              ) : null}
            </Space>
          ),
        }}
      />
    </PageSection>
  );
}
