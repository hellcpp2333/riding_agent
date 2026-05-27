# 骑行路线助手

基于 LLM Agent 的骑行路线规划 Web 应用，支持自然语言对话和结构化路线查询。

## 功能

- 自然语言对话规划骑行路线
- 地图可视化展示路线（百度地图 BMapGL）
- 沿途设施搜索（补给点、修车店、咖啡店等）
- 天气查询
- 多路线对比
- 对话记忆（自动摘要，支持多会话）

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI + LangGraph Agent |
| LLM | DeepSeek v4-pro（OpenAI 兼容 API） |
| 地图 | 百度地图 MCP Server + BMapGL |
| 持久化 | SQLite（LangGraph checkpoints） |

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

### 2. 配置环境变量

创建 `.env` 文件，填入你的 API Key：

- `OPENAI_API_KEY` — DeepSeek API Key
- `BAIDU_MAPS_API_KEY` — 百度地图服务端 AK（用于 MCP）

> 前端地图需要浏览器端 AK，在 `static/index.html` 中搜索 `YOUR_BAIDU_MAP_JS_AK` 替换。

### 3. 启动

```bash
uv run python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

浏览器打开 `http://localhost:8000`

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 前端页面 |
| POST | `/api/chat` | 对话（SSE 流式） |
| POST | `/api/route/plan` | 结构化路线规划 |
| GET | `/api/sessions` | 会话列表 |
| POST | `/api/sessions` | 新建会话 |

## 项目结构

```
.
├── app/
│   ├── agents/
│   │   └── agent.py      # LangGraph Agent
│   ├── api/
│   │   └── v1/
│   │       ├── routes.py # API 路由
│   │       └── schemas.py # Pydantic 模型
│   └── db.py             # 数据库工具
├── main.py               # FastAPI 入口
├── static/index.html     # 前端页面
├── langgraph.json        # LangGraph 配置
├── pyproject.toml        # 项目配置与依赖
└── .env                 # 环境变量
```

## 许可

MIT
