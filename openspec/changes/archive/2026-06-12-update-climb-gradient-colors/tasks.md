## 1. JavaScript — 统一颜色常量与地图叠加线

- [x] 1.1 在 `static/index.html` 中定义 `CLIMB_GRADE_COLORS` 常量数组 `[null, '#D8F5A2', '#F5BF2A', '#F98925', '#EE3E3E', '#B10D0D']`，替换原 `gradeColors`
- [x] 1.2 添加 `hexToRgba(hex, alpha)` 工具函数，供 canvas fill 使用
- [x] 1.3 更新地图 polyline 渲染代码，使用 `CLIMB_GRADE_COLORS[seg.difficulty]`

## 2. Canvas — 更新剖面图填充色

- [x] 2.1 更新 `climb-canvas` 绘制逻辑中的坡度填充色判断，改为 `hexToRgba(CLIMB_GRADE_COLORS[level], 0.5)` 方式，移除硬编码 rgba 值
- [x] 2.2 确保填充色对应的梯度分界值与颜色常量索引一致（<3%→1, 3-6%→2, 6-9%→3, 9-12%→4, >12%→5）

## 3. CSS — 更新图例和难度徽章

- [x] 3.1 更新 `static/css/style.css` 中 `.climb-gradient-legend .legend-dot.l1`–`.l5` 的 `background` 为对应 hex 色值
- [x] 3.2 更新 `.difficulty-1`–`.difficulty-5` 的 `background`/`color` 以匹配新的颜色主题

## 4. 验证

- [x] 4.1 启动服务，发送骑行路线规划请求，确认爬坡段地图叠加线颜色正确
- [x] 4.2 确认海拔剖面图中爬坡段填充色与地图线颜色一致
- [x] 4.3 确认爬坡段侧边栏中的图例（`.climb-gradient-legend`）颜色与 JS 端一致
- [x] 4.4 确认难度徽章在爬坡列表和侧边栏中的颜色与新方案协调
