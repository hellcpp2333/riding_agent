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
| LLM | OpenAI 兼容 API（支持 DeepSeek、GLM、OpenAI 等） |
| 地图 | 百度地图 MCP Server + BMapGL |
| 数据库 | SQLite（LangGraph checkpoints）+ MySQL（用户数据） |
| 缓存 | Redis（会话管理） |
| 存储 | 阿里云 OSS（头像上传） |

## 快速开始

### 1. 安装依赖

```bash
uv sync
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填入必填配置：

| 变量 | 说明 |
|------|------|
| `OPENAI_API_KEY` | LLM API Key |
| `OPENAI_BASE_URL` | LLM API 地址（可选，默认 OpenAI） |
| `LLM_MODEL` | 模型名称，如 `deepseek-chat`、`glm-5v-turbo`、`gpt-4o` |
| `BAIDU_MAPS_API_KEY` | 百度地图服务端 AK（MCP） |
| `BAIDU_MAPS_JS_AK` | 百度地图浏览器端 AK |

其余配置（MySQL、Redis、OSS）有默认值，按需修改。

### 3. 启动数据库（Docker）

```bash
docker compose up -d
```

启动 MySQL 和 Redis。不用 Docker 的话手动启动对应服务即可。

### 4. 启动应用

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
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
| POST | `/api/auth/register` | 注册 |
| POST | `/api/auth/login` | 登录 |
| POST | `/api/auth/logout` | 登出 |
| GET | `/api/auth/me` | 当前用户信息 |
| GET/PUT | `/api/user/profile` | 获取/更新用户资料 |
| POST | `/api/user/avatar` | 上传头像 |

## 项目结构

```
.
├── app/
│   ├── agents/
│   │   └── agent.py        # LangGraph Agent
│   ├── api/
│   │   └── v1/
│   │       ├── routes.py   # API 路由
│   │       ├── schemas.py  # 数据模型
│   │       └── user_routes.py  # 用户相关路由
│   ├── auth/
│   │   ├── routes.py       # 认证路由
│   │   ├── utils.py        # JWT 工具
│   │   └── dependencies.py # 认证依赖
│   ├── db.py               # SQLite 工具
│   ├── db_mysql.py         # MySQL 工具
│   ├── redis_client.py     # Redis 客户端
│   ├── models.py           # ORM 模型
│   └── services/
│       └── oss_service.py  # OSS 上传服务
├── main.py                 # FastAPI 入口
├── static/index.html       # 前端页面
├── langgraph.json          # LangGraph 配置
├── docker-compose.yml      # 本地开发数据库
├── pyproject.toml          # 项目配置与依赖
├── .env.example            # 环境变量模板
└── .env                    # 环境变量（不提交）
```

## 许可

MIT
