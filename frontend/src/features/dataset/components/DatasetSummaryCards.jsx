import { Col, Row, Statistic, Tag } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

export function DatasetSummaryCards({ summary, validation }) {
  const totals = summary?.totals;

  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} md={12} xl={6}>
        <PageSection title="Total Kelas">
          <Statistic value={totals?.class_count ?? 0} suffix="kelas" />
        </PageSection>
      </Col>
      <Col xs={24} md={12} xl={6}>
        <PageSection title="Total Gambar">
          <Statistic value={totals?.image_count ?? 0} suffix="gambar" />
        </PageSection>
      </Col>
      <Col xs={24} md={12} xl={6}>
        <PageSection title="Total Label">
          <Statistic value={totals?.label_file_count ?? 0} suffix="file" />
        </PageSection>
      </Col>
      <Col xs={24} md={12} xl={6}>
        <PageSection title="Validasi Dataset">
          <Statistic value={validation?.issue_count ?? 0} suffix="issue" />
          <Tag color={validation?.is_valid ? "success" : "error"}>
            {validation?.is_valid ? "Valid" : "Perlu Perbaikan"}
          </Tag>
        </PageSection>
      </Col>
    </Row>
  );
}
