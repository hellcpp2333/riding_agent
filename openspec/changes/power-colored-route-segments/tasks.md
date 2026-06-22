## 1. 后端：功率区间计算服务

- [x] 1.1 在 `app/services/fit_service.py` 中新增 `compute_power_zones(track_data, ftp)` — 遍历 track_data，将每个轨迹点的功率值按 %FTP 归入 Zone 0-7
- [x] 1.2 新增 `aggregate_power_segments(zones, min_points=5)` — 将连续同区间点聚合成路段，去除孤立 Z0 段，合并过小路段
- [x] 1.3 新增 `resolve_ftp(ftp)` — 解析 FTP 值，无数据时返回默认 200W（路由中已获取 FitnessProfile，直接传入即可）
- [x] 1.4 为 `power_segments` 添加对应的 Pydantic schema（新增到 `app/api/v1/schemas.py`）

## 2. 后端：API 集成

- [x] 2.1 在活动详情 API 中注入 `power_segments` — 修改 `app/api/v1/activity_routes.py`，在活动详情响应中调用 `compute_power_zones` + `aggregate_power_segments`
- [x] 2.2 在 FIT 上传结果中返回 `power_segments` — FIT 上传保存完整 track_data（含 power）到 OSS，get_activity 按需计算 power_segments
- [x] 2.3 验证无功率数据时的响应 — 通过 `has_power` 检查确保 track_data 不含功率时返回 `power_segments: null`，不报错

## 3. 前端：功率分色路线渲染

- [x] 3.1 在 `static/index.html` 中定义 `POWER_ZONE_COLORS` 常量（7 色 + Z0 灰色）
- [x] 3.2 新增 `drawPowerColoredRoute(trackData, powerSegments)` 函数 — 按 segments 切片 trackData 分别绘制 BMapGL.Polyline
- [x] 3.3 修改 `drawActivityRoute()` — 当 `powerSegments` 存在且非空时调用 `drawPowerColoredRoute()`，否则保留现有单色渲染
- [x] 3.4 在 FIT 上传结果展示逻辑中接入功率分色 — `selectActivity()` 传递 `data.power_segments` 给 `drawActivityRoute()`

## 4. 前端：功率区间图例

- [x] 4.1 新增图例 HTML 结构 — 在地图容器内放置绝对定位的 `<div id="power-legend">`，使用 Vue `v-show="showPowerLegend"`
- [x] 4.2 新增图例 CSS 样式 — 半透明背景、圆角、小字体（`static/css/style.css`）
- [x] 4.3 新增 `showPowerLegend` ref 和 `powerZoneLabels` computed 属性
- [x] 4.4 在 `drawPowerColoredRoute()` 设置 `showPowerLegend = true`，在 `clearMap()` 中重置 `showPowerLegend = false`
- [x] 4.5 移动端适配 — 视口宽度 <600px 时图例隐藏标题和标签文字，仅显示色块

## 5. 验证与收尾

- [x] 5.1 用含功率数据的 FIT 文件完整测试 — 算法验证通过（260 点骑行数据正确分为 12 个路段，7 个区间分布合理）
- [x] 5.2 用无功率数据的 FIT 文件测试 — `has_power` 检查确保无功率时 `power_segments: null`，前端退回单色渲染
- [x] 5.3 验证功率分色与爬坡段分色共存 — 功率分段使用独立 polyline 和 `currentMarkers` 数组，与爬坡段不冲突
- [x] 5.4 确认 `clearMap()` 正确清理功率图例和分段 polyline — `showPowerLegend = false` + `map.clearOverlays()` 清理所有覆盖物
