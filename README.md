# 骑行路线助手

基于 LLM Agent 的骑行路线规划 Web 应用，支持自然语言对话、路线规划、路书导入导出。

## 功能

- 自然语言对话规划骑行路线
- 地图可视化展示路线（百度地图 BMapGL）
- 沿途设施搜索（补给点、修车店、咖啡店等）
- 天气查询
- 多路线对比
- 对话记忆（自动摘要，支持多会话）
- **路书导入** — 上传 `.gpx` 文件（行者、Strava 等 App 导出格式），自动解析距离、爬升
- **路书管理** — 列表查看、地图预览、删除管理
- **路书导出** — 已保存路书一键下载 GPX，Agent 规划的路线也可导出
- **Agent 路书分析** — 对话框中让 Agent 分析已保存路书的距离、爬升、难度
- **FIT 文件上传** — 上传 Garmin/Wahoo 码表 `.fit` 文件，自动解析骑行数据
- **骑行水平分析** — 基于功率曲线估算 FTP、功体比、骑行等级
- **路线难度匹配** — 根据个人体能评估路线是否适合

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI + LangGraph Agent |
| LLM | OpenAI 兼容 API（支持 DeepSeek、GLM、OpenAI 等） |
| 地图 | 百度地图 MCP Server + BMapGL |
| 数据库 | SQLite（LangGraph checkpoints）+ MySQL（用户数据） |
| 缓存 | Redis（会话管理） |
| 存储 | 阿里云 OSS（头像 + GPX 文件） |

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
| POST | `/api/routes/import` | 导入 GPX 路书 |
| GET | `/api/routes` | 路书列表 |
| GET | `/api/routes/{id}` | 路书详情（含轨迹坐标） |
| GET | `/api/routes/{id}/export` | 下载 GPX 文件 |
| DELETE | `/api/routes/{id}` | 删除路书 |
| POST | `/api/routes/export-plan` | 导出规划路线为 GPX |
| GET | `/api/activities` | 活动记录列表 |
| POST | `/api/activities` | 上传 FIT 文件 |
| GET | `/api/activities/{id}` | 活动详情（含轨迹、功率曲线、心率区间） |
| DELETE | `/api/activities/{id}` | 删除活动记录 |
| GET | `/api/fitness` | 当前体能档案（FTP、功体比、等级） |
| GET | `/api/fitness/history` | FTP 变化趋势 |
| POST | `/api/fitness/match-route/{id}` | 评估路线与体能匹配度 |

## 项目结构

```
.
├── app/
│   ├── agents/
│   │   └── agent.py        # LangGraph Agent
│   ├── api/
│   │   └── v1/
│   │       ├── routes.py         # 对话与路线规划 API
│   │       ├── schemas.py        # 数据模型
│   │       ├── user_routes.py    # 用户相关路由
│   │       ├── route_routes.py       # 路书导入导出 API
│   │       ├── activity_routes.py    # 活动记录管理 API
│   │       └── fitness_routes.py     # 体能查询 API
│   ├── auth/
│   │   ├── routes.py             # 认证路由
│   │   ├── utils.py              # JWT 工具
│   │   └── dependencies.py       # 认证依赖
│   ├── db.py                     # SQLite 工具
│   ├── db_mysql.py               # MySQL 工具
│   ├── redis_client.py           # Redis 客户端
│   ├── models.py                 # ORM 模型
│   └── services/
│       ├── oss_service.py          # OSS 上传服务（头像）
│       ├── elevation_service.py    # 高程查询、爬坡检测、坐标转换
│       ├── dem_service.py          # 本地 SRTM DEM 高程服务
│       ├── fit_service.py          # FIT 解析、Power Curve、NP/TSS/IF
│       ├── fitness_service.py      # FTP 估算、骑行等级、路线匹配
│       └── route_service.py        # GPX 解析、距离计算、OSS 操作
	├── data/srtm/                   # 本地 SRTM DEM 瓦片
├── main.py                 # FastAPI 入口
├── static/index.html             # 前端页面
├── tests/                        # 测试
├── langgraph.json                # LangGraph 配置
├── docker-compose.yml            # 本地开发数据库
├── pyproject.toml                # 项目配置与依赖
├── .env.example                  # 环境变量模板
└── .env                          # 环境变量（不提交）
```

## 许可

MIT
