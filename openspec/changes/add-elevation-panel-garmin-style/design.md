## Context

此变更是对已回退的海拔剖面图功能的重新实现，融合 Garmin Connect 设计语言，并增加关键的 UX 改进：面板仅在路线存在时显示。当前代码库为无剖面图基线。

## Goals / Non-Goals

**Goals:**
- 地图区域 75% + 数据面板 25%（flex: 3/1）
- 面板和爬坡按钮通过 `v-show` 绑定 `elevationData` 状态控制显隐
- Canvas 海拔填充面积图（无折线描边）
- UCI 爬坡段检测 + 地图着色 + 侧边栏
- 后端 `[ELEVATION_JSON]` + SSE `elevation` 事件
- Garmin Connect earth-tone 风格

**Non-Goals:**
- 不修改 open-elevation API 调用
- 不影响距离标记功能

## Decisions

### 1. 面板显隐控制：`v-show="elevationData != null"`
- **决定**: `#elevation-panel` 和"爬坡段"按钮使用 `v-show="elevationData != null"` 控制显隐。`clearMap()` 时设置 `elevationData = null` 隐藏面板，收到 SSE elevation 事件时赋值显示面板
- **替代方案**: `v-if` 会销毁/重建 DOM（包括 Canvas），导致绑图状态丢失 → 不采用
- **理由**: `v-show` 仅切换 `display`，保留 DOM 和 Canvas 状态；地图全高度时视觉更整洁

### 2-5. 与 `add-garmin-elevation-panel` 设计决策一致（Canvas 填充面积图、窗口差分爬坡检测、Polyline 叠加层、CSS 侧边栏）

## Risks / Trade-offs

- [Risk] `elevationData` 初始为 null，面板不占空间 → 首次规划路线后面板突然出现，地图高度跳变 → 对 `#map-area` 和 `#elevation-panel` 使用 CSS transition 平滑过渡（`transition: flex 0.3s ease`）
