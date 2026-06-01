## Why

Header 单行挤入标题、标签、下拉框、按钮、头像共 6 个元素，即使 sidebar 加宽到 440px 仍显拥挤，头像被挤出或裁切。

## What Changes

- Header 改为 `flex-wrap: wrap` 两行布局
- 标题独占第一行 (`flex-basis: 100%`)
- 导航标签、会话选择、新建按钮、头像在第二行自然排列

## Capabilities

### Modified Capabilities
- `frontend-design-system`: Header 布局从单行改为双行

## Impact

- `static/css/style.css` — `#header` 和 `#header h1` 样式