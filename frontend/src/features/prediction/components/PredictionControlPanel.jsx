import { Button, Form, InputNumber, Segmented, Space, Upload, Typography } from "antd";
import { CameraOutlined, InboxOutlined, PlayCircleOutlined } from "@ant-design/icons";
import { PageSection } from "../../../app/shared/PageSection";
import { PredictionCameraCapture } from "./PredictionCameraCapture";

export function PredictionControlPanel({
  inputMode,
  onInputModeChange,
  fileList,
  selectedFile,
  scoreThreshold,
  onFileChange,
  onThresholdChange,
  onPredict,
  isPredicting,
  onClear,
  onCameraCapture,
  cameraResetSignal,
}) {
  return (
    <PageSection
      title="Kontrol Prediksi"
      subtitle="Pilih satu gambar statis, atur threshold, lalu jalankan prediksi."
    >
      <Space direction="vertical" size={14} style={{ width: "100%" }}>
        <Segmented
          block
          value={inputMode}
          onChange={onInputModeChange}
          options={[
            {
              label: "Upload Gambar",
              value: "upload",
              icon: <InboxOutlined />,
            },
            {
              label: "Ambil Dari Kamera",
              value: "camera",
              icon: <CameraOutlined />,
            },
          ]}
        />

        {inputMode === "upload" ? (
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
        ) : (
          <PredictionCameraCapture
            isActive={inputMode === "camera"}
            onCapture={onCameraCapture}
            resetSignal={cameraResetSignal}
          />
        )}

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
            disabled={!selectedFile}
          >
            Jalankan Prediksi
          </Button>
          <Button onClick={onClear}>Reset</Button>
        </Space>

        {selectedFile ? (
          <Typography.Text className="prediction-selected-file">
            File terpilih: {selectedFile.name ?? "gambar"}
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
