## Context

此变更是对之前已回退的 `add-elevation-profile-panel` + `polish-elevation-panel-garmin-style` + `refine-elevation-panel-layout` 三个 change 的重新实现，融合了所有改进并以 Garmin Connect 为设计参考。当前代码库已回退至无剖面图状态，各文件为干净基线。

已有的距离标记功能（`add-distance-markers`、`enlarge-distance-markers`、`redesign-distance-markers-white-dot`）与本次变更互不影响——距离标记操作 polyline 点序列，爬坡标记操作高程轨迹点。

## Goals / Non-Goals

**Goals:**
- 地图区域占主内容 75%，数据面板占 25%（flex: 3/1）
- 数据面板含 stats 卡片（距离/爬升/下降）和 Canvas 海拔填充面积图
- 爬坡段检测（UCI 规则：≥3% 坡度 + ≥500m 长度）
- 地图路线上彩色爬坡段覆盖层
- 爬坡侧边栏（右侧滑出）含导航、详情、分段海拔图
- 后端通过 `[ELEVATION_JSON]` + SSE `elevation` 事件传递结构化高程数据
- Garmin Connect 风格：earth-tone 配色、简洁排版

**Non-Goals:**
- 不重复实现 Haversine（已有 `haversineDistance` 在 index.html 中，且 `elevation_service.py` 中已有）
- 不修改 open-elevation API 调用逻辑
- 不影响距离标记功能

## Decisions

### 1. 后端：复用 `calculate_cumulative_distances` 设计
- **决定**: 在 `elevation_service.py` 中恢复 `calculate_cumulative_distances`，agent.py 中恢复 `[ELEVATION_JSON]` 输出，routes.py 中恢复 SSE `elevation` 事件
- **理由**: 与之前的设计相同，已被验证可行；前端需要 `dist` 字段绑制剖面图

### 2. Canvas 绑图：填充面积图，无折线描边
- **决定**: 海拔剖面图使用纯填充面积（`fillStyle` 半透明渐变），不绘制折线描边
- **理由**: Garmin Connect 风格以柔和的面积渐变表现地形轮廓，更美观

### 3. 爬坡段检测算法：窗口差分 + 合并
- **决定**: 对高程点序列计算窗口差分（5 点窗口）得到局部坡度，标记 ≥3% 的连续点，合并间距 < 100m 的相邻段，过滤总长 < 500m 的段，输出爬坡段数组
- **理由**: 窗口差分减少 DEM 噪声误判；合并相邻段避免碎片化

### 4. 地图爬坡标记：BMapGL.Polyline 叠加层
- **决定**: 为每个爬坡段创建独立的彩色 Polyline（线宽 8px，高于基础路线的 6px），叠加在基础路线上方
- **理由**: Polyline 层级叠加比替换线段更灵活，清除时不影响基础路线

### 5. 侧边栏：CSS transform + overlay
- **决定**: 侧边栏使用 `position:fixed; right:0; transform:translateX(100%)` + overlay 遮罩，通过 Vue 状态 `showClimbSidebar` 控制 `show` class
- **理由**: 纯 CSS 动画性能好，无需额外依赖

## Risks / Trade-offs

- [Risk] 高程 API（open-elevation）可能超时或返回空 → agent.py 已有 try/except 兜底显示"爬升数据暂不可用"
- [Risk] 超长路线（>200km）坐标点过多导致 Canvas 绑图卡顿 → 降采样至 300 个点
- [Trade-off] `map.clearOverlays()` 会清除所有覆盖物包括爬坡 Polyline → 需要在 `clearMap` 后重新触发爬坡标记（或保留 `clearMap` 行为无需额外操作）
