## Why

最新添加的海拔面板功能引入了两个 bug：
1. **地图无法加载**：`#map-container` 改为 `display:flex;flex-direction:column` 后，`#map-area{flex:3}` 在父容器高度计算不确定时无法获得有效高度，导致 `#map` 高度为 0，`initMap()` 持续重试失败
2. **爬坡段侧边栏提前出现**：侧边栏 overlay 和 sidebar 元素放在 `#app` 主 flex 容器内，可能干扰布局

## What Changes

- **修复地图加载**：`#map-container` 不使用 flex column 布局，改用 `:class` 动态切换高度百分比
  - `#map-area` 默认 `height: 100%`，当 `elevationData != null` 时切换为 `height: 75%`
  - `#elevation-panel` 默认隐藏（`v-show`），有数据时显示并占 `height: 25%`
  - `#map-container` 添加 `:class="{ 'has-elevation': elevationData != null }"` 绑定
- **修复侧边栏**：确认 overlay/sidebar 在 `#map-container` 外部，`position:fixed` 不影响布局流
- CSS 中移除 `#map-container` 的 `flex-direction:column`，移除 `#map-area` 的 `flex:3`，改用高度百分比

## Capabilities

### New Capabilities

_无新增能力。_

### Modified Capabilities

_无现有 spec 需要修改。_

## Impact

- `static/index.html` — `#map-container` 添加 `:class` 绑定
- `static/css/style.css` — 修改 `#map-container`、`#map-area`、`#elevation-panel` 的布局方式
