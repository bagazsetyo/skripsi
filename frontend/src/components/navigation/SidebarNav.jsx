import { Menu } from "antd";

export function SidebarNav({ items, selectedKey, onSelect }) {
  return (
    <Menu
      mode="inline"
      selectedKeys={[selectedKey]}
      items={items}
      onClick={({ key }) => onSelect(key)}
      theme="dark"
      style={{
        background: "transparent",
        borderInlineEnd: "none",
        paddingInline: 12,
      }}
    />
  );
}
