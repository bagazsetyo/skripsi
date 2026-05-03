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
  { title: "Output Dir", dataIndex: "output_dir", key: "output_dir" },
  { title: "Started At", dataIndex: "started_at", key: "started_at", width: 220 },
];

export function TrainingRunsTable({ runs }) {
  return (
    <PageSection
      title="Riwayat Training Run"
      subtitle="Menampilkan run yang sudah dibuat dari frontend maupun backend."
    >
      <Table
        rowKey="id"
        columns={columns}
        dataSource={runs}
        pagination={{ pageSize: 5, showSizeChanger: false }}
        size="middle"
        scroll={{ x: 1100 }}
      />
    </PageSection>
  );
}
