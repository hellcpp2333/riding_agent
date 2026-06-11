## Context

当前路线渲染流程：
- **聊天路线**：`drawRoute(routeData)` 解析百度地图返回的 route JSON → 提取 `steps[].path` 坐标点 → `BMapGL.Polyline` 渲染 → 添加起点/终点 Marker
- **导入路书**：`selectRoute(route)` 从后端获取 `track_data` → `BMapGL.Polyline` 渲染 → 添加起点/终点 Marker
- **清除**：`clearMap()` / `clearMapOverlays()` 通过 `map.clearOverlays()` + `currentMarkers = []` 清除

两条路线路径在同一个 `drawRoute` / `selectRoute` 函数中，是添加距离标记的最佳插入点。

BMapGL 支持 `BMapGL.Label` 用于在指定坐标显示文本标签，支持自定义样式（通过 CSS class 或内联样式）。可以将圆点 + 文字组合渲染为 Label，或使用多个 Label 分别渲染圆点和文字。

## Goals / Non-Goals

**Goals:**
- 聊天规划路线和导入路书上均显示距离标记
- 每 5km 间隔放置一个标记（5km、10km、15km…）
- 标记风格仿佳明路书：实心小圆点 + 距离文字
- 清除路线时一并移除距离标记
- 仅前端实现，不依赖后端改动

**Non-Goals:**
- 不修改后端 API
- 不添加点击交互（标记为纯展示）
- 不支持自定义标记间隔（固定 5km）
- 不对 POI 搜索结果添加标记

## Decisions

### 1. 使用 BMapGL.Label 渲染距离标记
- **决定**: 每个标记使用一个 `BMapGL.Label`，内容为 HTML/CSS 渲染的圆点 + 距离文字
- **替代方案**: 使用 `BMapGL.Marker` + 自定义 icon —— 需要额外图片资源或 Canvas 生成图标，复杂度更高
- **理由**: Label 天然支持 HTML 内容，样式灵活，无需额外资源文件；且 Label 不参与点击交互（符合 Non-Goal）

### 2. 标记点定位：沿 polyline 点序列插值
- **决定**: 对 polyline 的原始坐标点序列，使用 Haversine 公式计算逐段累计距离，当累计距离跨越 5km 整数倍时，在相邻两点之间线性插值出精确的 5km 位置
- **替代方案**: 在坐标点上找最接近 5km 倍数的点（不插值）—— 标记间距不准确，视觉上不均匀
- **理由**: 插值确保标记间距严格为 5km，视觉规整

### 3. 标记样式设计
- **决定**: 采用佳明风格——深灰色实心圆点（8px 直径）位于路线上，文字标签（如"5 km"）在圆点侧上方偏移 12px，白色半透明背景，深色文字，无边框
- **配色方案**: 圆点颜色 `#3a3a3a`（深灰），文字颜色 `#2c2416`（earth-tone），背景 `rgba(255,255,255,0.85)`

### 4. 标记生命周期管理
- **决定**: 距离标记 Label 对象存入独立数组 `distanceMarkers`，`clearMap()` 时遍历移除并清空
- **理由**: BMapGL 的 `map.clearOverlays()` 会清除所有覆盖物，但显式管理标记数组便于单独更新/移除

## Risks / Trade-offs

- [Risk] 密集坐标点的路线（如 step path 很密）计算量略大 → 实际坐标点通常 < 5000 个，Haversine 计算很快（< 10ms）
- [Risk] `map.clearOverlays()` 已清除所有覆盖物（含 Label），单独管理 `distanceMarkers` 数组可能导致引用已清除的 Label → `clearMap()` 应在调用 `clearOverlays()` 后将 `distanceMarkers` 置空即可
- [Trade-off] 导入路书的 `track_data` 坐标可能是 WGS-84 而地图是 BD-09，标记位置可能有偏移 → 坐标转换在 `selectRoute` 之前未做（现有导入路线也有此问题），本次不做处理
