import { Typography } from "antd";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export function PredictionPage() {
  return (
    <div className="page-stack">
      <div>
        <Typography.Title level={2}>Prediksi Real-Time</Typography.Title>
        <Typography.Paragraph type="secondary">
          Deteksi rambu lalu lintas secara real-time menggunakan kamera. Arahkan kamera ke
          rambu lalu lintas, sistem akan otomatis mendeteksi dan menampilkan hasilnya.
        </Typography.Paragraph>
      </div>

      <div
        style={{
          borderRadius: 12,
          overflow: "hidden",
          border: "1px solid #d9d9d9",
          background: "#fff",
          minHeight: 600,
        }}
      >
        <iframe
          src={`${API_BASE}/video-demo`}
          title="Video Prediksi Real-Time"
          style={{
            width: "100%",
            height: "calc(100vh - 220px)",
            minHeight: 600,
            border: "none",
            display: "block",
          }}
          allow="camera"
        />
      </div>
    </div>
  );
}
