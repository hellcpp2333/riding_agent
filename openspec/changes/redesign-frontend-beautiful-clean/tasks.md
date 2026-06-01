## 1. 创建设计系统 CSS 文件

- [x] 1.1 创建 `static/css/style.css` 文件
- [x] 1.2 在 `:root` 选择器中定义颜色 tokens（--color-bg, --color-primary, --color-text 等）
- [x] 1.3 在 `:root` 选择器中定义间距 tokens（--space-1 到 --space-10）
- [x] 1.4 在 `:root` 选择器中定义排版 tokens（--font-xs 到 --font-2xl, font weights）
- [x] 1.5 在 `:root` 选择器中定义圆角 tokens（--radius-sm 到 --radius-full）
- [x] 1.6 在 `:root` 选择器中定义阴影 tokens（--shadow-sm, --shadow-md, --shadow-lg, --shadow-glow）
- [x] 1.7 在 `:root` 选择器中定义过渡 tokens（--transition-fast, --transition-base）
- [x] 1.8 定义渐变 token `--gradient-auth`

## 2. 重构认证页面样式

- [x] 2.1 定义 `.auth-container` 样式（flex 布局，渐变背景）
- [x] 2.2 定义 `.auth-card` 样式（使用 tokens，圆角，阴影）
- [x] 2.3 定义 `.auth-card h2` 标题样式
- [x] 2.4 定义 `.auth-switch` 和链接样式
- [x] 2.5 定义 Element Plus 输入框的 CSS 覆盖（高度 44px，使用 tokens）

## 3. 重构主应用布局样式

- [x] 3.1 定义 `.main-app` 布局样式（flex, 100vh）
- [x] 3.2 定义 `#sidebar` 样式（宽度，背景色，边框）
- [x] 3.3 定义 `#header` 样式（内边距，背景色，边框）
- [x] 3.4 定义 `#nav-tabs` 和 `.nav-tab` 样式（悬停和激活状态）
- [x] 3.5 定义 `#session-select` 和 `#btn-new-session` 样式
- [x] 3.6 定义用户头像和下拉菜单样式

## 4. 重构聊天界面样式

- [x] 4.1 定义 `#messages` 容器样式（滚动，内边距）
- [x] 4.2 定义 `.msg` 基础样式（最大宽度，内边距，圆角）
- [x] 4.3 定义 `.msg.user` 消息气泡样式（蓝色背景，白色文字）
- [x] 4.4 定义 `.msg.assistant` 消息气泡样式（白色背景，边框）
- [x] 4.5 定义 `.route-card` 样式（在消息中展示路线数据）
- [x] 4.6 定义 `.tool-indicator` 样式（工具调用状态）
- [x] 4.7 定义消息出现动画（fade-in）

## 5. 重构操作栏和输入区域样式

- [x] 5.1 定义 `#actions` 按钮栏样式
- [x] 5.2 定义操作按钮样式（悬停状态）
- [x] 5.3 定义 `#input-area` 样式
- [x] 5.4 定义 `#message-input` 输入框样式（focus 状态使用 glow 效果）
- [x] 5.5 定义 `#btn-send` 发送按钮样式

## 6. 重构地图和路书管理样式

- [x] 6.1 定义 `#map-container` 和 `#map` 样式
- [x] 6.2 定义 `.map-route-info` 样式（浮动信息卡片）
- [x] 6.3 定义 `#routes-view` 容器样式
- [x] 6.4 定义 `.route-card` 样式（悬停和选中状态）
- [x] 6.5 定义 `.routes-empty` 空状态样式

## 7. 重构模态框和对话框样式

- [x] 7.1 定义 `.modal` 基础样式（遮罩层）
- [x] 7.2 定义 `.modal-content` 样式（居中，圆角，阴影）
- [x] 7.3 定义模态框输入框和按钮样式
- [x] 7.4 定义用户头像大图样式
- [x] 7.5 定义 Element Plus 组件的 CSS 覆盖（dialog, message-box, dropdown-menu 等）

## 8. 更新 HTML 文件

- [x] 8.1 从 `static/index.html` 中移除所有内联 `<style>` 标签
- [x] 8.2 在 `static/index.html` 的 `<head>` 中添加 `<link rel="stylesheet" href="/static/css/style.css">`
- [x] 8.3 验证 Baidu Maps script 标签保持 `__BAIDU_MAPS_JS_AK__` 占位符

## 9. 验证地图 API 配置

- [x] 9.1 检查 `.env` 文件中 `BAIDU_MAPS_JS_AK` 是否已设置
- [x] 9.2 启动应用验证地图正常加载
- [x] 9.3 测试登录、聊天、路线规划、路书管理等核心功能