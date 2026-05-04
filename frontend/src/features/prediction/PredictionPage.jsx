import { Alert, Button, Col, Result, Row, Space, Spin, Typography, message } from "antd";
import { ReloadOutlined } from "@ant-design/icons";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ActivePredictionModelCard } from "./components/ActivePredictionModelCard";
import { PredictionControlPanel } from "./components/PredictionControlPanel";
import { PredictionPreviewPanel } from "./components/PredictionPreviewPanel";
import { PredictionResultsTable } from "./components/PredictionResultsTable";
import { usePredictionWorkspace } from "./hooks/usePredictionWorkspace";

export function PredictionPage() {
  const {
    activeModel,
    isLoadingModel,
    isErrorModel,
    modelError,
    refetchModel,
    runPrediction,
    predictionResult,
    isPredicting,
    resetPrediction,
  } = usePredictionWorkspace();
  const [fileList, setFileList] = useState([]);
  const [inputMode, setInputMode] = useState("upload");
  const [selectedFile, setSelectedFile] = useState(null);
  const [scoreThreshold, setScoreThreshold] = useState(0.5);
  const [pendingImageUrl, setPendingImageUrl] = useState(null);
  const [predictionImageUrl, setPredictionImageUrl] = useState(null);
  const [cameraResetSignal, setCameraResetSignal] = useState(0);

  useEffect(() => {
    if (!selectedFile) {
      setPendingImageUrl(null);
      return undefined;
    }

    const nextUrl = URL.createObjectURL(selectedFile);
    setPendingImageUrl(nextUrl);

    return () => {
      URL.revokeObjectURL(nextUrl);
    };
  }, [selectedFile]);

  const handlePredict = async () => {
    if (!selectedFile) {
      return;
    }
    await runPrediction({ file: selectedFile, scoreThreshold });
    setPredictionImageUrl(pendingImageUrl);
  };

  const handleInputModeChange = (nextMode) => {
    setInputMode(nextMode);
    setFileList([]);
    setSelectedFile(null);
    setCameraResetSignal((value) => value + 1);
  };

  const handleUploadChange = ({ fileList: nextFileList }) => {
    setFileList(nextFileList);
    const nextFile = nextFileList[0]?.originFileObj ?? nextFileList[0] ?? null;
    setSelectedFile(nextFile);
    if (nextFile) {
      message.success("Gambar berhasil dipilih");
    }
  };

  const handleCameraCapture = (file) => {
    setFileList([]);
    setSelectedFile(file);
    message.success("Foto dari kamera berhasil diambil");
  };

  const handleClear = () => {
    setFileList([]);
    setSelectedFile(null);
    setScoreThreshold(0.5);
    setPredictionImageUrl(null);
    setCameraResetSignal((value) => value + 1);
    resetPrediction();
  };

  if (isLoadingModel) {
    return (
      <div className="page-loading">
        <Spin size="large" />
        <Typography.Text type="secondary">Memuat workspace prediksi...</Typography.Text>
      </div>
    );
  }

  if (isErrorModel) {
    return (
      <Result
        status="error"
        title="Gagal memuat model aktif"
        subTitle={modelError?.message || "Backend belum menyediakan model aktif untuk prediksi."}
        extra={
          <Button type="primary" icon={<ReloadOutlined />} onClick={refetchModel}>
            Coba Lagi
          </Button>
        }
      />
    );
  }

  return (
    <div className="page-stack">
      <div>
        <Typography.Title level={2}>Prediksi</Typography.Title>
        <Typography.Paragraph type="secondary">
          Gunakan halaman ini untuk menguji model dengan satu gambar statis. Sistem akan
          menampilkan lokasi rambu, nama kelas, dan confidence dari hasil deteksi.
        </Typography.Paragraph>
      </div>

      <Alert
        type="info"
        showIcon
        message="Alur singkat"
        description="Pilih gambar, atur threshold jika perlu, lalu tekan `Jalankan Prediksi`. Hasil akan muncul setelah backend selesai memproses gambar."
      />

      <Space wrap>
        <Button>
          <Link to="/guide">Buka User Guide</Link>
        </Button>
        <Button>
          <Link to="/method">Lihat Cara Kerja YOLOS</Link>
        </Button>
      </Space>

      <Row gutter={[16, 16]} align="stretch">
        <Col xs={24} xl={9} className="prediction-grid-col">
          <ActivePredictionModelCard activeModel={activeModel} onRefresh={refetchModel} />
        </Col>
        <Col xs={24} xl={15} className="prediction-grid-col">
          <PredictionControlPanel
            inputMode={inputMode}
            onInputModeChange={handleInputModeChange}
            fileList={fileList}
            selectedFile={selectedFile}
            scoreThreshold={scoreThreshold}
            onFileChange={handleUploadChange}
            onThresholdChange={setScoreThreshold}
            onPredict={handlePredict}
            isPredicting={isPredicting}
            onClear={handleClear}
            onCameraCapture={handleCameraCapture}
            cameraResetSignal={cameraResetSignal}
          />
        </Col>
      </Row>

      {predictionResult ? (
        <Row gutter={[16, 16]} align="stretch">
          <Col xs={24} xl={12} className="prediction-grid-col">
            <PredictionPreviewPanel
              imageUrl={predictionImageUrl}
              predictionResult={predictionResult}
            />
          </Col>
          <Col xs={24} xl={12} className="prediction-grid-col">
            <PredictionResultsTable predictionResult={predictionResult} />
          </Col>
        </Row>
      ) : null}

      <Alert
        type="success"
        showIcon
        message="Workspace prediksi sudah tersambung ke backend"
        description="Upload gambar, model aktif, dan hasil deteksi sekarang menggunakan endpoint backend secara langsung."
      />
    </div>
  );
}
