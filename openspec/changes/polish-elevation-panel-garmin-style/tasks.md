## 1. CSS：Stats 卡片化

- [x] 1.1 修改 `.stat-card` 样式：添加 `--color-bg` 背景、`--radius-md` 圆角、`--shadow-sm` 微阴影、内边距 8px 12px
- [x] 1.2 修改 `.elevation-stats` 样式：添加 `border-top: 1px solid var(--color-border-light)` 顶部分隔、`--color-bg` 浅色背景、gap 调整为 12px

## 2. CSS：图表渐变优化

- [x] 2.1 更新 `#elevation-canvas` 相关注释或 inline 说明（渐变值在 JS 中定义，CSS 无直接变化，但样式文件需要更新以备参考）

## 3. JS：海拔剖面图渐变升级

- [x] 3.1 修改 `drawElevationChart` 中的渐变定义：从 2 stop 升级为 3 stop（`rgba(58,125,68,0.30)` → `rgba(58,125,68,0.12)` → `rgba(58,125,68,0.02)`）
- [x] 3.2 修改 `drawClimbChart` 中的分段填充色透明度，使其与主图风格统一

## 4. 验证

- [x] 4.1 验证 stats 卡片化效果：圆角、阴影、分隔线
- [x] 4.2 验证剖面图渐变层次更丰富
