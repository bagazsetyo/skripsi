import { Table, Tag } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

function buildClassRows(summary, classes) {
  const trainClasses = new Map(
    (summary?.splits?.train?.classes ?? []).map((item) => [item.class_id, item])
  );
  const testClasses = new Map(
    (summary?.splits?.test?.classes ?? []).map((item) => [item.class_id, item])
  );

  return classes.map((item) => {
    const train = trainClasses.get(item.class_id);
    const test = testClasses.get(item.class_id);
    return {
      key: item.class_id,
      class_id: item.class_id,
      label: item.label,
      directory: item.directory,
      train_images: train?.image_count ?? 0,
      test_images: test?.image_count ?? 0,
      train_annotations: train?.annotation_count ?? 0,
      test_annotations: test?.annotation_count ?? 0,
    };
  });
}

const columns = [
  {
    title: "Class ID",
    dataIndex: "class_id",
    key: "class_id",
    width: 90,
  },
  {
    title: "Label",
    dataIndex: "label",
    key: "label",
    width: 320,
  },
  {
    title: "Folder",
    dataIndex: "directory",
    key: "directory",
    width: 320,
    render: (value) => <code>{value}</code>,
  },
  {
    title: "Train",
    dataIndex: "train_images",
    key: "train_images",
    width: 100,
  },
  {
    title: "Test",
    dataIndex: "test_images",
    key: "test_images",
    width: 100,
  },
  {
    title: "Anotasi Train",
    dataIndex: "train_annotations",
    key: "train_annotations",
    width: 140,
  },
  {
    title: "Anotasi Test",
    dataIndex: "test_annotations",
    key: "test_annotations",
    width: 140,
  },
  {
    title: "Status",
    key: "status",
    width: 120,
    render: (_, record) => {
      const totalImages = record.train_images + record.test_images;
      return (
        <Tag color={totalImages > 0 ? "success" : "default"}>
          {totalImages > 0 ? "Tersedia" : "Kosong"}
        </Tag>
      );
    },
  },
];

export function DatasetClassTable({ summary, classes }) {
  const rows = buildClassRows(summary, classes);

  return (
    <PageSection
      title="Daftar Kelas Dataset"
      subtitle="Semua kelas yang terdaftar pada dataset beserta jumlah data train, test, dan anotasinya."
    >
      <Table
        columns={columns}
        dataSource={rows}
        pagination={{ pageSize: 8, showSizeChanger: false }}
        size="middle"
        scroll={{ x: 1400 }}
      />
    </PageSection>
  );
}
