## 1. 后端：恢复结构化高程数据通路

- [ ] 1.1 在 `elevation_service.py` 中恢复 `calculate_cumulative_distances(points)` 函数
- [ ] 1.2 在 `agent.py` 中恢复 `calculate_cumulative_distances` 导入，恢复 tools_node 中 `[ELEVATION_JSON]` 结构化输出
- [ ] 1.3 在 `routes.py` 的 `chat` SSE endpoint 中恢复 `elevation` 事件发送
- [ ] 1.4 在 `routes.py` 的 `plan_route` SSE endpoint 中恢复 `elevation` 事件发送

## 2. 前端：布局调整

- [ ] 2.1 修改 `#map-container` 为 flex column，内含 `#map-area`（flex:3）和 `#elevation-panel`（flex:1）
- [ ] 2.2 在 `style.css` 中新增面板布局样式

## 3. 前端：数据面板 — Stats 卡片

- [ ] 3.1 在 `#elevation-panel` 内创建 `.elevation-stats` 区域（flex row），三个 stat-card：距离(km)、累计爬升(m)、累计下降(m)
- [ ] 3.2 新增 Vue 响应式状态 `elevationData` 和 `routeStats`（reactive），在收到 `elevation` SSE 事件时更新
- [ ] 3.3 在 `style.css` 中新增 stats 卡片样式（Garmin earth-tone 配色、数值加粗、标签小号）

## 4. 前端：Canvas 海拔剖面图

- [ ] 4.1 在 `#elevation-panel` 内创建 Canvas 元素，支持 Retina（devicePixelRatio），placeholder 文字
- [ ] 4.2 实现 `drawElevationChart()` 函数：坐标轴（纵轴海拔/m、横轴距离/km）、网格线、填充面积图（半透明渐变、无折线描边）、降采样至 300 点
- [ ] 4.3 响应 window resize 重绘图表，监听 Vue 数据变化触发重绘

## 5. 前端：爬坡段检测

- [ ] 5.1 实现 `detectClimbSegments(points)` 函数：窗口差分（5 点）计算局部坡度 → 标记 ≥3% 连续段 → 合并间距 <100m 的相邻段 → 过滤 <500m 的段 → 返回段数组 `[{startIdx, endIdx, avgGrade, distance, elevationGain, difficulty, difficultyLabel}]`
- [ ] 5.2 实现 UCI 难度分级逻辑：根据平均坡度和累计爬升分为 4级/3级/2级/1级/HC级

## 6. 前端：地图爬坡段着色

- [ ] 6.1 实现 `drawClimbSegmentsOnMap(points, segments)` 函数：为每个爬坡段创建彩色 Polyline（线宽 8px）叠加在基础路线上，颜色按坡度等级：绿<3%/黄3-6%/橙6-9%/红9-12%/深红>12%
- [ ] 6.2 在收到 elevation 数据后自动调用爬坡段检测和地图着色

## 7. 前端：爬坡段侧边栏

- [ ] 7.1 在 HTML 中新增 `#climb-sidebar-overlay` 和 `#climb-sidebar` 结构：导航栏（左右箭头+"第 X/共 Y 个"）、详情区（难度/坡度/距离/爬升）、分段海拔 Canvas `#climb-canvas`
- [ ] 7.2 实现侧边栏滑入/滑出动画（CSS transform translateX + overlay opacity transition）
- [ ] 7.3 实现 `drawClimbChart(canvas, segment, points)` 函数：爬坡段海拔剖面图，填充色按坡度等级分段着色
- [ ] 7.4 新增 Vue 状态 `climbSegments`、`activeClimbIndex`、`showClimbSidebar`、`activeSegment` computed
- [ ] 7.5 新增"爬坡段"按钮，仅在有爬坡段时显示
- [ ] 7.6 实现切换方法 `prevClimb()`/`nextClimb()`/`openClimbSidebar()`/`closeClimbSidebar()`
- [ ] 7.7 在 `clearMap()`/`clearMapOverlays()` 中重置爬坡状态
- [ ] 7.8 在 `style.css` 中新增侧边栏全部样式（earth-tone design system）

## 8. 集成与验证

- [ ] 8.1 启动服务，规划一条有起伏的骑行路线（≥10km），验证：地图缩小、面板显示 stats + 填充面积图、爬坡段彩色标记、侧边栏可打开并切换
- [ ] 8.2 验证导入路书后同样支持剖面图和爬坡分析
- [ ] 8.3 验证边界情况：无高程数据路线、纯平路（无爬坡段）、超长路线降采样
