## 1. 创建目录结构

- [x] 1.1 创建 `app/` 目录及 `__init__.py`
- [x] 1.2 创建 `app/agents/` 目录及 `__init__.py`
- [x] 1.3 创建 `app/api/` 目录及 `__init__.py`
- [x] 1.4 创建 `app/api/v1/` 目录及 `__init__.py`

## 2. 移动 Agent 模块

- [x] 2.1 将 `agent.py` 移动到 `app/agents/agent.py`
- [x] 2.2 更新 `app/agents/__init__.py` 导出 `build_agent`

## 3. 提取 API 路由

- [x] 3.1 创建 `app/api/v1/routes.py`
- [x] 3.2 将 `main.py` 中的 Pydantic 模型移到 `app/api/v1/schemas.py`
- [x] 3.3 将所有路由处理函数移到 `routes.py`，使用 `APIRouter`
- [x] 3.4 更新 `app/api/v1/__init__.py` 导出路由

## 4. 重构 main.py

- [x] 4.1 简化 `main.py` 为入口文件
- [x] 4.2 从 `app.agents` 导入 `build_agent`
- [x] 4.3 从 `app.api.v1` 导入并注册路由
- [x] 4.4 保持 lifespan 逻辑不变

## 5. 创建 langgraph.json

- [x] 5.1 创建 `langgraph.json` 配置文件

## 6. 更新文档和配置

- [x] 6.1 更新 `CLAUDE.md` 中的项目结构说明
- [x] 6.2 更新 `README.md` 中的项目结构说明
- [x] 6.3 更新 `pyproject.toml`（如有必要）

## 7. 验证

- [x] 7.1 测试服务启动：`uv run uvicorn main:app --reload`
- [x] 7.2 验证所有 API 接口正常工作
