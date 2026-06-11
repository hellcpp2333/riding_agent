## MODIFIED Requirements

### Requirement: Map container height reduction
地图容器 SHALL 在无路线数据时占主内容区全高（100%），当 elevationData 有数据时，`#elevation-panel` 出现并占 25% 高度，地图区域 `#map-area` 自动缩小至 75%。

#### Scenario: No route data - map full height
- **WHEN** 用户尚未规划任何路线或 elevationData 为 null
- **THEN** `#elevation-panel` 不渲染，`#map-area` 占满 `#map-container` 全高

#### Scenario: Route data arrives - panel appears
- **WHEN** 收到 elevation SSE 事件且包含轨迹点
- **THEN** `#elevation-panel` 渲染出现，地图缩小至 75% 高度

### Requirement: Route stats summary display
路线数据面板 SHALL 将三项指标（距离、累计爬升、累计下降）显示在面板底部，图表在上方。stats 区域固定高度约 48px，图表区域 flex:1 占满剩余空间。

#### Scenario: Stats at bottom of panel
- **WHEN** 路线数据面板渲染
- **THEN** stats（距离/爬升/下降）显示在面板最下方，海拔剖面图在 stats 上方

### Requirement: Climb sidebar conditional rendering
爬坡段侧边栏 SHALL 仅在 `climbSegments.length > 0` 时渲染 DOM 节点，无爬坡段时不加载。

#### Scenario: Sidebar not rendered without climbs
- **WHEN** 路线无满足 UCI 标准的爬坡段
- **THEN** `#climb-sidebar` 和 `#climb-sidebar-overlay` 不渲染
