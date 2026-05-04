import { Alert, Col, Collapse, Divider, List, Row, Steps, Tag, Typography } from "antd";
import { BookOutlined, InfoCircleOutlined } from "@ant-design/icons";
import { PageSection } from "../../app/shared/PageSection";
import { menuGuideDetails, predictionTips, quickStartSteps } from "./guideContent";

function PlaceholderPreview({ title }) {
  return (
    <div className="guide-preview-placeholder">
      <div className="guide-preview-window">
        <div className="guide-preview-bar">
          <span />
          <span />
          <span />
        </div>
        <div className="guide-preview-body">
          <div className="guide-preview-hero" />
          <div className="guide-preview-grid">
            <div />
            <div />
            <div />
          </div>
          <Typography.Text type="secondary">{title}</Typography.Text>
        </div>
      </div>
    </div>
  );
}

const collapseItems = menuGuideDetails.map((item) => {
  const Icon = item.icon;

  return {
    key: item.key,
    label: (
      <div className="guide-collapse-label">
        <Tag color={item.color} className="guide-menu-tag">
          <Icon />
          <span>{item.title}</span>
        </Tag>
        <Typography.Text>{item.summary}</Typography.Text>
      </div>
    ),
    children: (
      <Row gutter={[20, 20]}>
        <Col xs={24} xl={10}>
          <PlaceholderPreview title={item.imageLabel} />
        </Col>
        <Col xs={24} xl={14}>
          <div className="page-stack">
            <Typography.Paragraph style={{ marginBottom: 0 }}>
              {item.description}
            </Typography.Paragraph>

            <Alert
              type="info"
              showIcon
              icon={<InfoCircleOutlined />}
              message={`Fungsi utama menu ${item.title}`}
              description={
                <ul className="guide-inline-list">
                  {item.bullets.map((bullet) => (
                    <li key={bullet}>{bullet}</li>
                  ))}
                </ul>
              }
            />

            <div>
              <Typography.Title level={5}>Penjelasan Komponen</Typography.Title>
              <List
                className="guide-detail-list"
                dataSource={item.details}
                renderItem={(detail) => (
                  <List.Item>
                    <List.Item.Meta
                      title={detail.label}
                      description={detail.description}
                    />
                  </List.Item>
                )}
              />
            </div>
          </div>
        </Col>
      </Row>
    ),
  };
});

export function UserGuidePage() {
  return (
    <div className="page-stack">
      <div>
        <Typography.Title level={2}>User Guide</Typography.Title>
        <Typography.Paragraph type="secondary">
          Halaman ini menjelaskan cara memakai aplikasi secara ringkas agar pengguna baru
          dan dosen penguji dapat mengikuti alur sistem dengan cepat.
        </Typography.Paragraph>
      </div>

      <Alert
        type="info"
        showIcon
        icon={<BookOutlined />}
        message="Tujuan penggunaan aplikasi"
        description="Aplikasi ini dipakai untuk mengelola dataset, melakukan training model YOLOS, memilih model aktif, dan menguji hasil prediksi rambu lalu lintas Indonesia."
      />

      <PageSection
        title="Alur Penggunaan Singkat"
        subtitle="Empat langkah ini adalah alur paling aman untuk menjalankan aplikasi dari awal sampai prediksi."
      >
        <Steps direction="vertical" items={quickStartSteps} />
      </PageSection>

      <PageSection
        title="Manual Book Interaktif"
        subtitle="Klik salah satu menu di bawah untuk melihat gambar placeholder dan penjelasan detail tiap bagian halaman."
      >
        <Collapse items={collapseItems} accordion size="large" className="guide-collapse" />
      </PageSection>

      <PageSection
        title="Cara Melakukan Prediksi"
        subtitle="Fitur prediksi ditujukan untuk pengguna publik sehingga alurnya dibuat sesederhana mungkin."
      >
        <Steps
          direction="vertical"
          items={[
            {
              title: "Pilih gambar",
              description: "Unggah satu gambar statis yang berisi rambu lalu lintas.",
            },
            {
              title: "Atur threshold",
              description:
                "Score threshold mengatur seberapa yakin model sebelum hasil ditampilkan.",
            },
            {
              title: "Jalankan prediksi",
              description:
                "Backend akan memproses gambar dengan model aktif dan mengembalikan hasil deteksi.",
            },
            {
              title: "Baca hasil",
              description:
                "Sistem menampilkan kotak deteksi, nama kelas rambu, dan confidence untuk tiap objek.",
            },
          ]}
        />
      </PageSection>

      <PageSection
        title="Tips Penggunaan"
        subtitle="Catatan kecil ini membantu pengguna mendapatkan hasil yang lebih mudah dibaca."
      >
        <Row gutter={[16, 16]}>
          {predictionTips.map((tip) => (
            <Col xs={24} md={8} key={tip}>
              <div className="guide-tip-card">
                <Typography.Text>{tip}</Typography.Text>
              </div>
            </Col>
          ))}
        </Row>
      </PageSection>

      <Divider style={{ margin: 0 }} />
    </div>
  );
}
