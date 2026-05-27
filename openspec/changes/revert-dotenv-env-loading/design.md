## Context

当前代码状态（需要撤销）：
- `app/agents/agent.py` 顶部有 `load_dotenv()` 调用和错误处理的 env var 访问
- `main.py` 中没有 `load_dotenv()` 调用和 `BAIDU_MAPS_API_KEY` 检查

原始代码状态（恢复目标）：
- `main.py` 中有 `load_dotenv()` 调用和 `BAIDU_MAPS_API_KEY` 检查
- `app/agents/agent.py` 直接使用 `os.environ["KEY"]` 访问环境变量（无 load_dotenv）

## Goals / Non-Goals

**Goals:**
- 将 `agent.py` 恢复到原始状态（移除 load_dotenv() 和错误处理）
- 将 `main.py` 恢复到原始状态（恢复 load_dotenv() 和 BAIDU_MAPS_API_KEY 检查）
- 保持功能完全一致（只是恢复原始实现方式）

**Non-Goals:**
- 不改变任何功能行为
- 不添加新功能或修改配置方式

## Decisions

1. **恢复 main.py 的 load_dotenv()**：将 `from dotenv import load_dotenv; load_dotenv()` 移回 main.py 顶部
2. **恢复 main.py 的 BAIDU_MAPS_API_KEY 检查**：恢复 `os.environ.get("BAIDU_MAPS_API_KEY", "")` 和警告打印
3. **恢复 agent.py 的原始 env 访问**：将 `os.environ.get()` + 错误检查恢复为 `os.environ["KEY"]` 直接访问
4. **移除 agent.py 的 load_dotenv()**：删除 agent.py 顶部的 dotenv 相关代码

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| 恢复后 agent.py 可能在 load_dotenv() 前被导入 | 原始代码就是这样工作的，依赖导入顺序 |
| 环境变量缺失时错误提示不够友好 | 这是原始行为，本次只是恢复，不做改进 |

## Migration Plan

1. 修改 `app/agents/agent.py`：移除 load_dotenv() 和错误处理，恢复原始 env 访问
2. 修改 `main.py`：恢复 load_dotenv() 调用和 BAIDU_MAPS_API_KEY 检查
3. 测试应用启动正常
