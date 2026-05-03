import { Empty, Table, Tag } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

const columns = [
  {
    title: "Kelas",
    dataIndex: "class",
    key: "class",
    width: 260,
  },
  {
    title: "Confidence",
    dataIndex: "confidence",
    key: "confidence",
    width: 140,
    render: (value) => <Tag color="success">{(value * 100).toFixed(2)}%</Tag>,
  },
  {
    title: "Bounding Box",
    dataIndex: "box",
    key: "box",
    render: (value) => <code>[{value.map((item) => item.toFixed(1)).join(", ")}]</code>,
  },
];

export function PredictionResultsTable({ predictionResult }) {
  const detections = predictionResult?.detections ?? [];

  return (
    <PageSection
      title="Daftar Hasil Deteksi"
      subtitle="Setiap baris merepresentasikan satu objek rambu yang terdeteksi."
    >
      {detections.length === 0 ? (
        <Empty description="Belum ada hasil deteksi" />
      ) : (
        <Table
          rowKey={(record, index) => `${record.class}-${index}`}
          columns={columns}
          dataSource={detections}
          pagination={{ pageSize: 5, showSizeChanger: false }}
          size="middle"
          scroll={{ x: 900 }}
        />
      )}
    </PageSection>
  );
}
