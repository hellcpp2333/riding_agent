## Why

当前 elevation panel 功能完整但视觉风格较素——纯色填充、简单字体、无层次感。参照 Garmin Connect 路线页面的设计语言（大面积渐变填充海拔剖面、卡片式 stats、精致的视觉层次），在保持项目 earth-tone 色彩体系的前提下提升面板的精致度和专业感。

## What Changes

- 海拔剖面图优化：增加更细腻的渐变（多点 color stop）、基线阴影效果、更精致的网格线
- Stats 卡片化：三个指标改为独立卡片（圆角、微阴影、hover 微动效），数据大号加粗、标签小号灰色置于下方
- 面板整体：增加微妙的顶部分隔阴影、stats 区域用浅色背景与图表区区分
- 爬坡侧边栏：同样优化卡片风格、图表渐变
- 所有改动使用项目现有 `--color-*` 变量，不引入新色系

## Capabilities

### Modified Capabilities

- `elevation-profile-panel`: 图表渐变优化、stats 卡片化、面板视觉层次提升

## Impact

- `static/css/style.css` — 图表渐变、stats 卡片、面板阴影等样式更新
- `static/index.html` — `drawElevationChart` 渐变逻辑微调
