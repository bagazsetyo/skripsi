import { useState } from "react";
import { Button, Table, Tag } from "antd";
import { EyeOutlined } from "@ant-design/icons";
import { PageSection } from "../../../app/shared/PageSection";
import { DatasetImageGallery } from "./DatasetImageGallery";

function buildClassRows(summary, classes) {
  const trainClasses = new Map(
    (summary?.splits?.train?.classes ?? []).map((item) => [item.class_id, item])
  );
  const testClasses = new Map(
    (summary?.splits?.test?.classes ?? []).map((item) => [item.class_id, item])
  );

  return classes.map((item) => {
    const train = trainClasses.get(item.class_id);
    const test = testClasses.get(item.class_id);
    return {
      key: item.class_id,
      class_id: item.class_id,
      label: item.label,
      directory: item.directory,
      train_images: train?.image_count ?? 0,
      test_images: test?.image_count ?? 0,
      train_annotations: train?.annotation_count ?? 0,
      test_annotations: test?.annotation_count ?? 0,
    };
  });
}

export function DatasetClassTable({ summary, classes }) {
  const [gallery, setGallery] = useState({ open: false, label: null, train: 0, test: 0 });
  const rows = buildClassRows(summary, classes);

  const columns = [
    {
      title: "ID",
      dataIndex: "class_id",
      key: "class_id",
      width: 60,
    },
    {
      title: "Label",
      dataIndex: "label",
      key: "label",
      width: 300,
    },
    {
      title: "Train",
      dataIndex: "train_images",
      key: "train_images",
      width: 80,
      align: "center",
    },
    {
      title: "Test",
      dataIndex: "test_images",
      key: "test_images",
      width: 80,
      align: "center",
    },
    {
      title: "Anotasi",
      key: "annotations",
      width: 120,
      align: "center",
      render: (_, record) => record.train_annotations + record.test_annotations,
    },
    {
      title: "Status",
      key: "status",
      width: 100,
      align: "center",
      render: (_, record) => {
        const totalImages = record.train_images + record.test_images;
        return (
          <Tag color={totalImages > 0 ? "success" : "default"}>
            {totalImages > 0 ? "Tersedia" : "Kosong"}
          </Tag>
        );
      },
    },
    {
      title: "Aksi",
      key: "action",
      width: 100,
      align: "center",
      render: (_, record) => {
        const totalImages = record.train_images + record.test_images;
        return (
          <Button
            type="primary"
            size="small"
            icon={<EyeOutlined />}
            disabled={totalImages === 0}
            onClick={() =>
              setGallery({
                open: true,
                label: record.label,
                train: record.train_images,
                test: record.test_images,
              })
            }
          >
            Lihat
          </Button>
        );
      },
    },
  ];

  return (
    <PageSection
      title="Daftar Kelas Dataset"
      subtitle="Semua kelas yang terdaftar pada dataset beserta jumlah data train, test, dan anotasinya."
    >
      <Table
        columns={columns}
        dataSource={rows}
        pagination={{ pageSize: 8, showSizeChanger: false }}
        size="middle"
        scroll={{ x: 1000 }}
      />

      <DatasetImageGallery
        open={gallery.open}
        onClose={() => setGallery((prev) => ({ ...prev, open: false }))}
        classLabel={gallery.label}
        trainCount={gallery.train}
        testCount={gallery.test}
      />
    </PageSection>
  );
}
