## 1. HTML：添加动态 class 绑定

- [ ] 1.1 `#map-container` 添加 `:class="{ 'has-elevation': elevationData != null }"`

## 2. CSS：改用高度百分比布局

- [ ] 2.1 `#map-container`：移除 `display:flex;flex-direction:column`，保持 `flex:1;position:relative`
- [ ] 2.2 `#map-area`：移除 `flex:3;transition:flex`，改为 `height:100%;transition:height 0.3s ease`
- [ ] 2.3 新增 `.has-elevation #map-area { height: 75%; }`
- [ ] 2.4 `#elevation-panel`：移除 `flex:1;transition:flex`，改为 `height:25%`
- [ ] 2.5 `#elevation-panel[v-show]` 隐藏时确保不占空间

## 3. 验证

- [ ] 3.1 启动服务，验证页面加载后地图正常显示
- [ ] 3.2 无路线时面板隐藏，地图占满全部高度
- [ ] 3.3 规划路线后面板平滑出现，地图缩小至 75%
