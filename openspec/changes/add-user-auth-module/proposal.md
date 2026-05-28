## Why

当前骑行路线规划助手应用没有任何用户认证机制，所有用户共享匿名访问，无法保存个性化配置、历史路线记录和头像等个人信息。添加用户登录注册模块可以让用户拥有独立身份，实现个性化体验和用户状态管理。

## What Changes

- 新增用户注册和登录 API，支持用户名+密码认证
- 后端引入 MySQL 数据库存储用户账户信息（用户名、密码哈希、头像URL等）
- 引入 Redis 存储用户会话状态（登录态、在线状态）
- 前端新增登录/注册页面，采用 Element Plus 组件风格保持页面一致
- 登录后进入骑行助手主页面，右上角显示用户头像
- 点击头像弹出下拉菜单，包含个人信息、修改头像、退出登录等选项
- 头像上传与存储对接阿里云 OSS（Endpoint: oss-cn-shenzhen.aliyuncs.com）
- 现有聊天和路线规划 API 增加认证中间件保护，需登录态才能访问

## Capabilities

### New Capabilities
- `user-auth`: 用户注册、登录、登出、会话管理，包括 JWT token 认证和 Redis 会话状态
- `user-profile`: 用户个人信息管理，包括头像上传（阿里云 OSS）、查看和编辑个人资料
- `frontend-auth-ui`: 前端登录注册页面、认证守卫、用户头像下拉菜单等 UI 组件

### Modified Capabilities
<!-- No existing specs to modify -->

## Impact

- **后端新增依赖**: `aiomysql`（MySQL 异步驱动）、`redis`（Redis 异步客户端）、`PyJWT`（JWT 认证）、`oss2`（阿里云 OSS SDK）、`passlib[bcrypt]`（密码哈希）
- **新增后端模块**: `app/auth/` 认证相关路由、中间件、数据库模型；`app/services/` OSS 上传服务
- **修改后端**: `main.py` 增加 MySQL 连接池和 Redis 连接生命周期管理；`app/api/v1/routes.py` 增加认证依赖
- **前端修改**: `static/index.html` 重写为带认证流程的单页应用，引入 Element Plus CDN
- **基础设施**: 需要 MySQL 数据库和 Redis 服务运行，`.env` 新增 MySQL 和 Redis 连接配置
