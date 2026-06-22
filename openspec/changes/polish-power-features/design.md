## Context

`power-colored-route-segments` 变更引入了功率分色路线和英文图例，但有三处需要打磨：
1. 图例标签为英文（Active Recovery, Endurance 等），中文用户不直观
2. FIT 上传后仅有 `ElMessage.success` 文字提示，无摘要展示
3. Power Curve 是"能力曲线"（各时长最大平均功率），非骑行功率剖面

当前 `drawPowerCurveChart()` 使用 `<canvas>` 绘制固定 9 点的功率-时长曲线。要改为功率-时间剖面图，需要完整的 `[{time_sec, power}]` 数据。后端 `get_activity` 返回的 `track_data` 仅含 lat/lon/ele（`TrackPoint`），不含 time/power。需要扩展 API 或新增独立字段。

## Goals / Non-Goals

**Goals:**
- 功率图例标签全部中文化
- FIT 上传成功后自动选中活动并展示详情摘要（名称、距离、时长、爬升、功率等）
- Power Curve → 功率-时间剖面图：横轴时间(分:秒)，纵轴功率(W)，展示完整骑行过程

**Non-Goals:**
- 不修改后端 FTP 计算逻辑
- 不改变 Power Curve 在后端的数据结构（`power_curve` 仍保留为最佳平均功率，供体能评估使用）
- 不增加新的图表交互（缩放、拖拽等）

## Decisions

### 1. 图例标签：直接改常量

`POWER_ZONE_NAMES` 常量从英文改为中文数组。无架构影响。

### 2. FIT 上传反馈：上传成功后自动选中活动

当前上传成功后仅 toast 提示。改进方案：上传返回的 `ActivityListItem` 已含完整摘要字段（name, distance, duration, elevation_gain, avg_speed, avg_hr, avg_power, tss），上传成功后：
- 将返回的 activity 插入到列表头部并自动选中
- 自动调用 `selectActivity()` 加载详情（含 track_data 和power_segments），地图自动渲染路线

这样用户上传后立即看到路线和摘要，体验接近 Garmin Connect。

### 3. 功率剖面图数据：新增 `power_profile` 字段

`get_activity()` 从 OSS 加载的完整 track_data 已含 `power` 和 `timestamp`。新增 `power_profile` 字段（`[{time_sec: float, power: int}]`），与 `track_data` 并列返回。前端 `drawPowerCurveChart()` 重写为折线剖面图。

**替代方案**：在 `TrackPoint` 中加 power/time → 否决，因为 `track_data` 只含有效 GPS 点，而功率剖面需要所有点。

### 4. 图表渲染：Canvas 折线图

保持 Canvas API，与现有风格一致（爬坡段图也用 Canvas）。X 轴为累计时间（秒→分:秒格式），Y 轴为功率（W）。线条颜色使用 `#ee3e3e`（与现有 Power Curve 一致），下方半透明填充。

数据点过多时（>2000 点）使用降采样（取每 N 个点的中位数）。

## Risks / Trade-offs

- **`power_profile` 数据量**：典型 2 小时骑行 = 7200 个点（每秒一个 record），JSON 约 150KB → 设置最大点数限制（1000 点），超过时降采样
- **Canvas 重绘性能**：每次切换活动都重新计算 → 用 `requestAnimationFrame` 防抖（已有模式）
- **上传后自动选中**：如果用户连续上传多个文件，会覆盖当前展示 → 可接受，用户关注最新上传
