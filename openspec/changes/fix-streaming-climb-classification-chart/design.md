## Context

当前系统已实现流式回答、高程剖面和爬坡检测，但存在精度问题。流式分块为 3 字符/10ms，不是逐字效果。爬坡分类使用自定义阈值（Grade ≥ 8% → HC），与 UCI 国际标准不符。爬坡面板剖面图因 `flex:1` 撑满侧边栏。Garmin Connect 的爬坡详情面板使用固定 250px 图表高度和 UCI 标准分级。

## Goals / Non-Goals

**Goals:**
1. SSE token 逐字发送（chunk_size=1, delay=0），前端实时逐字渲染
2. 爬坡侧边栏中剖面图固定高度 250px，参照 Garmin 设计
3. 爬坡检测和分类严格遵循 UCI 标准：准入条件（≥1000m, ≥1.3%）+ Score 公式分级

**Non-Goals:**
- 不改变主高程剖面图（`#elevation-canvas`）的布局
- 不改变前端 stream 解析架构

## Decisions

### 1. 逐字流式：chunk_size=1, sleep=0
**选择**: 将 `routes.py` 中的 `chunk_size` 从 3 改为 1，`asyncio.sleep` 从 0.01 改为 0（移除）。

**理由**: 网络本身的 TCP 缓冲和 SSE 帧化已提供足够的分隔，无需人工延迟。1 字符块配合浏览器的增量渲染即可实现逐字效果。

**替代方案**: 在 agent_node 中使用真正的 LLM token streaming → 需要 LangGraph `astream_events` 重构，改动面大，且逐字视觉效果与 chunk_size=1 等效。

### 2. 爬坡图表固定高度
**选择**: `.climb-chart-container` 从 `flex: 1` 改为 `height: 250px`，配 `flex-shrink: 0`。

**理由**: Garmin `ClimbsSheet_chart__jZ+GK` 使用 `recharts-responsive-container` 内嵌 250px SVG。固定高度确保图表不随窗口放大而失真。

### 3. UCI 爬坡分级公式
**选择**: 使用标准 UCI 评分公式 `Score = Length(km) × Grade(%)²`，校准阈值。

**理由**: UCI 官方文档以长度和坡度的组合描述各级别，业界标准实现使用此二次公式。

**准入条件**: 长度 < 1000m 或坡度 < 1.3% → 不评级（UCI 规则第 1 条）

**阈值校准**（基于 refer/uci爬坡段分级规则.md 中的示例）:

| 级别 | UCI Score 范围 | 验证示例 |
|------|---------------|---------|
| 4级 | 20 – 79 | 2km@5% = 50 ✓, 5km@2.5% = 31 ✓ |
| 3级 | 80 – 199 | 1.6km@10% = 160 ✓ |
| 2级 | 200 – 399 | 15km@4% = 240 ✓, 5km@8% = 320 ✓ |
| 1级 | 400 – 600 | 8km@8% = 512 ✓, 20km@5% = 500 ✓ |
| HC级 | > 600 | 10km@8% = 640, 25km@6% = 900 ✓ |

## Risks / Trade-offs

1. **[分类结果变化]** UCI 阈值比旧规则更严格（旧规则 75m 爬升即可 4 级，现在需 ≥1000m 且 ≥1.3%）。短坡段不再被评级。→ 这是期望行为，符合 UCI 标准。

2. **[chunk_size=1 增加 SSE 帧数]** 一条 500 字符的回答产生 500 个 SSE 事件而非 167 个。→ 现代浏览器 SSE 解析性能充裕（数万 events/s），无实际影响。

## Open Questions

无。
