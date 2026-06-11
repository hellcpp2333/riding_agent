## Why

当前距离标记的样式是"上方文字标签 + 下方灰色圆点"的分离式布局，距离文字显示在圆点外部。改为佳明路书的经典风格：白色圆点直接覆盖在路线上，纯数字嵌入圆点内部（黑色字体），外部不显示任何文字。这种样式更简洁、更接近佳明原版路书的视觉语言。

## What Changes

- 标记圆点改为白色（`#fff`），保留深色细边框勾勒轮廓
- 距离数字（纯数字，无"km"后缀）居中显示在圆点内部，黑色字体
- 移除圆点外部的文字标签（原先的 `{N} km` 标签）
- 圆点尺寸增大到 22px，确保数字清晰可读
- `renderDistanceMarkers()` 函数的 HTML/CSS 模板整体替换

## Capabilities

### New Capabilities

_无新增能力。_

### Modified Capabilities

- `distance-markers`: 标记样式从"分离式灰点+外部文字"改为"白色圆点内嵌纯数字"

## Impact

- `static/index.html` — `renderDistanceMarkers()` 函数的 labelContent 模板
