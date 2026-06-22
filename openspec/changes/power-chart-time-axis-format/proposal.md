## Why

上轮将功率曲线横轴改为距离(km)，但 Garmin Connect 实际使用**时间**作为横轴，格式为 `H:MM:SS`（≥1小时）或 `MM:SS`（<1小时）。需切换回时间横轴并应用此格式化规则。

## What Changes

- 功率曲线横轴从距离(km)改回时间，标签格式：总时长 ≥1h → `H:MM:SS`，<1h → `MM:SS`
- 同时影响小图和放大弹窗两个图表

## Capabilities

### Modified Capabilities
- `power-profile-chart`: 横轴改回时间 + Garmin 时间格式

## Impact

- **前端**: `static/index.html` — `drawPowerProfileChart()` 和 `drawPowerProfileChartExpanded()` 的 X 轴标签计算逻辑
