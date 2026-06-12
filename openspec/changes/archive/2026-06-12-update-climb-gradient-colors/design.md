## Context

当前爬坡段可视化有 3 处独立定义颜色——JS 侧 `gradeColors` 数组（地图叠加线）、canvas 填充色（`rgba(...)` 硬编码）、CSS `legend-dot` 背景色（图例）——三者颜色不完全一致，且图例颜色顺序与 JS 错位。改造目标是统一为单一颜色方案并集中管理。

当前状态：
- JS `gradeColors`: `#4caf50 / #fdd835 / #ff9800 / #e53935 / #880e0e`
- Canvas fill: `rgba(76,175,80,...) / rgba(253,216,53,...) / rgba(255,152,0,...) / rgba(229,57,53,...) / rgba(136,14,14,...)`
- CSS legend l1–l5: `#d8f5a2 / #c0ca33 / #f98925 / #f5bf2a / #ee3e3e`（与 JS 不一致且顺序错位）
- CSS difficulty badges: `.difficulty-1`–`.difficulty-5` 使用各自配色

## Goals / Non-Goals

**Goals:**
- 统一所有可视化位置（地图 polyline、剖面图 canvas、图例 legend、难度徽章）的颜色为同一套方案
- 新版颜色: `<3% → #D8F5A2`, `3-6% → #F5BF2A`, `6-9% → #F98925`, `9-12% → #EE3E3E`, `>12% → #B10D0D`
- 在 JS 中定义单一颜色常量，canvas fill 和地图线均引用该常量

**Non-Goals:**
- 不改动爬坡段检测算法、分类逻辑或数据结构
- 不改动剖面图布局/尺寸
- 不新增后端 API

## Decisions

1. **单一颜色源**: 在 JS 中定义 `CLIMB_GRADE_COLORS` 数组/对象，canvas fill 和 polyline 均从该源读取，CSS 变量可作为备选但本次优先保证 JS 端一致
2. **Canvas fill 用 hex 转 rgba**: 在 JS 中统一维护 hex 色值，fill 时通过工具函数 `hexToRgba(hex, alpha)` 转换为 rgba，避免颜色值在代码中重复出现
3. **CSS legend 直接与 JS 颜色对齐**: 图例 `.l1`–`.l5` 的 `background` 更新为对应 hex 值；难度徽章 `.difficulty-1`–`.difficulty-5` 的 `background`/`color` 同步调整以匹配新主题色

## Risks / Trade-offs

- CSS 中图例和徽章颜色需与 JS 手动保持同步（无编译时检查）→ 在代码注释中标注颜色来源于 `CLIMB_GRADE_COLORS` 常量
