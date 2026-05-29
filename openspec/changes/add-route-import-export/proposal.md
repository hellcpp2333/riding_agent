## Why

当前骑行助手可以规划路线，但用户无法保存和管理自己的路书。骑行爱好者常用的行者、Strava 等 App 都使用 GPX 格式导出骑行轨迹，用户需要一个能导入这些路书、在地图上查看、让 AI 分析路线、以及导出 Agent 规划路线为 GPX 的功能。

## What Changes

- 新增 `routes` 表存储路书元数据
- 新增路书 CRUD API（导入 GPX、列表、详情、导出、删除、Agent 路线导出）
- GPX 文件存储到阿里云 OSS
- Agent 新增路书读取工具（list_user_routes、get_route_detail）
- 前端新增"路书"标签页，支持上传、列表管理、地图轨迹叠加、导出下载

## Capabilities

### New Capabilities
- `route-management`: 路书导入导出、GPX 解析、OSS 存储、列表管理、地图轨迹渲染

### Modified Capabilities
- `agent-tools`: Agent 新增路书查询和分析工具
- `frontend-ui`: 新增路书管理标签页

## Impact

- **后端新增**: `app/services/route_service.py`（GPX 解析、距离计算）、`app/api/v1/route_routes.py`（路书端点）
- **修改后端**: `app/models.py` 新增 Route 模型，`app/agents/agent.py` 新增工具，`main.py` 注册新路由
- **修改前端**: `static/index.html` 新增路书标签页和管理视图
- **无新增依赖**：使用 Python 标准库 `xml.etree.ElementTree` 解析 GPX，复用现有 `oss2` SDK
