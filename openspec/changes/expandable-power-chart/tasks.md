## 1. 放大按钮

- [x] 1.1 在功率曲线图区域右上角添加放大按钮 HTML（`<button class="btn-chart-expand">`），使用 CSS 绝对定位
- [x] 1.2 新增按钮 CSS 样式 — 半透明圆形按钮，hover 时高亮

## 2. 放大 Modal

- [x] 2.1 新增 Modal HTML 结构 — `.modal` + `#chart-modal`，内含 `<canvas id="power-profile-canvas-expanded">`
- [x] 2.2 新增 Modal CSS — `.chart-modal-content` 宽度 90vw / max 1200px，canvas 高度 420px
- [x] 2.3 新增 `showChartModal` ref 和 `openChartModal()` / `closeChartModal()` 函数

## 3. 放大版图表渲染

- [x] 3.1 新增 `drawPowerProfileChartExpanded(profile)` — 复用 `drawPowerProfileChart()` 逻辑，使用独立 canvas，X 轴标签每 ~5 分钟，最多 2000 数据点
- [x] 3.2 `openChartModal()` 中使用 `nextTick()` 确保 canvas DOM 就绪后调用渲染

## 4. 验证

- [x] 4.1 代码验证通过 — `nextTick` 已从 Vue 解构，Modal 使用 `.modal.show` 模式复用现有样式，`@click.self` 支持遮罩关闭
- [x] 4.2 无功率数据时 `v-if` 整个 chart-section 不渲染，放大按钮和 Modal 均不可见
