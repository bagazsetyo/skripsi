import { useState } from "react";
import { Button, Checkbox, Form, Input, Typography, Upload } from "antd";
import { InboxOutlined } from "@ant-design/icons";
import { PageSection } from "../../../app/shared/PageSection";

export function ModelImportForm({ onSubmit, isSubmitting }) {
  const [form] = Form.useForm();
  const [fileList, setFileList] = useState([]);

  const handleFinish = async (values) => {
    const zipFile = fileList[0]?.originFileObj;
    if (!zipFile) {
      form.setFields([
        {
          name: "archive",
          errors: ["Pilih file ZIP model terlebih dahulu."],
        },
      ]);
      return;
    }

    const formData = new FormData();
    formData.append("file", zipFile);
    if (values.display_name?.trim()) {
      formData.append("display_name", values.display_name.trim());
    }
    if (values.version?.trim()) {
      formData.append("version", values.version.trim());
    }
    formData.append("activate_after_import", values.activate_after_import ? "true" : "false");

    await onSubmit(formData);
    form.resetFields();
    setFileList([]);
  };

  return (
    <PageSection
      title="Import Model"
      subtitle="Upload file ZIP hasil training dari Google Colab atau environment lain, lalu daftarkan langsung ke registry aplikasi."
    >
      <Typography.Paragraph type="secondary">
        File ZIP idealnya berisi folder model Hugging Face lengkap, misalnya `config.json`,
        `preprocessor_config.json`, file bobot model, dan jika tersedia `metrics.json`
        atau `training_summary.json`.
      </Typography.Paragraph>

      <Form
        form={form}
        layout="vertical"
        initialValues={{ activate_after_import: false }}
        onFinish={handleFinish}
      >
        <Form.Item
          name="archive"
          label="File Model ZIP"
          required
          extra="Contoh: yolos-image-500.zip dari Google Colab."
        >
          <Upload.Dragger
            accept=".zip"
            multiple={false}
            maxCount={1}
            beforeUpload={() => false}
            fileList={fileList}
            onChange={({ fileList: nextFileList }) => setFileList(nextFileList)}
          >
            <p className="ant-upload-drag-icon">
              <InboxOutlined />
            </p>
            <p className="ant-upload-text">Klik atau drag file ZIP model ke area ini</p>
            <p className="ant-upload-hint">
              Model akan divalidasi sebelum dimasukkan ke registry.
            </p>
          </Upload.Dragger>
        </Form.Item>

        <Form.Item
          name="display_name"
          label="Display Name"
          extra="Nama yang tampil di daftar model. Jika kosong, sistem memakai nama versi."
        >
          <Input placeholder="Contoh: YOLOS Image 500 Colab" />
        </Form.Item>

        <Form.Item
          name="version"
          label="Version"
          extra="Opsional. Jika kosong, sistem akan memakai nama folder model di dalam ZIP."
        >
          <Input placeholder="Contoh: yolos-image-500" />
        </Form.Item>

        <Form.Item name="activate_after_import" valuePropName="checked">
          <Checkbox>Langsung jadikan model aktif setelah import</Checkbox>
        </Form.Item>

        <Button type="primary" htmlType="submit" loading={isSubmitting}>
          Import Model
        </Button>
      </Form>
    </PageSection>
  );
}
