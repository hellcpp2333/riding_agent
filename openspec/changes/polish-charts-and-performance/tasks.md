## 1. 爬坡剖面图坐标轴 + 图例

- [x] 1.1 `index.html`: `drawClimbChart()` 新增 Y 轴海拔标注（m）和 X 轴距离标注（km）
- [x] 1.2 `index.html`: `drawClimbChart()` 新增轴标题 "距离 (km)" 和 "海拔 (m)"，调整 padding
- [x] 1.3 `style.css`: `.climb-gradient-legend` 改为 `justify-content:space-between;padding:0 48px 0 48px` 对齐图表内容区

## 2. 主高程剖面图绿色系

- [x] 2.1 `index.html`: `drawElevationChart()` 填充渐变从蓝色改为 Garmin 绿色系
- [x] 2.2 `index.html`: `drawElevationChart()` 曲线描边色改为 `#66bb6a`

## 3. 路书切换性能优化

- [x] 3.1 `route_routes.py`: `GET /api/routes/{id}` track_data 后端降采样至最大 500 点
- [x] 3.2 `index.html`: `selectRoute()` 前端 polyline 点 >500 时进一步降采样
- [x] 3.3 `index.html`: `drawElevationChart()` 添加 `cancelAnimationFrame` 防抖
- [x] 3.4 `index.html`: `drawClimbChart()` 添加 `cancelAnimationFrame` 防抖
