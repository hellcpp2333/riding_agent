## 1. Bug Fix

- [x] 1.1 `agent.py`: `agent_node` 中 `llm_with_tools.stream()` 恢复为 `llm_with_tools.invoke()`，确保 tool_calls 完整
- [x] 1.2 验证：发送路线规划请求，确认 agent 正常完成（不再触发 GraphRecursionError）
