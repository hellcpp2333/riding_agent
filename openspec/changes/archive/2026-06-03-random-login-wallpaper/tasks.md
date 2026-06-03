## 1. 后端 — 静态资源挂载

- [x] 1.1 在 `main.py` 中添加 `asserts/` 目录的静态文件挂载（`app.mount("/asserts", StaticFiles(directory="asserts"), name="asserts")`）

## 2. 前端 — 随机壁纸逻辑

- [x] 2.1 在 `static/index.html` 的 Vue `setup()` 中定义壁纸文件名数组和随机选择逻辑，在 `onMounted` 之前计算随机图片 URL
- [x] 2.2 在 Vue 模板的 `.auth-container` 上通过 `:style` 动态绑定随机背景图片

## 3. 前端 — CSS 降级样式

- [x] 3.1 修改 `static/css/style.css` 中 `.auth-container` 的 `background` 属性，使用多重 background 实现图片在前、渐变在后（降级）

## 4. 验证

- [x] 4.1 启动服务，打开登录页面，确认随机壁纸正常显示且每次刷新更换
- [x] 4.2 模拟图片加载失败场景（使用浏览器 DevTools 阻止图片请求），确认降级为渐变背景
