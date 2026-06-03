## ADDED Requirements

### Requirement: 后端自动扫描壁纸目录
系统 SHALL 提供 `GET /api/wallpapers` 端点，自动扫描 `asserts/` 目录并返回所有 `.jpg` 文件的文件名列表。

#### Scenario: 正常返回图片列表
- **WHEN** 客户端请求 `GET /api/wallpapers`
- **THEN** 服务器返回 JSON `{"images": ["22190433.jpg", "22190451.jpg", ...]}`
- **AND** 列表包含 `asserts/` 目录下所有 `.jpg` 文件的基础文件名

#### Scenario: 目录为空时返回空列表
- **WHEN** `asserts/` 目录下无 `.jpg` 文件
- **THEN** 服务器返回 `{"images": []}`，HTTP 状态码 200

### Requirement: 前端动态获取壁纸列表
登录页面加载时，系统 SHALL 通过 `GET /api/wallpapers` 获取可用壁纸列表，随机选择一张作为背景。

#### Scenario: 正常获取并随机选择
- **WHEN** 用户打开登录页面
- **THEN** 前端调用 `/api/wallpapers` 获取图片列表
- **AND** 从列表中随机选择一张图片作为 `.auth-container` 的背景
- **AND** 图片以 `cover` 模式居中显示

#### Scenario: API 调用失败时降级
- **WHEN** `/api/wallpapers` 请求失败（网络错误、服务器错误等）
- **THEN** `.auth-container` 保持初始渐变背景（`--gradient-auth`）
- **AND** 登录功能不受任何影响

### Requirement: 无需硬编码文件名
系统 MUST NOT 在前端代码中硬编码壁纸文件名列表。向 `asserts/` 添加新 `.jpg` 文件后，下次页面加载时自动纳入随机池。

#### Scenario: 添加新图片自动生效
- **WHEN** 管理员向 `asserts/` 目录添加新的 `.jpg` 文件
- **AND** 用户刷新或打开登录页面
- **THEN** 新增图片出现在随机壁纸候选池中
- **AND** 无需修改任何前端或后端代码
