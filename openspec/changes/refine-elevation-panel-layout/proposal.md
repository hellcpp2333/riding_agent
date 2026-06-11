## Why

当前实现中 elevation panel 始终占地图下方 25% 高度，即使未规划路线也会显示空白占位，浪费地图空间。需要改为按需显示：无路线数据时地图保持全高，有路线数据时才展开面板。同时 stats 栏移到面板底部更符合骑行应用惯例。

## What Changes

- 海拔剖面面板由始终显示改为**条件显示**（`v-if` 有路线数据时才渲染），无数据时地图占满全高
- stats 栏从面板顶部移到面板底部（图表在上，距离/爬升/下降在下方），面积占比不变
- 爬坡段面板同样条件显示（无路线数据时不渲染相关 DOM）
- 不影响地图正常加载和渲染

## Capabilities

### Modified Capabilities

- `elevation-profile-panel`: 面板显示条件从始终可见改为 v-if 控制；stats 栏位置从上 1/5 移到最底部

## Impact

- `static/index.html` — elevation panel 添加 v-if；stats 区域移到 chart 下方；爬坡侧边栏条件渲染
- `static/css/style.css` — 调整 elevation-panel 内部 flex 顺序
