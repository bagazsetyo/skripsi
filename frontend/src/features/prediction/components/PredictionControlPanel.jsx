import { Button, Form, InputNumber, Space, Upload, Typography } from "antd";
import { InboxOutlined, PlayCircleOutlined } from "@ant-design/icons";
import { PageSection } from "../../../app/shared/PageSection";

export function PredictionControlPanel({
  fileList,
  scoreThreshold,
  onFileChange,
  onThresholdChange,
  onPredict,
  isPredicting,
  onClear,
}) {
  return (
    <PageSection
      title="Kontrol Prediksi"
      subtitle="Pilih satu gambar statis, atur threshold, lalu jalankan prediksi."
    >
      <Space direction="vertical" size={14} style={{ width: "100%" }}>
        <Upload.Dragger
          className="prediction-uploader-compact"
          accept="image/*"
          beforeUpload={() => false}
          multiple={false}
          maxCount={1}
          fileList={fileList}
          onChange={onFileChange}
        >
          <p className="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p className="ant-upload-text">Klik atau drag gambar ke area ini</p>
          <p className="ant-upload-hint">
            Input saat ini mendukung satu file gambar untuk prediksi statis.
          </p>
        </Upload.Dragger>

        <Form layout="vertical" className="prediction-inline-form">
          <Form.Item label="Score Threshold" style={{ marginBottom: 0 }}>
            <InputNumber
              min={0}
              max={1}
              step={0.05}
              value={scoreThreshold}
              onChange={(value) => onThresholdChange(value ?? 0.5)}
              style={{ width: "100%" }}
            />
          </Form.Item>
        </Form>

        <Space wrap>
          <Button
            type="primary"
            icon={<PlayCircleOutlined />}
            onClick={onPredict}
            loading={isPredicting}
            disabled={fileList.length === 0}
          >
            Jalankan Prediksi
          </Button>
          <Button onClick={onClear}>Reset</Button>
        </Space>

        {fileList.length > 0 ? (
          <Typography.Text className="prediction-selected-file">
            File terpilih: {fileList[0]?.name ?? fileList[0]?.originFileObj?.name ?? "gambar"}
          </Typography.Text>
        ) : null}

        <Typography.Text type="secondary">
          Threshold yang lebih tinggi akan menampilkan deteksi yang lebih selektif.
        </Typography.Text>
        <Typography.Text type="secondary">
          Jika Anda mengganti file gambar, hasil preview lama tetap dipertahankan sampai tombol
          `Jalankan Prediksi` ditekan lagi.
        </Typography.Text>
      </Space>
    </PageSection>
  );
}
