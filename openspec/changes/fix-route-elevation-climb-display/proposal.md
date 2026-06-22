## Why

路书页选择路线后，地图下方的路线概况栏（距离/爬升/下降）和爬坡段面板不显示。经对比 git 历史（commit `92412b8`），原版 `clearMapOverlays()` 使用逐条 `map.removeOverlay()` 移除覆盖物，工作正常；上一轮修复中将其替换为 `map.clearOverlays()` 后，BMapGL 的 `clearOverlays()` 调用可能因覆盖物引用状态不一致而导致后续的路线渲染流程受影响。需要恢复到已验证可工作的逐条移除方案，并增强错误鲁棒性。

## What Changes

- `clearMapOverlays()` 恢复为逐条 `map.removeOverlay()` 方案（与原版 `92412b8` 一致），每条移除包裹 try/catch 防止个别失败阻断整体流程
- 将 `selectRoute()` 中的 `clearMapOverlays()` 调用移入 try 块内，确保即使清理失败也能执行后续的路线加载
- 保留之前添加的 `showPowerLegend` 重置逻辑
- 在 `selectRoute()` 末尾的 `ElMessage.success` 前增加 `data.elevation_gain` 的防御性检查，避免 `undefined.toFixed()` 导致异常

## Capabilities

### New Capabilities

- `route-detail-resilience`: 路书详情加载的错误鲁棒性——即使地图覆盖物清理失败，也要保证路线、高程面板、爬坡段正常加载

### Modified Capabilities

<!-- 纯 bug 修复，不修改已有 spec -->

## Impact

- `static/index.html`:
  - `clearMapOverlays()` — 恢复逐条移除 + try/catch 包裹
  - `selectRoute()` — 移动 `clearMapOverlays()` 到 try 块内，增加防御性检查
