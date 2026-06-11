## Why

骑行路线规划缺少地形可视化能力。用户看不到路线的海拔剖面图，无法评估爬坡难度和节奏。需要仿照 Garmin Connect 的设计语言，新增海拔数据面板和爬坡段分析功能。面板仅在路线上存在时显示，避免空白面板占用空间。

## What Changes

- 地图容器高度减少 1/4（flex: 3），底部新增数据面板（flex: 1），整体保持 flex 纵向分割
- **面板显隐控制**：地图上没有规划路线时，数据面板和爬坡段按钮均隐藏（`v-show="elevationData != null"`），地图占满全部高度
- **数据面板**：上方 1/5 为 stats 卡片区（距离 km、累计爬升 m、累计下降 m），下方 4/5 为 Canvas 海拔剖面图（纵轴海拔、横轴距离、纯填充面积图）
- **爬坡段检测**：前端实现 UCI 规则坡度检测（窗口差分 → 合并相邻段 → 过滤 <500m），按等级着色
- **地图爬坡标记**：在路线 polyline 上叠加彩色爬坡段覆盖层（线宽 8px）
- **爬坡侧边栏**：右侧滑出，显示导航、难度等级、平均坡度、距离、累计爬升、分段海拔图（坡度颜色编码）
- 后端恢复结构化高程数据通路：`[ELEVATION_JSON]` + SSE `elevation` 事件
- Garmin Connect 风格：earth-tone 配色、简洁排版

## Capabilities

### New Capabilities

- `elevation-profile-panel`: 路线数据摘要面板 + 海拔-距离剖面图，Garmin Connect 风格，仅在路线存在时显示
- `climb-segment-analysis`: UCI 爬坡段识别、地图着色标记、侧边栏详情

### Modified Capabilities

_无现有 spec 需要修改。_

## Impact

- `static/index.html` — 面板 HTML（含 `v-show` 显隐控制）、爬坡侧边栏、Vue 状态、Canvas 绑图、爬坡检测、地图着色
- `static/css/style.css` — 面板/侧边栏样式
- `app/agents/agent.py` — 恢复 `calculate_cumulative_distances` 导入和 `[ELEVATION_JSON]`
- `app/api/v1/routes.py` — 恢复 SSE `elevation` 事件
- `app/services/elevation_service.py` — 恢复 `calculate_cumulative_distances`
