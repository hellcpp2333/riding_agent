## Context

当前存在两个问题：

1. **路书删除按钮无响应**：`static/index.html` 第 305-310 行已有 `ElMessage` polyfill（应对 Edge Tracking Prevention 阻止 Element Plus CDN），但 `ElMessageBox` 缺少类似 polyfill。当 CDN 被阻止时，`ElMessageBox` 为 `undefined`，调用 `.confirm()` 抛出 `TypeError` 被 catch 吞掉（`e !== 'cancel'`），仅 console 输出。同时 `deleteRouteConfirm` 直接使用 `fetch` 而非 `apiFetch`，绕过了 401 拦截。

2. **爬坡段地图不联动高亮**：`openClimbSidebar`/`prevClimb`/`nextClimb` 仅更新 `activeClimbIndex` 并绘制 canvas 图表，不触 `drawClimbSegmentsOnMap` 重绘。`drawClimbSegmentsOnMap` 渲染所有段为相同样式（`strokeOpacity: 0.75`, `strokeWeight: 8`），无"当前选中"概念。

## Goals / Non-Goals

**Goals:**
- 添加 `ElMessageBox` polyfill 使删除确认对话框在 CDN 被阻止时仍能工作
- `deleteRouteConfirm` 改用 `apiFetch` 统一请求处理
- 爬坡段切换时重绘地图叠加线，当前选中段高亮（高透明度/粗线），非选中段淡化
- 切换爬坡段时地图自动平移到当前段中心

**Non-Goals:**
- 不修改后端 API
- 不改动爬坡检测算法或分类逻辑
- 不改动 sidebar 布局

## Decisions

1. **ElMessageBox polyfill**：使用原生 `window.confirm()` 作为回退，保持与 Element Plus 原始行为一致（确认返回 resolve，取消返回 reject('cancel')）
2. **drawClimbSegmentsOnMap 接受 activeIndex 参数**：渲染时分三段处理 — 当前选中段（高亮）、非选中段（低透明度）、无选中时（全部默认样式）。不引入新的 overlay 数组，直接在现有 `climbPolylines` 上重建
3. **地图平移**：使用 BMapGL `map.setViewport(segPoints)` 自动计算最佳视角适配爬坡段

## Risks / Trade-offs

- `setViewport` 的缩放可能过于激进（长段 zoom in 不够）→ 使用合适 padding
- 每次切换重绘所有 polyline 有轻微性能开销 → 爬坡段数量通常 ≤10，可接受
