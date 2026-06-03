## Why

登录页面当前使用固定渐变背景（`--gradient-auth`），视觉效果单一，缺乏个性化和新鲜感。每次打开登录页面显示随机壁纸可以提升用户体验，让应用更加生动、有吸引力。

## What Changes

- 在登录页面加载时，从 `asserts/` 文件夹中随机选择一张图片作为背景壁纸
- 壁纸以全屏覆盖方式显示，作为登录表单卡片的背景层
- 保留现有渐变背景作为降级方案（当图片加载失败时回退）

## Capabilities

### New Capabilities
- `random-login-wallpaper`: 登录页面加载时从 asserts 文件夹随机选择图片作为全屏背景壁纸，图片加载失败时降级为现有渐变背景

### Modified Capabilities
<!-- 无现有 capability 受影响 -->

## Impact

- **前端 HTML**: `static/index.html` — 在 Vue `onMounted` 中新增随机壁纸选择逻辑
- **前端 CSS**: `static/css/style.css` — 修改 `.auth-container` 背景样式，支持 CSS 背景图覆盖
- **资源文件**: `asserts/` 文件夹中的 5 张 JPG 图片作为壁纸素材
