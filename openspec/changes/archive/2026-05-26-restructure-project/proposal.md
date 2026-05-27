## Why

当前项目结构较为扁平，所有代码文件都位于根目录下，缺乏清晰的模块划分。随着项目规模增长，这种结构会导致代码难以维护和扩展。需要重构为更规范的分层结构，提高代码的可读性和可维护性。

## What Changes

- 创建 `app/` 目录作为应用核心代码的根目录
- 将 `agent.py` 移动到 `app/agents/` 目录
- 将 API 路由逻辑从 `main.py` 拆分到 `app/api/v1/` 目录
- 创建 `langgraph.json` 配置文件用于 LangGraph 配置
- 更新所有相关导入路径
- 更新 `pyproject.toml` 和 `CLAUDE.md` 中的启动命令

## Capabilities

### New Capabilities

无新功能引入，此为纯结构重构。

### Modified Capabilities

无需求变更，此为纯结构重构。

## Impact

- **代码移动**:
  - `agent.py` → `app/agents/agent.py`
  - API 路由 → `app/api/v1/routes.py`
- **新建文件**:
  - `app/__init__.py`
  - `app/agents/__init__.py`
  - `app/api/__init__.py`
  - `app/api/v1/__init__.py`
  - `langgraph.json`
- **修改文件**:
  - `main.py` - 简化为入口文件，导入 app 模块
  - `pyproject.toml` - 更新启动命令
  - `CLAUDE.md` - 更新项目结构说明
  - `README.md` - 更新项目结构说明
- **删除文件**: 无
