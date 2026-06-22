## Context

当前 `drawPowerProfileChart()` 在 220px 高的 `<canvas>` 中渲染功率剖面图，canvas 宽度随侧边栏变化（约 400-500px）。用户查看 2 小时以上的骑行数据时，每秒一个数据点导致折线挤压，细节不可辨。

参考 Garmin Connect：活动详情页的功率图可点击放大，展开为接近全屏的图表面板，横轴显著拉宽（约 900-1200px）。

## Goals / Non-Goals

**Goals:**
- 功率曲线图右上角显示放大按钮
- 放大后弹出 Modal，内含全宽 Canvas 渲染完整功率数据
- 关闭按钮 + 点击遮罩关闭
- 放大版横轴刻度更密集（参考 Garmin：每 5-10 分钟一个标签）

**Non-Goals:**
- 不增加图表交互（缩放、拖拽、选区）
- 不修改后端 API

## Decisions

### 1. Modal 方案：复用现有 `.modal` 样式

项目已有 `.modal` / `.modal.show` / `.modal-content` 样式，用于路线规划、搜索等弹窗。放大图表 Modal 在此基础上增加 `.chart-modal-content` 变体（更宽，90vw）。

### 2. 放大按钮：Canvas 上方绝对定位

按钮放置于 `.act-chart-section` 容器内，使用 `position: absolute; top: 8px; right: 8px`。图标使用 Unicode `⛶` 或 SVG，简约风格。

### 3. 放大渲染：独立 `drawPowerProfileChartExpanded()`

与 `drawPowerProfileChart()` 共享数据（从 `activityDetail.power_profile` 读取），但使用独立的 canvas ID (`power-profile-canvas-expanded`) 和更大的尺寸。Modal 打开时调用渲染，关闭时清理。

### 4. X 轴刻度：动态计算

放大版每 ~5 分钟显示一个时间标签（原始版每段 1/5 总时长）。刻度数量 = max(5, floor(total_min / 5))。避免标签重叠。

## Risks / Trade-offs

- **Modal 打开时 Canvas 未渲染**：`v-if` 可能导致 DOM 未就绪 → 使用 `v-show` + `nextTick()` 确保 canvas 存在后再绘制
