## Context

当前 elevation panel 实现中，海拔剖面图使用简单的两色渐变（`rgba(58,125,68,0.35)` → `rgba(58,125,68,0.05)`），stats 区域为纯文本 flex 排列，无卡片容器。Garmin Connect 的设计语言特征是：细腻的多色渐变、卡片化指标、清晰的视觉分隔。

## Goals / Non-Goals

**Goals:**
- 海拔剖面图渐变升级为多点 color stop（顶部半透明 → 中部浅色 → 底部近乎透明），模拟 Garmin 的精致感
- Stats 三指标改为独立卡片，圆角 + 微阴影 + 浅色背景
- Stats 区域与图表区域用浅色背景或分隔线区分
- 爬坡侧边栏内的图表同步优化
- 全部使用现有 `--color-*` CSS 变量

**Non-Goals:**
- 不改变面板尺寸和布局结构
- 不引入新颜色体系
- 不改变交互逻辑

## Decisions

### 1. 剖面图渐变：多点 stop

**选择**：3 色 stop 渐变 — `rgba(58,125,68,0.30)` → `rgba(58,125,68,0.12)` → `rgba(58,125,68,0.02)`

**理由**：Garmin Connect 的海拔图有明显的"顶部浓、底部淡"层次，多点渐变更接近自然地形视觉。

### 2. Stats 卡片化

**选择**：每个 stat 用独立 `.stat-card` 容器，背景 `--color-bg`（浅米色）、border-radius `--radius-md`、box-shadow `--shadow-sm`。

**理由**：与 Garmin 的指标卡片风格一致，同时颜色完全来自 earth-tone 系统。

### 3. 图表与 Stats 区域分隔

**选择**：Stats 区域使用 `--color-bg` 背景 + 顶部分隔线 `border-top: 1px solid --color-border-light`。

**理由**：视觉上区分"图"与"数据"，层次清晰。

## Risks / Trade-offs

- [Canvas 渐变性能] → 多点渐变绘制开销可忽略，无影响
