## Context

上次改造引入 `douglas_peucker_smooth()` 替换 `smooth_elevations()`，但 DP 算法依赖 `dist`（累计距离）字段。原有代码中 `calculate_elevation_stats(points)` 被调用时 points 可能没有 `dist` 字段（来自 `lookup_elevations` 的返回值只有 `lat, lon, ele`）。旧 `smooth_elevations` 不需要 `dist`，所以没问题；DP 需要 `dist`，导致 KeyError 静默失败，整个高程 JSON 序列化失败，前端面板不显示。

## Goals / Non-Goals

**Goals:**
1. 修复 DP 平滑的 dist 依赖顺序
2. 新增 Markdown 表格渲染
3. 新增爬坡坡度颜色图例

## Decisions

### 1. DP 平滑顺序修复
**方案**: 所有调用 `douglas_peucker_smooth()` 之前确保已调 `calculate_cumulative_distances()` 添加 `dist` 字段。

具体修改:
- `agent.py`: 调换顺序——先 `calculate_cumulative_distances` 再 `calculate_elevation_stats`
- `enrich_route_with_elevation`: 无 ele 分支先 `calculate_cumulative_distances(elev)` 再 `douglas_peucker_smooth`
- `calculate_elevation_stats`: 防御性检查——若无 `dist` 字段则使用 index 作为近似距离

### 2. Markdown 表格渲染
纯前端正则解析，无需引入库:
```js
// 匹配: | col1 | col2 |\n|------|------|\n| val1 | val2 |
text.replace(/^\|(.+)\|\n\|[-: |]+\|\n((?:\|.+\|\n?)+)/gm, '<table>...</table>')
```

### 3. 坡度颜色图例
参照 Garmin `ClimbsUtil_climbsLegend` 组件，在 `#climb-canvas` 下方添加水平条状图例，从左到右对应递增坡度，颜色使用 Garmin 配色。

## Open Questions

无。
