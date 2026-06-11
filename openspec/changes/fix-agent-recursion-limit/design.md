## Context

`llm_with_tools.stream()` 在 LangChain 中返回 `AIMessageChunk`，每个 chunk 的 `tool_calls` 是增量式的（index-based accumulation）。直接 `list(chunk.tool_calls)` 只取最后一个 chunk 的 tool_calls 片段，导致 AIMessage 的 tool_calls 是不完整的 dict 列表（缺少 `name`/`args` 等关键字段），graph 路由器无法识别，agent 反复进入 agent_node。

正确的流式 tool_calls 处理需要使用 `AIMessageChunk.__add__` 累加合并，但 SSE 层已经逐字分块，agent_node 不需要流式。

## Decision

**选择**: `agent_node` 恢复为 `llm_with_tools.invoke()`

**理由**: SSE 层（`routes.py`）已通过 `for ch in text: yield {"event": "token"}` 实现逐字流式显示。agent_node 使用 `invoke()` 不影响前端流式体验，同时保证 tool_calls 完整。
