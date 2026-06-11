## MODIFIED Requirements

### Requirement: Elevation profile chart
海拔剖面图的填充渐变 SHALL 使用多点 color stop（至少 3 个层级），从顶部 `rgba(58,125,68,0.30)` 渐变到中部 `rgba(58,125,68,0.12)` 再到底部 `rgba(58,125,68,0.02)`，呈现类似 Garmin Connect 的自然地形剖面视觉效果。

#### Scenario: Multi-stop gradient applied
- **WHEN** 海拔剖面图渲染
- **THEN** 填充区域使用三层渐变，顶部颜色最深底部最浅

### Requirement: Route stats summary display
Stats 指标 SHALL 以独立卡片形式展示，每个卡片使用 `--color-bg` 背景、`--radius-md` 圆角、`--shadow-sm` 微阴影。Stats 区域与图表区域之间 SHALL 有 `--color-border-light` 分隔线区分。

#### Scenario: Stats displayed as cards
- **WHEN** 路线数据面板渲染
- **THEN** 三个指标各占独立卡片，有背景色、圆角、阴影，与图表区域用分隔线隔开
