# 路书导入导出 — 设计方案

## 概述

为骑行助手增加路书（GPX 格式骑行轨迹）的导入导出功能。用户可上传 .gpx 文件，在地图上显示轨迹，让 Agent 分析路线数据，管理历史路书，以及导出 Agent 规划的路线为 GPX 文件。

## 数据模型

### MySQL `routes` 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK AUTO_INCREMENT | 路书 ID |
| user_id | BIGINT NOT NULL FK → users.id | 所属用户 |
| name | VARCHAR(128) NOT NULL | 路书名称（取自 GPX `<name>` 或用户输入） |
| description | VARCHAR(512) | 简短描述 |
| gpx_oss_url | VARCHAR(1024) | GPX 文件 OSS 地址 |
| distance | DOUBLE | 总距离（米），导入时解析计算 |
| elevation_gain | DOUBLE | 累计爬升（米），导入时解析计算 |
| track_points | INT | 轨迹点数量 |
| source | VARCHAR(32) NOT NULL | `import`（导入）或 `agent`（Agent 规划） |
| created_at | DATETIME NOT NULL DEFAULT NOW() | |
| updated_at | DATETIME NOT NULL DEFAULT NOW() ON UPDATE | |

### OSS 存储

- 路径格式：`routes/{user_id}/{timestamp}_{uuid}.gpx`
- 复用现有 `oss2` SDK 和阿里云 OSS 配置
- GPX 文件大小限制：10MB

### GPX 解析

使用 `xml.etree.ElementTree` 解析标准 GPX 1.0/1.1 格式：
- 提取 `<trk>/<trkseg>/<trkpt>` 的 lat/lon/ele
- 用 Haversine 公式计算相邻点距离，累加得总距离
- 用高程差累加正增量得累计爬升

## API 端点

全部挂载在 `/api/routes`，需要 JWT 认证（`Depends(get_current_user)`）。

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/routes/import` | 上传 GPX 文件（multipart），解析后存 OSS + DB，返回解析结果 |
| GET | `/api/routes` | 返回当前用户路书列表（id、name、distance、source、created_at） |
| GET | `/api/routes/{id}` | 单条路书详情，含完整轨迹点坐标数组 |
| GET | `/api/routes/{id}/export` | 从 OSS 拉取 GPX 文件，返回 `StreamingResponse` 下载 |
| DELETE | `/api/routes/{id}` | 删除路书（OSS 对象 + DB 记录） |
| POST | `/api/routes/export-plan` | 请求体带路线坐标数组，组装 GPX 返回下载（不存库） |

## Agent 集成

在 `build_agent` 中新增 2 个工具：

### `list_user_routes(user_id: int) -> str`

查询 DB 返回用户路书列表（id、名称、距离、时间）。Agent 在用户问"我有哪些路书"时调用。

### `get_route_detail(user_id: int, route_id: int) -> str`

读取单条路书详情。返回统计信息（距离、爬升、轨迹点数）和采样坐标点（每隔 N 个点取一个，避免 token 超限）。用户说"分析这条路线"时 Agent 调用。

### System Prompt 补充

在 `SYSTEM_PROMPT` 中添加路书相关指引：
- 用户提到路书时主动调用相关工具
- 导入新路书后可以主动询问是否需要分析
- 分析路线时告知距离、爬升、难度评估

## 前端设计

### 布局

顶部导航栏新增"路书"标签页，点击切换到路书管理视图。

### 路书管理视图

- **工具栏**：导入按钮（触发文件选择器）、搜索框
- **路书列表**：卡片式，每张显示名称、距离、来源标签、时间
- **点击卡片**：在地图上叠加显示轨迹，展示详情面板（距离、爬升、轨迹点数）
- **操作按钮**：导出（下载 GPX）、删除（确认弹窗）
- **地图集成**：复用页面已有的百度地图实例，轨迹用 `BMap.Polyline` 渲染

### 上传流程

1. 点击"导入路书" → 文件选择器（accept=".gpx"）
2. 前端调 POST `/api/routes/import` → 后端解析并返回摘要
3. 弹窗确认（显示名称、距离、爬升）→ 确认后保存
4. 列表刷新，新路书出现在顶部

### 导出流程

1. 路书列表/详情中点击"导出" → GET `/api/routes/{id}/export`
2. 浏览器触发 .gpx 文件下载

## 文件变更范围

| 文件 | 变更 |
|------|------|
| `app/models.py` | 新增 `Route` 模型 |
| `app/services/route_service.py` | **新建** — GPX 解析、OSS 上传下载、距离计算 |
| `app/api/v1/route_routes.py` | **新建** — 路书 CRUD 端点 |
| `app/agents/agent.py` | 新增 `list_user_routes`、`get_route_detail` 工具，更新 System Prompt |
| `main.py` | 注册路书路由 |
| `static/index.html` | 新增路书标签页、管理视图、地图轨迹叠加 |
| `app/api/v1/schemas.py` | 新增路书相关 Pydantic schema |

## 错误处理

- 非 GPX 文件 → 400（"仅支持 .gpx 格式"）
- 文件过大 → 400（"文件大小不能超过 10MB"）
- GPX 解析失败 → 400（"GPX 格式无效：{具体错误}"）
- 路书不存在 → 404
- 无权限访问他人路书 → 403
- OSS 上传失败 → 500 并记录日志
