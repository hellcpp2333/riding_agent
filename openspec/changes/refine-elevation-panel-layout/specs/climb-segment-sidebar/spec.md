## MODIFIED Requirements

### Requirement: Climb sidebar panel
爬坡段侧边栏 SHALL 仅在检测到爬坡段时渲染（`v-if="climbSegments.length > 0"`），无爬坡段时不创建 DOM 节点。overlay 遮罩层同样条件渲染。

#### Scenario: Sidebar hidden without climb segments
- **WHEN** `climbSegments` 数组为空
- **THEN** `#climb-sidebar` 和 `#climb-sidebar-overlay` 不渲染，DOM 中不存在
