## Context

当前 `power_profile` 含 `time_sec`/`power`/`hr`，横轴为累计时间。Garmin Connect 功率图使用距离(km) 作为横轴，并叠加平均功率参考线。用户期望对齐此体验。

## Goals / Non-Goals

**Goals:**
- 横轴改为距离 (km)，更直观关联路线位置
- 放大弹窗更长（canvas 450px），刻度间距拉开
- 图表上绘制平均功率虚线 + 文字标签

**Non-Goals:**
- 不提供时间/距离切换（保持简洁）
- 不修改心率区间等其他图表

## Decisions

### 1. 距离计算：后端累积 Haversine

`power_profile` 构建时同步计算累计距离：从 track_data 的 lat/lon 逐点累加 haversine 距离。`PowerProfilePoint` 新增 `dist_km: float`。

### 2. 横轴刻度：距离（km）

Garmin 风格刻度策略：
- 总距离 < 10km → 每 1km 一个标签
- 10-50km → 每 5km 一个标签
- > 50km → 每 10km 一个标签

### 3. 平均功率虚线

在图表绘制完成后，计算 `avgPower = mean(power_profile.map(p => p.power))`。在对应 Y 坐标绘制水平虚线（`strokeStyle: '#f39c12'`，`setLineDash([6,4])`），左端显示 "平均 xxx W" 标签。

### 4. 放大弹窗加长

canvas 高度从 420px → 450px，横轴标签间距相应拉开。
