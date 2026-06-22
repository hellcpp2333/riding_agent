## 1. 后端：PowerProfilePoint 增加 dist_km

- [x] 1.1 修改 `app/api/v1/schemas.py` — `PowerProfilePoint` 新增 `dist_km: float` 字段
- [x] 1.2 修改 `app/api/v1/activity_routes.py` — `get_activity()` 中构建 power_profile 时同步计算累计距离（Haversine）

## 2. 前端：横轴改为距离 + 平均功率虚线

- [x] 2.1 修改 `drawPowerProfileChart()` — X 轴改为距离(km)，按 Garmin 风格设置刻度间隔（<10km: 1km, 10-50km: 5km, >50km: 10km）
- [x] 2.2 在图表上绘制平均功率虚线 — 金黄色水平虚线（`#f39c12`，`setLineDash([6,4])`），左侧显示 "平均 xxx W"
- [x] 2.3 同步修改 `drawPowerProfileChartExpanded()` — 同样使用距离横轴 + 平均功率虚线，弹窗版 Y 轴 6 格、字体更大

## 3. 样式：放大弹窗加长

- [x] 3.1 修改 `static/css/style.css` — `#power-profile-canvas-expanded` 高度 420px → 450px

## 4. 验证

- [x] 4.1 代码验证通过 — 后端 schema 添加 dist_km 成功，前端两个图表函数均已使用距离横轴 + 平均功率虚线
- [x] 4.2 无功率时 v-if 跳过整个 chart-section，无图表无报错
