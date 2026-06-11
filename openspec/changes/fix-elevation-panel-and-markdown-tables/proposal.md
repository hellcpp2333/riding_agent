## Why

存在两个问题和一个缺失功能：
1. **对话中 Markdown 表格未渲染**：LLM 回答中的 Markdown 表格（`| col1 | col2 |`）显示为原始文本，用户体验差
2. **海拔面板和爬坡段面板不显示**：上次 DP 平滑改造引入 bug——`douglas_peucker_smooth()` 依赖 `dist` 字段，但 `calculate_elevation_stats()` 和 `enrich_route_with_elevation()` 在计算距离之前就调用了 DP 平滑，导致 KeyError 整个高程数据流中断
3. **爬坡段剖面图缺少坡度颜色图例**：Garmin Connect 在爬坡图表下方有 `<3% / 3-6% / 6-9% / 9-12% / >12%` 的颜色标注，我们的面板缺失

## What Changes

### 1. Markdown 表格渲染
- 前端 `formatText()` 新增 Markdown 表格解析：`|...|` → `<table>`
- 支持表头行、分隔行、对齐语法

### 2. 修复海拔/爬坡面板不显示（关键 Bug）
- `agent.py`: `calculate_elevation_stats(elev_points)` → 先调 `calculate_cumulative_distances` 再加 DP 平滑
- `elevation_service.py`: `enrich_route_with_elevation()` 无高程分支先计算 dist 再 DP 平滑
- `elevation_service.py`: `calculate_elevation_stats()` 防御性检查 `dist` 字段

### 3. 爬坡剖面图下方添加坡度颜色图例
- 爬坡侧边栏 `.climb-sidebar-body` 底部新增 `.climb-gradient-legend`
- 颜色与 Garmin 一致：`#d8f5a2`(浅绿<3%), `#c0ca33`(绿3-6%), `#f98925`(橙6-9%), `#f5bf2a`(黄9-12%), `#ee3e3e`(红>12%)

## Capabilities

### New Capabilities
- `markdown-table-rendering`: 对话消息中的 Markdown 表格渲染为 HTML `<table>`

### Modified Capabilities
- `elevation-enrichment`: 修复 DP 平滑的 dist 字段依赖顺序，确保高程数据流不中断
- `climb-detection`: 新增前端坡度颜色图例

## Impact

- **后端**: `app/services/elevation_service.py`（修复 dist 依赖顺序）、`app/agents/agent.py`（修复 stats 计算顺序）
- **前端**: `static/index.html`（表格解析 + 坡度图例）、`static/css/style.css`（图例样式）
