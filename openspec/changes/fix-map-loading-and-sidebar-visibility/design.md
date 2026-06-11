## Context

Bug 根因分析：

1. **地图加载失败**：`#map-container{display:flex;flex-direction:column}` 使其成为 flex column 容器。`#map-area{flex:3}` 依赖父容器有确定的高度才能计算 flex 分配。在复杂的多层 flex 嵌套中，浏览器可能无法为 `#map-container` 确定高度（其父 flex row 中 `align-items:stretch` 对 `display:flex` 子元素的行为因浏览器而异），导致 `#map-area` 高度为 0 → `#map{height:100%}` 为 0 → BMapGL 初始化失败。

2. **侧边栏**：经检查，overlay 和 sidebar 元素在 `#map-container` 外部且为 `position:fixed`，不应影响布局。若用户看到侧边栏，实际应为 overlay 半透明遮罩仍在 DOM 中（尽管 opacity:0），视觉上不明显。此问题在修复 #1 后自然消失。

## Goals / Non-Goals

**Goals:**
- 修复地图加载
- 确保无路线时面板和侧边栏不显示

**Non-Goals:**
- 不改变功能逻辑

## Decisions

### 使用 `:class` 动态高度替代 flex column
- **决定**: `#map-container` 添加 `:class="{ 'has-elevation': elevationData != null }"`，CSS 中 `.has-elevation #map-area { height: 75%; }`，`#map-area` 默认 `height: 100%`
- **理由**: 百分比高度直接从 `#map-container`（已有确定高度）继承，不依赖 flex 分配算法，兼容性更好
- CSS 中 `#map-container` 恢复为简单的 `flex:1;position:relative`（原始状态）
