import { useEffect, useRef, useState } from "react";
import { Alert, Button, Space, Typography } from "antd";
import { CameraOutlined, ReloadOutlined } from "@ant-design/icons";

export function PredictionCameraCapture({ isActive, onCapture, resetSignal }) {
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const [isStarting, setIsStarting] = useState(false);
  const [error, setError] = useState(null);
  const [capturedName, setCapturedName] = useState(null);

  useEffect(() => {
    if (!isActive) {
      stopCamera();
      return undefined;
    }

    startCamera();
    return () => {
      stopCamera();
    };
  }, [isActive]);

  useEffect(() => {
    setCapturedName(null);
    setError(null);
  }, [resetSignal]);

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  };

  const startCamera = async () => {
    try {
      setIsStarting(true);
      setError(null);
      stopCamera();
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" },
        audio: false,
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (nextError) {
      setError("Kamera tidak dapat diakses. Pastikan izin kamera sudah diberikan.");
    } finally {
      setIsStarting(false);
    }
  };

  const handleCapture = async () => {
    const video = videoRef.current;
    if (!video || !video.videoWidth || !video.videoHeight) {
      setError("Gambar kamera belum siap diambil.");
      return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", 0.92));
    if (!blob) {
      setError("Gagal membuat hasil capture dari kamera.");
      return;
    }

    const fileName = `camera-capture-${Date.now()}.jpg`;
    const file = new File([blob], fileName, { type: "image/jpeg" });
    setCapturedName(fileName);
    setError(null);
    onCapture(file);
  };

  return (
    <div className="prediction-camera-panel">
      <div className="prediction-camera-frame">
        <video ref={videoRef} autoPlay playsInline muted className="prediction-camera-video" />
      </div>

      <Space wrap>
        <Button
          icon={<ReloadOutlined />}
          onClick={startCamera}
          loading={isStarting}
        >
          Nyalakan Ulang Kamera
        </Button>
        <Button type="primary" icon={<CameraOutlined />} onClick={handleCapture}>
          Ambil Foto
        </Button>
      </Space>

      {capturedName ? (
        <Typography.Text className="prediction-selected-file">
          Foto terakhir: {capturedName}
        </Typography.Text>
      ) : null}

      <Typography.Text type="secondary">
        Arahkan kamera ke rambu, lalu tekan `Ambil Foto`. Hasil foto akan dipakai seperti
        input gambar biasa.
      </Typography.Text>

      {error ? (
        <Alert type="warning" showIcon message={error} />
      ) : null}
    </div>
  );
}
