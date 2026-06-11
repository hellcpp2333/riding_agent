## Why

经过三次 CSS 修复尝试（flex column → 百分比高度 → absolute positioning），地图仍无法加载。根本问题在于：试图在固定高度的 viewport 内垂直分割地图空间（75% 地图 + 25% 面板），这种布局在 Baidu BMapGL 的初始化机制下极不稳定——BMapGL 需要 `#map` 元素在初始化时有确定的非零尺寸。

参考 Garmin Connect 的架构：地图是一个独立区域，不与其他面板共享垂直空间。所有数据可视化（统计卡片、海拔图、分段详情）在**可滚动内容区**中展示，地图保持完整高度。

## What Changes

- **移除地图容器内的 elevation-panel**：`#map-container` 恢复为原始的 `flex:1;position:relative`，仅含 `#map` 元素
- **海拔数据面板移入侧边栏**：在侧边栏的对话区域上方或路书标签页中，新增可滚动的海拔数据展示区
- **统计卡片**（距离/爬升/下降）：在有 elevation 数据时，以紧凑卡片形式显示在对话区顶部
- **海拔剖面图**：Canvas 图显示在侧边栏可滚动区域中（不再占用地图空间）
- **爬坡段列表**：以卡片列表形式展示各爬坡段（难度、坡度、距离、爬升），点击可展开该段的海拔图
- **爬坡段侧边栏**：保留右侧滑出功能，从爬坡段列表点击触发
- **地图爬坡着色**：保留在路线上的彩色覆盖层

## Capabilities

### New Capabilities

- `sidebar-elevation-display`: 侧边栏内海拔数据展示（stats 卡片 + 剖面图 + 爬坡段列表 + 侧边栏详情），地图保持全高度

### Modified Capabilities

- `elevation-profile-panel`: 移除地图下方分割面板，数据展示迁移至侧边栏

## Impact

- `static/index.html` — 移除 `#elevation-panel`、`#map-area` wrapper；在侧边栏新增海拔展示区；调整爬坡侧边栏
- `static/css/style.css` — 恢复原始地图布局 CSS，新增侧边栏海拔展示区样式
- `app/agents/agent.py` — 不变（保留结构化高程数据输出）
- `app/api/v1/routes.py` — 不变（保留 SSE elevation 事件）
- `app/services/elevation_service.py` — 不变
