## Context

项目已有两种弹窗模式：
- 自定义 `.modal`（route-modal、search-modal）：大地色调遮罩 + 毛玻璃，`.modal-content` 卡片样式
- Element Plus `<el-dialog>`（Profile Dialog）：通过 CSS override 匹配主题

路书删除使用 `ElMessageBox.confirm()` — 不匹配上述任何一种，尤其是 polyfill 回退到 `window.confirm()` 时完全是浏览器原生样式。

## Goals / Non-Goals

**Goals:**
- 删除确认弹窗使用与 route-modal/search-modal 相同的 `.modal` 设计系统
- 保持 `async/await` 调用方式（Promise 封装）
- 确认按钮使用红色危险样式

**Non-Goals:**
- 不创建通用 confirm 工具函数（本次仅用于删除场景）
- 不修改后端 API

## Decisions

1. **复用 `.modal` CSS**：新增 `<div class="modal confirm-dialog">` 使用已有 `.modal`/`.modal-content`/.btn-row 样式，仅加少量 confirm 专用微调
2. **Promise 封装**：用 `showConfirmDialog` ref + pending resolve/reject 实现 `showDeleteConfirm()` → Promise，调用方保持 `await showDeleteConfirm()`
3. **移除 ElMessageBox polyfill**：不再需要

## Risks / Trade-offs

- 自定义弹窗不阻止页面其他交互（与 `ElMessageBox` 行为不同）→ 遮罩层已有 `backdrop-filter: blur`，视觉上已足够隔离
