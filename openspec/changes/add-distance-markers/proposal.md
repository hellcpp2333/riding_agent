## Why

当前地图上展示的路线只有起点和终点两个标记，长距离路线（如 50km+）中途缺乏距离参考点。骑行者无法直观了解已骑行多远、前方还有多少距离。仿照佳明（Garmin）路书的风格，在路线上每隔 5km 添加距离标记点，让用户一眼看清路线的距离尺度和分段节奏。

## What Changes

- 前端新增 Haversine 距离计算函数，对路线点序列计算累计距离
- 前端实现 `addDistanceMarkers(points)` 函数：沿路线每 5km 插值定位一个标记点，使用 BMapGL 自定义覆盖物渲染佳明风格距离标记（实心圆点 + 距离文字标签，如"5 km"、"10 km"）
- `drawRoute()` 渲染聊天路线后自动调用距离标记函数
- `selectRoute()` 渲染导入路书后自动调用距离标记函数
- `clearMap()` / `clearMapOverlays()` 清除时一并移除距离标记
- 距离标记样式：深色小圆点（直径 8px）贴合路线，文字标签偏移展示距离公里数，配色与路线主色调协调

## Capabilities

### New Capabilities

- `distance-markers`: 路线距离标记点系统，沿地图上的路线每 5km 放置佳明风格的标记（圆点 + 距离文字），适用于聊天规划路线和导入路书

### Modified Capabilities

_无现有 spec 需要修改。_

## Impact

- `static/index.html` — 新增 JS 函数：Haversine 距离计算、5km 插值定位、BMapGL.Label 距离标记渲染；修改 `drawRoute()`、`selectRoute()` 添加标记调用；修改 `clearMap()`/`clearMapOverlays()` 清理标记引用
