## 1. 后端：高程数据结构化输出

- [x] 1.1 在 `elevation_service.py` 中新增 `calculate_cumulative_distances(points)` 函数，对轨迹点计算从起点累加的 Haversine 距离（米），返回带 `dist` 字段的点列表
- [x] 1.2 在 `agent.py` 的 `tools_node` 中，将高程轨迹点数据结构化（lat/lon/ele/dist），作为独立字段附在工具返回中（JSON 格式），而非纯文本拼接
- [x] 1.3 在 `routes.py` 的 `event_generator`（chat 和 plan_route）中新增 `elevation` SSE 事件类型，解析工具结果中的高程轨迹点并发送给前端

## 2. 前端：布局调整

- [x] 2.1 修改 `index.html` 的 `#map-container` 结构，在其下方新增 `#elevation-panel` 容器（占主内容区 25% 高度），两端用 flexbox 纵向排列
- [x] 2.2 在 `style.css` 中新增 `#elevation-panel` 样式：采用 earth-tone 设计系统变量（背景、边框、圆角），高度 25%，内边距 12px

## 3. 前端：路线数据摘要面板

- [x] 3.1 在 `index.html` 的 `#elevation-panel` 内创建 stats 区域（上方 1/5），用 flex 横向排列三个指标卡片：距离(km)、累计爬升(m)、累计下降(m)，每个卡片含数值和中文标签
- [x] 3.2 新增 Vue 响应式状态 `elevationData`（points 数组）和 `routeStats`（distance/gain/loss），在收到 `elevation` SSE 事件时更新
- [x] 3.3 在 `style.css` 中新增 stats 卡片样式，数值加粗大号字体，标签小号次要色

## 4. 前端：海拔剖面图（填充面积图）

- [x] 4.1 在 `#elevation-panel` 内创建 Canvas 元素（下方 4/5），设置合适尺寸，支持 Retina（devicePixelRatio 缩放）
- [x] 4.2 实现 `drawElevationChart(canvas, points)` 函数：绘制坐标轴（纵轴海拔 m、横轴距离 km）、网格线、纯填充面积图（无折线描边，仅用半透明渐变填充表现地形轮廓），点过多时降采样至 300 个
- [x] 4.3 新增图表样式（轴标签字体、网格线颜色、折线颜色、填充渐变）使用 earth-tone 色值
- [x] 4.4 响应窗口 resize 重绘图表

## 5. 前端：爬坡段识别与地图标记

- [x] 5.1 实现 `detectClimbSegments(points)` 函数：遍历高程轨迹点计算局部坡度（窗口差分），合并连续满足坡度>=3% 且长度>=500m 的区段，计算每个爬坡段的平均坡度、总距离、累计爬升
- [x] 5.2 实现 `drawClimbSegmentsOnMap(map, points, segments)` 函数：按坡度等级颜色（绿<3%/黄3-6%/橙6-9%/红9-12%/深红>12%）在地图上叠加彩色 Polyline 覆盖对应坐标段
- [x] 5.3 在收到 elevation 数据后自动执行爬坡段检测和地图标记

## 6. 前端：爬坡段侧边栏

- [x] 6.1 在 `index.html` 中新增 `#climb-sidebar` 侧边栏结构：顶部"第 X/共 Y 个"导航（左右箭头 + 文字），中间难度等级/平均坡度/距离/累计爬升详情区，底部爬坡段海拔-距离 Canvas
- [x] 6.2 实现侧边栏滑入/滑出动画（CSS transform translateX），overlay 遮罩层点击关闭
- [x] 6.3 实现 `drawClimbChart(canvas, segment, points)` 函数：绘制爬坡段海拔剖面图（纯填充面积，无折线描边），填充色按坡度等级分段着色（绿<3%/黄3-6%/橙6-9%/红9-12%/深红>12%）
- [x] 6.4 实现切换交互：上下箭头切换爬坡段 → 更新侧边栏内容 → 地图高亮当前段
- [x] 6.5 新增 Vue 响应式状态 `climbSegments`、`activeClimbIndex`、`showClimbSidebar`，以及切换/关闭方法
- [x] 6.6 新增 `#climb-sidebar` 所有样式，遵循 earth-tone design 系统

## 7. 集成与验证

- [x] 7.1 端到端测试：输入路线规划 → 地图缩小 → 面板显示 stats + 图表 → 爬坡段标记显示 → 侧边栏可切换
- [x] 7.2 边界情况验证：无高程数据路线、纯平路（无爬坡段）、超长路线降采样
