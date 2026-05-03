import { Table, Tag, Typography } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

const columns = [
  {
    title: "Split",
    dataIndex: "split",
    key: "split",
    render: (value) => <Typography.Text strong>{String(value).toUpperCase()}</Typography.Text>,
  },
  {
    title: "Kelas",
    dataIndex: "class_count",
    key: "class_count",
  },
  {
    title: "Gambar",
    dataIndex: "image_count",
    key: "image_count",
  },
  {
    title: "Label",
    dataIndex: "label_file_count",
    key: "label_file_count",
  },
  {
    title: "Anotasi",
    dataIndex: "annotation_count",
    key: "annotation_count",
  },
  {
    title: "Status",
    key: "status",
    render: (_, record) => (
      <Tag color={record.image_count > 0 ? "processing" : "default"}>
        {record.image_count > 0 ? "Terisi" : "Kosong"}
      </Tag>
    ),
  },
];

export function DatasetSplitTable({ summary }) {
  const dataSource = Object.values(summary?.splits ?? {}).map((split) => ({
    key: split.split,
    ...split,
  }));

  return (
    <PageSection
      title="Ringkasan Split Dataset"
      subtitle="Perbandingan train dan test berdasarkan jumlah kelas, gambar, label, dan anotasi."
    >
      <Table
        columns={columns}
        dataSource={dataSource}
        pagination={false}
        size="middle"
        scroll={{ x: 720 }}
      />
    </PageSection>
  );
}
