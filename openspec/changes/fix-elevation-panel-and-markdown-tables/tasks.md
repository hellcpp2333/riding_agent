## 1. 修复海拔面板 Bug

- [x] 1.1 `agent.py`: `tools_node` 中将 `calculate_cumulative_distances` 提到 `calculate_elevation_stats` 之前
- [x] 1.2 `elevation_service.py`: `enrich_route_with_elevation()` 无 ele 分支先 `calculate_cumulative_distances` 再 `douglas_peucker_smooth`
- [x] 1.3 `elevation_service.py`: `calculate_elevation_stats()` 防御性处理——若 points 无 `dist` 则使用 index 计算近似距离
- [x] 1.4 验证：规划路线，确认海拔面板和爬坡段面板正常显示

## 2. Markdown 表格渲染

- [x] 2.1 `index.html`: `formatText()` 新增 Markdown 表格 → HTML `<table>` 的正则替换
- [x] 2.2 `style.css`: 新增 `.msg table` 样式（边框、斑马纹、响应式）
- [x] 2.3 验证：发送"列出北京5个景点，用表格展示名称和地址"，确认渲染为表格

## 3. 爬坡剖面图坡度颜色图例

- [x] 3.1 `index.html`: 爬坡侧边栏 `.climb-chart-container` 下方新增 `.climb-gradient-legend` HTML
- [x] 3.2 `style.css`: 图例样式——水平排列的色块 + 标签，参照 Garmin 配色
- [x] 3.3 验证：打开爬坡段侧边栏，确认图表下方有 5 级颜色标注
