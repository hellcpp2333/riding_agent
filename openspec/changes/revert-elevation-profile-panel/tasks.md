## 1. 后端：移除结构化高程数据通路

- [ ] 1.1 在 `elevation_service.py` 中移除 `calculate_cumulative_distances` 函数（约 12 行，含 docstring）
- [ ] 1.2 在 `agent.py` 中移除 `calculate_cumulative_distances` 导入，移除 tools_node 中的 `[ELEVATION_JSON]` 输出逻辑（约 7 行）
- [ ] 1.3 在 `routes.py` 的 `chat` SSE endpoint 中移除 `elevation` 事件发送块（约 10 行），恢复 `[高程数据]` 分割为简单版本
- [ ] 1.4 在 `routes.py` 的 `plan_route` SSE endpoint 中移除 `elevation` 事件发送块（约 10 行），恢复 `[高程数据]` 分割为简单版本

## 2. 前端：恢复原始文件

- [ ] 2.1 使用 `git checkout HEAD -- static/index.html` 恢复前端页面
- [ ] 2.2 使用 `git checkout HEAD -- static/css/style.css` 恢复样式文件
- [ ] 2.3 在 `static/index.html` 中重新添加 favicon `<link>` 标签

## 3. 验证

- [ ] 3.1 启动服务，验证聊天和路线规划功能正常
- [ ] 3.2 验证高程文本摘要（累计爬升/下降）在聊天消息中仍显示
- [ ] 3.3 验证地图全高度展示，无面板和侧边栏
- [ ] 3.4 验证 export GPX 按钮正常
