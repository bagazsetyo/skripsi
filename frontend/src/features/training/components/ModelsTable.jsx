import { Button, Space, Table, Tag, Typography } from "antd";
import { CheckCircleOutlined } from "@ant-design/icons";
import { PageSection } from "../../../app/shared/PageSection";

function formatMetric(value, digits = 3) {
  return typeof value === "number" ? value.toFixed(digits) : "-";
}

function getLastLoss(metrics) {
  const history = metrics?.loss_history;
  if (!Array.isArray(history) || history.length === 0) {
    return null;
  }

  return history[history.length - 1]?.loss ?? null;
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
    title: "mAP@0.5",
    dataIndex: ["metrics", "mAP_50"],
    key: "mAP_50",
    width: 110,
    render: (value) => formatMetric(value),
  },
  {
    title: "Precision",
    dataIndex: ["metrics", "precision"],
    key: "precision",
    width: 110,
    render: (value) => formatMetric(value),
  },
  {
    title: "Recall",
    dataIndex: ["metrics", "recall"],
    key: "recall",
    width: 110,
    render: (value) => formatMetric(value),
  },
  {
    title: "Mean IoU",
    dataIndex: ["metrics", "mean_iou"],
    key: "mean_iou",
    width: 110,
    render: (value) => formatMetric(value),
  },
  {
    title: "Loss Akhir",
    dataIndex: "metrics",
    key: "loss_final",
    width: 120,
    render: (metrics) => formatMetric(getLastLoss(metrics)),
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
      subtitle={
        <Space direction="vertical" size={2}>
          <span>Model hasil training yang tersimpan dan bisa dipilih sebagai model aktif.</span>
          <Typography.Text type="secondary">
            Nilai yang lebih baik umumnya: `mAP`, `precision`, `recall`, dan `IoU` makin besar. `Loss` justru makin kecil makin baik.
          </Typography.Text>
        </Space>
      }
    >
      <Table
        rowKey="id"
        columns={columns(onActivate, isActivating)}
        dataSource={models}
        pagination={{ pageSize: 5, showSizeChanger: false }}
        size="middle"
        scroll={{ x: 1700 }}
      />
    </PageSection>
  );
}
