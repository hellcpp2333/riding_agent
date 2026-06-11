## Why

海拔剖面图面板（elevation profile panel）和爬坡段侧边栏（climb sidebar）是实验性 UI 功能，导致页面布局复杂、代码臃肿，且与核心对话交互体验不协调。需要回到添加剖面图之前更简洁的布局状态，保留地图全高度展示和路线信息浮层。

## What Changes

- 移除前端海拔剖面图面板（`#elevation-panel`），恢复地图容器全高度布局
- 移除前端爬坡段侧边栏（`#climb-sidebar`）及其 overlay
- 移除前端 Canvas 绑图逻辑（`drawElevationChart`、`drawClimbChart`）
- 移除前端爬坡段检测逻辑（`detectClimbSegments`、`drawClimbSegmentsOnMap`）
- 移除前端 elevation 相关 Vue 响应式状态（`elevationData`、`routeStats`、`climbSegments`、`activeClimbIndex`、`showClimbSidebar`）
- 移除前端"爬坡段"按钮
- 移除 CSS 中面板和侧边栏的样式
- 移除后端 `[ELEVATION_JSON]` 结构化高程数据输出（agent.py 中 `calculate_cumulative_distances` 调用及 JSON 拼接）
- 移除后端 SSE `elevation` 事件类型（routes.py 中 chat 和 plan_route 的 elevation 事件）
- 移除后端 `calculate_cumulative_distances` 函数（elevation_service.py）
- 保留：高程服务基础设施（open-elevation 查询、坐标转换、统计计算）、文本形式的高程摘要（`[高程数据]` 段落继续在聊天消息中显示）
- 保留：favicon（`asserts/icon.png`）

## Capabilities

### New Capabilities

_无新增能力。_

### Modified Capabilities

_无现有 spec 需要修改。_

## Impact

- `static/index.html` — 移除 elevation-panel、climb-sidebar、climb overlay、相关 Vue 状态和方法、Canvas 绑图函数
- `static/css/style.css` — 移除 elevation panel 和 climb sidebar 相关样式规则
- `app/agents/agent.py` — 移除 `calculate_cumulative_distances` 导入和 `[ELEVATION_JSON]` 输出
- `app/api/v1/routes.py` — 移除 SSE `elevation` 事件发送逻辑，恢复 `[高程数据]` 简单分割
- `app/services/elevation_service.py` — 移除 `calculate_cumulative_distances` 函数
