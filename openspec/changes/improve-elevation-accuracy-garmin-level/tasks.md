## 1. 阶段 1: 参数即刻优化

- [x] 1.1 `elevation_service.py`: `sample_points()` 默认 `interval_m` 从 30.0 改为 15.0
- [x] 1.2 `elevation_service.py`: `calculate_elevation_stats()` 默认 `min_gain_threshold` 从 3.0 改为 1.0
- [x] 1.3 `elevation_service.py`: `enrich_route_with_elevation()` 中 GPX 自带高程时 `smooth_elevations(window=1)` 不平滑
- [x] 1.4 验证：启动服务，规划路线对比新旧采样密度

## 2. 阶段 2: 本地 SRTM DEM 缓存

- [x] 2.1 新增 `app/services/dem_service.py`：`SRTMProvider` 类，HGT 二进制直接读取 + 双线性插值
- [x] 2.2 `dem_service.py`：`ElevationProvider` facade 类，SRTM 优先 + Open Elevation API fallback
- [x] 2.3 创建 `data/srtm/` 目录 + 下载脚本（覆盖中国区所需的 HGT 瓦片列表）
- [x] 2.4 `elevation_service.py`: 新增 `lookup_elevations_local()` 调用 `ElevationProvider`，替代 `lookup_elevations_batched()`
- [x] 2.5 `agent.py`: `tools_node` 中改用 `lookup_elevations_local()` 替代 `lookup_elevations_batched()`
- [x] 2.6 `route_routes.py`: `enrich_route_with_elevation()` 调用链改为本地 DEM 优先
- [x] 2.7 `pyproject.toml`: 无需新增依赖（HGT 二进制读取纯 Python 实现）
- [x] 2.8 验证：下载几个北京区域 HGT 瓦片，测试本地查询速度与精度

## 3. 阶段 3: Douglas-Peucker 智能平滑

- [x] 3.1 `elevation_service.py`: 新增 `douglas_peucker_smooth(points, epsilon=3.0)` 函数
- [x] 3.2 `elevation_service.py`: `calculate_elevation_stats()` 中 `smooth_elevations()` 调用改为 `douglas_peucker_smooth()`
- [x] 3.3 `elevation_service.py`: `enrich_route_with_elevation()` DP 平滑替换移动平均（GPX 无 ele 分支）
- [x] 3.4 验证：对比移动平均 vs DP 平滑的剖面图，确认拐点保留效果

## 4. 清理与端到端验证

- [x] 4.1 移除不再使用的 `smooth_elevations()` 移动平均函数（仍被 GPX has_ele 分支以 window=1 使用，保留）
- [x] 4.2 端到端测试：规划路线 → 15m 采样 → 本地 DEM 查询 → DP 平滑 → 前端剖面图
- [x] 4.3 端到端测试：导入 GPX 路书（含高程）→ 不平滑 → 1m 阈值统计
