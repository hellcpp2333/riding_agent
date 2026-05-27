## Why

撤销 `use-load-dotenv-for-env-vars` 变更中所做的改动。该变更将 `load_dotenv()` 移到了 `agent.py` 并添加了错误处理，但现在需要恢复到原始的环境变量加载方式。

## What Changes

- 从 `app/agents/agent.py` 中移除 `load_dotenv()` 调用和相关的错误处理
- 恢复 `main.py` 中的 `load_dotenv()` 调用
- 恢复 `main.py` 中的 `BAIDU_MAPS_API_KEY` 环境变量检查和警告
- 将 `agent.py` 中的环境变量访问恢复为原始的 `os.environ["KEY"]` 方式

**Breaking Changes**: None (恢复到之前的状态)

## Capabilities

### New Capabilities

- **revert-env-loading**: 恢复到原始的环境变量加载方式

### Modified Capabilities

- None (这是实现细节的回退，不涉及规范变更)

## Impact

- `app/agents/agent.py` - 移除 load_dotenv() 调用和错误处理，恢复原始环境变量访问
- `main.py` - 恢复 load_dotenv() 调用和 BAIDU_MAPS_API_KEY 检查
