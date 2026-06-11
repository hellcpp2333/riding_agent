## Why

上一轮将 `#map` 改为 `position:absolute;inset:0` 后，Baidu BMapGL 无法正确读取地图元素的 `offsetWidth`/`offsetHeight`（absolute 元素在某些浏览器/场景下尺寸报告异常），导致 `initMap()` 检测到尺寸为 0 而持续重试失败。

## What Changes

- `#map` 恢复为 `width:100%;height:100%`（普通流）
- `#map-container` 添加 `height:100%`（从 Grid 行获取确定高度）
- 移除 `position:absolute;inset:0` 和 `min-height:0`

CSS Grid 的 `1fr`/`3fr` 行高是确定值，`height:100%` 可正确解析。

## Impact

- `static/css/style.css` — 3 行
