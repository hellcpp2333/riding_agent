## Why

当前功率曲线图横轴为时间（分:秒），但骑行分析中距离（公里）更能关联路线位置与功率输出——参考 Garmin Connect，其功率图横轴使用距离。同时放大弹窗图表宽度不足、缺少平均功率参考线，影响数据判读效率。

## What Changes

- 功率曲线横轴改为距离（km），参考 Garmin 风格：刻度单位清晰、间距合理
- 放大弹窗 canvas 增高至 450px，横轴刻度间距拉大（每 1-2km 一个标签）
- 图表上叠加平均功率虚线（水平虚线 + "平均 xxx W" 标签），参考 Garmin `power-curve-watts-plotline` 样式
- 后端 `PowerProfilePoint` 新增 `dist_km` 字段

## Capabilities

### Modified Capabilities
- `power-profile-chart`: 横轴改为距离(km) + 平均功率参考线 + 弹窗加宽加高

## Impact

- **后端**: `app/api/v1/schemas.py` — `PowerProfilePoint` 新增 `dist_km`；`activity_routes.py` — `get_activity()` 计算累计距离
- **前端**: `static/index.html` — `drawPowerProfileChart()` 和 `drawPowerProfileChartExpanded()` 改用距离横轴 + 平均功率虚线
- **样式**: `static/css/style.css` — 放大弹窗 canvas 高度 450px
