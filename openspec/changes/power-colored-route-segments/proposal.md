## Why

当前查看 FIT 文件活动路线时，地图上只以单一红色折线展示轨迹，无法直观了解骑行过程中功率的输出分布。参考 Garmin Connect 的活动详情页，其路线会根据各路段功率区间着色（7 个功率区间对应不同颜色），用户可以一目了然地看到哪里输出高功率、哪里在恢复。引入此能力可大幅提升骑行数据分析的直观性和专业度。

## What Changes

- 后端新增功率区间计算服务：根据 track_data 中各点的功率值和用户 FTP，将每个轨迹点归入 7 个功率区间（Zone 1-7，对应 Active Recovery / Endurance / Tempo / Threshold / VO2Max / Anaerobic / Neuromuscular）
- 后端 API 响应中新增 `power_segments` 字段：按连续相同功率区间将轨迹点聚合为路段列表，每个路段包含起止索引、功率区间编号和平均功率
- 前端新增 `drawPowerColoredRoute()` 函数：根据功率区间为不同路段绘制不同颜色的 BMapGL 折线（7 色方案参考 Garmin Connect 的功率区间配色）
- 前端在活动详情页（`drawActivityRoute`）和 FIT 上传结果展示中，当存在功率数据时自动使用分色渲染替代单色折线
- 前端新增功率区间图例组件：在地图角落显示 7 个功率区间的颜色-标签对应关系

## Capabilities

### New Capabilities
- `power-zone-calculation`: 后端功率区间计算 — 根据轨迹点功率和用户 FTP，将每个点归入 7 个功率区间并聚合成连续路段
- `power-colored-map-render`: 前端功率分色路线渲染 — 在百度地图上按功率区间使用不同颜色绘制路段，含图例展示

### Modified Capabilities
<!-- No existing specs need requirement changes -->

## Impact

- **后端**: `app/services/fit_service.py` — 新增功率区间计算函数；`app/api/v1/fitness_routes.py` 或 `app/api/v1/activity_routes.py` — API 响应新增 `power_segments` 字段
- **前端**: `static/index.html` — 新增 `drawPowerColoredRoute()` 替换/扩展 `drawActivityRoute()`；新增功率图例 HTML 结构和样式
- **依赖**: 无新增第三方依赖，复用现有 `fitdecode` 解析的功率数据和百度地图 BMapGL Polyline API
