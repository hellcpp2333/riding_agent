## Why

当前骑行路线助手存在 4 个核心体验缺陷：1) 对话回答为非流式（等待完整回答后才一次性渲染），用户感知延迟严重；2) 高程采样精度不足（100m 间隔 + Open Elevation API 分辨率有限），导致累计爬升/下降与实际偏差较大；3) 导入 GPX 路书后无法显示高程剖面图和爬坡段；4) 爬坡段虽有前端检测逻辑但不可见（数据流未打通）。参照 Garmin Connect 的 Courses 功能中 30-50m 级采样精度、5 级爬坡分类（cat4-cat1-HC）、坡段颜色编码的高程剖面图，系统性修复这些问题。

## What Changes

### 1. 对话流式回答
- 后端 `agent_node` 从 `llm_with_tools.invoke()` 改为 `llm_with_tools.astream()`，实现 token 级流式输出
- 前端 SSE 接收 `token` 事件后逐字追加到消息，而非等待完整内容后替换

### 2. 高程采样精度提升
- 采样间隔从 100m 降至 30m，采样窗口从 5 点降到 3 点（保留更多地形细节）
- 爬升/下降阈值从 5m 降至 3m，避免过滤小起伏
- 后端 `[ELEVATION_JSON]` 中的 `stats` 改为来自平滑后、阈值 3m 的计算结果
- 前端不再重复计算爬升/下降，直接使用后端 stats 数据

### 3. 导入路书高程剖面图支持
- 后端 `GET /api/routes/{id}` 返回时附带完整的 `elevation` 字段（含 points + stats）
- 若 GPX 文件本身有高程数据（`<ele>` 标签），直接使用并构建剖面图数据
- 若 GPX 文件无高程数据，后端自动调用 Open Elevation API 补充（30m 采样间隔）
- 前端 `selectRoute()` 统一走 `handleElevationData()` 数据流，确保面板更新

### 4. 爬坡段检测与展示（参考 Garmin）
- 参照 Garmin 的 5 级爬坡分类：cat4 (3-5%), cat3 (5-8%), cat2 (8-10%), cat1 (10-12%), HC (>12%)
- 端点检测改为连续坡段识别：最小坡段长度 300m（原为 500m），与 Garmin 一致
- 后端新增 `detect_climbs()` 函数，在 `[ELEVATION_JSON]` 中附带 `climbs` 数组
- 前端 `elevation-panel` 爬坡段列表已存在，确保从后端数据正确渲染
- 高程剖面图上用渐变颜色标注爬坡段（绿→黄→橙→红→深红），参照 Garmin 配色

## Capabilities

### New Capabilities
- `streaming-chat-response`: LLM 回答以 token 级流式输出到前端，用户可实时看到文字生成
- `elevation-enrichment`: 路线自动高程富化——规划路线和导入路书均通过 Open Elevation API 获取高程数据，30m 采样精度
- `climb-detection`: 参照 Garmin 5 级爬坡分类（cat4-cat1-HC），后端自动检测爬坡段并返回结构化数据

### Modified Capabilities
<!-- No existing specs have requirement-level changes -->

## Impact

- **后端**: `app/agents/agent.py`（tools_node 流式改造 + 高程采样参数调整）、`app/services/elevation_service.py`（新增爬坡检测 + 采样参数可配置化）、`app/api/v1/routes.py`（chat SSE 改为 token 级事件）、`app/api/v1/route_routes.py`（路书详情返回 elevation 数据）
- **前端**: `static/index.html`（SSE token 增量渲染、路书详情统一数据流、爬坡分类参数对齐）
- **依赖**: 无新增依赖，仍使用现有 Open Elevation API
