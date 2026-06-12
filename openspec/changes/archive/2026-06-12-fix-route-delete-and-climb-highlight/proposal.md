## Why

路书板块的删除按钮点击后无任何反应——根因是 `ElMessageBox` 缺少 polyfill（`ElMessage` 已有），在 Edge Tracking Prevention 阻止 Element Plus CDN 加载时 `ElMessageBox.confirm()` 抛出 TypeError 被静默吞掉。同时，爬坡段切换（列表点击/上一个下一个）仅更新了侧边栏图表，地图上的爬坡叠加线没有区分高亮当前选中段，用户无法在地图上直观定位当前爬坡。

## What Changes

- 为 `ElMessageBox` 添加 polyfill（与现有 `ElMessage` polyfill 对齐），确保在 CDN 被阻止时删除确认对话框仍能工作
- 修复 `deleteRouteConfirm` 使用 `apiFetch` 统一请求（当前直接调用 `fetch` 绕过了 auth 过期处理）
- 爬坡段切换时重新绘制地图叠加线，当前选中段使用高不透明度/更粗线宽，非选中段降低不透明度以形成视觉区分
- 点击爬坡列表项或侧边栏前后切换时，地图视角自动平移到当前爬坡段区域

## Capabilities

### New Capabilities

- `climb-map-highlight`: 爬坡段在地图上高亮展示，选中段与非选中段有明确的视觉区分，且切换时地图跟随定位

### Modified Capabilities

- `climb-detection`: 更新 "Color-coded climb visualization on map" 需求，增加当前选中段高亮行为

## Impact

- `static/index.html` — `deleteRouteConfirm`、`drawClimbSegmentsOnMap`、`openClimbSidebar`/`prevClimb`/`nextClimb`、`ElMessageBox` polyfill
