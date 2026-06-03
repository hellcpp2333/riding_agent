## ADDED Requirements

### Requirement: 随机登录壁纸显示
登录页面每次加载时，系统 SHALL 从 `asserts/` 文件夹中随机选择一张 JPG 图片作为 `.auth-container` 区域的背景壁纸。

#### Scenario: 正常加载随机壁纸
- **WHEN** 用户打开登录页面（未认证状态）
- **THEN** `.auth-container` 背景显示为 `asserts/` 文件夹中的一张随机图片
- **AND** 图片以 `cover` 模式填充整个容器
- **AND** 图片居中显示

#### Scenario: 壁纸作为表单背景层
- **WHEN** 随机壁纸正在显示
- **THEN** 登录/注册表单卡片（`.auth-card`）浮于壁纸之上
- **AND** 表单卡片保持其原有的白色背景和阴影样式

### Requirement: 壁纸加载失败降级
当随机选择的壁纸图片加载失败时，系统 SHALL 降级为现有的渐变背景（`--gradient-auth` 定义的渐变）。

#### Scenario: 图片加载失败时降级为渐变
- **WHEN** 随机选择的壁纸图片 URL 无法加载（404、网络错误等）
- **THEN** `.auth-container` 显示为 `--gradient-auth` 定义的渐变背景
- **AND** 用户体验不受影响，登录功能正常

### Requirement: 静态资源可访问
系统 SHALL 通过 HTTP 提供 `asserts/` 文件夹中的图片文件，使其可在前端页面中通过 URL 引用。

#### Scenario: 图片可通过 URL 访问
- **WHEN** 浏览器请求 `/asserts/<filename>.jpg`
- **THEN** 服务器返回对应图片文件，Content-Type 为 `image/jpeg`
