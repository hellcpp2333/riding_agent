## Context

`random-login-wallpaper` 变更已实现随机壁纸功能，但壁纸文件名硬编码在 `static/index.html` 中。每当向 `asserts/` 添加新图片时，必须手动更新 JS 数组。需要改为后端自动扫描目录、前端动态获取的方式。

当前项目结构：
- `main.py` 已有 `GET /` 端点返回 HTML（替换 AK 占位符），已有 `/asserts` 静态文件挂载
- `static/index.html` 中 Vue `setup()` 同步计算 `wallpaperStyle`（常量），初始渲染即确定

## Goals / Non-Goals

**Goals:**
- 向后端 `asserts/` 文件夹添加 `.jpg` 图片后无需修改任何代码即可生效
- 前端每次加载登录页面从服务器获取最新壁纸列表再随机选择
- API 调用失败时降级为渐变背景，不影响登录功能

**Non-Goals:**
- 不添加图片上传/管理界面
- 不实现壁纸缓存策略
- 不修改已有的 CSS 降级机制

## Decisions

### 1. 后端 API 方案：新增 `GET /api/wallpapers` 端点

**选择**: 在 `main.py` 中直接定义路由（`@app.get("/api/wallpapers")`），使用 `glob.glob("asserts/*.jpg")` 扫描文件。

**理由**: 
- 最简实现，无需新建文件或模块
- `glob` 是标准库，零依赖
- 只返回文件名，安全（不暴露服务器路径）

**备选方案**:
- 在 `app/api/v1/routes.py` 中添加 → 过度设计，壁纸列表不需要版本化 API 的复杂性
- 用 `os.listdir` → 功能等价但 `glob` 天然支持扩展名过滤

### 2. 前端改造：`wallpaperStyle` 从常量改为 `ref`

**选择**: 将 `wallpaperStyle` 从普通对象改为 `ref({ background: 'var(--gradient-auth)' })`，初始值为纯渐变。在 `onMounted` 中 fetch API，成功后更新 `wallpaperStyle.value`。

**理由**:
- 初始渲染立即显示渐变背景（无闪烁）
- API 成功后平滑切换为壁纸
- fetch 失败时保持渐变，天然降级

**备选方案**:
- 在 `setup()` 顶层用 `async/await` → Vue 3 `setup()` 不支持顶层 await（非 SFC + 无 `<script setup>` 语法糖时），且会阻塞组件渲染
- 用 `computed` → 不需要，壁纸在一次会话中不变

### 3. API 不返回完整 URL

**选择**: API 只返回文件名列表，前端拼接 `/asserts/` 前缀。

**理由**: 保持 API 简洁，前端已知道静态文件挂载路径。若未来 CDN 化也只需改前端一处。

## Risks / Trade-offs

- [API 调用增加一次网络请求] → 请求极小（文件名列表），且在用户输入凭证之前完成，不影响体验
- [`glob` 在主线程同步执行] → 文件数量极少（<100），耗时微秒级，无性能风险
- [首次渲染无壁纸] → 初始值设为渐变，用户看到渐变一闪而过是正常行为
