## ADDED Requirements

### Requirement: Elevation trajectory data in SSE stream
后端 SHALL 在路线规划完成后，通过独立的 `elevation` SSE 事件发送结构化高程轨迹点数组。每个轨迹点包含：纬度(lat)、经度(lon)、海拔(ele)、累计距离(dist)。

#### Scenario: Elevation event emitted after route
- **WHEN** map_directions 工具返回结果且高程查询成功
- **THEN** SSE 流依次发送 route 事件和 elevation 事件

#### Scenario: Elevation event with sample data
- **WHEN** 路线包含 500 个原始坐标点且采样间隔为 100m
- **THEN** elevation 事件中的 points 数组包含采样后 ~100 个点，每个点含 lat/lon/ele/dist

### Requirement: Cumulative distance calculation
后端 SHALL 对采样后的高程轨迹点计算累计距离（从起点开始累加的 Haversine 距离，单位：米），作为 dist 字段包含在每个轨迹点中。

#### Scenario: Distance accumulation correct
- **WHEN** 轨迹包含 3 个点 A(0m), B(100m), C(250m)
- **THEN** 三点的 dist 分别为 0.0, 100.0, 250.0

### Requirement: Elevation service extension
`elevation_service.py` SHALL 新增 `calculate_cumulative_distances(points)` 函数，接受含 lat/lon 的坐标点列表，返回带 dist 字段的坐标点列表。

#### Scenario: Cumulative distances calculated
- **WHEN** 传入 [(lat1,lon1), (lat2,lon2), (lat3,lon3)]
- **THEN** 返回的点列表每个包含 dist 字段，值为从第一个点起的累计距离（米）

### Requirement: Elevation event JSON schema
elevation 事件 SHALL 使用以下 JSON 结构：
```json
{
  "points": [
    {"lat": 39.9, "lon": 116.4, "ele": 50.0, "dist": 0.0},
    {"lat": 39.91, "lon": 116.41, "ele": 55.0, "dist": 150.0}
  ]
}
```

#### Scenario: Valid JSON structure
- **WHEN** elevation 事件被前端解析
- **THEN** points 数组可迭代，每个元素含 lat/lon/ele/dist 四字段
