## 1. 后端流式回答改造

- [x] 1.1 `agent.py`: 将 `agent_node` 中 `llm_with_tools.invoke()` 改为 `llm_with_tools.astream()`，收集 text 和 tool_calls 并返回
- [x] 1.2 `agent.py`: 重构 `tools_node`，在 tool call 过程中保持流式 token 输出不中断
- [x] 1.3 `routes.py`: 将 `/api/chat` 的 `stream_mode` 改为 `"messages"`，直接从 chunk 提取 `token` 事件逐条发送
- [x] 1.4 `routes.py`: `/api/route/plan` 同样改为流式输出
- [x] 1.5 验证：发送对话请求，确认前端实时显示流式文字

## 2. 高程采样精度提升

- [x] 2.1 `elevation_service.py`: 将 `sample_points` 默认 `interval_m` 从 500.0 改为 30.0
- [x] 2.2 `elevation_service.py`: 将 `smooth_elevations` 默认 `window` 从 5 改为 3
- [x] 2.3 `elevation_service.py`: 将 `calculate_elevation_stats` 默认 `min_gain_threshold` 从 5.0 改为 3.0
- [x] 2.4 `elevation_service.py`: 新增 `lookup_elevations_batched()` 函数，支持 >1000 点的路线分批次查询（每批 800 点），单批失败有重试
- [x] 2.5 `agent.py`: `tools_node` 中调用 `lookup_elevations_batched()` 替代 `lookup_elevations()`，采样间隔改用 30m
- [x] 2.6 验证：规划一条已知爬升量的路线（如妙峰山），对比新旧累计爬升数据差异

## 3. 爬坡段后端检测

- [x] 3.1 `elevation_service.py`: 新增 `detect_climbs(points)` 函数，使用 5 点滑动窗口计算局部坡度，检测连续上坡段
- [x] 3.2 `elevation_service.py`: 新增 `classify_climb(avg_grade, gain)` 函数，按 Garmin 5 级标准分类（HC/1/2/3/4级）
- [x] 3.3 `elevation_service.py`: 爬坡段最小长度设为 300m，最小起始坡度 3%，终止条件为坡度 < 2% 且已超 200m
- [x] 3.4 `agent.py`: `tools_node` 中计算高程后调用 `detect_climbs()`，将 `climbs` 数组加入 `[ELEVATION_JSON]`
- [x] 3.5 验证：规划含爬坡路线，确认 `[ELEVATION_JSON]` 中包含 `climbs` 数据

## 4. 导入路书高程支持

- [x] 4.1 `route_service.py`: 修改 `parse_gpx()` 保留完整坐标→高程映射，新增返回 `has_elevation` 标志
- [x] 4.2 `elevation_service.py`: 新增 `enrich_route_with_elevation()` 函数——若 GPX 有 ele 则直接使用并平滑，若无则用 Open Elevation API 补充
- [x] 4.3 `route_routes.py`: `GET /api/routes/{id}` 响应中新增 `elevation` 字段（含 points + stats + climbs），调用 `enrich_route_with_elevation()`
- [x] 4.4 `route_routes.py`: 对过长轨迹点（>2000 点）采样至 30m 间隔再返回，避免前端卡顿
- [x] 4.5 验证：导入含高程的 GPX 路书，点击查看详情，确认出现高程剖面图和爬坡段

## 5. 前端流式渲染与高程数据流统一

- [x] 5.1 `index.html`: 修改 SSE `token` 事件处理——增量追加文字到当前 AI 消息，而不是替换
- [x] 5.2 `index.html`: 为流式输出中的消息增加"生成中"光标动画（typing indicator）
- [x] 5.3 `index.html`: `handleElevationData()` 中直接使用 `data.stats` 和 `data.climbs`，不再前端自行计算
- [x] 5.4 `index.html`: `selectRoute()` 从后端 `elevation` 字段取数据，调用 `handleElevationData()` 统一数据流
- [x] 5.5 `index.html`: 更新 `classifyClimb()` 对齐后端 5 级分类标准
- [x] 5.6 `index.html`: 移除 `detectClimbSegments()` 前端重复实现（数据源已切换到后端）
- [x] 5.7 验证：规划路线 → 确认流式文字 + 高程剖面 + 爬坡列表；导入路书 → 确认同样显示完整
