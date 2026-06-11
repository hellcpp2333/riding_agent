## 1. HTML 结构调整

- [ ] 1.1 在 `#elevation-panel` 上添加 `v-if="elevationData"`，无路线数据时不渲染面板
- [ ] 1.2 将 `.elevation-stats` 区域从 `.elevation-chart-container` 上方移到其下方（stats 在底部）
- [ ] 1.3 将 `#climb-sidebar` 和 `#climb-sidebar-overlay` 用 `v-if="climbSegments.length > 0"` 包裹

## 2. CSS 调整

- [ ] 2.1 调整 `#elevation-panel` 内部 flex 顺序：`.elevation-chart-container` flex:1，`.elevation-stats` 固定高度约 48px
- [ ] 2.2 确保 `#map-area` 在父容器 flex:1 且 `#elevation-panel` 不存在时自动占满全高

## 3. JS 逻辑调整

- [ ] 3.1 在 `handleElevationData` 中，数据到达后通过 `nextTick` 触发 `drawElevationChart()`
- [ ] 3.2 在 `clearMap` 中设置 `elevationData.value = null` 确保面板隐藏

## 4. 验证

- [ ] 4.1 验证无路线时地图全高，规划路线后面板出现，地图缩小
- [ ] 4.2 验证新建会话后面板消失，地图恢复全高
