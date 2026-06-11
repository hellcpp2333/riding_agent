## Context

当前距离标记的 CSS 样式内联在 `renderDistanceMarkers()` 函数中，位于 `static/index.html`。圆点 8px 直径，文字 11px，路线 polyline 宽度为 5-6px。圆点过小，与路线线条视觉占比失衡。

## Goals / Non-Goals

**Goals:**
- 圆点直径增大到 14px，完全覆盖路线宽度
- 文字和阴影比例协调

**Non-Goals:**
- 不改变标记生成逻辑（间隔、插值算法）
- 不修改标记位置

## Decisions

### 样式参数调整
- **圆点**: `width:8px;height:8px` → `width:14px;height:14px`
- **阴影**: `box-shadow:0 0 0 2px rgba(255,255,255,0.7)` → `0 0 0 3px rgba(255,255,255,0.8)`（白色光环分隔路线与圆点）
- **文字**: `font-size:11px` → `font-size:12px`，`padding:1px 5px` → `padding:2px 6px`

## Risks / Trade-offs

- 无风险。纯 CSS 数值修改，不影响功能逻辑。
