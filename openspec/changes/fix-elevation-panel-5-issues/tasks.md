## 1. 后端：ELEVATION_JSON 新增 stats 字段

- [ ] 1.1 修改 `agent.py` 中 `[ELEVATION_JSON]` 输出，在 JSON 中增加 `"stats"` 字段（gain/loss/max/min 直接取自 `calculate_elevation_stats` 返回值）

## 2. 布局：面板移回地图下方（CSS Grid）

- [ ] 2.1 HTML：新增 `.map-right` wrapper 包裹 `#map-container` 和 `#elevation-panel`
- [ ] 2.2 HTML：移除 sidebar 内的 `#elevation-summary`
- [ ] 2.3 CSS：`.map-right{flex:1;display:grid;grid-template-rows:1fr}`
- [ ] 2.4 CSS：`.map-right.has-elevation{grid-template-rows:3fr 1fr}`
- [ ] 2.5 CSS：`#map{position:absolute;inset:0}` 确保 BMapGL 始终有确定尺寸
- [ ] 2.6 CSS：`#elevation-panel` 面板样式（grid 第二行），`v-show` 控制显隐
- [ ] 2.7 CSS：移除 sidebar 内 elevation 相关样式

## 3. 数据统一：前端使用后端 stats

- [ ] 3.1 修改 `handleElevationData()`：使用 `data.stats.gain/loss` 替代自行计算的 gain/loss
- [ ] 3.2 修改 `updateElevationPanel()`：直接从 `routeStats` 读取并显示

## 4. 剖面图样式改进（Garmin 风格）

- [ ] 4.1 Canvas 高度增大至 200px
- [ ] 4.2 填充渐变改为 Garmin 蓝色系
- [ ] 4.3 网格线和轴标签颜色加深
- [ ] 4.4 同步更新 `drawClimbChart` 配色

## 5. 导入路书 elevation 支持

- [ ] 5.1 修改 `selectRoute()`：若 `track_data` 含 `ele`，构建 elevation 数据结构并调用 `handleElevationData()`
- [ ] 5.2 `clearMapOverlays()` 中重置 elevation 状态

## 6. 爬坡段面板修复

- [ ] 6.1 爬坡段按钮移至 `#map-container` 内部（浮动工具栏）
- [ ] 6.2 验证爬坡段列表和侧边栏在聊天路线和导入路书场景均正常

## 7. 验证

- [ ] 7.1 规划路线：地图正常加载，面板显示在地图下方，stats 数值与 AI 回答一致
- [ ] 7.2 剖面图高度 ≥200px，蓝色系配色
- [ ] 7.3 导入路书后面板更新
- [ ] 7.4 爬坡段按钮可见，侧边栏正常
- [ ] 7.5 切换/清除路线后面板正确更新/隐藏
