## Why

新用户登录后进入对话页面时，消息栏（`#messages`）为空，缺乏引导感。添加一段欢迎语可以让用户快速了解应用功能，降低首次使用的认知门槛。

## What Changes

- 在对话栏（`#messages` 区域）初始状态时显示一段欢迎语，介绍应用的核心功能
- 欢迎语在用户发送第一条消息后自动消失（被正常消息流替代）
- 欢迎语样式与助手消息一致，但采用特殊排版（居中、图标、功能引导卡片）

## Capabilities

### New Capabilities

- `chat-welcome-message`: 对话栏欢迎语——用户进入新会话或首次使用时，在消息区域展示功能引导性的欢迎内容

### Modified Capabilities

<!-- No existing capabilities modified -->

## Impact

- `static/index.html` — 在 Vue 模板的 `#messages` 区域添加欢迎语 DOM 结构，在 JS 中添加相关状态控制逻辑
- `static/css/style.css` — 添加欢迎语相关样式
