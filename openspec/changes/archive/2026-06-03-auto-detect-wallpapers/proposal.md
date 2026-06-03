## Why

当前 `random-login-wallpaper` 功能将壁纸文件名硬编码在 `static/index.html` 的 `WALLPAPER_IMAGES` 数组中。每次向 `asserts/` 文件夹添加新图片时都需要手动修改代码，维护成本高且容易遗漏。改为自动扫描服务器端文件夹可彻底消除这一痛点。

## What Changes

- 新增后端 API `GET /api/wallpapers`，自动扫描 `asserts/` 目录返回所有 `.jpg` 文件名列表
- 前端改为在 `onMounted` 中通过 fetch 调用该 API 获取图片列表，再随机选择
- 移除前端硬编码的 `WALLPAPER_IMAGES` 数组
- 首次渲染时使用渐变背景作为初始状态，API 响应后切换为随机壁纸

## Capabilities

### New Capabilities
- `auto-detect-wallpapers`: 后端自动扫描 `asserts/` 目录，通过 API 向前端提供可用壁纸列表；前端动态获取并随机选择，无需硬编码文件名

### Modified Capabilities
<!-- 无现有 capability 受影响 -->

## Impact

- **后端**: `main.py` — 新增 `GET /api/wallpapers` 端点
- **前端**: `static/index.html` — 替换硬编码数组为动态 fetch，`wallpaperStyle` 从常量改为 `ref`
