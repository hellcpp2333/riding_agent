## 1. 修复路书删除按钮

- [x] 1.1 在 `ElMessage` polyfill 后添加 `ElMessageBox` polyfill（`window.confirm` 回退）
- [x] 1.2 `deleteRouteConfirm` 改用 `apiFetch` 替代 `fetch`，统一 auth 处理

## 2. 爬坡段地图高亮

- [x] 2.1 `drawClimbSegmentsOnMap` 增加 `activeIndex` 参数，选中段 `strokeOpacity: 0.9, strokeWeight: 10`，非选中段 `strokeOpacity: 0.35, strokeWeight: 6`
- [x] 2.2 `openClimbSidebar`/`prevClimb`/`nextClimb` 切换后调用 `drawClimbSegmentsOnMap` 重绘，并调用 `map.setViewport` 平移地图
- [x] 2.3 爬坡列表项点击（`climb-list-item`）同样触发地图高亮和平移

## 3. 验证

- [x] 3.1 验证路书删除按钮弹出确认对话框，确认后成功删除并刷新列表
- [x] 3.2 验证爬坡段列表点击/前后切换时地图正确高亮当前段
- [x] 3.3 验证地图自动平移到选中爬坡段区域
