## 1. 前端：距离计算与插值

- [ ] 1.1 在 `static/index.html` 中新增 `haversineDistance(lat1, lon1, lat2, lon2)` 函数，返回两点间距离（米）
- [ ] 1.2 新增 `interpolatePoint(p1, p2, ratio)` 函数，在两点间按比例线性插值坐标
- [ ] 1.3 新增 `findDistanceMarkers(points, intervalM=5000)` 函数：遍历坐标点，计算累计 Haversine 距离，在每 5km 整数倍处通过插值定位返回标记点数组 `[{lng, lat, distKm}]`

## 2. 前端：距离标记渲染

- [ ] 2.1 新增 `renderDistanceMarkers(markerPoints)` 函数：为每个标记点创建 `BMapGL.Label`，内容为 CSS 渲染的圆点（8px 直径、深灰色 #3a3a3a）+ 距离文字（"{N} km"、earth-tone #2c2416、半透明白底），文字偏移显示在圆点侧上方
- [ ] 2.2 新增全局数组 `distanceMarkers = []` 追踪所有距离标记 Label 对象

## 3. 前端：集成到路线渲染

- [ ] 3.1 修改 `drawRoute()` 函数：在 polyline 渲染后，调用 `findDistanceMarkers(points)` → `renderDistanceMarkers(markerPoints)`，将生成的 Label 加入 `distanceMarkers` 数组
- [ ] 3.2 修改 `selectRoute()` 函数：在 polyline 渲染后，对 `track_data` 坐标调用距离标记渲染
- [ ] 3.3 修改 `clearMap()` / `clearMapOverlays()`：将 `distanceMarkers` 置空（`clearOverlays()` 已从地图移除所有覆盖物）

## 4. 验证

- [ ] 4.1 启动服务，规划一条 ≥ 10km 的骑行路线，验证地图上显示 5km、10km 距离标记，样式为佳明风格圆点+文字
- [ ] 4.2 导入一条 ≥ 5km 的路书，验证距离标记正确显示
- [ ] 4.3 验证短路线（< 5km）不显示距离标记
- [ ] 4.4 验证切换路线/清除聊天时距离标记被正确移除
