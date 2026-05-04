import { Alert, Col, Row, Steps, Tag, Typography } from "antd";
import {
  BookOutlined,
  CameraOutlined,
  DatabaseOutlined,
  LineChartOutlined,
  RadarChartOutlined,
  RocketOutlined,
} from "@ant-design/icons";
import { PageSection } from "../../app/shared/PageSection";

const quickStartSteps = [
  {
    title: "Cek Dataset",
    description:
      "Buka menu Dataset untuk melihat jumlah gambar, jumlah anotasi, dan memastikan data terbaca oleh sistem.",
  },
  {
    title: "Siapkan Training",
    description:
      "Masuk ke menu Training & Model untuk memilih semua kelas atau subset kelas, lalu jalankan training.",
  },
  {
    title: "Pilih Model Aktif",
    description:
      "Setelah model tersedia, aktifkan model yang ingin dipakai untuk proses prediksi.",
  },
  {
    title: "Jalankan Prediksi",
    description:
      "Buka menu Prediksi, unggah gambar rambu, lalu sistem akan menampilkan label, confidence, dan bounding box.",
  },
];

const menuGuides = [
  {
    title: "Dashboard",
    icon: <LineChartOutlined />,
    color: "geekblue",
    description:
      "Menampilkan ringkasan umum sistem seperti model aktif, kondisi dataset, dan riwayat training terbaru.",
  },
  {
    title: "Dataset",
    icon: <DatabaseOutlined />,
    color: "cyan",
    description:
      "Digunakan untuk melihat statistik dataset, pembagian train-test, daftar kelas, dan hasil validasi dataset.",
  },
  {
    title: "Training & Model",
    icon: <RocketOutlined />,
    color: "volcano",
    description:
      "Dipakai untuk membuat training run baru, melihat model yang tersedia, serta memilih model aktif.",
  },
  {
    title: "Prediksi",
    icon: <RadarChartOutlined />,
    color: "green",
    description:
      "Digunakan untuk menguji model dengan gambar statis dan melihat hasil deteksi rambu lalu lintas.",
  },
];

const predictionTips = [
  "Gunakan gambar yang cukup jelas agar bentuk rambu mudah terbaca oleh model.",
  "Jika hasil deteksi terlalu sedikit, turunkan score threshold secara bertahap.",
  "Pastikan model aktif sudah sesuai dengan eksperimen yang ingin diuji.",
];

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
        title="Panduan Setiap Menu"
        subtitle="Bagian ini membantu memahami fungsi masing-masing menu tanpa harus mencoba semuanya sekaligus."
      >
        <Row gutter={[16, 16]}>
          {menuGuides.map((item) => (
            <Col xs={24} md={12} key={item.title}>
              <div className="guide-menu-card">
                <Tag color={item.color} className="guide-menu-tag">
                  {item.icon}
                  <span>{item.title}</span>
                </Tag>
                <Typography.Paragraph style={{ marginBottom: 0 }}>
                  {item.description}
                </Typography.Paragraph>
              </div>
            </Col>
          ))}
        </Row>
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
          {predictionTips.map((tip, index) => (
            <Col xs={24} md={8} key={tip}>
              <div className="guide-tip-card">
                <div className="guide-tip-icon">
                  {index === 0 ? <CameraOutlined /> : index === 1 ? <RadarChartOutlined /> : <RocketOutlined />}
                </div>
                <Typography.Text>{tip}</Typography.Text>
              </div>
            </Col>
          ))}
        </Row>
      </PageSection>
    </div>
  );
}
