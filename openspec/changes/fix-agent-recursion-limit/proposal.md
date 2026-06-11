## Why

Agent 在对话规划路线时触发 `GraphRecursionError: Recursion limit of 30 reached`，陷入 agent ↔ tools 无限循环。根因是 `agent_node` 使用 `llm_with_tools.stream()` 时，LangChain 流式模式下 `tool_calls` 以增量 chunk 方式返回（每个 chunk 携带部分 tool_call 数据），简单的 `list(chunk.tool_calls)` 无法正确累积完整的 tool_call 结构，导致 AIMessage 缺少有效的 tool_calls，graph 路由器无法识别工具调用而反复进入 agent_node。

**核心问题**：流式 token 输出在 `routes.py` 的 SSE 层已通过文本分块实现，`agent_node` 内部不需要也不应该使用 `llm.stream()`。`invoke()` 返回的完整 AIMessage 自带完整 tool_calls，可被 graph 正确路由。

## What Changes

- `agent_node` 从 `llm_with_tools.stream()` 恢复为 `llm_with_tools.invoke()`，确保 tool_calls 完整返回
- SSE 层逐字流式效果不受影响（`routes.py` 中对 `msg.content` 逐字符分块已经实现流式显示）

## Capabilities

<!-- Bug fix only — no new capability or spec change -->

## Impact

- **后端**: `app/agents/agent.py` — `agent_node` 1 行改动
