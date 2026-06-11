## 1. 后端：恢复结构化高程数据通路

- [ ] 1.1 在 `elevation_service.py` 中恢复 `calculate_cumulative_distances(points)` 函数
- [ ] 1.2 在 `agent.py` 中恢复 `calculate_cumulative_distances` 导入，恢复 `[ELEVATION_JSON]` 输出
- [ ] 1.3 在 `routes.py` 的 `chat` SSE endpoint 中恢复 `elevation` 事件
- [ ] 1.4 在 `routes.py` 的 `plan_route` SSE endpoint 中恢复 `elevation` 事件

## 2. 前端：布局调整 + 面板显隐控制

- [ ] 2.1 修改 `#map-container` 为 flex column，内含 `#map-area`（flex:3）和 `#elevation-panel`（flex:1，`v-show="elevationData != null"`）
- [ ] 2.2 在 `style.css` 中新增布局样式，`#map-area` 和 `#elevation-panel` 使用 `transition: flex 0.3s ease` 平滑过渡
- [ ] 2.3 爬坡段按钮添加 `v-show="elevationData != null"`（与面板同步显隐）

## 3. 前端：数据面板 — Stats 卡片

- [ ] 3.1 在 `#elevation-panel` 内创建 `.elevation-stats` 区域（flex row），三个 stat-card
- [ ] 3.2 新增 Vue 响应式状态 `elevationData`（初始 null）和 `routeStats`（reactive），收到 SSE `elevation` 事件时更新
- [ ] 3.3 在 `style.css` 中新增 stats 卡片样式（Garmin earth-tone）

## 4. 前端：Canvas 海拔剖面图

- [ ] 4.1 在面板内创建 Canvas 元素（Retina 适配），placeholder 文字
- [ ] 4.2 实现 `drawElevationChart()`：坐标轴、网格线、填充面积图（半透明渐变、无折线描边）、降采样 300 点
- [ ] 4.3 响应 resize + Vue nextTick 后重绘

## 5. 前端：爬坡段检测

- [ ] 5.1 实现 `detectClimbSegments(points)`：5 点窗口差分 → 标记 ≥3% → 合并 <100m → 过滤 <500m
- [ ] 5.2 UCI 难度分级（4级/3级/2级/1级/HC级）

## 6. 前端：地图爬坡段着色

- [ ] 6.1 实现 `drawClimbSegmentsOnMap(points, segments)`：彩色 Polyline 叠加层（线宽 8px）
- [ ] 6.2 收到 elevation 数据后自动调用爬坡检测和地图着色

## 7. 前端：爬坡段侧边栏

- [ ] 7.1 HTML 结构：`#climb-sidebar-overlay` + `#climb-sidebar`（导航栏 + 详情 + Canvas）
- [ ] 7.2 CSS 动画：`transform: translateX(100%)` + overlay opacity
- [ ] 7.3 实现 `drawClimbChart(canvas, segment, points)`：分段海拔图，坡度颜色编码
- [ ] 7.4 Vue 状态：`climbSegments`、`activeClimbIndex`、`showClimbSidebar`、`activeSegment` computed
- [ ] 7.5 切换方法：`prevClimb()`/`nextClimb()`/`openClimbSidebar()`/`closeClimbSidebar()`
- [ ] 7.6 `clearMap()`/`clearMapOverlays()` 中重置 `elevationData = null` 及所有爬坡状态
- [ ] 7.7 `style.css` 中新增侧边栏样式

## 8. 验证

- [ ] 8.1 初始状态：无路线时面板和爬坡按钮隐藏，地图全高度
- [ ] 8.2 规划路线后：面板平滑出现，地图 75%，stats + 剖面图正确，爬坡段着色 + 侧边栏可用
- [ ] 8.3 清除路线后：面板隐藏，地图恢复全高度
- [ ] 8.4 边界：无高程数据、纯平路（无爬坡段）、超长路线降采样
