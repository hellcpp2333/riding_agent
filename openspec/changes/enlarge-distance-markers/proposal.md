## Why

当前距离标记点的圆点直径仅 8px，在路线 polyline（6px 宽）上视觉占比太小，不够醒目。需要调大圆点使其刚好覆盖路线宽度，让标记更突出、更接近佳明路书的视觉效果。

## What Changes

- 增大距离标记圆点直径：从 8px → 14px
- 增大阴影扩散范围：从 `0 0 0 2px` → `0 0 0 3px`，确保圆点边缘与路线之间有清晰的白色分隔
- 文字字号从 11px → 12px，保持与圆点比例协调

## Capabilities

### New Capabilities

_无新增能力。_

### Modified Capabilities

- `distance-markers`: 标记圆点尺寸从 8px 增大到 14px，文字从 11px 增大到 12px

## Impact

- `static/index.html` — `renderDistanceMarkers()` 函数中的 inline CSS 样式值
