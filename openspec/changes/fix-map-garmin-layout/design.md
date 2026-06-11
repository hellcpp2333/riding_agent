## Context

参考 Garmin Connect 的路书页面架构（`refer/Garmin Connect.html`）：
- 页面为**可滚动单列布局**：上部是路书详情和分段数据（可滚动），下部是地图（固定高度）
- 地图使用 LeafletJS，容器 CSS 极简：`z-index:0;position:relative`，无 flex 嵌套
- 每个爬坡段有独立的海拔图（Recharts SVG），内联在分段列表中
- 地图不和任何内容面板共享垂直空间

本项目的适配方案：侧边栏（440px 固定宽度）作为数据展示区，地图填满剩余空间。海拔数据以卡片和可滚动列表形式展示在侧边栏内。

## Goals / Non-Goals

**Goals:**
- 地图 100% 可靠加载（不依赖复杂 CSS 高度计算）
- 海拔数据完整展示（stats、剖面图、爬坡段）
- Garmin 风格的侧边栏数据展示
- 保留后端高程数据通路

**Non-Goals:**
- 不改变后端
- 不改变距离标记功能

## Decisions

### 1. 架构：地图全高度 + 侧边栏数据面板
- **决定**: 地图容器仅含 `#map` 元素，无垂直分割。海拔数据全部展示在侧边栏中。
- **理由**: 消除地图初始化失败的根本原因（无高度竞争），与 Garmin 架构一致
- **CSS**: `#map-container{flex:1;position:relative}` + `#map{width:100%;height:100%}`

### 2. 侧边栏海拔展示区布局
- 在对话模式下，elevation 数据到达后在对话区顶部插入海拔信息卡（stats + 剖面图 + 爬坡段列表）
- 使用 Vue 条件渲染，数据到达前不显示
- 爬坡段列表项可点击，触发右侧滑出详情侧边栏

### 3. 爬坡段详情保留现有侧边栏设计
- 右侧滑出面板保持不变（`position:fixed`），但移出 `#map-container` 至顶层 `#app` 内
