## 1. HTML：恢复地图容器 + 移除分割面板

- [ ] 1.1 移除 `#map-area` wrapper 和 `#elevation-panel`，`#map-container` 内仅保留 `<div id="map"></div>`
- [ ] 1.2 移除 `#map-container` 上的 `:class` 绑定
- [ ] 1.3 移动 `#climb-sidebar-overlay` 和 `#climb-sidebar` 到 `#app` 末尾（脱离 map-container 影响）

## 2. HTML：侧边栏新增海拔数据展示区

- [ ] 2.1 在侧边栏对话区上方（welcome message 之后）新增 `#elevation-summary` 区块，`v-show="elevationData != null"`
- [ ] 2.2 区块内含 stats 卡片行（距离/爬升/下降）和 Canvas 海拔剖面图
- [ ] 2.3 区块内含爬坡段列表（`v-if="climbSegments.length > 0"`），每项显示难度标签、坡度、距离、爬升，点击打开侧边栏
- [ ] 2.4 "爬坡段"按钮放在 stats 卡片旁（而非 actions 栏）

## 3. CSS：恢复地图样式 + 新增侧边栏海拔样式

- [ ] 3.1 `#map-container` 恢复为 `flex:1;position:relative`；`#map{width:100%;height:100%}`
- [ ] 3.2 移除 `#map-area`、`.has-elevation`、`#elevation-panel` 相关 CSS
- [ ] 3.3 新增 `#elevation-summary` 样式（紧凑卡片，earth-tone 配色，max-height + overflow-y:auto 滚动）
- [ ] 3.4 新增爬坡段列表卡片样式
- [ ] 3.5 保留 `#climb-sidebar` 和 overlay 样式不变

## 4. 验证

- [ ] 4.1 启动服务，验证地图正常加载（不再重试超时）
- [ ] 4.2 规划一条有起伏的路线，验证侧边栏显示 stats + 剖面图 + 爬坡段列表
- [ ] 4.3 验证侧边栏可滚动，爬坡段可点击打开详情
- [ ] 4.4 验证无路线时海拔区域隐藏
