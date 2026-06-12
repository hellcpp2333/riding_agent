## 1. 新增自定义确认弹窗

- [x] 1.1 在 Vue 模板中添加 confirm dialog（复用 `.modal` CSS），含标题、提示文字、取消和确认按钮
- [x] 1.2 在 `setup()` 中添加 `confirmDialog` 响应式状态和 `showDeleteConfirm`/`closeConfirm` 方法
- [x] 1.3 确认按钮使用红色危险样式（`.btn-danger-confirm`），CSS 中添加对应样式

## 2. 替换删除流程

- [x] 2.1 `deleteRouteConfirm` 改用 `await showDeleteConfirm()` 替代 `await ElMessageBox.confirm()`
- [x] 2.2 移除 `ElMessageBox` polyfill（不再需要）

## 3. 验证

- [x] 3.1 点击删除按钮，确认弹窗以项目统一风格弹出
- [x] 3.2 点击确认后成功删除路书并刷新列表
- [x] 3.3 点击取消后弹窗关闭，路书不被删除
