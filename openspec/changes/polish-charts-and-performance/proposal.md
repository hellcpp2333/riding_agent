## Why

存在三个体验问题：1) 爬坡面板中剖面图缺少横轴（距离）和纵轴（海拔）标签，底部图例未对齐图表宽度；2) 主高程剖面图使用蓝色填充，与 Garmin 的绿色系不符；3) 切换路书时存在明显卡顿，尤其在加载含大量轨迹点的 GPX 或触发远程 API 查询时。

## What Changes

### 1. 爬坡剖面图坐标轴 + 图例优化
- `drawClimbChart()` 新增 Y 轴海拔标注（m）、X 轴距离标注（km）、轴标题
- `.climb-gradient-legend` 改为 `justify-content:space-between` 对齐图表左右边界，色块间有均匀间隔
- 参考 Garmin `ClimbsUtil_legendItem` 布局

### 2. 主高程剖面图绿色系
- 填充渐变从蓝色 `rgba(25,118,210,...)` 改为 Garmin 绿色 `rgba(76,175,80,0.45)` → `rgba(76,175,80,0.02)`
- 参考 Garmin 剖面图使用 `#d8f5a2` 系绿色

### 3. 路书切换性能优化
- **前端**: `selectRoute()` 中 track_data 大数组（>500 点）在前端做降采样，减少 polyline 渲染点数
- **前端**: elevation chart canvas 绘制前先 `cancelAnimationFrame` 防止重复绘制
- **后端**: `GET /api/routes/{id}` 对 track_data 强制降采样至 500 点（已保留关键拐点），减少传输量
- **后端**: elevation 富化结果缓存到 Route 模型（避免每次加载都重新计算）

## Capabilities

### New Capabilities
- `elevation-chart-style`: 爬坡和主剖面图的 Garmin 风格坐标轴、颜色、图例规范

### Modified Capabilities
- `elevation-enrichment`: 路书高程数据缓存策略，避免重复计算

## Impact

- **后端**: `app/api/v1/route_routes.py`（track_data 降采样）、`app/models.py`（elevation 缓存字段，可选）
- **前端**: `static/index.html`（drawClimbChart 坐标轴、drawElevationChart 颜色、selectRoute 性能）
- **样式**: `static/css/style.css`（图例布局）
