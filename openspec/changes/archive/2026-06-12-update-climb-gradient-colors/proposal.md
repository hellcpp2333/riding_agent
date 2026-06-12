## Why

当前爬坡段的颜色方案（绿#4caf50 / 黄#fdd835 / 橙#ff9800 / 红#e53935 / 深红#880e0e）对比度过强且饱和度不一，在海拔剖面图和地图叠加线上视觉效果不够统一。需要替换为一套更协调、更符合骑行社区常用坡度配色规范的渐变方案，提升可视化的一致性和可读性。

## What Changes

- 更新爬坡段5级渐变色，将坡度`<3% / 3-6% / 6-9% / 9-12% / >12%`的颜色分别替换为 `#D8F5A2 / #f5bf2a / #f98925 / #ee3e3e / #b10d0d`
- 更新海拔剖面图（canvas）中爬坡段填充色及图例色块
- 更新地图叠加线（polyline）的爬坡段颜色
- 更新爬坡段侧边栏中坡度图例（`.climb-gradient-legend`）的颜色展示
- **BREAKING**: 修改 `climb-detection` spec 中的颜色映射规范

## Capabilities

### New Capabilities

- `climb-gradient-color-scheme`: 定义爬坡段坡度分级颜色映射方案，统一剖面图、地图叠加线和图例的颜色使用

### Modified Capabilities

- `climb-detection`: 更新 Requirement "Color-coded climb visualization on map" 和 "Elevation chart with gradient-colored climbs" 中的颜色映射值

## Impact

- `static/index.html` — 前端 Vue 组件中 `gradeColors` 数组、chart 填充逻辑、legend HTML、polyline strokeColor
- `openspec/specs/climb-detection/spec.md` — 颜色映射规范值
