## 1. 后端 — 新增壁纸列表 API

- [x] 1.1 在 `main.py` 中新增 `GET /api/wallpapers` 端点，使用 `glob` 扫描 `asserts/*.jpg` 返回文件名列表

## 2. 前端 — 动态获取壁纸列表

- [x] 2.1 移除 `static/index.html` 中硬编码的 `WALLPAPER_IMAGES` 数组，将 `wallpaperStyle` 从常量改为 `ref`（初始值为渐变背景）
- [x] 2.2 在 Vue `onMounted` 中调用 `/api/wallpapers`，获取列表后随机选择并更新 `wallpaperStyle`

## 3. 验证

- [x] 3.1 启动服务，验证 `/api/wallpapers` 返回正确的文件列表
- [x] 3.2 打开登录页面，确认随机壁纸正常显示且每次刷新随机更换
- [x] 3.3 向 `asserts/` 添加一张新图片，刷新页面确认自动纳入壁纸池（无需改代码）
