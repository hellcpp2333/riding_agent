## 1. 创建设计系统 CSS

- [x] 1.1 创建 `static/css/style.css`，定义所有 `:root` 设计 tokens
- [x] 1.2 编写组件样式（auth, layout, chat, actions, input, map, routes, modals）
- [x] 1.3 编写 Element Plus 样式覆盖

## 2. 更新前端 HTML

- [x] 2.1 从 `static/index.html` 移除 `<style>` 标签
- [x] 2.2 添加 `<link rel="stylesheet" href="/static/css/style.css">`
- [x] 2.3 确认 Baidu Maps script 保留 `__BAIDU_MAPS_JS_AK__` 占位符

## 3. 更新后端配置

- [x] 3.1 在 `main.py` 中添加 `StaticFiles` 挂载

## 4. 验证

- [x] 4.1 检查 `.env` 中 `BAIDU_MAPS_JS_AK` 已设置
- [x] 4.2 启动服务，验证 CSS 可访问、地图密钥正常替换、API 正常