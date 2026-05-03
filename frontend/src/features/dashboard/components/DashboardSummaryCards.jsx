import { Col, Row, Statistic, Tag } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

export function DashboardSummaryCards({
  datasetSummary,
  models,
  trainingRuns,
  activeModel,
}) {
  const totals = datasetSummary?.totals;
  const successfulRuns = trainingRuns.filter((item) => item.status === "completed").length;

  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} md={12} xl={6}>
        <PageSection title="Model Aktif">
          <Statistic value={activeModel?.display_name ?? "-"} />
          <Tag color={activeModel?.is_active ? "success" : "default"}>
            {activeModel?.is_active ? "Active" : "Idle"}
          </Tag>
        </PageSection>
      </Col>
      <Col xs={24} md={12} xl={6}>
        <PageSection title="Total Kelas">
          <Statistic value={totals?.class_count ?? 0} suffix="kelas" />
        </PageSection>
      </Col>
      <Col xs={24} md={12} xl={6}>
        <PageSection title="Total Model">
          <Statistic value={models.length} suffix="versi" />
        </PageSection>
      </Col>
      <Col xs={24} md={12} xl={6}>
        <PageSection title="Training Selesai">
          <Statistic value={successfulRuns} suffix={`dari ${trainingRuns.length}`} />
        </PageSection>
      </Col>
    </Row>
  );
}
