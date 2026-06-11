## 1. CSS：用绝对定位替代百分比高度

- [ ] 1.1 `#map-area`：移除 `height:100%`，改为 `position:absolute;inset:0;transition:bottom 0.3s ease`
- [ ] 1.2 `.has-elevation #map-area`：`height:75%` → `bottom:25%`
- [ ] 1.3 `#elevation-panel`：添加 `position:absolute;bottom:0;left:0;right:0`，保持 `height:25%`

## 2. 验证

- [ ] 2.1 启动服务，验证地图正常加载（`initMap` 不再重试超时）
- [ ] 2.2 验证面板显隐正常，地图在有无路线时高度正确
