## Why

当前 sidebar 宽度 380px 过窄，导致 header 中的标题、导航标签、会话选择器、新建按钮、用户头像挤在一起，底部输入框 placeholder 文字显示不全。

## What Changes

- 将 `#sidebar` 宽度从 `380px` 增加到 `440px`
- 增加 `min-width` 从 `320px` 到 `380px`

## Capabilities

### Modified Capabilities
- `frontend-design-system`: 调整 sidebar 宽度

## Impact

- `static/css/style.css` — 修改 `#sidebar` 的 `width` 和 `min-width`