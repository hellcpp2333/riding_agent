## Context

当前 `add-elevation-profile-panel` 实现中：
- `#elevation-panel` 始终渲染，占 `#map-container` 的 flex:1（25%），空状态时显示占位文字
- stats 栏在 elevation-panel 顶部（flex:1），图表在下方（flex:4）
- `#climb-sidebar` 始终存在于 DOM 中

需要改为按需显示，并将 stats 移到底部。

## Goals / Non-Goals

**Goals:**
- 无路线数据时地图保持全高（`#map-area` flex:1 占满，`#elevation-panel` 不渲染）
- 有路线数据时 `#elevation-panel` 出现，stats 在底部（面积占比不变，图表在上 stats 在下）
- 不影响地图初始化、BMapGL 加载、窗口 resize 行为

**Non-Goals:**
- 不改变 stats 的外观样式
- 不改变图表渲染逻辑

## Decisions

### 1. 面板显示控制：`v-if` vs `v-show`

**选择**：`v-if="elevationData"`

**理由**：无路线时完全从 DOM 移除，`#map-area` 自动回弹到全高（flex:1）。`v-show` 保留 DOM 占位，达不到"地图恢复全尺寸"的效果。

### 2. Stats 位置：底部 vs 顶部

**选择**：Chart 在上（flex:1），Stats 在底部（固定高度约 48px）。

**理由**：骑行应用（Strava、Komoot）惯例——海拔图在上、数据在下方。原 flex 比例倒置为 stats:chart = 1:4，现在改为 chart 占 flex:1，stats 定高。

### 3. 爬坡侧边栏条件渲染

**选择**：仅在 `climbSegments.length > 0` 时渲染侧边栏和 overlay。

**理由**：无爬坡段时无需 DOM 节点。

## Risks / Trade-offs

- [v-if 切换导致 Canvas 重新挂载] → `nextTick` 后重新调用 `drawElevationChart()`
- [面板出现/消失时地图 resize] → 地图自动适应父容器尺寸变化，BMapGL 会处理
