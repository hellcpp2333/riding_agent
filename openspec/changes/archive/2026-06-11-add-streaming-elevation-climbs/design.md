## Context

当前系统通过 LangGraph agent 调用 LLM 完成对话。`agent_node` 使用 `llm_with_tools.invoke()`（非流式），导致用户需要等待完整回答生成后才能看到内容。前端 SSE 接收的是 node 级别的 `updates` 事件（每次 node 完成后发送完整消息），而非 token 级事件。

高程数据方面，后端在 `map_directions` 工具返回后，以 100m 间隔采样坐标点，通过 Open Elevation API (https://api.open-elevation.com/api/v1/lookup) 查询高程。Open Elevation API 底层使用 SRTM/ALOS DEM 数据，分辨率约 30m。配合 5m 最小阈值和 5 点移动平均平滑，对小起伏地形的爬升/下降估计偏低。

Garmin Connect 的 Courses 功能使用设备记录的高分辨率 GPS 轨迹（~1s 采样），配合高精度 DEM 数据进行高程修正。爬坡分类采用 5 级体系，以颜色编码（绿→黄→橙→红→深红）标注不同坡度段。

## Goals / Non-Goals

**Goals:**
1. 实现 LLM token 级流式输出，用户可实时阅读回答内容
2. 提升高程采样精度至 30m 间隔，降低平滑窗口和阈值，使累计爬升/下降更接近实际
3. 导入 GPX 路书后自动显示高程剖面图和爬坡段
4. 实现 Garmin 风格 5 级爬坡分类，在剖面图和地图上可视化爬坡段

**Non-Goals:**
- 不使用付费高程 API 或自建 DEM 数据源（继续使用免费 Open Elevation API）
- 不修改前端 UI 整体布局（仅修改数据流和渲染逻辑）
- 不涉及地图底图更换或 API 迁移

## Decisions

### 1. 流式输出方案：LangGraph `astream_events` vs 手动 `astream`
**选择**: 修改 `agent_node` 内部使用 `llm_with_tools.astream()` 生成 token，通过 `ToolMessage` 携带 `streaming_content` 字段传递给 SSE 层。

**理由**: 当前 `stream_mode="updates"` 在 node 级别发送事件。若改用 `astream_events` 模式，需要重构整个 graph 的流式架构，跨文件修改量大。改为在 agent_node 内部使用 LLM 的 `.astream()` 方法，将 token 收集到消息中，SSE 层逐 token 发送，改动集中在 agent.py 和 routes.py。

**替代方案**: 改用 `stream_mode="messages"` + `llm_with_tools.astream()` → 需要重构 tools_node 的回调处理，但 LangGraph 的 `stream_mode="messages"` 原生支持 token 事件，更规范。**最终选择此方案**，因为这是 LangGraph 推荐的流式模式，且不需要修改 ToolMessage 结构。

### 2. 高程采样精度优化
**选择**: 采样间隔从 100m 降至 30m，平滑窗口从 5 点降至 3 点，爬升阈值从 5m 降至 3m。

**理由**: 
- 30m 间隔匹配 Open Elevation API 底层 DEM 分辨率（SRTM 1 arc-sec ≈ 30m）
- 3 点窗口保留更多微地形特征，同时仍能消除单个点的高程抖动
- 3m 阈值过滤 DEM 噪声（SRTM 相对高程精度约 2-5m），同时保留真实小起伏

### 3. GPX 路书高程处理
**选择**: 优先使用 GPX 自带高程数据（设备 GPS），缺失时回退到 Open Elevation API。

**理由**: GPX 设备记录的高程通常比 DEM 查询更准确（反映实际骑行轨迹）。但部分 GPX 文件可能不含 `<ele>` 标签，需要 API 补充。后端在 `GET /api/routes/{id}` 返回时附带 `elevation` 字段，前端直接使用。

### 4. 爬坡段检测算法
**选择**: 在后端 `elevation_service.py` 新增 `detect_climbs()` 函数，使用滑动窗口检测连续上坡段。

**参考 Garmin 分类标准**:
| 等级 | 标签 | 条件（坡度 或 爬升）| 颜色 |
|------|------|---------------------|------|
| 5 | HC级 | avgGrade ≥ 8% 或 gain ≥ 800m | 深红 #880e0e |
| 4 | 1级 | avgGrade ≥ 6% 或 gain ≥ 500m | 红色 #e53935 |
| 3 | 2级 | avgGrade ≥ 5% 或 gain ≥ 300m | 橙色 #ff9800 |
| 2 | 3级 | avgGrade ≥ 4% 或 gain ≥ 150m | 黄色 #fdd835 |
| 1 | 4级 | avgGrade ≥ 3% 或 gain ≥ 75m | 绿色 #4caf50 |

**最小坡段长度**: 300m（Garmin 使用 ~250-400m 作为最小可识别爬坡段）

## Risks / Trade-offs

1. **[API 请求量增加]** 采样间隔从 100m 降至 30m，API 请求点数增加约 3 倍（100km 路线约 3300 点 vs 1000 点）。Open Elevation API 单次请求上限约 1000 点，长路线需要分批请求。→ **缓解**: 实现分批查询（每批 800 点），增加总超时和重试逻辑。

2. **[Open Elevation API 可用性]** 免费 API 无 SLA 保证，可能临时不可用。→ **缓解**: 已有 try/except 兜底处理，API 失败时显示"爬升数据暂不可用"。

3. **[流式模式下 tool call 处理复杂化]** LLM 流式输出时 tool_calls 只在最后 chunk 出现，需要等待完整响应后再决定路由。→ **缓解**: 使用 LangGraph 的 `stream_mode="messages"` 模式，框架自动处理此问题。

4. **[GPX 高程数据精度不一致]** 不同设备记录的 GPX 高程质量差异大（气压计 > GPS > 无高程）。→ **缓解**: 后端统一做平滑处理，确保一致性。

## Migration Plan

1. 部署新版本后端代码（无数据库迁移）
2. 已有 GPX 路书在下次访问详情时自动获取高程富化
3. 回滚: 将 agent_node 改回 `invoke()`，采样参数改回 100m/5m 阈值即可恢复旧行为
4. 无需数据迁移或配置变更

## Open Questions

1. 30m 采样间隔是否导致 API 请求过慢（单次最多 1000 点，100km 路线约需 4 次请求）？→ 可通过性能测试验证，若超时可降至 50m
2. 是否需要缓存同一路线的高程查询结果？→ 后续优化，初期不做
