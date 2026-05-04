import { Button, Space, Table, Tag } from "antd";
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
      />
    </PageSection>
  );
}
