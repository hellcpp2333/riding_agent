## Context

当前项目结构：
```
langchain_dev/
├── main.py          # FastAPI 入口 + API 路由
├── agent.py         # LangGraph Agent 定义
├── static/          # 前端静态文件
├── pyproject.toml   # 项目配置
└── .env             # 环境变量
```

问题：所有业务逻辑混在根目录，缺乏模块化，不利于后续扩展。

## Goals / Non-Goals

**Goals:**
- 建立清晰的分层目录结构
- 分离 Agent 逻辑和 API 路由
- 保持现有功能完全不变
- 为未来模块扩展预留空间

**Non-Goals:**
- 不改变任何业务逻辑
- 不添加新功能
- 不修改 API 接口签名

## Decisions

### 1. 目录结构设计

采用标准的 FastAPI 项目结构：

```
langchain_dev/
├── app/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agent.py      # 原 agent.py
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           └── routes.py  # API 路由
├── main.py               # 简化的入口文件
├── static/               # 前端静态文件
├── langgraph.json        # LangGraph 配置
├── .env                  # 环境变量
└── pyproject.toml        # 项目配置
```

**理由**: 这是 FastAPI 项目的常见结构，`app/` 作为核心代码根目录，`api/v1/` 支持未来版本迭代。

### 2. main.py 简化策略

`main.py` 保留为最小入口文件，只负责：
- 加载环境变量
- 创建 FastAPI 应用
- 注册路由
- 配置 lifespan

**理由**: 入口文件应保持简洁，便于快速理解项目启动流程。

### 3. routes.py 设计

将 `main.py` 中的路由定义移到 `app/api/v1/routes.py`，包括：
- `@app.get("/")` - 前端页面
- `@app.get("/api/sessions")` - 会话列表
- `@app.post("/api/sessions")` - 新建会话
- `@app.post("/api/chat")` - 对话
- `@app.post("/api/route/plan")` - 路线规划

使用 FastAPI 的 `APIRouter` 进行路由组织。

**理由**: 路由集中管理，便于添加新版本 API。

## Risks / Trade-offs

- **导入路径变更**: 所有模块导入路径需要更新，可能有遗漏 → 运行测试验证
- **启动命令兼容**: 需确保 `uv run uvicorn main:app` 仍然有效 → 验证启动

## Migration Plan

1. 创建新目录结构和 `__init__.py` 文件
2. 移动 `agent.py` 到 `app/agents/`
3. 创建 `app/api/v1/routes.py`，提取路由逻辑
4. 修改 `main.py`，导入并注册路由
5. 创建 `langgraph.json`
6. 更新文档和配置
7. 测试启动验证