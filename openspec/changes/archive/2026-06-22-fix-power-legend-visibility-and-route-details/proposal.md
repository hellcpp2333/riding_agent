## Why

运动页面新增功率区间图例（power legend）和功率曲线功能后，出现两个回归问题：(1) 功率区间图例在所有页面的地图上都显示，而它只应在运动页且选中具体运动记录时出现；(2) 路书页点击路书后，之前正常工作的爬坡段标记、高程面板等细节无法加载，原因是地图状态清理逻辑不完整导致跨页面状态污染。

## What Changes

- **功率图例可见性条件**: 功率区间图例仅在 `currentTab === 'activities'` 且 `selectedActivity` 不为空时才显示，对话页和路书页的地图上不显示
- **地图状态清理完整性**: `clearMapOverlays()` 函数补齐缺失的状态重置（包括 `showPowerLegend`），确保切换页面/选择路书时地图状态干净
- **路书详情加载修复**: 修复因跨Tab切换时地图覆盖物残留导致的路书爬坡段、高程面板等详情无法正常渲染的问题

## Capabilities

### New Capabilities

- `power-legend-scope`: 功率区间图例的可见性范围控制，限定在运动页选中运动记录时显示

### Modified Capabilities

<!-- 本次为纯 bug 修复，不涉及已有 spec 的需求变更 -->

## Impact

- `static/index.html` — 前端单文件，包含所有 UI 模板和 JS 逻辑
  - 功率图例 `v-show` 条件增加 Tab 和选中状态判断
  - `clearMapOverlays()` 函数补充 `showPowerLegend` 重置
  - 确保跨 Tab 切换时地图覆盖物状态一致
