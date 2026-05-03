import { Table, Tag } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

const columns = [
  { title: "Run Name", dataIndex: "run_name", key: "run_name", width: 220 },
  {
    title: "Status",
    dataIndex: "status",
    key: "status",
    width: 120,
    render: (value) => {
      const color =
        value === "completed" ? "success" : value === "failed" ? "error" : value === "running" ? "processing" : "default";
      return <Tag color={color}>{value}</Tag>;
    },
  },
  {
    title: "Selected Classes",
    dataIndex: "selected_classes",
    key: "selected_classes",
    render: (value) => `${value?.length ?? 0} kelas`,
  },
  {
    title: "Started At",
    dataIndex: "started_at",
    key: "started_at",
    width: 220,
  },
  {
    title: "Error",
    dataIndex: "error_message",
    key: "error_message",
    render: (value) => value ?? "-",
  },
];

export function DashboardRecentRunsTable({ trainingRuns }) {
  const recentRuns = trainingRuns.slice(0, 5);

  return (
    <PageSection
      title="Training Terakhir"
      subtitle="Aktivitas training terbaru agar kondisi eksperimen mudah dipantau dari dashboard."
    >
      <Table
        rowKey="id"
        columns={columns}
        dataSource={recentRuns}
        pagination={false}
        size="middle"
        scroll={{ x: 1100 }}
      />
    </PageSection>
  );
}
