import { Card, Space, Typography } from "antd";

export function PageSection({ title, subtitle, extra, children }) {
  return (
    <Card className="page-card" extra={extra}>
      <Space direction="vertical" size={16} style={{ width: "100%" }}>
        <div>
          <Typography.Title level={4} style={{ marginBottom: 4 }}>
            {title}
          </Typography.Title>
          {subtitle ? (
            <Typography.Paragraph type="secondary" style={{ marginBottom: 0 }}>
              {subtitle}
            </Typography.Paragraph>
          ) : null}
        </div>
        {children}
      </Space>
    </Card>
  );
}
