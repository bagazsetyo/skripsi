import { Button, Col, Form, Input, InputNumber, Row, Select, Space, Switch } from "antd";
import { PageSection } from "../../../app/shared/PageSection";

export function TrainingRunForm({ config, isSubmitting, onSubmit }) {
  const [form] = Form.useForm();
  const defaults = config?.defaults;
  const availableClasses = config?.available_classes ?? [];

  const handleFinish = async (values) => {
    await onSubmit({
      ...values,
      selection_mode: values.selection_mode ?? "all",
      selected_classes:
        values.selection_mode === "subset" ? values.selected_classes ?? [] : [],
    });
    form.resetFields(["run_name", "output_version"]);
  };

  return (
    <PageSection
      title="Buat Training Run"
      subtitle="Mendukung semua kelas atau subset kelas tertentu untuk eksperimen model."
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          ...defaults,
          selection_mode: defaults?.selection_mode ?? "all",
          selected_classes: defaults?.selected_classes ?? [],
          activate_after_training: defaults?.activate_after_training ?? true,
          use_amp: defaults?.use_amp ?? true,
        }}
        onFinish={handleFinish}
      >
        <Row gutter={[16, 0]}>
          <Col xs={24} md={12}>
            <Form.Item
              label="Run Name"
              name="run_name"
              rules={[{ required: true, message: "Run name wajib diisi" }]}
            >
              <Input placeholder="mis. yolos-subset-eksperimen-1" />
            </Form.Item>
          </Col>
          <Col xs={24} md={12}>
            <Form.Item label="Output Version" name="output_version">
              <Input placeholder="kosongkan untuk auto-generate" />
            </Form.Item>
          </Col>
          <Col xs={24} md={12}>
            <Form.Item label="Selection Mode" name="selection_mode">
              <Select
                options={[
                  { label: "Semua kelas", value: "all" },
                  { label: "Subset kelas", value: "subset" },
                ]}
              />
            </Form.Item>
          </Col>
          <Col xs={24} md={12}>
            <Form.Item noStyle shouldUpdate={(prev, curr) => prev.selection_mode !== curr.selection_mode}>
              {({ getFieldValue }) =>
                getFieldValue("selection_mode") === "subset" ? (
                  <Form.Item
                    label="Selected Classes"
                    name="selected_classes"
                    rules={[{ required: true, message: "Pilih minimal satu kelas" }]}
                  >
                    <Select
                      mode="multiple"
                      optionFilterProp="label"
                      options={availableClasses.map((item) => ({
                        label: `${item.class_id} - ${item.label}`,
                        value: item.label,
                      }))}
                      placeholder="Pilih kelas yang akan dipakai"
                    />
                  </Form.Item>
                ) : null
              }
            </Form.Item>
          </Col>
          <Col xs={24} md={8}>
            <Form.Item label="Epochs" name="epochs">
              <InputNumber min={1} max={500} style={{ width: "100%" }} />
            </Form.Item>
          </Col>
          <Col xs={24} md={8}>
            <Form.Item label="Batch Size" name="batch_size">
              <InputNumber min={1} max={64} style={{ width: "100%" }} />
            </Form.Item>
          </Col>
          <Col xs={24} md={8}>
            <Form.Item label="Image Size" name="image_size">
              <InputNumber min={224} max={1024} step={32} style={{ width: "100%" }} />
            </Form.Item>
          </Col>
          <Col xs={24} md={8}>
            <Form.Item label="Learning Rate" name="learning_rate">
              <InputNumber min={0.000001} max={1} step={0.0001} style={{ width: "100%" }} />
            </Form.Item>
          </Col>
          <Col xs={24} md={8}>
            <Form.Item label="Weight Decay" name="weight_decay">
              <InputNumber min={0} max={1} step={0.0001} style={{ width: "100%" }} />
            </Form.Item>
          </Col>
          <Col xs={24} md={8}>
            <Form.Item label="Score Threshold" name="score_threshold">
              <InputNumber min={0} max={1} step={0.05} style={{ width: "100%" }} />
            </Form.Item>
          </Col>
          <Col xs={24} md={12}>
            <Form.Item label="Model Name" name="model_name">
              <Input />
            </Form.Item>
          </Col>
          <Col xs={24} md={6}>
            <Form.Item label="Use AMP" name="use_amp" valuePropName="checked">
              <Switch />
            </Form.Item>
          </Col>
          <Col xs={24} md={6}>
            <Form.Item label="Activate After Training" name="activate_after_training" valuePropName="checked">
              <Switch />
            </Form.Item>
          </Col>
        </Row>

        <Space>
          <Button type="primary" htmlType="submit" loading={isSubmitting}>
            Mulai Training
          </Button>
          <Button htmlType="button" onClick={() => form.resetFields()}>
            Reset
          </Button>
        </Space>
      </Form>
    </PageSection>
  );
}
