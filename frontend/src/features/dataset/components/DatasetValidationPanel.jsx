import { Alert, Col, Empty, Row, Table, Tag } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

const issueColumns = [
  { title: "Split", dataIndex: "split", key: "split", width: 90 },
  { title: "Folder", dataIndex: "directory", key: "directory", width: 240 },
  { title: "File", dataIndex: "file", key: "file", width: 240 },
  {
    title: "Jenis Issue",
    dataIndex: "issue_type",
    key: "issue_type",
    width: 180,
    render: (value) => <Tag color="error">{value}</Tag>,
  },
  { title: "Detail", dataIndex: "detail", key: "detail" },
];

export function DatasetValidationPanel({ validation }) {
  const issues = [
    ...(validation?.splits?.train?.issues ?? []),
    ...(validation?.splits?.test?.issues ?? []),
  ].map((item, index) => ({ key: `${item.file}-${index}`, ...item }));

  return (
    <PageSection
      title="Hasil Validasi Dataset"
      subtitle="Validasi backend memeriksa pasangan file, label kosong, class id, dan format bounding box."
    >
      <Row gutter={[16, 16]}>
        <Col xs={24} xl={10}>
          <Alert
            type={validation?.is_valid ? "success" : "error"}
            showIcon
            message={validation?.is_valid ? "Dataset valid" : "Dataset memiliki issue"}
            description={
              validation?.is_valid
                ? "Tidak ditemukan issue pada split train maupun test."
                : `Ditemukan ${validation?.issue_count ?? 0} issue yang perlu diperbaiki.`
            }
          />
        </Col>
        <Col xs={24} xl={14}>
          <Alert
            type="info"
            showIcon
            message="Ringkasan cepat"
            description={`Train issue: ${validation?.splits?.train?.issue_count ?? 0}, Test issue: ${validation?.splits?.test?.issue_count ?? 0}`}
          />
        </Col>
      </Row>

      {issues.length === 0 ? (
        <Empty description="Tidak ada issue validasi dataset" />
      ) : (
        <Table
          columns={issueColumns}
          dataSource={issues}
          pagination={{ pageSize: 5, showSizeChanger: false }}
          size="middle"
          scroll={{ x: 1100 }}
        />
      )}
    </PageSection>
  );
}
