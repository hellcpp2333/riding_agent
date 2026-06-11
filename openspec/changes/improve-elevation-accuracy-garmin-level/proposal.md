## Why

当前高程采样使用 Open Elevation API 远程查询（公开 SRTM ~30m DEM），受 API 限制只能 30m 等距采样。Garmin Connect 使用本地高精度 DEM 数据库 + 全点覆盖的方式，精度远超我们。通过三步渐进优化——参数调优、本地 SRTM DEM 缓存、Douglas-Peucker 智能平滑——无需更换收费 API，即可最大程度逼近 Garmin 的效果。

## What Changes

### 阶段 1: 参数即刻优化（无新依赖）
- GPX 路线自带高程时 `smooth_elevations(window=3→1)`：设备气压计数据已精确，不平滑
- 规划路线采样间隔 `30m→15m`：加倍密度捕获微地形
- 爬升阈值 `3m→1m`：更精确累积统计

### 阶段 2: 本地 SRTM DEM 缓存（新增依赖 `rasterio`）
- 下载 SRTM 1 arc-sec (~30m) HGT 瓦片覆盖中国区域，本地查询
- 新增 `SRTMElevationProvider` 类：自动加载对应瓦片，双线性插值查询
- 路线高程富化不再走 Open Elevation API，直接本地毫秒级全量查询
- 保留 Open Elevation API 作为 fallback（本地瓦片未覆盖区域）

### 阶段 3: Douglas-Peucker 智能平滑
- 替代简单移动平均，保留地形拐点、删除平缓段冗余
- 使用 `simplification` 库，epsilon=3m 高程变化阈值
- 剖面图更清晰，爬升统计更准确

## Capabilities

### New Capabilities
- `local-dem-elevation`: 本地 SRTM DEM 数据库提供毫秒级高程查询，支持双线性插值，自动 fallback 到 Open Elevation API

### Modified Capabilities
- `elevation-enrichment`: 采样间隔改为 15m，阈值改为 1m，GPX 路线不再平滑，新增 Douglas-Peucker 替代移动平均

## Impact

- **新增依赖**: `rasterio`（本地 SRTM 读取）、`simplification`（Douglas-Peucker）
- **新增文件**: `app/services/dem_service.py`（本地 DEM 查询服务）
- **数据文件**: `data/srtm/`（SRTM HGT 瓦片，需下载 ~2-3GB）
- **修改文件**: `app/services/elevation_service.py`（采样参数、平滑策略、DEM provider 切换）、`app/agents/agent.py`（调用链适配）
