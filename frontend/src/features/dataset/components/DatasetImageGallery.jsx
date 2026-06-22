import { useEffect, useState } from "react";
import { Image, Modal, Pagination, Segmented, Spin, Typography, Empty } from "antd";
import { datasetApi } from "../api/datasetApi";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
const PER_PAGE = 30;

export function DatasetImageGallery({ open, onClose, classLabel, trainCount, testCount }) {
  const [split, setSplit] = useState("train");
  const [page, setPage] = useState(1);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!open || !classLabel) return;
    setPage(1);
    setSplit(trainCount > 0 ? "train" : "test");
  }, [open, classLabel]);

  useEffect(() => {
    if (!open || !classLabel) return;
    let cancelled = false;
    setLoading(true);
    datasetApi
      .getImages({ split, classLabel, page, perPage: PER_PAGE })
      .then((result) => {
        if (!cancelled) setData(result);
      })
      .catch(() => {
        if (!cancelled) setData(null);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [open, classLabel, split, page]);

  const total = data?.total ?? 0;
  const images = data?.images ?? [];

  return (
    <Modal
      open={open}
      onCancel={onClose}
      title={
        <span>
          Galeri Gambar &mdash; <code>{classLabel}</code>
        </span>
      }
      footer={null}
      width={960}
      styles={{ body: { maxHeight: "75vh", overflowY: "auto" } }}
    >
      <div style={{ marginBottom: 16, display: "flex", alignItems: "center", gap: 16, flexWrap: "wrap" }}>
        <Segmented
          value={split}
          onChange={(value) => {
            setSplit(value);
            setPage(1);
          }}
          options={[
            { label: `Train (${trainCount})`, value: "train", disabled: trainCount === 0 },
            { label: `Test (${testCount})`, value: "test", disabled: testCount === 0 },
          ]}
        />
        <Typography.Text type="secondary">
          {total} gambar ditemukan
        </Typography.Text>
      </div>

      {loading ? (
        <div style={{ textAlign: "center", padding: 60 }}>
          <Spin size="large" />
        </div>
      ) : images.length === 0 ? (
        <Empty description="Tidak ada gambar" />
      ) : (
        <>
          <Image.PreviewGroup>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(140px, 1fr))",
                gap: 8,
              }}
            >
              {images.map((img) => (
                <div
                  key={img.filename}
                  style={{
                    border: "1px solid #f0f0f0",
                    borderRadius: 8,
                    overflow: "hidden",
                    background: "#fafafa",
                  }}
                >
                  <Image
                    src={`${API_BASE}${img.url}`}
                    alt={img.filename}
                    width="100%"
                    height={120}
                    style={{ objectFit: "cover", display: "block" }}
                    placeholder={
                      <div
                        style={{
                          width: "100%",
                          height: 120,
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          background: "#f5f5f5",
                        }}
                      >
                        <Spin size="small" />
                      </div>
                    }
                  />
                  <div
                    style={{
                      padding: "4px 6px",
                      fontSize: 11,
                      color: "#888",
                      whiteSpace: "nowrap",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                    }}
                    title={img.filename}
                  >
                    {img.filename}
                  </div>
                </div>
              ))}
            </div>
          </Image.PreviewGroup>

          {total > PER_PAGE && (
            <div style={{ textAlign: "center", marginTop: 16 }}>
              <Pagination
                current={page}
                pageSize={PER_PAGE}
                total={total}
                onChange={setPage}
                showSizeChanger={false}
                size="small"
              />
            </div>
          )}
        </>
      )}
    </Modal>
  );
}
