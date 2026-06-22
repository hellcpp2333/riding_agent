## Context

路书详情（`selectRoute`）的加载流程：`clearMapOverlays()` → API 获取数据 → 绘制路线 → `handleElevationData()` 设置高程面板和爬坡段。

上一轮修复将 `clearMapOverlays()` 从逐条 `map.removeOverlay()` 改为 `map.clearOverlays()`。BMapGL 的 `clearOverlays()` 一次性清除所有覆盖物，但在跨 Tab 场景下，如果某些覆盖物（如 `BMapGL.Label` 距离标记）的引用状态与地图内部状态不一致，`clearOverlays()` 的行为可能与逐条移除不同，导致后续路线渲染路径（特别是 `handleElevationData`）受影响。

对比 commit `92412b8`（功率功能添加前的最后一个稳定版本），其 `clearMapOverlays` 使用逐条移除方案且工作正常。

## Goals / Non-Goals

**Goals:**
- 路书页选择路线后，路线概况栏（距离/爬升/下降）正常显示
- 路书页选择路线后，爬坡段标记正常渲染在地图上
- `clearMapOverlays()` 的覆盖物移除错误不阻断路线加载流程
- 不影响活动页的功率区间图例和功率曲线功能

**Non-Goals:**
- 不修改后端 API
- 不修改高程计算或爬坡检测算法
- 不修改功率相关的 UI 和逻辑

## Decisions

### 1. clearMapOverlays 恢复逐条移除 + try/catch

**方案**: 回归 commit `92412b8` 的逐条 `map.removeOverlay()` 方案，为每个循环增加 try/catch。

```javascript
function clearMapOverlays() {
    if (!map) return;
    for (const overlay of currentMarkers) {
        try { if (overlay) map.removeOverlay(overlay); } catch (e) { /* skip */ }
    }
    for (const dm of distanceMarkers) {
        try { if (dm) map.removeOverlay(dm); } catch (e) { /* skip */ }
    }
    for (const pl of climbPolylines.value) {
        try { if (pl) map.removeOverlay(pl); } catch (e) { /* skip */ }
    }
    currentMarkers = [];
    distanceMarkers = [];
    elevationData.value = null;
    routeStats.distance = 0;
    routeStats.gain = 0;
    routeStats.loss = 0;
    climbSegments.value = [];
    climbPolylines.value = [];
    activeClimbIndex.value = 0;
    showClimbSidebar.value = false;
    showPowerLegend.value = false;
    updateElevationPanel();
}
```

**理由**:
- 与已验证可工作的版本（`92412b8`）保持一致
- try/catch 是唯一的增强——原版如果某条移除失败会直接抛异常阻断后续流程
- 保留 `showPowerLegend` 重置（来自上一轮修复）

**备选方案**（未采用）:
- 继续使用 `map.clearOverlays()`：用户反馈路书高程面板仍不显示，说明此方案有问题

### 2. selectRoute 中 clearMapOverlays 移入 try 块

**方案**: 将 `clearMapOverlays()` 调用从 try 块外移入 try 块内。

```javascript
async function selectRoute(route) {
    selectedRouteId.value = route.id;
    try {
        clearMapOverlays();  // 移入 try 块
        const resp = await apiFetch(`/api/routes/${route.id}`);
        ...
    } catch (e) {
        ElMessage.error('加载路书详情失败');
    }
}
```

**理由**: 即使 `clearMapOverlays` 因任何原因失败，API 请求和路线渲染仍会执行，确保路线详情（高程面板、爬坡段）能被加载。

### 3. ElMessage.success 增加防御性检查

**方案**: `data.elevation_gain` 调用 `.toFixed()` 前检查其存在性。

```javascript
ElMessage.success(`${data.name}: ${(data.distance / 1000).toFixed(1)}km, 爬升${(data.elevation_gain ?? 0).toFixed(0)}m`);
```

**理由**: 如果 `elevation_gain` 为 `undefined`（极少数情况），`undefined.toFixed()` 会抛异常进入 catch 块，导致 "加载路书详情失败" 的误导性错误提示，且 `handleElevationData` 的结果被丢弃。

## Risks / Trade-offs

- **低风险**: 改动范围仅限于 `clearMapOverlays` 和 `selectRoute` 两个已有函数
- **try/catch 吞错**: 如果覆盖物移除持续失败，用户不会看到错误提示。但地图覆盖物泄漏远优于路线详情完全无法加载
- **回滚方案**: `git revert` 回到 `map.clearOverlays()` 版本即可
