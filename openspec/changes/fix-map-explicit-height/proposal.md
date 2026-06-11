## Why

经过分析 Garmin Connect 的渲染代码（`refer/地图缩放代码变化.md`），发现关键规律：

- **Garmin 的 map 容器使用内联样式 `style="height: 100%; width: 100%;"`** 强制设定尺寸
- 其父容器仅使用 `position: relative; z-index: 0`，不做 flex/grid 复杂嵌套

在我们的实现中，`.map-right` 作为 flex 子元素，高度由 `align-items: stretch` 隐式分配。虽然**使用高度**（used height）是 100vh，但**计算高度**（computed height）仍为 `auto`。CSS Grid 的 `fr` 单位和子元素的 `height: 100%` 都需要父元素有**确定的指定高度**才能解析——这导致整条高度链断裂，`#map` 最终高度为 0。

## What Changes

- `.map-right` 添加 `height: 100%`，从 `.main-app{height:100vh}` 获得确定高度
- 整条高度链：`.main-app(100vh)` → `.map-right(100%)` → Grid `1fr` → `#map-container(100%)` → `#map(100%)` 全部确定

## Impact

- `static/css/style.css` — 1 行
