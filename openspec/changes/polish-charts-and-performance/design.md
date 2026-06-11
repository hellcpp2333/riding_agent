## Context

当前剖面图缺少坐标轴标注（爬坡图表完全无轴标签），主剖面图颜色为蓝色系，路书切换存在性能问题。

## Decisions

### 1. 爬坡图表坐标轴
- Y 轴（左）: 显示 3-4 个海拔刻度值 + 单位 "m"
- X 轴（下）: 显示 3-4 个距离刻度值 + 单位 "km"
- padding 调整: left 40→48（容纳 4 位数海拔），bottom 28→36（容纳轴标题）

### 2. 主剖面图颜色
- 蓝色 `rgba(25,118,210,0.55/0.25/0.02)` → Garmin 绿色 `rgba(76,175,80,0.45)` → `rgba(129,199,132,0.15)` → `rgba(200,230,201,0.02)`
- 曲线描边改为 `#66bb6a`

### 3. 性能优化策略
- **前端降采样**: track_data > 500 时，前端用步进取样（不超过 500 个 polyline 点）
- **canvas 防抖**: `drawElevationChart()` 使用 `requestAnimationFrame` 并在重绘前 cancel
- **后端降采样**: route detail API 返回的 track_data 硬上限 500 点（地图渲染超过此数无意义）
- **避免重复富化**: elevation 数据如果后端已计算过则缓存

## Open Questions

- 是否给 Route 模型加 `elevation_json` 字段做持久化缓存？→ 建议后续优化，当前先做前端降采样。
