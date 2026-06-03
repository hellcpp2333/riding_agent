## Context

当前登录页面（`static/index.html`）使用 CSS 变量 `--gradient-auth` 定义的固定渐变背景。`asserts/` 文件夹中包含 5 张 JPG 壁纸图片（`22190433.jpg` ~ `22190577.jpg`）。需求是在登录页面加载时随机选择一张作为全屏背景。

当前技术栈为纯前端方案：Vue 3 CDN + Element Plus CDN，无构建工具，所有文件直接从 `static/` 目录提供。

## Goals / Non-Goals

**Goals:**
- 每次打开登录页面时，随机从 `asserts/` 中选择一张图片作为 `.auth-container` 的背景
- 图片以 `background-size: cover` + `background-position: center` 方式全屏覆盖
- 图片加载失败时自动降级为现有的 `--gradient-auth` 渐变背景

**Non-Goals:**
- 不修改注册页面逻辑
- 不添加图片预加载或缓存策略
- 不修改后端 API
- 不改变登录表单的布局或功能

## Decisions

### 1. 使用 JavaScript 动态设置背景（而非纯 CSS）

**选择**: 在 Vue `setup()` 中用 JavaScript 随机选择图片路径，设置到 `.auth-container` 的 `style.backgroundImage`。

**理由**: CSS 无法实现随机选择（`random()` 函数仅在最新 CSS 草案中且支持度极低）。通过 JS 可以在组件初始化时（`onMounted` 前）确定图片路径。

**备选方案**: 
- 服务端在响应 HTML 时注入随机图片路径 → 过于复杂，需要修改 FastAPI 路由和模板系统
- 使用 CSS `@counter-style` 或 `nth-child` 随机 → 不可靠，无法实现真随机

### 2. 图片路径格式

**选择**: 使用相对路径 `/asserts/<filename>`，图片文件名在 JS 中硬编码为数组。

**理由**: FastAPI 默认通过 `app.mount("/static", StaticFiles(...))` 提供静态文件服务，当前无针对 `asserts/` 的挂载。需要添加静态文件挂载或将 `asserts/` 移入 `static/`。考虑到最小化改动，选择添加 FastAPI 静态文件挂载：`app.mount("/asserts", StaticFiles(directory="asserts"))`。

**备选方案**:
- 将 asserts 文件夹移入 static/ → 图片与前端资源耦合，不如独立挂载清晰
- 将图片转为 Base64 内联 → 体积过大，影响页面加载

### 3. 降级策略

**选择**: 优先使用 `background` 简写属性设置图片 + `background-size: cover` + `background-position: center`，并在 `<img>` 的 `onerror` 等价逻辑不可用时，利用 CSS 的后备机制：当 `background-image` 的 URL 返回错误时，浏览器不显示图片层，`.auth-container` 的 `background` 中预设的 fallback 渐变生效。

具体做法：使用 `background: url(...) center/cover no-repeat, var(--gradient-auth)` — CSS 支持多重 background，当第一个层（图片）加载失败时，第二个层（渐变）作为背景显示。

## Risks / Trade-offs

- [图片加载失败] → 通过 CSS 多重 background 实现降级，渐变始终作为后备层
- [图片路径硬编码] → 文件名数组维护成本低（仅 5 张图片），后续可考虑通过 API 动态获取文件列表
- [大图加载慢] → 非目标需求，当前图片尺寸合理；后续可考虑压缩或懒加载
