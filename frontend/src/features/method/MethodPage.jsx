import { Alert, Card, Col, Collapse, Row, Steps, Tag, Typography } from "antd";
import { BulbOutlined, InfoCircleOutlined } from "@ant-design/icons";
import { PageSection } from "../../app/shared/PageSection";
import {
  analogies,
  methodFacts,
  methodFaq,
  methodFlowSteps,
} from "./methodContent";

function MethodIllustration() {
  return (
    <div className="method-illustration">
      <div className="method-illustration-frame">
        <div className="method-illustration-row">
          <div className="method-illustration-image" />
          <div className="method-illustration-patches">
            <div />
            <div />
            <div />
            <div />
            <div />
            <div />
            <div />
            <div />
            <div />
          </div>
        </div>
        <div className="method-illustration-arrow">Transformer</div>
        <div className="method-illustration-output">
          <div className="method-output-box">
            <span className="method-output-label">Bounding Box</span>
          </div>
          <div className="method-output-meta">
            <Tag color="processing">Label Kelas</Tag>
            <Tag color="success">Confidence</Tag>
          </div>
        </div>
      </div>
    </div>
  );
}

const faqItems = methodFaq.map((item, index) => ({
  key: String(index + 1),
  label: item.question,
  children: <Typography.Paragraph style={{ marginBottom: 0 }}>{item.answer}</Typography.Paragraph>,
}));

export function MethodPage() {
  return (
    <div className="page-stack">
      <div>
        <Typography.Title level={2}>Cara Kerja YOLOS</Typography.Title>
        <Typography.Paragraph type="secondary">
          Halaman ini menjelaskan alur kerja Vision Transformer dan YOLOS dengan bahasa
          yang sederhana agar mudah dipahami oleh pengguna umum maupun dosen penguji.
        </Typography.Paragraph>
      </div>

      <Alert
        type="info"
        showIcon
        icon={<InfoCircleOutlined />}
        message="Ringkasan sederhana"
        description="Sistem menerima gambar, membagi gambar menjadi bagian-bagian kecil, mempelajari hubungan antarbagian dengan transformer, lalu menentukan jenis rambu dan letaknya pada gambar."
      />

      <PageSection
        title="Gambaran Umum"
        subtitle="Bagian ini membantu melihat ide besarnya dulu sebelum masuk ke penjelasan langkah per langkah."
      >
        <Row gutter={[20, 20]} align="middle">
          <Col xs={24} xl={11}>
            <MethodIllustration />
          </Col>
          <Col xs={24} xl={13}>
            <div className="page-stack">
              <Typography.Paragraph style={{ marginBottom: 0 }}>
                Pada aplikasi ini, model tidak hanya menebak isi gambar secara umum. Model
                juga mencari lokasi objek rambu pada gambar. Karena itu, keluaran sistem
                berupa <strong>bounding box</strong>, <strong>label kelas</strong>, dan
                <strong> confidence</strong>.
              </Typography.Paragraph>
              <Typography.Paragraph style={{ marginBottom: 0 }}>
                Secara sederhana, gambar dipandang sebagai kumpulan bagian kecil. Bagian-bagian
                ini dipelajari bersama-sama oleh transformer sehingga sistem dapat memahami
                konteks gambar secara lebih utuh.
              </Typography.Paragraph>
            </div>
          </Col>
        </Row>
      </PageSection>

      <PageSection
        title="Langkah Kerja Sistem"
        subtitle="Urutan ini menjelaskan apa yang terjadi dari gambar masuk sampai hasil prediksi tampil di frontend."
      >
        <Steps
          direction="vertical"
          items={methodFlowSteps.map((step) => {
            const Icon = step.icon;
            return {
              title: (
                <div className="method-step-title">
                  <Tag color={step.color} className="guide-menu-tag">
                    <Icon />
                    <span>{step.title}</span>
                  </Tag>
                </div>
              ),
              description: (
                <div className="page-stack" style={{ gap: 8 }}>
                  <Typography.Paragraph style={{ marginBottom: 0 }}>
                    {step.summary}
                  </Typography.Paragraph>
                  <Typography.Text type="secondary">{step.simple}</Typography.Text>
                </div>
              ),
            };
          })}
        />
      </PageSection>

      <PageSection
        title="Analogi Sederhana"
        subtitle="Analogi ini bisa dipakai saat menjelaskan metode ke dosen non-bidang."
      >
        <Row gutter={[16, 16]}>
          {analogies.map((item) => (
            <Col xs={24} md={8} key={item.title}>
              <Card className="method-analogy-card" bordered={false}>
                <div className="method-analogy-icon">
                  <BulbOutlined />
                </div>
                <Typography.Title level={5}>{item.title}</Typography.Title>
                <Typography.Paragraph style={{ marginBottom: 0 }}>
                  {item.description}
                </Typography.Paragraph>
              </Card>
            </Col>
          ))}
        </Row>
      </PageSection>

      <PageSection
        title="Hal Penting yang Perlu Diingat"
        subtitle="Bagian ini menekankan poin-poin yang sering ditanyakan saat presentasi."
      >
        <Row gutter={[16, 16]}>
          {methodFacts.map((fact) => (
            <Col xs={24} md={8} key={fact.title}>
              <div className="method-fact-card">
                <Typography.Title level={5}>{fact.title}</Typography.Title>
                <Typography.Paragraph style={{ marginBottom: 0 }}>
                  {fact.description}
                </Typography.Paragraph>
              </div>
            </Col>
          ))}
        </Row>
      </PageSection>

      <PageSection
        title="Pertanyaan yang Sering Muncul"
        subtitle="Jawaban singkat ini bisa dipakai sebagai pegangan saat demo atau sidang."
      >
        <Collapse items={faqItems} accordion className="guide-collapse" />
      </PageSection>
    </div>
  );
}
