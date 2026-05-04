import { Empty, Tag } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

function buildBoxStyle(box, imageWidth, imageHeight) {
  const [xMin, yMin, xMax, yMax] = box;
  return {
    left: `${(xMin / imageWidth) * 100}%`,
    top: `${(yMin / imageHeight) * 100}%`,
    width: `${((xMax - xMin) / imageWidth) * 100}%`,
    height: `${((yMax - yMin) / imageHeight) * 100}%`,
  };
}

export function PredictionPreviewPanel({ imageUrl, predictionResult }) {
  const detections = predictionResult?.detections ?? [];
  const imageWidth = predictionResult?.image_width ?? 1;
  const imageHeight = predictionResult?.image_height ?? 1;

  return (
    <PageSection
      title="Preview Hasil Prediksi"
      subtitle="Bounding box divisualisasikan langsung di atas gambar yang diunggah."
    >
      {!imageUrl ? (
        <Empty description="Belum ada gambar yang dipilih" />
      ) : (
        <div className="prediction-preview-wrapper prediction-preview-compact">
          <img src={imageUrl} alt="Preview prediksi" className="prediction-preview-image" />
          <div className="prediction-overlay">
            {detections.map((detection, index) => (
              <div
                key={`${detection.class}-${index}`}
                className="prediction-box"
                style={buildBoxStyle(detection.box, imageWidth, imageHeight)}
              >
                <Tag color="processing" className="prediction-box-label">
                  {detection.class} ({(detection.confidence * 100).toFixed(1)}%)
                </Tag>
              </div>
            ))}
          </div>
        </div>
      )}
    </PageSection>
  );
}
