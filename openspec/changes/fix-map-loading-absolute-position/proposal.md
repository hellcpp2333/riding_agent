## Why

之前的两次修复尝试均未解决地图加载问题。根因是 CSS 百分比高度的规范限制：`#map-area { height: 100% }` 需要其父元素 `#map-container` 有**显式指定的高度**才能解析。但 `#map-container` 的高度来自 flex 拉伸（`align-items: stretch`），其 CSS 指定值仍为 `auto`，导致 `height: 100%` 无法解析 → `#map-area` 高度为 0 → `#map` 高度为 0 → BMapGL 初始化失败。

## What Changes

- 用 `position: absolute; inset: 0` 替代 `height: 100%`，使 `#map-area` 通过绝对定位填满 `#map-container`
- `.has-elevation #map-area { bottom: 25% }` 在面板显示时为底部留出空间
- `#elevation-panel` 改用 `position: absolute; bottom: 0; left: 0; right: 0; height: 25%`
- CSS 过渡改为 `transition: bottom 0.3s ease`

## Capabilities

_无新增或修改的 spec。纯 bug 修复。_

## Impact

- `static/css/style.css` — `#map-area`、`#elevation-panel` 的定位方式
