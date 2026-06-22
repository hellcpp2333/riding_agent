## Context

骑行路线助手 Web 应用有三个 Tab（对话、路书、运动），共享右侧地图区域。近期运动页面新增了功率曲线图和功率区间着色路线功能，引入了 `showPowerLegend` 状态和对应的地图图例 UI。该功能在实现时存在两个状态管理缺陷：

1. **功率图例无条件显示**：图例 UI 的 `v-show` 仅绑定了 `showPowerLegend`，未检查当前 Tab 和活动选中状态，导致对话页和路书页的地图上也显示功率区间图例
2. **地图状态清理不完整**：`clearMapOverlays()` 函数（用于路书选择和详情切换）缺少对 `showPowerLegend` 的重置，可能导致跨页面状态污染，使路书的高程面板、爬坡段等细节无法正常加载

关键组件关系：
- `clearMap()` — 完整清理（调用 `map.clearOverlays()` + 重置所有状态），用于对话页路由绘制和活动页路由绘制
- `clearMapOverlays()` — 轻量清理（手动移除 tracked overlays + 部分状态重置），用于路书选择和切换
- `drawActivityRoute()` — 调用 `clearMap()` 后按功率分段着色，设置 `showPowerLegend = true`

## Goals / Non-Goals

**Goals:**
- 功率区间图例仅在运动Tab且选中具体运动记录时显示
- 路书页选择路书后，爬坡段标记、高程面板等细节正常加载和渲染
- `clearMapOverlays()` 覆盖所有需要重置的地图状态

**Non-Goals:**
- 不修改功率图例本身的样式或内容
- 不新增功率相关的功能特性
- 不修改后端 API 逻辑
- 不修改爬坡检测和高程计算算法

## Decisions

### 1. 功率图例可见性通过 v-show 条件控制

**方案**: 在 `v-show` 中增加 `currentTab === 'activities' && selectedActivity` 条件。

```html
<!-- 修改前 -->
<div id="power-legend" v-show="showPowerLegend" class="power-legend">

<!-- 修改后 -->
<div id="power-legend" v-show="showPowerLegend && currentTab === 'activities' && selectedActivity" class="power-legend">
```

**理由**: 
- 最小化改动，仅在模板层增加条件判断
- Vue 响应式变量 `currentTab` 和 `selectedActivity` 已存在，无需新增状态
- 即使 `showPowerLegend` 意外为 `true`，额外条件也能兜底

**备选方案**（未采用）:
- 在 Tab 切换时通过 `watch(currentTab)` 手动设置 `showPowerLegend = false`：额外引入 watcher，增加维护成本
- 在图例组件中加入 props：过度工程化，当前无需组件拆分

### 2. clearMapOverlays 补齐缺失的状态重置

**方案**: 在 `clearMapOverlays()` 函数末尾增加 `showPowerLegend.value = false`。

**当前缺失项**:
| 状态 | clearMap() | clearMapOverlays() |
|------|-----------|-------------------|
| showPowerLegend | ✓ | **✗ 缺失** |
| elevationData | ✓ | ✓ |
| climbSegments | ✓ | ✓ |
| climbPolylines | ✓ | ✓ |
| currentMarkers | ✓ | ✓ |

`selectRoute()` 调用 `clearMapOverlays()` 后立即通过 `handleElevationData()` 恢复高程/爬坡状态，因此这些字段的清理是正确的。唯一遗漏是 `showPowerLegend`，它不会被后续逻辑重新设置（路书不需要功率图例），导致残留。

**理由**:
- 保证 `clearMapOverlays()` 与 `clearMap()` 在状态重置范围上一致
- 路书选择流程无需感知功率状态

## Risks / Trade-offs

- **低风险**: 改动仅在 2-3 行 HTML/JS，不影响数据流或 API 调用
- **回归风险**: 如果 `currentTab` 或 `selectedActivity` 在非预期时机变更，图例可能意外隐藏。但这两个变量的语义明确，不存在歧义
- **回滚方案**: 直接 revert 修改即可恢复原状
