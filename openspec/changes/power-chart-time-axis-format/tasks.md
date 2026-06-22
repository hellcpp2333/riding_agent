## 1. 横轴改回时间 + Garmin 格式

- [x] 1.1 新增 `_fmtTime(sec)` 辅助函数 — ≥1h: H:MM:SS, <1h: MM:SS
- [x] 1.2 修改 `drawPowerProfileChart()` — X 轴从 `dist_km` 改为 `time_sec`，标签用 `_fmtTime()`
- [x] 1.3 修改 `drawPowerProfileChartExpanded()` — 同上，弹窗版刻度间距更大

## 2. 验证

- [x] 2.1 代码检查：格式函数正确，两图表均使用时间横轴，无残留 dist_km/maxDist 引用
