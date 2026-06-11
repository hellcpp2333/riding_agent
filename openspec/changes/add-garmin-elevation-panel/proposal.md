## Why

骑行路线规划缺少地形可视化能力。用户看不到路线的海拔剖面图，无法评估爬坡难度和节奏。需要仿照 Garmin Connect 的设计语言，新增海拔数据面板和爬坡段分析功能，让骑行者能直观了解路线的地形特征和爬升分布。

## What Changes

- 地图容器高度减少 1/4（flex: 3），底部新增数据面板（flex: 1），整体保持 flex 纵向分割
- **数据面板**：上方 1/5 为 stats 卡片区（距离 km、累计爬升 m、累计下降 m），下方 4/5 为 Canvas 海拔剖面图（纵轴海拔、横轴距离、纯填充面积图）
- **爬坡段检测**：前端实现 UCI 规则坡度检测（窗口差分计算局部坡度，合并连续 ≥3% 坡度且长度 ≥500m 的区段），按等级着色（绿<3%/黄3-6%/橙6-9%/红9-12%/深红>12%）
- **地图爬坡标记**：在路线 polyline 上叠加彩色爬坡段覆盖层
- **爬坡侧边栏**：右侧滑出，显示"第 X/共 Y 个"导航、难度等级、平均坡度、距离、累计爬升，以及该段的坡度颜色编码海拔图
- 后端恢复结构化高程数据通路：`[ELEVATION_JSON]` 输出 + SSE `elevation` 事件
- 整体 UI 风格模仿 Garmin Connect（深色 earth-tone 配色、简洁数据卡片、填充面积图）

## Capabilities

### New Capabilities

- `elevation-profile-panel`: 路线数据摘要面板 + 海拔-距离剖面图，Garmin Connect 风格
- `climb-segment-detection`: UCI 规则爬坡段识别、地图着色标记、侧边栏详情

### Modified Capabilities

_无现有 spec 需要修改。_

## Impact

- `static/index.html` — 布局调整（#map-area + #elevation-panel）、新增面板 HTML、爬坡侧边栏、Vue 响应式状态、Canvas 绑图逻辑、爬坡检测算法、地图着色覆盖层
- `static/css/style.css` — 面板样式、stats 卡片、图表容器、侧边栏动画
- `app/agents/agent.py` — 恢复 `calculate_cumulative_distances` 导入和 `[ELEVATION_JSON]` 输出
- `app/api/v1/routes.py` — 恢复 SSE `elevation` 事件发送
- `app/services/elevation_service.py` — 恢复 `calculate_cumulative_distances` 函数
