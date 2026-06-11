## Context

参考 Garmin Connect 的路书页面分析（`refer/Garmin Connect.html`）：
- 使用 Leaflet 地图 + Recharts SVG 图表
- 地图区域有固定高度，不与其他面板 flex 竞争
- 海拔剖面图使用蓝色系渐变填充

适配方案：用 CSS Grid 替代 flex 垂直分割，Grid 的 `1fr` 轨道在只有 1 个子元素时自动占满，在 2 个子元素时按比例分配。这解决了 flex 的高度传播问题。

## Goals / Non-Goals

**Goals:**
- 面板位于地图下方（Grid 3fr/1fr 分割）
- Stats 数值与 AI 回答一致（共享后端 stats）
- 剖面图 200px+ 高度，Garmin 蓝色系配色
- 导入路书后面板同步更新
- 爬坡段列表和侧边栏正常工作

**Non-Goals:**
- 不改变距离标记功能
- 不改变后端 API 接口

## Decisions

### 1. CSS Grid 布局解决地图高度问题
```css
.map-right { flex: 1; display: grid; grid-template-rows: 1fr; }
.map-right.has-elevation { grid-template-rows: 3fr 1fr; }
#map-container { min-height: 0; position: relative; }
#map { position: absolute; inset: 0; }
```
- `position:absolute;inset:0` 使 BMapGL 始终有确定尺寸（Grid 轨道已确定）

### 2. 数据源统一
- Agent.py 中 `[ELEVATION_JSON]` 结构: `{"points": [...], "stats": {"gain":..., "loss":..., "max":..., "min":...}}`
- 前端 `handleElevationData(data)` 使用 `data.stats.gain/loss` 替代自行计算

### 3. Garmin 风格配色
- 填充渐变: `rgba(25,118,210,0.45)` → `rgba(25,118,210,0.02)`（Garmin 蓝色系）
- 网格线: `#d5dce6`
- 轴文字: `#5a6a7e`
- Canvas 高度: 200px

### 4. 导入路书 elevation 支持
- `selectRoute()` 中，若 `data.track_data` 含 `ele` 字段，构建 `{points: [{lat, lon, ele, dist}], stats: {gain, loss, max, min}}` 结构
- 使用已有的 `haversineDistance` 计算 dist
- 调用 `handleElevationData(builtData)` 触发面板更新
