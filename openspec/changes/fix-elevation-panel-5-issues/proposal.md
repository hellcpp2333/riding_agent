## Why

当前海拔面板存在 5 个问题，影响用户体验和数据准确性：

1. **面板位置错误**：海拔面板在侧边栏内，地图下方无数据展示。用户期望面板位于地图下方（75%/25% 分割），对话面板尺寸不变
2. **数据不一致**：前端 `handleElevationData` 自行计算爬升/下降（阈值 5m），与后端 AI 回答中 `calculate_elevation_stats`（先平滑再计算）结果不同
3. **剖面图样式不佳**：高度仅 130px，填充色过浅（`rgba(196,148,112,0.45)`），与 Garmin 的蓝色系填充面积图差距大
4. **切换路线不更新**：导入路书调用 `selectRoute()` 不触发 elevation 数据流，面板数值残留旧路线数据
5. **爬坡段不显示**：爬坡段列表在侧边栏内 visibility 受限，且 climb sidebar 依赖 elevation 数据流程未覆盖导入路书场景

## What Changes

### 1. 面板回归地图下方（使用 CSS Grid）
- 新增 `.map-right` wrapper 包裹地图和面板，`display:grid;grid-template-rows:1fr`（默认）
- 有 elevation 数据时动态切换 `grid-template-rows:3fr 1fr`
- `#map-container` 内 `#map` 使用 `position:absolute;inset:0` 确保 BMapGL 初始化时始终有确定尺寸

### 2. 统一数据源
- 后端 `[ELEVATION_JSON]` 新增 `stats` 字段（gain/loss/max/min），直接来自 `calculate_elevation_stats`
- 前端直接使用 `data.stats` 显示，不再自行计算

### 3. 剖面图样式改进（参照 Garmin）
- Canvas 高度增大至 200px+
- 填充色改为 Garmin 风格蓝色系渐变：`rgba(25,118,210,0.4)` → `rgba(25,118,210,0.05)`
- 网格线和轴标签颜色加深
- 爬坡段海拔图同步更新配色

### 4. 导入路书支持
- `selectRoute()` 加载路书详情后，若 `track_data` 含高程数据，构建 elevation 数据结构并触发面板更新
- 清理 `clearMapOverlays()` 时重置 elevation 状态

### 5. 爬坡段面板修复
- 爬坡段按钮放在地图上方（`#map-container` 内部小型浮动工具栏）
- 爬坡段列表和侧边栏确保在导入路书场景也正常工作

## Capabilities

### Modified Capabilities
- `elevation-profile-panel`: 面板移至地图下方，数据源统一，样式更新
- `climb-segment-analysis`: 支持导入路书场景

## Impact

- `static/index.html` — 新增 `.map-right` wrapper；`#elevation-summary` 从 sidebar 移至地图下方；`#elevation-panel` 恢复为地图下方面板
- `static/css/style.css` — Grid 布局；面板样式；深色图表配色；移除 sidebar 内 elevation 样式
- `app/agents/agent.py` — `[ELEVATION_JSON]` 新增 `stats` 字段
- `app/services/elevation_service.py` — 不变
- `app/api/v1/routes.py` — 不变
