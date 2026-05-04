import { Alert, Button, Result, Spin, Typography } from "antd";
import { ReloadOutlined } from "@ant-design/icons";
import { useEffect, useState } from "react";
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
  const [scoreThreshold, setScoreThreshold] = useState(0.5);
  const [imageUrl, setImageUrl] = useState(null);

  useEffect(() => {
    if (fileList.length === 0) {
      setImageUrl(null);
      return undefined;
    }

    const nextUrl = URL.createObjectURL(fileList[0].originFileObj ?? fileList[0]);
    setImageUrl(nextUrl);

    return () => {
      URL.revokeObjectURL(nextUrl);
    };
  }, [fileList]);

  const handlePredict = async () => {
    if (fileList.length === 0) {
      return;
    }
    const file = fileList[0].originFileObj ?? fileList[0];
    await runPrediction({ file, scoreThreshold });
  };

  const handleClear = () => {
    setFileList([]);
    setScoreThreshold(0.5);
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
          Halaman ini akan menjadi area upload gambar, preview, dan hasil deteksi bounding box.
        </Typography.Paragraph>
      </div>

      <ActivePredictionModelCard activeModel={activeModel} onRefresh={refetchModel} />

      <PredictionControlPanel
        fileList={fileList}
        scoreThreshold={scoreThreshold}
        onFileChange={({ fileList: nextFileList }) => setFileList(nextFileList)}
        onThresholdChange={setScoreThreshold}
        onPredict={handlePredict}
        isPredicting={isPredicting}
        onClear={handleClear}
      />

      {predictionResult ? (
        <>
          <PredictionPreviewPanel imageUrl={imageUrl} predictionResult={predictionResult} />
          <PredictionResultsTable predictionResult={predictionResult} />
        </>
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
