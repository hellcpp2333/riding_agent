## Why

当前路书删除确认使用 `ElMessageBox.confirm()`（CDN 被阻止时回退到 `window.confirm()`），弹出的是浏览器原生对话框或 Element Plus 预设样式，与项目大地色调的设计系统不一致。需要替换为自定义确认弹窗组件，复用已有的 `.modal` 风格，保持整体 UI 统一。

## What Changes

- 新增自定义确认弹窗组件（复用 `.modal`/`.modal-content` CSS），含标题、提示文案、取消/确认按钮
- 删除按钮改用 Vue 响应式状态 (`showConfirmDialog`) 控制弹窗显隐，以 Promise 封装保持 `async/await` 调用流
- 确认按钮使用危险色样式（红色），取消按钮使用描边样式，与 `btn-danger` 按钮风格呼应
- 移除 `ElMessageBox` polyfill（不再需要）

## Capabilities

### New Capabilities

- `custom-confirm-dialog`: 自定义确认弹窗组件，使用项目现有 `.modal` 设计系统，支持 Promise 化调用

### Modified Capabilities

<!-- None -->

## Impact

- `static/index.html` — 新增 confirm dialog 模板、`confirmDialog` 状态、`showConfirm`/`cancelConfirm` 方法；简化 `deleteRouteConfirm`
- `static/css/style.css` — 确认弹窗内边距微调（与现有 `.modal-content` 一致即可，无需大量新增）
