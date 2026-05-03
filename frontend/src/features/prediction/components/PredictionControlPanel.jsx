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
      <Space direction="vertical" size={16} style={{ width: "100%" }}>
        <Upload.Dragger
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

        <Form layout="vertical">
          <Form.Item label="Score Threshold">
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

        <Typography.Text type="secondary">
          Threshold yang lebih tinggi akan menampilkan deteksi yang lebih selektif.
        </Typography.Text>
      </Space>
    </PageSection>
  );
}
