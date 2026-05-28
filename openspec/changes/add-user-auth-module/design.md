## Context

当前应用是无状态的 FastAPI + LangGraph 骑行路线规划助手，使用 SQLite 存储会话检查点，无用户认证。所有访问者共享匿名体验。需要引入用户系统以支持个性化体验。

**约束**:
- 保持现有 LangGraph agent 和百度地图 MCP 集成不变
- 前端目前使用纯 HTML/CSS/JS，需要引入 Vue 3 + Element Plus CDN 来实现认证 UI
- 项目使用 `uv` 管理依赖

## Goals / Non-Goals

**Goals:**
- 用户可通过用户名/密码注册和登录
- 用户数据（用户名、密码哈希、头像 URL）持久化到 MySQL
- 登录态通过 Redis 管理（会话 token、在线状态）
- 前端登录后进入骑行助手页面，右上角显示头像和下拉菜单
- 头像上传到阿里云 OSS
- 现有 API（聊天、路线规划）受认证保护

**Non-Goals:**
- 不包含 OAuth/第三方登录（如微信、Google）
- 不包含密码找回/邮箱验证功能
- 不包含用户权限/角色系统（所有登录用户权限一致）
- 不修改现有 LangGraph agent 逻辑或百度地图 MCP 调用

## Decisions

### 1. 认证方案：JWT Token + Redis 会话

**决策**: 登录成功后返回 JWT access token（有效期 24h），同时在 Redis 中存储会话映射 `session:{token}` → `user_id`。前端在后续请求的 `Authorization: Bearer <token>` 头中携带 token。

**理由**: JWT 自包含，服务端无需每次查库验证；Redis 会话支持主动踢出（退出登录时删除 Redis key）和在线状态管理。

**替代方案**: 纯 session-cookie 方案——但前端是纯 HTML/JS SPA，跨域 cookie 配置复杂，JWT + Bearer 更简单。

### 2. 密码哈希：bcrypt via passlib

**决策**: 使用 `passlib[bcrypt]` 对密码进行哈希存储，bcrypt rounds=12。

**理由**: bcrypt 是业界标准，passlib 提供简洁的 Python API，与 FastAPI 生态集成良好。

### 3. MySQL 异步驱动：aiomysql + SQLAlchemy 2.0

**决策**: 使用 `aiomysql` 作为异步驱动，SQLAlchemy 2.0 `async_session` 管理数据库会话。用户表在应用启动时自动创建（如果不存在）。

**表结构**:
```sql
users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(512) DEFAULT NULL,
    nickname VARCHAR(64) DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
```

**理由**: aiomysql 是成熟的 MySQL 异步驱动，SQLAlchemy 提供 ORM 和 DDL 能力，避免手写建表 SQL。

### 4. Redis 会话管理：redis.asyncio

**决策**: 使用 `redis.asyncio.Redis` 连接池。存储两个 key 模式：
- `auth:session:{token}` → `{"user_id": ..., "login_at": ...}`，TTL 24h
- `auth:user:{user_id}:status` → `{"online": true, "last_seen": ...}`，TTL 5min（心跳刷新）

**理由**: 异步 Redis 与 FastAPI 事件循环兼容，不会阻塞。TTL 自动清理过期会话。

### 5. 前端：Vue 3 + Element Plus CDN

**决策**: 在 `static/index.html` 中引入 Vue 3 和 Element Plus CDN，登录/注册页面使用 Element Plus 的 `el-form`、`el-input`、`el-button` 组件。主页面保持现有布局，右上角添加 `el-dropdown` 头像菜单。

**理由**: 项目当前无构建步骤（纯 HTML），CDN 方式零配置引入。Element Plus 组件风格统一，与现有 Ant Design 风格的 CSS 颜色变量（#1890ff）兼容。

**替代方案**: 创建 React/Vue 构建项目——但对于一个小型单页应用来说过度工程化。

### 6. 头像存储：阿里云 OSS

**决策**: 使用 `oss2` SDK，上传头像时生成唯一文件名 `avatars/{user_id}/{timestamp}_{random}.jpg`，返回公共读 URL 存储到 MySQL `avatar_url` 字段。

**环境变量**:
- `OSS_ACCESS_KEY_ID`
- `OSS_ACCESS_KEY_SECRET`
- `OSS_BUCKET_NAME`
- `OSS_ENDPOINT=oss-cn-shenzhen.aliyuncs.com`

### 7. API 认证中间件：FastAPI Depends

**决策**: 创建 `get_current_user` 依赖项，从 `Authorization` 头解析 JWT token，验证签名后查询 Redis 会话，返回用户信息。需要认证的端点使用 `Depends(get_current_user)`。

现有 `/api/chat` 和 `/api/route/plan` 添加认证依赖；`/api/auth/*` 端点无需认证。

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Redis 宕机导致所有会话失效 | Redis 会话 TTL 24h，宕机恢复后用户需重新登录，影响可控 |
| MySQL 连接池耗尽 | 设置合理的 pool_size（默认 5），监控连接数 |
| JWT token 泄露 | TTL 24h 较短，退出登录时 Redis 侧失效 token |
| OSS 头像上传滥用 | 限制文件大小 5MB、格式 jpg/png，后续可加频率限制 |
| 前端 CDN 加载失败 | Element Plus 和 Vue 使用国内 CDN 镜像（如 cdn.jsdelivr.net） |
| 密码强度不足 | 前端表单校验最少 6 位，后端可加强制规则 |

## Migration Plan

1. 部署 MySQL 和 Redis 实例，配置环境变量
2. 应用启动时自动创建 `users` 表
3. 前端 `index.html` 替换为带认证流程的版本
4. 现有用户无影响——首次访问会重定向到登录页面
5. 回滚：切换回旧版 `index.html`，移除 API 认证依赖即可恢复匿名访问

## Open Questions

- 是否需要用户名唯一性约束之外的其他约束（如禁止特殊字符）？——当前仅做 UNIQUE 约束，前端校验长度 3-20 字符
- OSS bucket 是公共读还是私有读？——当前设为公共读（头像需要浏览器直接访问），如需隐私可改为签名 URL
