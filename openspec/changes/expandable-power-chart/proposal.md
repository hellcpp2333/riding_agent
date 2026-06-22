## Why

当前功率曲线图嵌入活动详情侧边栏中，高度仅 220px，横轴空间有限，难以清晰查看长距离骑行的功率变化细节。参考 Garmin Connect 的活动分析页面，其功率图表支持放大至独立面板查看，横轴完整展开。本次添加图表放大功能改善数据可读性。

## What Changes

- 功率曲线图右上角新增放大按钮（⊕ 图标）
- 点击后弹出全屏风格 Modal，内嵌大尺寸 Canvas 重新渲染完整功率剖面图
- 放大后的横轴参考 Garmin 风格：时间刻度更密集，图表宽度自适应容器
- Modal 右上角有关闭按钮，点击遮罩层也可关闭

## Capabilities

### New Capabilities
<!-- None — this is a UI enhancement within existing capability -->

### Modified Capabilities
- `power-profile-chart`: 新增图表放大交互 — 放大按钮 + Modal 全尺寸渲染

## Impact

- **前端**: `static/index.html` — 新增放大按钮 HTML、Modal 结构、`expandPowerChart()`/`closePowerChart()` 函数、放大版 Canvas 渲染逻辑
- **样式**: `static/css/style.css` — 新增放大按钮样式、Modal 内图表容器样式
